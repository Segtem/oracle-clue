# Oracle Clue

Revisor asistido de cambios para Oracle Factory. Busca defectos concretos en un diff y deja evidencia para que una persona los evalúe. No aprueba ni modifica código.

## Enfoque del prototipo

Oracle Clue será una CLI que se ejecuta desde la máquina del desarrollador contra cualquier checkout Git. No requiere instalar una GitHub App ni agregar una dependencia de ejecución al repositorio revisado. Al principio podrá usar un agente local mediante un adaptador; la interfaz de análisis no quedará atada a un proveedor. Una configuración opcional `.oracle-clue.toml` podrá declarar convenciones, límites y comandos de prueba.

El comando de revisión será de solo lectura y tomará el diff, la spec OpenSpec enlazada, las reglas del proyecto y la evidencia de pruebas disponible. Entregará hallazgos estructurados con ruta y líneas, escenario de reproducción, impacto, evidencia, confianza y requisito relacionado cuando corresponda. Si la evidencia no alcanza, registrará una pregunta o incertidumbre, no un defecto afirmado.

La persona triagea cada hallazgo: corregido, aceptado con motivo o descartado con motivo. Un cambio posterior invalida el informe anterior. Oracle evalúa por separado si la evidencia satisface los requisitos; la aprobación del revisor no sustituye ese veredicto ni la decisión humana de cierre.

## Límites del primer prototipo

- Solo revisa cambios entre una base y el checkout actual; no hace revisión general de todo el repositorio.
- No edita archivos, no comenta en GitHub y no aprueba ni fusiona PR.
- El primer criterio de éxito será detectar defectos sembrados en un conjunto pequeño de cambios y mantener pocos falsos positivos.
- GitHub será una integración posterior, usando el mismo formato de informe.

## Estado

La arquitectura inicial está registrada en la tarea Trackertast `20261002-212339-prototipar`. El primer próximo paso es implementar un generador reproducible de paquete de revisión y probarlo con defectos sembrados antes de conectar un modelo.
