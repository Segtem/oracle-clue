# Prototipar revisión de cambios con Oracle Clue

- ESTADO: ABIERTA
- PRIORIDAD: 50
- ETIQUETAS: 

### Nota (2026-10-02 21:24:33 UTC)

Acordado: CLI local fuera del ciclo de instalación de cada repo; agente/modelo intercambiable; primera etapa arma contexto reproducible y luego valida hallazgos sobre defectos sembrados. No toca archivos ni toma decisiones.

## Decisiones del prototipo

- CLI local que acepta la ruta a cualquier checkout Git; nada que instalar en cada repositorio revisado.
- Adaptadores intercambiables para agentes locales; empezar por generar contexto reproducible antes de acoplar una llamada a modelo.
- Entrada: base, diff, spec OpenSpec enlazada, reglas opcionales del repo y evidencia de pruebas.
- Salida: hallazgos estructurados, rastreables a archivo/líneas y al commit revisado. Incluir incertidumbre explícita.
- Solo lectura. La persona hace triage y conserva autoridad para aceptar, descartar o corregir hallazgos.
- Un diff nuevo invalida los hallazgos previos. Oracle mantiene su rol separado de juzgar evidencia contra requisitos.
- No GitHub App, comentarios ni auto-fix en el primer corte.

### Nota (2026-10-02 22:28:35 UTC)

Esbozo funcional completado: flujo read-only, CLI conceptual, adaptador, límites, evaluación y schema JSON versionado en docs/. Próximo paso: implementar el bundle y validarlo con defectos sembrados.

### Nota (2026-10-02 22:30:44 UTC)

Remoto público Segtem/oracle-clue confirmado en GitHub; se publica el esbozo de arquitectura en main.

### Nota (2026-10-02 23:11:37 UTC)

Auditoría: schema del modelo restringido a pendiente; triage humano separado con motivo/actor/fecha y hash del informe. Añadidos contexto, estado incompleto, lado del diff y verificación. 7 pruebas JSON Schema OK. Sigue siendo esbozo y contratos, no CLI implementada.


### Nota (2026-10-03 12:37:35 UTC)

Usuario autorizó preparar paquete y GitHub Release. Primer corte alpha 0.1.0a1: generador determinista del contexto y validador de informes, instalable por uv. Adaptadores IA y evaluación de precisión siguen pendientes; no se publica una capacidad que aún no existe.

### Nota (2026-10-03 12:56:50 UTC)

Clue: 21 tests de contratos y recolección/validación OK contra el wheel instalado con Python 3.11.16. Entry point probado fuera del checkout: contexto, informe fixture válido, rango falso rechazado y repo intacto. Twine valida wheel y sdist. No se evaluó precisión de IA: el alpha no invoca modelos.

## Próximo paso

Integrar el corte alpha 0.1.0a1 en main, construir los artefactos definitivos y publicar tag/GitHub Release con wheel, sdist y SHA256SUMS. Después el usuario publica en PyPI; verificar instalación desde el índice tras su aviso. Clue conserva pendiente el adaptador IA y la evaluación con defectos sembrados y cambios limpios.
