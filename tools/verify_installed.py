"""Comprueba el entry point del wheel instalado sobre un repo temporal."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile


def main():
    p=argparse.ArgumentParser();p.add_argument('--clue',required=True);args=p.parse_args()
    executable=str(Path(args.clue).absolute())
    with tempfile.TemporaryDirectory() as tmp:
        work=Path(tmp);repo=work/'repo';repo.mkdir()
        def run(*cmd,ok=True,cwd=work):
            r=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
            if ok and r.returncode:raise AssertionError(r.stdout+r.stderr)
            if not ok:assert r.returncode,r.stdout+r.stderr
            return r
        def git(*cmd):return run('git','-C',str(repo),*cmd)
        git('init','-q');git('config','user.name','Fixture');git('config','user.email','fixture@example.invalid')
        code=repo/'con espacios.py';code.write_text('resultado = 1\n')
        git('add','.');git('commit','-qm','base');base=git('rev-parse','HEAD').stdout.strip()
        code.write_text('resultado = 1 / 0\n');git('add','.');git('commit','-qm','defecto')
        package=work/'contexto.json'
        run(executable,'preparar','--repo',str(repo),'--base',base,'--salida',str(package))
        bundle=json.loads(package.read_text())
        report={'schema_version':'oracle-clue.review/v1',**{key:bundle[key] for key in ['repo','base','head','diff_sha256','context_sha256']},
                'provider':{'name':'fixture externa','model':None},'review_status':'completo','limitations':[],
                'findings':[{'id':'F1','kind':'bug','severity':'alta','confidence':1,
                'title':'División por cero','explanation':'La expresión divide por cero.',
                'location':{'file':'con espacios.py','side':'head','start_line':1,'end_line':1},
                'trigger':'Ejecutar el archivo','evidence':'Denominador literal 0',
                'verification':'Ejecutar en el entorno de pruebas.','status':'pendiente'}]}
        output=work/'informe.json';output.write_text(json.dumps(report))
        run(executable,'validar',str(output),'--paquete',str(package),'--repo',str(repo))
        report['findings'][0]['location']['end_line']=999;output.write_text(json.dumps(report))
        run(executable,'validar',str(output),'--paquete',str(package),'--repo',str(repo),ok=False)
        assert git('status','--porcelain').stdout==''
    print('OK: CLI instalada, paquete de revisión, informe válido, rechazo de rango falso y repo intacto.')


if __name__=='__main__':main()
