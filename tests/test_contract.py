import copy
import json
from pathlib import Path
import unittest
from jsonschema import Draft202012Validator, FormatChecker

ROOT=Path(__file__).resolve().parents[1]

class Contratos(unittest.TestCase):
    def setUp(self):
        self.report=Draft202012Validator(json.loads((ROOT/'docs/hallazgos.schema.json').read_text()))
        self.triage=Draft202012Validator(json.loads((ROOT/'docs/triage.schema.json').read_text()), format_checker=FormatChecker())
        self.finding={'id':'F1','kind':'bug','severity':'alta','confidence':0.8,'title':'Caso de prueba', 'explanation':'Falla con el valor vacío.', 'location':{'file':'app.py','side':'head','start_line':3,'end_line':4},'trigger':'Entrada vacía','evidence':'División por cero en la rama agregada.','verification':'Ejecutar el caso vacío.','status':'pendiente'}
        self.valid={'schema_version':'oracle-clue.review/v1','repo':'ejemplo','base':'a'*40,'head':'b'*40,'diff_sha256':'c'*64,'context_sha256':'d'*64,'provider':{'name':'ejemplo','model':None},'review_status':'completo','limitations':[],'findings':[self.finding]}
        self.decision={'schema_version':'oracle-clue.triage/v1','report_sha256':'e'*64,'decisions':[{'finding_id':'F1','status':'descartado','reason':'El escenario está excluido por contrato.','actor':'persona','at':'2026-10-02T22:00:00Z'}]}

    def test_schemas_y_ejemplos_validos(self):
        for v in (self.report,self.triage): Draft202012Validator.check_schema(v.schema)
        self.report.validate(self.valid); self.triage.validate(self.decision)

    def test_modelo_no_puede_resolver_hallazgos(self):
        for status in ('corregido','descartado','riesgo_aceptado'):
            self.finding['status']=status
            self.assertFalse(self.report.is_valid(self.valid))

    def test_decision_sin_motivo_actor_o_referencia_es_invalida(self):
        for campo in ('reason','actor','finding_id','at'):
            payload=copy.deepcopy(self.decision); del payload['decisions'][0][campo]
            self.assertFalse(self.triage.is_valid(payload))
        self.decision['decisions'][0]['reason']=''
        self.assertFalse(self.triage.is_valid(self.decision))

    def test_informe_incompleto_exige_limitaciones(self):
        self.valid['review_status']='incompleto'
        self.assertFalse(self.report.is_valid(self.valid))
        self.valid['limitations']=['Faltó un archivo de contexto.']
        self.report.validate(self.valid)

    def test_contexto_y_modelo_deben_declararse(self):
        payload=copy.deepcopy(self.valid); del payload['context_sha256']
        self.assertFalse(self.report.is_valid(payload))
        del self.valid['provider']['model']
        self.assertFalse(self.report.is_valid(self.valid))

    def test_ubicacion_incluye_lado_y_verificacion(self):
        for path in ('side','end_line'):
            payload=copy.deepcopy(self.valid); del payload['findings'][0]['location'][path]
            self.assertFalse(self.report.is_valid(payload))
        del self.finding['verification']
        self.assertFalse(self.report.is_valid(self.valid))

    def test_triage_rechaza_fecha_invalida(self):
        self.decision['decisions'][0]['at']='ayer'
        self.assertFalse(self.triage.is_valid(self.decision))
