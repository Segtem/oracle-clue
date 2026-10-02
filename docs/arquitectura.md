# Esbozo funcional de Oracle Clue

## Propósito y frontera

Clue encuentra riesgos concretos introducidos por un cambio y prepara evidencia para el triage humano. El flujo de desarrollo completo pertenece a Oracle Factory. Clue no reemplaza pruebas, revisión humana, Oracle ni al agente que implementa.

## Ejecución

- La herramienta se instala una vez en el entorno del desarrollador o se ejecuta desde su checkout de desarrollo. Los repos revisados no instalan Clue como dependencia obligatoria.
- Entrada conceptual: `clue review --repo <ruta> --base <ref> [--change <id>] [--provider codex|claude]`. La ruta por defecto será el cwd.
- La CLI recolecta datos Git y archivos explícitos; invoca el adaptador seleccionado en modo de solo lectura; valida el informe; imprime Markdown y conserva JSON.
- `.oracle-clue.toml` será opcional y declarará rutas de contexto, comandos de test sugeridos y convenciones locales. Sus comandos requieren aceptación explícita del operador antes de ejecutarse.

## Flujo de análisis

1. Resolver repo, HEAD, base y diff. Rechazar base inexistente y diff vacío; limitar tamaño y excluir binarios/secretos conocidos.
2. Asociar el cambio con una tarea o paquete OpenSpec por id explícito o metadatos, sin inferir aprobación.
3. Reunir spec aceptada, archivos cambiados, reglas y evidencia de tests que el operador entregue. El primer prototipo no ejecuta pruebas.
4. Pedir al proveedor solo defectos plausibles introducidos por el diff. Cada afirmación debe enlazar evidencia y ubicación.
5. Validar schema, archivo/rango de línea contra el diff y registrar hash de base, HEAD y diff. Invalidar el reporte si alguno cambia.
6. Dejar cada hallazgo en estado pendiente hasta que una persona lo corrija, descarte con motivo o acepte como riesgo.

## Interfaz de proveedor

Un adaptador recibe un paquete serializado y devuelve JSON conforme al schema. El primer adaptador de prueba puede llamar a `codex exec` en modo read-only; después se compara Claude CLI usando el mismo corpus. Clue no entrega permisos de escritura al proveedor. La revisión no debe fallar silenciosamente a un proveedor alternativo ni esconder su identidad, modelo o errores.

## Esquema de hallazgos

`docs/hallazgos.schema.json` fija el formato. Clases iniciales: bug, seguridad, regresión, discrepancia_con_spec y pregunta. Severidad y confianza son campos separados; una confianza baja no se presenta como hallazgo confirmado. Cada elemento debe incluir título, explicación breve, archivo/líneas, escenario activador, evidencia observable y recomendación de verificación. No permitir que el modelo escriba o autoaplique parches.

## Evaluación del prototipo

Preparar cambios de prueba con defectos conocidos y cambios limpios. Registrar defectos sembrados detectados, falsos positivos, ubicaciones correctas y defectos repetidos entre proveedores. No declarar éxito por elocuencia: el criterio es utilidad accionable para una persona.

## Evolución posterior

1. Generador determinista del paquete de revisión y pruebas.
2. Adaptador de agente local, schema validado y reportes vinculados a hash.
3. Triage humano persistente en Trackertast/Factory.
4. Integración GitHub opcional que publica el reporte en PR; sigue sin aprobar ni fusionar automáticamente.
