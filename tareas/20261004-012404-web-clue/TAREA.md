# Crear una web pixel art de Oracle Clue con guía precisa

- ESTADO: ABIERTA
- PRIORIDAD: 60
- ETIQUETAS:

## Pedido y alcance

El usuario pidió crear una web con pixel art para explicar cómo usar Oracle Clue. Se autoriza implementar documentación, recursos visuales nativos y pruebas de la web; conservar la CLI y su versión publicada. Instalación desde PyPI con uv, ejemplos reales y responsabilidades/límites explícitos. Commit/push y publicación web según autorización vigente. No inventar aprobaciones humanas ni presentar validaciones estructurales como revisión de calidad.

## Trabajo delegado

agy2: sitio nuevo y guía de Oracle Clue. Root: verificar comandos, contratos, navegador y despliegue.

### Nota (2026-10-04 01:24:04 UTC)

Pedido aceptado por el usuario en conversación: crear web pixel art explicando el uso. Se trabaja en rama separada; no se cambia runtime ni se simula aceptación de un producto.

### Nota (2026-10-04 01:31:11 UTC)

Root habilitó Pages (build_type workflow) en el repositorio y agregó workflow de publicación estática desde docs/. agy2 conserva ownership de las páginas/guía/assets; no cambia el programa. URL prevista https://segtem.github.io/oracle-clue/. Publicación final tras verificar.

### Nota (2026-10-04 02:08:45 UTC)

agy2 entregó sitio nuevo y guía; root corrigió alcance de hashes, rangos que incluyen contexto sin modificar, stdout opcional, preservación de informes y triage que pide decisiones explícitas sin fingir correcciones. También separó arquitectura vigente/futura, corrigió desborde móvil y acumulación RAF. Se reemplazaron tests estáticos/dump-dom por guía extraída del HTML y comprobaciones funcionales en Chromium. CLI publicada 0.1.0a1: 21 tests existentes OK. Guía desde cero completa ejecutada con CLI de PyPI en repo nuevo: paquete, informe manual del defecto visible, validación, línea 999 rechazada, triage fixture sin aprobación real, cambio de bytes del informe rechazado y HEAD corregido que invalida el paquete anterior. 11 comprobaciones Chromium OK, 320/390/768/1440 y sin dependencias de red en runtime. Capturas revisadas. Runtime, schemas y versión intactos. Pages configurado workflow. No hay adaptador IA, piloto humano ni ejecución en Windows/macOS. El informe histórico de agy2 describe su entrega inicial; esta nota y las evidencias finales describen la integración corregida.

- Adjunto: [clue-web-browser-final.json](clue-web-browser-final.json)

- Adjunto: [clue-web-guide-evidence.json](clue-web-guide-evidence.json)

- Adjunto: [portada-light.png](portada-light.png)

- Adjunto: [guia-mobile.png](guia-mobile.png)

## Próximo paso

Integrar esta rama en main, empujar y verificar publicación real: Actions/Pages y bytes HTTP frente a docs/. Después registrar evidencia del despliegue y cerrar con commit del ID: done.
