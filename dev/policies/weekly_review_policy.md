# Policy: Weekly Review Canon

## Objetivo

Formalizar una revision recurrente de salud arquitectonica y operativa del repo
sin mezclarla con una iniciativa `M3` o `M4`.

## Naturaleza del control

- la review semanal es un control canonico recurrente
- no sustituye `M0-M4`
- no redefine el pipeline `F1-F10`
- no autoriza cambios de codigo por si misma
- no cierra ni reabre fases de una iniciativa existente salvo que sus hallazgos
  se traduzcan despues a trabajo gobernado

## Modos de revision semanal

### `BASELINE_INICIAL_MIT`

Primera corrida profunda del control semanal cuando el repo aun no dispone de
una revision semanal canonica valida.

Reglas:

- no compara contra una revision semanal anterior
- debe producir una fotografia base del repo
- debe crear el primer registro vivo de hallazgos arquitectonicos
- debe dejar una linea base MIT para revisiones futuras

### `DELTA_SEMANAL_MIT`

Corrida recurrente una vez existe una `BASELINE_INICIAL_MIT` valida.

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

## Relacion con el resto de la gobernanza

- `F8` sigue siendo la validacion real de una iniciativa concreta
- la review semanal inspecciona la salud del repo, no valida el cierre de una
  iniciativa concreta
- si la review detecta trabajo material, ese trabajo debe abrir despues un flujo
  gobernado propio
- la primera corrida semanal valida debe declararse explicitamente como
  `BASELINE_INICIAL_MIT`

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
