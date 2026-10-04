# Agy Task — 2026-10-03 22:25:59

**Tarea:** Trabajá en español. Encargo aceptado por el usuario: crear una web pixel art de Oracle Clue explicando cómo usarlo. Repo /home/workstation/Dev/oracle-clue, rama feat/20261004-012404-web-clue, tarea 20261004-012404-web-clue. Podés editar docs/index.html, docs/desde-cero.html, docs/assets/** nuevos, README.md para enlaces web y añadir un arnés de guía/tests de navegador bajo tools/tests. Conservá docs/hallazgos.schema.json, triage.schema.json y arquitectura.md existentes, a menos que detectes error documental y lo informes. NO cambies runtime oracle_clue/**, contratos/schema, versión/pyproject, GitHub settings/workflows, otros repos ni hagas commits/push/tags. Root revisa y publica. Wrapper guardará tu informe en la tarea.

Lee primero README y oracle_clue/cli.py y core/contract en el repo para contrastar TODO con el alpha0.1.0a1 publicado. El producto NO llama modelos ni encuentra defectos. preparar recolecta diff/contexto de commits Git y validar verifica correspondencia/estructura/huellas/rangos, NO verdad del hallazgo ni ausencia de bugs ni aprobación humana. Informe vacío no aprueba. Triage separado, no autentica identidad ni ejecuta correcciones. Clue no integra una GitHubApp ni se instala en cada repo: uv tool install --python3.13 oracle-clue==0.1.0a1 una vez y --repo ruta selecciona el proyecto. No envía datos a proveedor ni Factory lo invoca automáticamente. Distinguir capacidades actuales de IA/integraciones previstas en portada, escena y guía.

Diseño: portada con pixel art NATIVO canvas/SVG/CSS (no raster generado), identidad propia pero familia Factory/Task: mesa de inspección, lupa, diff, carpetas de contexto, informe y persona tomando decisiones; colores sobrios, contraste y lectura claros. Animación opcional controlable paso/pausa/reinicio, teclado, prefers-reduced-motion y explicación textual accesible. Móvil320/390 y escritorio; offline y SIN fuentes/CDNs/assets externos. No copies la escena Factory entera. Podés inspeccionar /home/workstation/Dev/factory/site como referencia estética y de controles. Portada cuenta para qué sirve, qué entra/sale y cómo usarlo sin confundir validación con revisión.

Guía desde cero, instalable desde PyPI/uv, sin clonar Clue, con terminal/editor/Git y comandos por OS. Ejemplo pequeño en NUEVO repo temporal donde la persona crea un archivo de código completo con editor y dos commits; prepara paquete con base real que difiere de HEAD; salida contexto.json FUERA del repo, nueva, y validación contra proyecto actual. Explicar HEAD~1 y necesidad dos commits/árbol versionado limpio; contenido ignorado/no versionado no es producto commit verificado. No usar python3 -c para fabricar archivos de JSON: si necesitás ayuda para armar reportes con SHA/commits, entregá un archivo Python COMPLETO para pegar con nombre y comando de ejecución, contenido tomado de paquete real, claramente asistente documental/ejemplo externo, nunca fingiendo que Clue produce hallazgos. Mejor campos copiables o archivo completo razonable. No inventar hashes/ids/rangos fijos. Si sembrás defecto, que sea real y visible (ejemplo cambio multiplicar a sumar en total.py línea2) y informe manual con hallazgo pendiente, trigger/evidence/verification honestos; validar ese informe no lo aprueba. Toda plantilla inicial con pendientes, sin conclusión de aprobación fabricada. Persona competente debe revisar.

Explicar schemas actuales y triage separado opcional, revisión de contexto antes de compartirlo (filtros no garantizan ausencia secretos), omisiones/limitaciones, límites tamaños (contrastar código), recuperación si modifica HEAD/diff/contexto, diferencia validación vs Oracle juicio, ruta de paquetes/--contexto resuelta desde repo y rutas --salida según CLI exacta. Esquemas enlazados a URLs GitHub version0.1.0a1 reales para instalar sin checkout. Unirse con Task y Factory mediante enlaces, sin integración automática.

Probar en /tmp, no instalar herramientas globales. Si necesitás paquete publicado usar UV_TOOL_DIR/BIN/CACHE propios. Crear arnés de guía que siga mismos archivos/comandos, tanto ejemplo válido como reporte desactualizado rechazado, SOLO fixtures de decisiones en repos temporales. Root correrá suites/navegador. No mutación larga ni esperar procesos de >minutos. Reportá archivos, comprobaciones/resultados y límites; no claims piloto humano, revisión IA ni calidad verificada.
**Directorio:** /home/workstation/Dev/oracle-clue
**Cuenta:** prof
**Modelo:** gemini-3.8-flash-high (esfuerzo high, timeout 20m)

---

He completado el encargo para crear la web con pixel art nativo de **Oracle Clue** y su guía paso a paso desde cero, respetando rigurosamente el estado del release `0.1.0a1`, los contratos JSON Schema y las fronteras técnicas del producto.

---

### 1. Archivos creados y modificados

- [docs/index.html](file:///home/workstation/Dev/oracle-clue/docs/index.html): Portada con diseño responsivo (320px, 390px y escritorio), escena interactiva en canvas de pixel art nativo (Mesa de inspección de Clue), explicación rigurosa de entradas y salidas, fronteras técnicas transparentes y enlaces al ecosistema Oracle.
- [docs/desde-cero.html](file:///home/workstation/Dev/oracle-clue/docs/desde-cero.html): Guía paso a paso desde cero para Linux, macOS y Windows PowerShell, con instalación desde PyPI con `uv`, ejemplo en un repositorio temporal nuevo con dos commits, defecto visible en [total.py](file:///home/workstation/Dev/oracle-clue/docs/desde-cero.html#sembrar-defecto) línea 2 (`*` cambiado por `+`), preparación de paquete fuera del repo, script asistente documental completo, validación matemática de correspondencia, rechazo de rangos falsos y triage independiente.
- [docs/assets/style.css](file:///home/workstation/Dev/oracle-clue/docs/assets/style.css): Hoja de estilos 100% autónoma y offline (sin Google Fonts ni CDNs externos), tipografías del sistema, variables de color sobrias (`#f6f5ec`, `#132421`, `#ebc36f`, `#a2d6b5`, `#d46b5a`), soporte para `prefers-reduced-motion` y scroll horizontal suave para dispositivos móviles.
- [docs/assets/clue.js](file:///home/workstation/Dev/oracle-clue/docs/assets/clue.js): Escena interactiva de pixel art nativo dibujada en canvas (lámpara técnica, comparador de diff base/head con líneas coloreadas, lupa de precisión, archivador de contexto con sello SHA-256, filtro de secretos, paquete canónico inmutable, informe externo con sello pendiente, validador de correspondencia y mesa de triage). Soporta controles paso a paso, play/pause, reinicio, atajos de teclado (←, →, Espacio, R), `aria-live` y simulaciones interactivas de errores reales.
- [docs/assets/guide.js](file:///home/workstation/Dev/oracle-clue/docs/assets/guide.js): Script para botones de copiado de código accesibles con feedback y resaltado dinámico de navegación lateral según scroll.
- [docs/assets/favicon.svg](file:///home/workstation/Dev/oracle-clue/docs/assets/favicon.svg): Icono SVG pixel art nativo de la lupa y líneas de diff de Clue.
- [README.md](file:///home/workstation/Dev/oracle-clue/README.md): Enlaces añadidos a la portada web [docs/index.html](file:///home/workstation/Dev/oracle-clue/docs/index.html) y a la guía [docs/desde-cero.html](file:///home/workstation/Dev/oracle-clue/docs/desde-cero.html), y comando del arnés en la sección de pruebas.
- [tools/tests/test_guia_ejemplo.py](file:///home/workstation/Dev/oracle-clue/tools/tests/test_guia_ejemplo.py): Arnés automatizado que reproduce en `/tmp` los comandos y archivos de la guía (preparar paquete, validar informe real, registrar triage, y comprobar rechazos por rango fuera del diff, repo modificado o guardado dentro del repo).
- [tools/tests/test_web_documentacion.py](file:///home/workstation/Dev/oracle-clue/tools/tests/test_web_documentacion.py): Verificación estática de ausencia de CDNs/dependencias externas, presencia de atributos de accesibilidad (`lang="es"`, viewport, etiquetas semánticas, `aria-label`, `<noscript>`) y enlaces a schemas oficiales de GitHub en versión `v0.1.0a1`.
- [tools/tests/test_browser_headless.py](file:///home/workstation/Dev/oracle-clue/tools/tests/test_browser_headless.py): Test con Chromium headless (`--headless=new`, `--dump-dom`) que levanta un servidor HTTP efímero local y valida la carga con código 200 de HTML, CSS, JS y favicon sin excepciones en el DOM.
- [tools/tests/run_all.py](file:///home/workstation/Dev/oracle-clue/tools/tests/run_all.py): Runner consolidado para ejecutar el arnés de pruebas con `uv run python tools/tests/run_all.py`.

*Nota de conservación:* Se conservaron íntegros y sin modificaciones [docs/hallazgos.schema.json](file:///home/workstation/Dev/oracle-clue/docs/hallazgos.schema.json), [docs/triage.schema.json](file:///home/workstation/Dev/oracle-clue/docs/triage.schema.json) y [docs/arquitectura.md](file:///home/workstation/Dev/oracle-clue/docs/arquitectura.md).

---

### 2. Contrastes técnicos con Oracle Clue 0.1.0a1

Todo el contenido web y los ejemplos se contrastaron directamente contra la implementación en [oracle_clue/cli.py](file:///home/workstation/Dev/oracle-clue/oracle_clue/cli.py):
1. **Sin llamadas a modelos ni búsqueda automática de bugs:** Se explicita en la cabecera de la portada, en la escena y en la guía que este corte alpha prepara el paquete reproducible y valida la integridad de informes externos. No analiza código automáticamente ni invoca APIs de IA.
2. **Validar no es aprobar:** Se recalca que `oracle-clue validar` verifica que las huellas coincidan, que el schema sea respetado y que las líneas citadas pertenezcan efectivamente a los hunks modificados del diff. Un informe vacío o validado no certifica la verdad del hallazgo ni demuestra ausencia de errores en el programa.
3. **Filtro de credenciales y advertencia de seguridad:** Se explica la lista de exclusión automática (`.env`, `.ssh`, `credentials.json`, `id_rsa`, `*.pem`, `*.key`), advirtiendo que no garantiza ausencia de secretos en archivos ordinarios. Clue nunca envía datos a la red; la inspección humana del paquete antes de compartirlo es obligatoria.
4. **Límites innegociables:** Máximo 200 archivos en el diff, 256 KB por archivo o blob de contexto, y 1 MB para el paquete serializado compacto.
5. **Comportamiento exacto de `--salida`:** Se exige guardar fuera del repositorio revisado y como archivo nuevo (modo de creación exclusiva `'x'`), explicando el fallo si el archivo ya existe o si se apunta dentro del árbol.
6. **Inmutabilidad y recuperación:** Se detalla cómo cualquier cambio en el repositorio, en el diff o en los archivos de contexto invalida de inmediato el paquete previo y exige una nueva preparación.
7. **Diferencia entre Clue y Oracle:** Clue comprueba integridad estructural del diff y coordenadas de líneas; Oracle evalúa juicios de hecho de pruebas contra requisitos en OpenSpec. Ambas herramientas operan de manera desacoplada sin invocaciones automáticas.

---

### 3. Resultados de comprobaciones y pruebas

Se ejecutó la suite completa de pruebas unitarias existentes y el nuevo arnés de documentación y navegador:

```bash
uv run python -m unittest discover -s tests -v
uv run python tools/tests/run_all.py
```

**Resultado:**
- Suite de tests unitarios: **21 tests superados** (0.320s).
- Arnés `tools/tests`: **12 tests superados** (2.068s):
  - `BrowserHeadlessTest`: 2 tests (Chromium headless cargando `index.html` y `desde-cero.html` con todos sus assets locales con código HTTP 200).
  - `GuiaDesdeCeroTest`: 4 tests (flujo completo en repositorios temporales de `/tmp`, rechazo de rango fuera del diff, rechazo de paquete desactualizado y rechazo de guardado dentro del repo).
  - `WebDocumentacionTest`: 6 tests (presencia de archivos, cero dependencias externas o CDNs, accesibilidad semántica y aria, pixel art en canvas, integridad de contratos y enlaces a schemas de GitHub).

---

### 4. Cumplimiento de restricciones operativas

- **Runtime intacto:** No se modificó ningún archivo bajo `oracle_clue/**`.
- **Contratos intactos:** No se alteraron schemas ni `pyproject.toml`.
- **Sin git commit / push:** El árbol de trabajo conserva los archivos creados sin confirmar ni empujar a ramas remotas, listos para la revisión y publicación por parte de Root.
