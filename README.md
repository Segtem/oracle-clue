# Oracle Clue — 0.1.0a1 (alpha)

CLI local para preparar contexto reproducible y validar informes externos de revisión de cambios Git. Funciona por separado de Oracle Factory y no requiere una GitHub App ni una dependencia en cada repositorio revisado.

**Este primer corte no llama a un modelo ni encuentra defectos automáticamente.** Entrega el contexto y las comprobaciones de integridad sobre los que se construirá ese revisor. Nunca aprueba, edita código ni fusiona cambios.

- **Mesa de inspección interactiva (pixel art nativo):** [docs/index.html](docs/index.html)
- **Guía paso a paso desde cero:** [docs/desde-cero.html](docs/desde-cero.html)

## Instalación

La versión alpha 0.1.0a1 está [publicada en PyPI](https://pypi.org/project/oracle-clue/0.1.0a1/):

```bash
uv tool install --python 3.13 oracle-clue==0.1.0a1
uv tool update-shell
oracle-clue --version
```

Requiere Git y Python >=3.11. También se puede ejecutar sin instalación persistente: `uvx --from oracle-clue==0.1.0a1 oracle-clue --help`. Los artefactos originales y sus hashes permanecen en el [release](https://github.com/Segtem/oracle-clue/releases/tag/v0.1.0a1).

## Preparar una revisión

Con los cambios confirmados en Git, seleccionar una base que difiera de HEAD. `HEAD~1` compara el último commit con su padre:

```bash
oracle-clue preparar --repo ./mi-proyecto --base HEAD~1 --salida contexto.json
```

La salida debe estar fuera de la carpeta revisada y ser un archivo nuevo. Sin `--salida`, el JSON se imprime por stdout. Para incluir archivos de contexto explícitos, agregar `--contexto spec.md --contexto evidencia/pruebas.txt`; sus rutas se resuelven desde la raíz del repo.

El paquete contiene commits base/HEAD, diff por archivo, contenido anterior/actual, rangos por lado y huellas del diff y contexto. Las mismas entradas producen el mismo JSON. `diff_sha256` corresponde a la representación Git raw sin abreviar (rutas, modos e ids de blobs); `context_sha256` abarca además texto, parches, omisiones y archivos seleccionados.

Rechaza cambios versionados sin commit, base inexistente, diff vacío y entradas demasiado grandes. El límite es 200 archivos, 256 KB por archivo y 1 MB para el paquete serializado compacto. Declara omisiones de binarios, enlaces, submódulos y rutas de credenciales conocidas. El filtro no garantiza que otros archivos no contengan secretos; el operador revisa el contexto antes de entregarlo a un proveedor. Clue no envía estos datos a la red.

## Validar un informe externo

Una persona o un proveedor externo produce el informe conforme a [hallazgos.schema.json](https://github.com/Segtem/oracle-clue/blob/v0.1.0a1/docs/hallazgos.schema.json). Los hallazgos conservan el estado `pendiente` y las huellas deben corresponder al paquete:

```bash
oracle-clue validar informe.json --paquete contexto.json --repo ./mi-proyecto
```

La CLI vuelve a recolectar el contexto actual y compara el paquete completo; verifica schema, huellas, ids únicos, rutas y rangos de línea del lado correcto del diff. Si hubo omisiones, exige un informe `incompleto` con limitaciones. Un informe vacío nunca equivale a aprobación.

El triage humano se guarda separado, según [triage.schema.json](https://github.com/Segtem/oracle-clue/blob/v0.1.0a1/docs/triage.schema.json). `validar` acepta `--triage decisiones.json` para comprobar el hash exacto del informe, fechas, ids referenciados y decisiones no duplicadas. No crea decisiones ni autentica al revisor o a quien figura como actor.

## Qué sigue

Adaptador de IA de solo lectura, evaluación con defectos sembrados y cambios limpios, e integración opcional con Factory/GitHub. La [arquitectura](https://github.com/Segtem/oracle-clue/blob/v0.1.0a1/docs/arquitectura.md) distingue el flujo previsto del alcance de este alpha. Oracle conserva su función separada: evaluar evidencia contra requisitos acordados.

## Pruebas

```bash
uv run python -m unittest discover -s tests -v
uv run python tools/tests/run_all.py
# Con Playwright disponible y Chromium instalado:
node tools/test_site.cjs
```

Las pruebas crean repos temporales, siembran un defecto y verifican que el paquete lo contiene y que un informe fixture apunta al cambio correcto. Comprueban también omisiones, límites, contexto modificado y contratos inválidos. El arnés en `tools/tests/` extrae los archivos y comandos de la guía publicada y ejecuta el recorrido completo en un repositorio temporal, incluidos los rechazos por ubicación inválida y contexto obsoleto. `tools/test_site.cjs` verifica en Chromium navegación, teclado, copia, pausa, movimiento reducido, enlaces y tamaños de pantalla. No sustituye una auditoría completa de accesibilidad ni una prueba con una persona principiante. No miden todavía precisión de un modelo.
