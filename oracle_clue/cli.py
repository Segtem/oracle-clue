"""Preparación local de contexto y validación de informes; no invoca modelos."""
from __future__ import annotations

import argparse
import hashlib
from importlib import resources
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

from jsonschema import Draft202012Validator, FormatChecker, ValidationError
from . import __version__

LIMIT = 1_000_000
FILE_LIMIT = 256_000


class ClueError(Exception):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encoded(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def git(repo: Path, *args: str) -> bytes:
    p = subprocess.run(["git", "--no-pager", "--literal-pathspecs", "-C", str(repo), *args],
                       capture_output=True, timeout=30)
    if p.returncode:
        raise ClueError("Git no pudo completar " + args[0] + ": " + p.stderr.decode("utf-8", "replace").strip())
    return p.stdout


def path_ok(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name) and not p.is_absolute() and ".." not in p.parts and "\\" not in name and not re.match(r"^[A-Za-z]:", name)


def sensitive(name: str) -> bool:
    parts = [p.lower() for p in PurePosixPath(name).parts]
    return any(p in {".env", ".aws", ".ssh", "credentials", "credentials.json", "secrets", "secrets.json", "id_rsa", "id_ed25519"}
               or p.startswith(".env.") or p.endswith((".pem", ".key", ".p12", ".pfx")) for p in parts)


def resolve_commit(repo: Path, ref: str) -> str:
    return git(repo, "rev-parse", "--verify", "--end-of-options", ref + "^{commit}").decode().strip()


def blob(repo: Path, oid: str) -> bytes:
    if set(oid) == {"0"}:
        return b""
    size = int(git(repo, "cat-file", "-s", oid))
    if size > FILE_LIMIT:
        raise ClueError(f"archivo supera el límite de {FILE_LIMIT} bytes; reducí el cambio")
    return git(repo, "cat-file", "blob", oid)


def prepare(repo: Path, base_ref: str, context_names=()) -> dict:
    repo = repo.expanduser().resolve()
    top = Path(git(repo, "rev-parse", "--show-toplevel").decode("utf-8").strip()).resolve()
    if repo != top:
        raise ClueError("--repo debe señalar la raíz del checkout Git")
    head = resolve_commit(repo, "HEAD")
    base = resolve_commit(repo, base_ref)
    # Este primer corte revisa commits. Evita presentar cambios locales como revisados.
    if git(repo, "diff", "--no-ext-diff", "--no-textconv", "--name-only", head, "--"):
        raise ClueError("hay cambios versionados sin commit; confirmalos o usá un checkout limpio")
    raw = git(repo, "diff", "--raw", "-z", "--no-abbrev", "--no-renames", base, head, "--")
    if not raw:
        raise ClueError("el diff está vacío")
    records = raw.split(b"\0")[:-1]
    if len(records) > 400:
        raise ClueError("el cambio supera 200 archivos; dividí la revisión")
    files, omissions = [], []
    for i in range(0, len(records), 2):
        fields = records[i].decode("ascii").split()
        oldmode, newmode, oldoid, newoid, status = fields
        oldmode = oldmode.lstrip(":")
        try:
            name = records[i + 1].decode("utf-8")
        except UnicodeDecodeError as e:
            raise ClueError("nombre de archivo no UTF-8; no se puede representar el cambio") from e
        if not path_ok(name):
            raise ClueError("ruta no admitida en el diff")
        reason = None
        if sensitive(name):
            reason = "ruta de credenciales conocida"
        elif any(mode not in {"000000", "100644", "100755"} for mode in (oldmode, newmode)):
            reason = "enlace simbólico o submódulo"
        if reason:
            omissions.append({"file": name, "reason": reason})
            continue
        before, after = blob(repo, oldoid), blob(repo, newoid)
        try:
            before_text, after_text = before.decode("utf-8"), after.decode("utf-8")
        except UnicodeDecodeError:
            omissions.append({"file": name, "reason": "contenido no UTF-8"})
            continue
        if b"\0" in before or b"\0" in after:
            omissions.append({"file": name, "reason": "contenido binario"})
            continue
        patch = git(repo, "diff", "--no-ext-diff", "--no-textconv", "--no-renames", "--no-color",
                    "--unified=3", base, head, "--", name).decode("utf-8")
        # .gitattributes puede clasificar como binario un blob UTF-8.
        if "Binary files " in patch and not re.search(r"(?m)^@@ ", patch):
            omissions.append({"file": name, "reason": "Git lo clasifica como binario"})
            continue
        ranges = {"base": [], "head": []}
        for match in re.finditer(r"(?m)^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", patch):
            for side, offset in (("base", 1), ("head", 3)):
                start, count = int(match[offset]), int(match[offset + 1] or "1")
                if count:
                    ranges[side].append([start, start + count - 1])
        files.append({"file": name, "status": status, "base_text": before_text, "head_text": after_text,
                      "patch": patch, "ranges": ranges})
        if len(encoded(files)) > LIMIT:
            raise ClueError("contexto demasiado grande; dividí la revisión")
    contexts = []
    for name in sorted(set(context_names)):
        if not path_ok(name) or sensitive(name):
            raise ClueError("contexto debe ser una ruta relativa sin credenciales conocidas")
        p = repo / name
        if any(part.is_symlink() for part in [p, *p.parents] if part != repo and part.is_relative_to(repo)):
            raise ClueError("no se siguen enlaces simbólicos de contexto")
        if not p.resolve().is_relative_to(repo) or not p.is_file():
            raise ClueError("contexto inexistente o fuera del repositorio: " + name)
        if p.stat().st_size > FILE_LIMIT:
            raise ClueError("contexto demasiado grande: " + name)
        data = p.read_bytes()
        if b"\0" in data:
            raise ClueError("contexto binario: " + name)
        contexts.append({"file": name, "text": data.decode("utf-8"), "sha256": digest(data)})
    result = {"schema_version": "oracle-clue.bundle/v1", "repo": str(repo), "base": base, "head": head,
              "diff_sha256": digest(raw), "files": files, "contexts": contexts, "omissions": omissions,
              "limitations": ["Solo se revisa la diferencia entre commits; archivos no versionados no forman parte del diff.",
                              "Preparar contexto no ejecuta revisión de IA, pruebas ni aprobación humana.",
                              "El filtro de rutas conocidas no garantiza ausencia de secretos en otros archivos."]}
    result["context_sha256"] = digest(encoded(result))
    if len(encoded(result)) > LIMIT:
        raise ClueError("paquete supera el límite de un millón de bytes")
    # Comprobar que no cambió la entrada mientras se recolectaba.
    if resolve_commit(repo, "HEAD") != head or git(repo, "diff", "--no-ext-diff", "--no-textconv", "--name-only", head, "--"):
        raise ClueError("el checkout cambió durante la preparación")
    for ctx in contexts:
        if digest((repo / ctx["file"]).read_bytes()) != ctx["sha256"]:
            raise ClueError("el contexto cambió durante la preparación")
    return result


def schema(name: str):
    data = resources.files("oracle_clue").joinpath("schemas", name).read_text(encoding="utf-8")
    return Draft202012Validator(json.loads(data), format_checker=FormatChecker())


def read_json(path: Path):
    if path.stat().st_size > LIMIT * 2:
        raise ClueError("JSON demasiado grande")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_report(report: dict, bundle: dict, repo: Path) -> None:
    if not isinstance(bundle, dict) or bundle.get("schema_version") != "oracle-clue.bundle/v1":
        raise ClueError("paquete de contexto inválido")
    try:
        current = prepare(repo, bundle["base"], [c["file"] for c in bundle["contexts"]])
    except (KeyError, TypeError) as e:
        raise ClueError("paquete de contexto mal formado") from e
    if current != bundle:
        raise ClueError("el paquete no coincide con el repositorio/contexto actual")
    schema("hallazgos.schema.json").validate(report)
    for key in ("repo", "base", "head", "diff_sha256", "context_sha256"):
        if report[key] != bundle[key]:
            raise ClueError("informe desactualizado o distinto del paquete: " + key)
    if bundle["omissions"] and report["review_status"] != "incompleto":
        raise ClueError("un paquete con omisiones exige un informe incompleto")
    seen = set()
    files = {f["file"]: f for f in bundle["files"]}
    for finding in report["findings"]:
        if finding["id"] in seen:
            raise ClueError("id de hallazgo duplicado: " + finding["id"])
        seen.add(finding["id"])
        location = finding["location"]
        name, side = location["file"], location["side"]
        start, end = location["start_line"], location["end_line"]
        if not path_ok(name) or name not in files or start > end:
            raise ClueError("ubicación de hallazgo inválida")
        if not any(low <= start <= end <= high for low, high in files[name]["ranges"][side]):
            raise ClueError("el rango del hallazgo no pertenece a ese lado del diff")


def validate_triage(triage: dict, report: dict, report_bytes: bytes) -> None:
    schema("triage.schema.json").validate(triage)
    if triage["report_sha256"] != digest(report_bytes):
        raise ClueError("triage vinculado a otro informe")
    ids = {f["id"] for f in report["findings"]}
    seen = set()
    for decision in triage["decisions"]:
        fid = decision["finding_id"]
        if fid not in ids or fid in seen:
            raise ClueError("decisión duplicada o hallazgo inexistente")
        seen.add(fid)


def write_bundle(bundle: dict, output: Path | None) -> None:
    text = json.dumps(bundle, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if output is None:
        print(text, end="")
        return
    if output.expanduser().resolve().is_relative_to(Path(bundle["repo"])):
        raise ClueError("guardá el paquete fuera del repo revisado")
    with output.expanduser().open("x", encoding="utf-8") as target:
        target.write(text)
    print(f"Paquete preparado: {output}; omisiones: {len(bundle['omissions'])}. No es un informe de revisión.")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="oracle-clue", description="Prepara contexto Git y valida informes externos; no invoca IA ni aprueba cambios.")
    p.add_argument("--version", action="version", version=f"oracle-clue {__version__}")
    sub = p.add_subparsers(dest="command", required=True)
    prep = sub.add_parser("preparar", help="reunir diff entre commits y archivos explícitos sin modificar el repo")
    prep.add_argument("--repo", type=Path, default=Path.cwd())
    prep.add_argument("--base", required=True)
    prep.add_argument("--contexto", action="append", default=[], help="ruta relativa al repo; repetible")
    prep.add_argument("--salida", type=Path, help="JSON nuevo fuera del repo; por defecto stdout")
    val = sub.add_parser("validar", help="comprobar schema, contexto vigente, ubicaciones y triage opcional")
    val.add_argument("informe", type=Path)
    val.add_argument("--paquete", type=Path, required=True)
    val.add_argument("--repo", type=Path, default=Path.cwd())
    val.add_argument("--triage", type=Path)
    args = p.parse_args(argv)
    try:
        if args.command == "preparar":
            write_bundle(prepare(args.repo, args.base, args.contexto), args.salida)
        else:
            report, bundle = read_json(args.informe), read_json(args.paquete)
            validate_report(report, bundle, args.repo)
            if args.triage:
                validate_triage(read_json(args.triage), report, args.informe.read_bytes())
            print("Formato y vigencia verificados. No confirma los hallazgos ni autentica al revisor o al actor humano.")
        return 0
    except (ClueError, OSError, UnicodeError, ValueError, ValidationError, subprocess.TimeoutExpired) as e:
        print(f"CLUE: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
