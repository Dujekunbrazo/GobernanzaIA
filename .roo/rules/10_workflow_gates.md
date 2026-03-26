# Workflow Gates (Obligatorio)

Este repo se trabaja siguiendo el SOP:
- Lee `dev/workflow.md` antes de proponer planes o ejecutar cambios.

## Fases (resumen)
F1 ASK PROPUESTO -> Gate: `dev/guarantees/ask_gate.md`
F2 VALIDACIÓN USUARIO + designación de `motor_auditor`
F3 AUDITORÍA + ASK CONGELADO
F4 PLAN PROPUESTO -> Gate: `dev/guarantees/plan_gate.md`
F5 AUDITORÍA + PLAN CONGELADO
F6 IMPLEMENTACIÓN -> Gate: `dev/guarantees/implementation_gate.md`
F7 POST-AUDITORÍA / DEBUG
F8 DOCS + CIERRE -> Gate: `dev/guarantees/docs_gate.md`
F9 LECCIONES FINALES

## Regla de alcance
Si algo no está en el Ask congelado, parar y reabrir F1.
Si algo no está en el plan congelado, parar y reabrir F4.

## Regla de auditoría

- `PASS` solo si no hay hallazgos abiertos.
- Solo los problemas materiales son `hallazgos`.
- El ruido editorial o cosmético debe ir a `observaciones`.

## Regla de trazabilidad conversacional
Cada turno de trabajo debe registrarse en la bitácora diaria por IA
(`dev/records/bitacora/`) según `dev/policies/bitacora_rules.md`.
