# Token Budget Policy (Hard)

Proposito:
- controlar coste de contexto y coste operativo sin degradar calidad ni
  trazabilidad

## 1) Regla general

- optimizar coste total por iniciativa o tarea, no solo coste por llamada
- se permite gastar mas en un paso si evita relectura masiva, reauditorias o
  remediaciones largas posteriores
- mas contexto no equivale a mejor gobernanza

## 2) Reglas de contexto

- preferir retrieval dirigido a volcado amplio de archivos
- preferir resumenes y extractos relevantes a logs o trazas completas
- si una evidencia puede citarse con extracto corto y referencia clara, no se
  debe pegar el bloque completo

## 3) Reglas por capa

### Gobernanza normativa

- cargar solo los documentos minimos necesarios segun fase y tipo de consulta
- usar `governance_search` antes de lecturas amplias

### Codigo vivo local

- usar `symdex_code` para localizar y luego leer solo el bloque necesario
- evitar abrir muchos archivos completos cuando basta un simbolo concreto

### Memoria estructural persistente

- usar `codebase-memory-mcp` como retrieval estructural
- pedir paths, nodos, blast radius o call paths concretos; no dumps grandes
  del grafo

### Evidencia runtime real

- resumir trazas y logs al minimo relevante
- registrar solo la evidencia necesaria para sostener expected vs observed

## 4) Reglas por fase

- `F1-F5`:
  - priorizar contexto corto y evidencia estructurada
- `F6`:
  - activar supervision por commit solo cuando el riesgo lo justifique
- `F7`:
  - contrastar plan, diffs y validaciones reales sin reinyectar historia
    completa
- `F8`:
  - guiar caso por caso y evitar volcados completos de trace o terminal

## 5) Escalado de esfuerzo

- `medium` por defecto
- `high` cuando haya integracion multiarchivo o remediacion acotada
- `max` solo cuando el riesgo o la complejidad lo justifiquen

## 6) Prohibiciones

- prohibido pegar logs completos por comodidad
- prohibido releer toda la iniciativa por rutina si el retrieval dirigido basta
- prohibido usar checkpoints de `F6` por rutina si el tramo es trivial
- prohibido usar la capa estructural como excusa para cargar contexto masivo

## 7) Criterio de aceptabilidad

La politica de coste es aceptable cuando:

- reduce relectura y contexto bruto
- mantiene trazabilidad suficiente
- no rompe validacion real
- favorece precision frente a volumen
