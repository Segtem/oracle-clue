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


### Nota (2026-10-03 13:12:23 UTC)

Release alpha publicado y verificado: https://github.com/Segtem/oracle-clue/releases/tag/v0.1.0a1. Tag v0.1.0a1 sobre 007192e73df8a33610b16bdeeb4d7e91ebb9dfa5; main empujado. Wheel, sdist y SHA256SUMS remotos coinciden con los artefactos probados. PyPI queda pendiente del usuario.

## Próximo paso

El usuario publica en PyPI los artefactos probados del release v0.1.0a1 (también en dist/), siguiendo NOTAS-DE-RELEASE.md. Tras su aviso, verificar instalación desde PyPI con uv en un entorno limpio y actualizar la guía para usar el índice. Después implementar el adaptador IA y evaluar precisión; este alpha solo prepara contexto y valida informes externos.
