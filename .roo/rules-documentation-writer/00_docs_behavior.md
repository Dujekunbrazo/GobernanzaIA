# Documentation Writer Mode Behavior

Objetivo: mantener documentación técnica clara, exacta y verificable.

## Reglas base
1) No inventes rutas, comandos, features o estados.
2) Todo lo documentado debe ser verificable en el repo o en logs aportados.
3) Respeta el SOP: `F8/F9` en `dev/workflow.md` y el Docs Gate: dev/guarantees/docs_gate.md.
4) Este modo no define un rol oficial de gobernanza distinto a `motor_activo` o `motor_auditor`.
5) Para gobernanza dinámica, usa `governance_search` antes de cualquier lectura directa.
6) Declara herramienta usada y fuente canónica usada en cada respuesta técnica.
7) Si faltan MCPs activos, declara limitación operativa.
8) No uses iniciativas previas como fuente principal de proceso si existe fuente canónica.

## README.md (política estricta)
- README.md NO se reescribe completo.
- Se actualizan secciones existentes.
- Si hace falta una sección nueva: pedir confirmación explícita antes de crearla.

## Otros documentos (si aplica)
- Si el cambio afecta a docs internas (dev/, doc/, scripts/):
  - actualiza solo lo necesario
  - mantén estilo consistente
  - evita duplicar información ya existente

## Salida esperada
- Lista breve de archivos de documentación tocados
- Qué secciones se modificaron
- Qué quedó pendiente (si algo requiere confirmación)
- Herramienta y fuente canónica usadas
