# Token Budget Policy (Hard)

Proposito:
- controlar coste de contexto y coste operativo sin degradar calidad ni
  trazabilidad
- fijar uso proporcional de modelos y tooling

## 1) Regla general

- optimizar coste total por iniciativa o tarea, no solo coste por llamada
- se permite gastar mas en un paso si evita relectura masiva, reauditorias o
  remediaciones largas posteriores
- mas contexto no equivale a mejor gobernanza
- el modelo caro se usa para pensar; no para leer bruto

## 2) Reglas de contexto

- preferir retrieval dirigido a volcado amplio de archivos
- preferir resumenes y extractos relevantes a logs o trazas completas
- si una evidencia puede citarse con extracto corto y referencia clara, no se
  debe pegar el bloque completo
- una vez existe `plan.md`, no debe reinyectarse entero por rutina en cada
  fase

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

## 4) Reglas por carril

### Carril iniciativa

- `M0`:
  - prioridad a codigo vivo, memoria estructural y compactacion fuerte
- `plan.md`:
  - se permite `Opus medium`
  - el input de planificacion debe llegar limpio y estructurado
- auditoria:
  - trabajar sobre `plan.md`, codigo vivo y diffs, no sobre historia completa
- implementacion:
  - `Sonnet medium`
  - evitar releer todo `plan.md`; usar cabecera, tramo activo y DoD relevante
- validacion y cierre:
  - `Sonnet low` por defecto
  - subir a `medium` si emerge fallo material o reapertura real

### Carril weekly review

- briefing factual:
  - `Sonnet`
  - foco en hechos verificables y evidencia
- review estrategica:
  - `Opus`
  - prohibido releer codigo bruto si el briefing factual es suficiente
- weekly no debe arrastrarse completo a una iniciativa; solo se promueve
  evidencia minima y candidate entry

## 5) Reglas de modelo

- `Claude Opus`, `medium`:
  - crear o redisenar materialmente `plan.md`
  - realizar la review estrategica del weekly
- `Claude Sonnet`, `medium`:
  - briefing factual del weekly
  - implementacion
- `Claude Sonnet`, `low`:
  - validacion real
  - cierre
  - lecciones
- `Codex`:
  - auditoria formal
  - aterrizaje tecnico en `M0`

## 6) Reglas de sesion

- al pasar de planificacion a implementacion, preferir sesion nueva o contexto
  limpio si la conversacion ya arrastra demasiado historial
- no usar el weekly previo como contexto largo de iniciativa; usar backlog,
  candidate entry y evidencia minima
- no usar el backlog como si fuera un plan encubierto

## 7) Prohibiciones

- prohibido pegar logs completos por comodidad
- prohibido releer toda la iniciativa por rutina si el retrieval dirigido basta
- prohibido usar checkpoints de implementacion por rutina si el tramo es
  trivial
- prohibido usar la capa estructural como excusa para cargar contexto masivo
- prohibido usar `Opus` para exploracion factual que puede hacer `Sonnet`
- prohibido que weekly, backlog y plan dupliquen la misma semantica sustantiva

## 8) Criterio de aceptabilidad

La politica de coste es aceptable cuando:

- reduce relectura y contexto bruto
- mantiene trazabilidad suficiente
- no rompe validacion real
- favorece precision frente a volumen
- asigna el modelo correcto al tipo de trabajo correcto
