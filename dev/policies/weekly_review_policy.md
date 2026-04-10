# Policy: Weekly Review Canon

## Objetivo

Formalizar una revision recurrente de salud arquitectonica, operativa y de
claridad del repo sin mezclarla con una iniciativa `M3` o `M4`.

## Naturaleza del control

- la review semanal es un control canonico recurrente
- no sustituye `M0-M4`
- no redefine el pipeline de iniciativa
- no autoriza cambios de codigo por si misma
- no cierra ni reabre fases de una iniciativa existente salvo que sus hallazgos
  se traduzcan despues a trabajo gobernado
- opera en dos capas:
  - capa factual con `Claude Sonnet`
  - capa estrategica con `Claude Opus`
- `Codex` puede intervenir despues para aterrizar una candidata en `M0`

## Modos de revision semanal

### `BASELINE_WEEKLY`

Primera corrida profunda del control semanal cuando el repo aun no dispone de
una revision semanal canonica valida.

Reglas:

- no compara contra una revision semanal anterior
- debe producir una fotografia base del repo
- debe crear el primer registro vivo de hallazgos arquitectonicos
- debe dejar lineas base MIT y Krug para revisiones futuras
- debe analizar el repo completo con profundidad alta y retrieval dirigido
- debe sembrar backlog e initiative candidates iniciales cuando corresponda

### `DELTA_WEEKLY`

Corrida recurrente una vez existe una `BASELINE_WEEKLY` valida.

Reglas:

- compara contra la ultima revision semanal valida
- distingue hallazgos `nuevos`, `persistentes`, `resueltos` y
  `reclasificados`
- debe registrar tendencia y delta, no redescubrir el repo completo sin
  necesidad

## Alcance minimo

La review semanal debe poder:

- reconstruir un estado sintetico del repo para esa semana
- identificar hallazgos materiales y riesgos sistemicos
- dejar evidencia trazable para comparacion futura
- preparar, en revisiones posteriores del canon, la remediacion gobernada de
  hallazgos via `M3` o `M4`
- distinguir entre problemas MIT, Krug y mixtos

## Relacion con el resto de la gobernanza

- `F8` sigue siendo la validacion real de una iniciativa concreta
- la review semanal inspecciona la salud del repo, no valida el cierre de una
  iniciativa concreta
- si la review detecta trabajo material, ese trabajo debe abrir despues un flujo
  gobernado propio
- la primera corrida semanal valida debe declararse explicitamente como
  `BASELINE_WEEKLY`
- la review semanal no genera `plan.md`
- la review semanal solo puede producir hallazgos, candidatos y backlog vivo

## Regla de evidencia

- toda afirmacion material de la review debe anclarse a evidencia del repo,
  signals operativas disponibles o retrieval canonico del stack de contexto
- si falta evidencia, el estado correcto es `BLOQUEADO` o `NO_EVIDENCIA`

## Criterio de aceptabilidad

La review semanal solo se considera canonica si:

- produce artefactos trazables
- no depende de memoria conversacional
- no crea una ruta paralela a `M4`
- no introduce implementacion sin apertura formal posterior
- diferencia de forma explicita entre baseline inicial y delta semanal
- deja explicitado el uso conjunto de MIT y Krug

