# Architect Mode Behavior

Cuando el usuario solicite cualquier cambio técnico:

1. NO implementes nada.
2. Verifica SIEMPRE que existe un `ASK CONGELADO` para la iniciativa.
3. Si no existe Ask congelado:
   - No planifiques.
   - Indica reabrir F1-F3 (Ask).
4. Genera un plan estructurado solo después de Ask congelado.
5. Sigue `dev/workflow.md`.
6. Aplica el Plan Gate (`dev/guarantees/plan_gate.md`).
7. Este modo no define un rol oficial de gobernanza; el rol válido es `motor_activo`.
8. Guarda el plan en `dev/records/initiatives/<initiative_id>/plan.md`.
9. Para gobernanza dinámica, usa `governance_search` antes de cualquier lectura
   directa.
10. Declara herramienta usada y fuente canónica usada en cada respuesta
    técnica.
11. Si faltan MCPs activos, declara limitación operativa.
12. No uses iniciativas previas como fuente principal de proceso si existe
    fuente canónica.
13. Si Roo va a intervenir como canal de auditoría en `F5`, pregunta antes si
    el usuario desea mantener o cambiar la API/modelo para esa auditoría.

La salida debe incluir:

- Objetivo
- Alcance
- No-alcance
- Impacto técnico
- Riesgos (Top 3)
- Plan por commits atómicos (numerados)
- Rollback
- Definition of Done
- Referencia al documento de Ask congelado
- Herramienta y fuente canónica usadas

Marca siempre el resultado como:

`PLAN PROPUESTO — PENDIENTE DE AUDITORIA DEL MOTOR_AUDITOR`
