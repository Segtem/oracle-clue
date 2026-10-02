# Prototipar revisión de cambios con Oracle Clue

- ESTADO: ABIERTA
- PRIORIDAD: 50
- ETIQUETAS: 

### Nota (2026-10-02 21:24:33 UTC)

Acordado: CLI local fuera del ciclo de instalación de cada repo; agente/modelo intercambiable; primera etapa arma contexto reproducible y luego valida hallazgos sobre defectos sembrados. No toca archivos ni toma decisiones.

# Oracle Clue: prototipar revisor de cambios

## Decisiones del prototipo

- CLI local que acepta la ruta a cualquier checkout Git; nada que instalar en cada repositorio revisado.
- Adaptadores intercambiables para agentes locales; empezar por generar contexto reproducible antes de acoplar una llamada a modelo.
- Entrada: base, diff, spec OpenSpec enlazada, reglas opcionales del repo y evidencia de pruebas.
- Salida: hallazgos estructurados, rastreables a archivo/líneas y al commit revisado. Incluir incertidumbre explícita.
- Solo lectura. La persona hace triage y conserva autoridad para aceptar, descartar o corregir hallazgos.
- Un diff nuevo invalida los hallazgos previos. Oracle mantiene su rol separado de juzgar evidencia contra requisitos.
- No GitHub App, comentarios ni auto-fix en el primer corte.

## Próximo paso

Implementar el generador de paquete de revisión para `--base <ref>` (diff, metadatos y spec OpenSpec enlazada) y validarlo con un repo de prueba que contenga defectos sembrados.

### Nota (2026-10-02 21:26:04 UTC)

Inicialicé ~/Dev/oracle-clue con Git y Oracle; README define el enfoque y los límites iniciales. Todavía no hay revisión automática implementada ni remote GitHub configurado.
