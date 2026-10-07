# El paquete y el informe no guardan la ruta absoluta del checkout

- ESTADO: ABIERTA
- PRIORIDAD: 30
- ETIQUETAS: privacidad


## Objetivo

Hoy el paquete (`oracle-clue.bundle/v1`) y el informe (`oracle-clue.review/v1`) guardan en `repo` la ruta absoluta del checkout revisado (p. ej. `/home/<usuario>/…`). Oracle Factory versiona los informes de los revisores en la carpeta de cada candidato, así que esa ruta privada termina en repositorios públicos. Pedido de Brian (2026-10-07, desde Oracle Factory): guardar una ruta relativa o un alias, y que `validar` reciba el checkout con `--repo` como hoy, sin exigir que coincida la ruta guardada.
