# Oracle Clue 0.1.0a1

Primer corte alpha: contexto reproducible y validación de informes externos. **No incluye revisión automática con IA.**

- `oracle-clue preparar`: diferencia entre commits y contexto explícito, sin cambiar archivos del repositorio ni ejecutar pruebas/proveedores.
- `oracle-clue validar`: contratos de informe/triage, vigencia de contexto, ids y ubicaciones en el diff.
- Límites de tamaño y omisiones declaradas de binarios, enlaces y rutas conocidas de credenciales.
- Wheel con schemas incluidos, sdist y SHA256SUMS.

## Validación

Contratos positivos/negativos, repos Git temporales con defectos sembrados y CLI instalada fuera del checkout. Los resultados exactos quedan en `20261002-212339-prototipar`. La instalación se prueba en Linux. No se afirma evaluación de precisión de IA ni autenticación de personas.

## Publicación manual en PyPI

Los artefactos probados están adjuntos al release y en `dist/`. Verificar SHA256SUMS y publicar con las credenciales del mantenedor:

```bash
uv publish dist/oracle_clue-0.1.0a1-py3-none-any.whl dist/oracle_clue-0.1.0a1.tar.gz
```

Este release no implica que ya esté en PyPI. Tras subirlo, comprobar `uvx --from oracle-clue==0.1.0a1 oracle-clue --version` en un entorno limpio.
