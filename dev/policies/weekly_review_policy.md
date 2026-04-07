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
