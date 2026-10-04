"""Reproduce los archivos y comandos publicados en la guía, en un repo nuevo.
CLUE_EXECUTABLE permite comprobar el paquete de PyPI sin importar este checkout.
El triage usado aquí es un fixture, nunca una decisión sobre un proyecto real.
"""
from html.parser import HTMLParser
from pathlib import Path
import json
import os
import shlex
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]

class Guide(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.section = None
        self.in_code = False
        self.in_pre = False
        self.blocks = {}
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        if tag == 'section':
            self.section = dict(attrs).get('id')
        if tag == 'pre':
            self.in_pre = True
        if tag == 'code' and self.in_pre:
            self.in_code = True
            self.blocks.setdefault(self.section, []).append('')
    def handle_endtag(self, tag):
        if tag == 'code':
            self.in_code = False
        if tag == 'pre':
            self.in_pre = False
        if tag == 'section':
            self.section = None
    def handle_data(self, data):
        if self.in_code:
            self.blocks[self.section][-1] += data

class GuideExecution(unittest.TestCase):
    def test_actual_guide_with_success_and_rejections(self):
        blocks = Guide((ROOT / 'docs/desde-cero.html').read_text()).blocks
        evidence = []
        with tempfile.TemporaryDirectory(prefix='clue-web-guia-') as tmp:
            cwd = Path(tmp)
            env = os.environ.copy()
            env.pop('PYTHONPATH', None)
            env['PYTHONDONTWRITEBYTECODE'] = '1'
            env['UV_CACHE_DIR'] = str(cwd / 'uv-cache')
            env['GIT_CONFIG_GLOBAL'] = os.devnull
            env['GIT_CONFIG_NOSYSTEM'] = '1'
            cli = [os.environ['CLUE_EXECUTABLE']] if 'CLUE_EXECUTABLE' in os.environ else [sys.executable, '-m', 'oracle_clue.cli']
            if 'CLUE_EXECUTABLE' not in os.environ:
                env['PYTHONPATH'] = str(ROOT)
            def commands(text, expected=0, stdin=None):
                nonlocal cwd
                for line in text.strip().splitlines():
                    args = shlex.split(line)
                    if args[0] == 'mkdir':
                        (cwd / args[1]).mkdir()
                        continue
                    if args[0] == 'cd':
                        cwd = (cwd / args[1]).resolve()
                        continue
                    if args[0] == 'oracle-clue':
                        args = cli + args[1:]
                    result = subprocess.run(args, cwd=cwd, env=env, text=True, input=stdin,
                                            capture_output=True, timeout=90)
                    evidence.append({'command': line, 'returncode': result.returncode,
                                     'stdout': result.stdout, 'stderr': result.stderr})
                    self.assertEqual(result.returncode, expected, evidence[-1])
                    if expected:
                        self.assertIn('CLUE:', result.stderr)
            # Commands and complete editor contents come directly from the HTML.
            commands(blocks['crear-repo'][0])
            commands(blocks['crear-repo'][1])
            original = blocks['crear-repo'][2]
            (cwd / 'total.py').write_text(original)
            commands(blocks['crear-repo'][3])
            (cwd / 'total.py').write_text(blocks['sembrar-defecto'][0])
            commands(blocks['sembrar-defecto'][1])
            commands(blocks['sembrar-defecto'][2])
            (cwd / 'especificacion.md').write_text(blocks['contexto'][0])
            commands(blocks['contexto'][1])
            commands(blocks['preparar'][0])
            commands(blocks['preparar'][1])
            (cwd / 'armar_informe.py').write_text(blocks['informe'][0])
            commands(blocks['informe'][1])
            commands(blocks['validar'][0])
            report_path = cwd.parent / 'revisiones/informe.json'
            report = json.loads(report_path.read_text())
            location = report['findings'][0]['location']
            # Apply the malformed location shown in the guide; then restore it.
            location.update(json.loads('{' + blocks['validar'][2] + '}'))
            report_path.write_text(json.dumps(report))
            commands(blocks['validar'][3], expected=1)
            location.update(start_line=2, end_line=2)
            report_path.write_text(json.dumps(report))
            (cwd / 'armar_triage.py').write_text(blocks['triage'][0])
            fixture = 'HALLAZGO-01\nriesgo_aceptado\nSolo fixture automatizado, sin aprobar software real.\nFixture\n'
            commands(blocks['triage'][1], stdin=fixture)
            commands(blocks['triage'][2])
            # Changing report bytes must invalidate its linked decision record.
            report_path.write_text(report_path.read_text() + '\n')
            commands(blocks['triage'][2], expected=1)
            # Following the repair invalidates the old package/report.
            (cwd / 'total.py').write_text(original)
            commands(blocks['recuperacion'][0])
            commands(blocks['recuperacion'][1], expected=1)
        if target := os.environ.get('GUIDE_EVIDENCE'):
            Path(target).write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    unittest.main()
