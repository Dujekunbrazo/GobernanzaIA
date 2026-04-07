# Structural Analysis Execution Policy (Hard)

Propósito:
- regular cómo se ejecuta un análisis estructural serio con
  `codebase-memory-mcp`
- evitar análisis superficiales basados solo en hubs, recuentos o intuición
- obligar a declarar límites metodológicos del grafo cuando existan

## 1) Preconditions

Antes de analizar, debe verificarse:

- proyecto correcto identificado en la capa estructural
- indexado persistido y estado listo para consulta
- modo de indexación conocido (`fast`, `moderate` o `full`)

Si alguna de estas precondiciones falla:

- no se analiza
- el estado correcto es `BLOQUEADO`

## 2) Minimum protocol

Un análisis estructural serio debe dejar trazado, como mínimo:

- el proyecto o índice usado
- el modo de indexación usado
- al menos `1` traza crítica real
- al menos `1` hub o punto de acoplamiento relevante
- al menos `1` limitación metodológica observada

No es aceptable cerrar un análisis con:

- solo hubs
- solo recuentos de nodos o edges
- solo intuiciones sobre arquitectura

## 3) Expected outputs

Cuando aplique, el análisis debe responder con evidencia:

- quién llama a quién
- qué impacta cambiar un símbolo relevante
- qué hubs existen
- qué límites del grafo impiden responder mejor

Cuando haga falta semántica fina del código:

- `codebase-memory-mcp` no sustituye a `symdex_code`
- el análisis debe declarar cuándo necesita lectura exacta de código como capa
  secundaria

## 4) Known graph limits to declare

Cuando aparezcan, deben declararse explícitamente:

- routes HTTP huérfanas o desconectadas del grafo
- edges `TESTS` a nivel clase pero no de método
- `RAISES` subindexado
- ruido excesivo de nodos `Section`
- imposibilidad de reconstruir secuencia exacta de ejecución desde el grafo

## 5) Prohibitions

- prohibido presentar el grafo como si devolviera código fuente
- prohibido presentar una limitación del grafo como si fuera ausencia real de
  wiring
- prohibido cerrar un análisis estructural sin declarar sus límites
- prohibido usar `cross_service` como si fuera apto cuando el boundary
  Python -> HTTP dinámico no esté realmente conectado

## 6) Acceptability criteria

El análisis estructural se considera aceptable cuando:

- parte de un proyecto/indexado verificado
- declara el modo de indexación
- incluye una traza crítica real
- incluye un hub real
- incluye una limitación metodológica real
- no finge que el grafo resuelve preguntas que no puede responder

## 7) References

- `dev/policies/context_routing_policy.md`
- `dev/policies/structural_memory_policy.md`
- `dev/policies/context_stack_policy.md`
