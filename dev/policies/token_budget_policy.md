# Token Budget Policy (Hard)

Propósito:
- controlar coste de contexto y coste operativo sin degradar calidad ni
  trazabilidad.

## 1) Regla general

- optimizar coste total por iniciativa, no solo coste por llamada
- se permite gastar más en un paso si evita relectura masiva, reauditorías o
  remediaciones largas posteriores
- más contexto no equivale a mejor gobernanza

## 2) Reglas de contexto

- preferir `resume_packet` a releer toda la iniciativa en reentrada
- preferir retrieval dirigido a volcado amplio de archivos
- preferir resúmenes y extractos relevantes a logs o trazas completas
- si una evidencia puede citarse con extracto corto y referencia clara, no se
  debe pegar el bloque completo

## 3) Reglas por capa

### Gobernanza normativa

- cargar solo los documentos mínimos necesarios según fase y tipo de consulta
- usar `governance_search` antes de lecturas amplias

### Runtime del orquestador

- usar `phase_ticket` y `resume_packet` como bootstrap estándar
- prohibido rehidratar una fase pegando de nuevo todos los artefactos

### Código vivo local

- usar `symdex_code` para localizar y luego leer solo el bloque necesario
- evitar abrir muchos archivos completos cuando basta un símbolo concreto

### Memoria estructural persistente

- usar `codebase-memory-mcp` como retrieval estructural
- pedir paths, nodos, blast radius o call paths concretos; no dumps grandes
  del grafo

### Evidencia runtime real

- resumir trazas y logs al mínimo relevante
- registrar solo la evidencia necesaria para sostener expected vs observed

## 4) Reglas por fase

- `F1-F5`:
  - priorizar contexto corto y evidencia estructurada
- `F6`:
  - activar supervisión por commit solo cuando el riesgo lo justifique
- `F7`:
  - contrastar plan, diffs y validaciones reales sin reinyectar historia
    completa
- `F8`:
  - guiar caso por caso y evitar volcados completos de trace o terminal

## 5) Escalado de esfuerzo

- `medium` por defecto
- `high` cuando haya integración multiarchivo o remediación acotada
- `max` solo cuando el auditor lo justifique o exista excepción/reapertura
  crítica

## 6) Prohibiciones

- prohibido pegar logs completos por comodidad
- prohibido releer toda la iniciativa en cada chat nuevo
- prohibido usar checkpoints de `F6` por rutina si el tramo es trivial
- prohibido usar la capa estructural como excusa para cargar contexto masivo

## 7) Criterio de aceptabilidad

La política de coste es aceptable cuando:

- reduce relectura y contexto bruto
- mantiene trazabilidad suficiente
- no rompe validación real
- favorece precisión frente a volumen
