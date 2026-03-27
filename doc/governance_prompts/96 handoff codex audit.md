Actúa como revisor técnico de gobernanza para mejorar un `handoff.md` antes de crear `ask.md`.

Sigue estrictamente:
- `AGENTS.md`
- `dev/workflow.md`
- `dev/prompts/m4_opening_handoff.md`
- `dev/prompts/ask_discovery.md`
- `dev/guarantees/ask_gate.md`

Contexto:
- Estamos en `M4` ya abierto.
- Existe `dev/records/initiatives/<initiative_id>/handoff.md`.
- Esta revisión NO crea una fase nueva.
- Esta revisión NO sustituye `F1`, `F2` ni `F3`.
- Tu tarea es endurecer el `handoff.md` para que `ask.md` pueda derivarse con menos ambigüedad y menos riesgo.

Objetivo:
Revisar a fondo el `handoff.md` actual, detectar carencias materiales y proponer una versión mejorada del handoff antes de redactar `ask.md`.

Reglas duras:
- No implementar código.
- No crear `ask.md`.
- No emitir auditoría formal `PASS`/`FAIL`.
- No inventar alcance que no esté sustentado por evidencia.
- No mezclar plan final de commits dentro del handoff más allá de un borrador inicial.
- Si falta contexto crítico, declarar `BLOQUEADO` con evidencia.

Criterios de revisión obligatorios:
1. ¿El handoff define claramente el problema y el objetivo?
2. ¿La evidencia técnica es concreta, verificable y suficiente?
3. ¿El alcance propuesto está claro y separado del no-alcance?
4. ¿Hay supuestos explícitos y están marcados como tales?
5. ¿Las preguntas abiertas están bien separadas entre bloqueantes y no bloqueantes?
6. ¿Las opciones y trade-offs están realmente formulados o solo insinuados?
7. ¿La recomendación está justificada por evidencia?
8. ¿El borrador de plan por commits es coherente con el alcance?
9. ¿Están claros los criterios para derivar a `ask.md`?
10. ¿Están claros los criterios para derivar después a `plan.md`?
11. ¿Hay scope creep, claims no demostrados o lenguaje ambiguo?
12. ¿Falta alguna restricción material para que `F1` salga bien?

Salida obligatoria:
Entrega exactamente estas secciones:

1. `Diagnóstico del handoff actual`
2. `Hallazgos materiales`
3. `Huecos que impedirían un buen ask`
4. `Ambigüedades o claims débiles`
5. `Información que debe preservarse sí o sí`
6. `Información que debe moverse o recortarse`
7. `Preguntas que deben quedar explícitas antes de F1`
8. `Propuesta de handoff mejorado`

Regla para los hallazgos:
- Prioriza solo problemas materiales para mandato, evidencia, alcance, trazabilidad o derivación correcta a `ask.md`.
- No llenes la revisión de observaciones cosméticas.

En `Propuesta de handoff mejorado`:
- reescribe el handoff completo
- mantén estructura compatible con `dev/prompts/m4_opening_handoff.md`
- mejora precisión, trazabilidad y separación entre alcance / no-alcance / supuestos / preguntas / trade-offs
- conserva todo lo valioso del original
- elimina ruido, duplicidad y claims no sostenidos

Si el handoff ya está fuerte:
- dilo explícitamente
- aun así devuelve una versión pulida del handoff con mejoras de claridad y derivación a `ask.md`

Archivo a revisar:
`dev/records/initiatives/<initiative_id>/handoff.md`
