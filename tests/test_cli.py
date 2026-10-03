"""Repositorio temporal con defectos sembrados; no se llama a un modelo."""
import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from oracle_clue import cli as c
from jsonschema import ValidationError


class RevisionLocal(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root / 'repo'
        self.repo.mkdir()
        self.git('init', '-q')
        self.git('config', 'user.name', 'Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        (self.repo/'notas.py').write_text('def valida(titulo):\n    return bool(titulo.strip())\n')
        self.commit()
        self.base = self.git('rev-parse','HEAD').strip()
        (self.repo/'notas.py').write_text('def valida(titulo):\n    return bool(titulo)\n')
        self.commit()

    def git(self, *args):
        return subprocess.run(['git','-C',str(self.repo),*args],check=True,capture_output=True,text=True).stdout

    def commit(self):
        self.git('add','.');self.git('commit','-qm','fixture')

    def report(self,bundle):
        return {'schema_version':'oracle-clue.review/v1',**{k:bundle[k] for k in ['repo','base','head','diff_sha256','context_sha256']},
                'provider':{'name':'fixture externa','model':None},'review_status':'completo','limitations':[],
                'findings':[{'id':'F1','kind':'bug','severity':'media','confidence':0.8,
                'title':'Acepta espacios','explanation':'bool no elimina espacios.',
                'location':{'file':'notas.py','side':'head','start_line':2,'end_line':2},
                'trigger':'Título con espacios','evidence':'Se quitó strip en el diff.',
                'verification':'Probar valida con tres espacios.','status':'pendiente'}]}

    def test_contexto_determinista_y_defecto_sembrado(self):
        before=self.git('status','--porcelain')
        b=c.prepare(self.repo,self.base)
        self.assertEqual(b,c.prepare(self.repo,self.base))
        self.assertIn('-    return bool(titulo.strip())',b['files'][0]['patch'])
        self.assertIn('+    return bool(titulo)',b['files'][0]['patch'])
        self.assertEqual(before,self.git('status','--porcelain'))
        c.validate_report(self.report(b),b,self.repo)

    def test_diff_vacio_o_base_invalida(self):
        for ref in ['HEAD','--output=/tmp/no','ref-inexistente']:
            with self.assertRaises(c.ClueError):c.prepare(self.repo,ref)

    def test_cambios_sin_commit(self):
        (self.repo/'notas.py').write_text('modificado')
        with self.assertRaises(c.ClueError):c.prepare(self.repo,self.base)

    def test_hashes_y_contexto_cambiados(self):
        (self.repo/'spec.md').write_text('rechazar espacios')
        b=c.prepare(self.repo,self.base,['spec.md']);r=self.report(b)
        (self.repo/'spec.md').write_text('nuevo acuerdo')
        with self.assertRaises(c.ClueError):c.validate_report(r,b,self.repo)
        self.commit()
        with self.assertRaises(c.ClueError):c.validate_report(r,b,self.repo)

    def test_informe_de_otro_contexto_y_paquete_manipulado(self):
        b=c.prepare(self.repo,self.base);r=self.report(b)
        r['head']='a'*40
        with self.assertRaises(c.ClueError):c.validate_report(r,b,self.repo)
        b['files'][0]['ranges']['head']=[[1,200]]
        with self.assertRaises(c.ClueError):c.validate_report(self.report(b),b,self.repo)

    def test_ubicaciones_ids_y_decisiones_del_modelo(self):
        b=c.prepare(self.repo,self.base)
        for loc in [{'file':'../afuera','side':'head','start_line':1,'end_line':1},
                    {'file':'notas.py','side':'head','start_line':8,'end_line':8},
                    {'file':'notas.py','side':'head','start_line':2,'end_line':1}]:
            r=self.report(b);r['findings'][0]['location']=loc
            with self.assertRaises(c.ClueError):c.validate_report(r,b,self.repo)
        r=self.report(b);r['findings']*=2
        with self.assertRaises(c.ClueError):c.validate_report(r,b,self.repo)
        r=self.report(b);r['findings'][0]['status']='descartado'
        with self.assertRaises(ValidationError):c.validate_report(r,b,self.repo)

    def test_ubicacion_de_linea_borrada(self):
        (self.repo/'notas.py').unlink();self.commit()
        b=c.prepare(self.repo,self.base);r=self.report(b)
        r['findings'][0]['location']['side']='base'
        c.validate_report(r,b,self.repo)
        r['findings'][0]['location']['side']='head'
        with self.assertRaises(c.ClueError):c.validate_report(r,b,self.repo)

    def test_secretos_binarios_y_symlinks_se_declaran_sin_incluirlos(self):
        (self.repo/'.env').write_text('SECRET=secreto_fixture')
        (self.repo/'binary').write_bytes(b'\0abc')
        (self.repo/'link').symlink_to(self.repo/'.env')
        self.commit()
        b=c.prepare(self.repo,self.base)
        self.assertEqual(len(b['omissions']),3)
        self.assertNotIn('secreto_fixture',json.dumps(b))
        with self.assertRaises(c.ClueError):c.validate_report(self.report(b),b,self.repo)
        r=self.report(b);r.update(review_status='incompleto',limitations=['Se omitieron tres archivos.'])
        c.validate_report(r,b,self.repo)

    def test_contexto_fuera_del_repo_o_credenciales(self):
        (self.root/'externo').write_text('dato')
        (self.repo/'contexto').symlink_to(self.root/'externo')
        for name in ['../externo','contexto','.env','/etc/passwd','C:/credenciales']:
            with self.assertRaises(c.ClueError):c.prepare(self.repo,self.base,[name])

    def test_limites_sin_truncamiento_silencioso(self):
        (self.repo/'large').write_text('x'*(c.FILE_LIMIT+1));self.commit()
        with self.assertRaises(c.ClueError):c.prepare(self.repo,self.base)

    def test_salida_fuera_del_repo_y_sin_sobrescritura(self):
        b=c.prepare(self.repo,self.base)
        with self.assertRaises(c.ClueError):c.write_bundle(b,self.repo/'review.json')
        out=self.root/'bundle.json';out.write_text('original')
        with self.assertRaises(FileExistsError):c.write_bundle(b,out)
        self.assertEqual(out.read_text(),'original')

    def test_no_ejecuta_textconv(self):
        (self.repo/'.gitattributes').write_text('*.py diff=hostil\n');self.commit()
        self.git('config','diff.hostil.textconv','comando_que_no_existe_123')
        self.assertTrue(c.prepare(self.repo,self.base)['files'])

    def test_triage_referencia_vigente_y_ids_unicos(self):
        b=c.prepare(self.repo,self.base);r=self.report(b);data=c.encoded(r)
        t={'schema_version':'oracle-clue.triage/v1','report_sha256':c.digest(data),'decisions':[
            {'finding_id':'F1','status':'riesgo_aceptado','reason':'Fixture','actor':'fixture','at':'2026-10-03T12:00:00Z'}]}
        c.validate_triage(t,r,data)
        t['decisions']*=2
        with self.assertRaises(c.ClueError):c.validate_triage(t,r,data)
        t['decisions']=t['decisions'][:1];t['report_sha256']='a'*64
        with self.assertRaises(c.ClueError):c.validate_triage(t,r,data)

    def test_schemas_distribuidos_coinciden_con_contratos(self):
        root=Path(__file__).resolve().parents[1]
        for name in ['hallazgos.schema.json','triage.schema.json']:
            self.assertEqual(c.schema(name).schema,json.loads((root/'docs'/name).read_text()))
