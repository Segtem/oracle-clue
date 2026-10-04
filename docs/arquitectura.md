# Arquitectura de Oracle Clue

Estado 0.1.0a1: implementados `preparar` (diff entre commits, con árbol versionado limpio) y `validar` (informe externo y triage opcional). `review`, adaptadores, configuración automática e integración con Factory/GitHub siguen siendo diseño futuro.

## Propósito y frontera

El diseño completo busca encontrar riesgos concretos introducidos por un cambio y preparar evidencia para el triage humano. El alpha publicado prepara contexto y valida informes externos; todavía no encuentra riesgos automáticamente. El flujo de desarrollo completo pertenece a Oracle Factory. Clue no reemplaza pruebas, revisión humana, Oracle ni al agente que implementa.

## Ejecución prevista del revisor futuro

- La herramienta se instala una vez en el entorno del desarrollador o se ejecuta desde su checkout de desarrollo. Los repos revisados no instalan Clue como dependencia obligatoria.
- Entrada conceptual: `clue review --repo <ruta> --base <ref> [--change <id>] [--provider codex|claude]`. La ruta por defecto será el cwd.
- La CLI recolecta datos Git y archivos explícitos; invoca el adaptador seleccionado en modo de solo lectura; valida el informe; imprime Markdown y conserva JSON.
- `.oracle-clue.toml` será opcional y declarará rutas de contexto, comandos de test sugeridos y convenciones locales. Sus comandos requieren aceptación explícita del operador antes de ejecutarse.

## Flujo previsto de análisis

1. Resolver repo, HEAD, base y diff. Rechazar base inexistente y diff vacío; limitar tamaño y excluir binarios/secretos conocidos.
2. Asociar el cambio con una tarea o paquete OpenSpec por id explícito o metadatos, sin inferir aprobación.
3. Reunir spec aceptada, archivos cambiados, reglas y evidencia de tests que el operador entregue. El primer prototipo no ejecuta pruebas.
4. Pedir al proveedor solo defectos plausibles introducidos por el diff. Cada afirmación debe enlazar evidencia y ubicación.
5. Validar schema, archivo/rango de línea contra el diff y registrar hash de base, HEAD y diff. Invalidar el reporte si alguno cambia.
6. Dejar cada hallazgo en estado pendiente hasta que una persona lo corrija, descarte con motivo o acepte como riesgo.

## Interfaz de proveedor

Un adaptador recibe un paquete serializado y devuelve JSON conforme al schema. El primer adaptador de prueba puede llamar a `codex exec` en modo read-only; después se compara Claude CLI usando el mismo corpus. Clue no entrega permisos de escritura al proveedor. La revisión no debe fallar silenciosamente a un proveedor alternativo ni esconder su identidad, modelo o errores.

## Esquema de hallazgos

`docs/hallazgos.schema.json` fija el formato. Clases iniciales: bug, seguridad, regresión, discrepancia_con_spec y pregunta. Severidad y confianza son campos separados; una confianza baja no se presenta como hallazgo confirmado. Cada elemento debe incluir título, explicación breve, archivo/líneas, lado base/head del diff, escenario activador, evidencia observable y recomendación de verificación (`verification`). No permitir que el modelo escriba o autoaplique parches.

## Evaluación del prototipo

Preparar cambios de prueba con defectos conocidos y cambios limpios. Registrar defectos sembrados detectados, falsos positivos, ubicaciones correctas y defectos repetidos entre proveedores. No declarar éxito por elocuencia: el criterio es utilidad accionable para una persona.

## Evolución posterior

1. Generador determinista del paquete de revisión y pruebas.
2. Adaptador de agente local, schema validado y reportes vinculados a hash.
3. Triage humano persistente en Oracle Task/Factory.
4. Integración GitHub opcional que publica el reporte en PR; sigue sin aprobar ni fusionar automáticamente.

## Frontera entre el modelo y la decisión humana

El adaptador entrega hallazgos pendientes. La CLI completa la identidad del proveedor, modelo (o `null` si no se informa), hashes de commit/diff/contexto y estado de ejecución con datos comprobados; esos metadatos no se toman como afirmaciones del modelo. `review_status: incompleto` requiere explicar limitaciones; un informe vacío o incompleto no equivale a aprobación.

El informe original se conserva separado del triage; el enlace por hash detecta cambios en sus bytes, sin impedir editar el archivo. El triage humano vive en `docs/triage.schema.json`, enlazado por el hash del informe, con id de hallazgo, decisión, motivo, actor y fecha. El schema del informe rechaza estados corregido/descartado/riesgo_aceptado. Guardar un nombre de actor no autentica una identidad: esa garantía requiere el canal humano de Factory o GitHub.

La validación publicada comprueba también lo que JSON Schema no garantiza: ids únicos; `start_line <= end_line`; rutas relativas dentro del checkout; rangos pertenecientes al lado correcto del diff; referencias a hallazgos existentes y decisiones vinculadas al informe vigente. El hash del contexto incluye los archivos explícitos de spec, reglas o evidencia que el operador seleccionó, además del diff. Un contexto cambiado exige otra revisión. La confianza declarada por el modelo no es una probabilidad calibrada.

Ejecutar un agente desde una CLI local no implica inferencia local: Codex/Claude pueden enviar contexto al proveedor que tengan configurado. El operador elige proveedor y alcance de archivos. El paquete debe declarar omisiones y truncamientos; no prometer detección infalible de secretos ni analizar repos completos por defecto.

## Verificación del contrato

`tests/test_contract.py` valida ambos schemas y casos positivos/negativos. Requiere `jsonschema` (solo para pruebas): `uv run --with jsonschema python -m unittest discover -s tests -v`. Los tests de CLI agregan recolección y validación sobre repos temporales. Todavía no existe análisis automático ni evaluación de precisión de un modelo.
