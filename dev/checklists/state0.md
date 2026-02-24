# Checklist Estado 0

Objetivo: asegurar que el repo cumple organización base según reglas vigentes.

## Gobernanza

- [ ] `AGENTS.md` actualizado
- [ ] `dev/workflow.md` actualizado
- [ ] Políticas en `dev/policies/` completas y coherentes
- [ ] Reglas Roo alineadas a políticas

## Estructura

- [ ] Layout raíz cumple `dev/policies/repo_layout_rules.md`
- [ ] `scripts/` en estructura `dev/ops/migration`
- [ ] Runbooks heredados en cuarentena

## Calidad de nombres

- [ ] `scripts/dev/check_naming_compliance.py` sin errores

## Estado base limpio

- [ ] Sin `__pycache__/`
- [ ] Sin artefactos de prueba fuera de rutas esperadas

## Validación final

- [ ] `scripts/dev/check_state0.py` sin errores
