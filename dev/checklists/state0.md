# Checklist Estado 0

Objetivo: asegurar que el repo cumple organización base según reglas vigentes.

## Gobernanza

- [ ] `AGENTS.md` actualizado
- [ ] `dev/workflow.md` actualizado
- [ ] Políticas en `dev/policies/` completas y coherentes
- [ ] `dev/policies/git_workflow_rules.md` presente y referenciado

## Estructura

- [ ] Layout raíz cumple `dev/policies/repo_layout_rules.md` para el tipo de
      repo actual (baseline reusable o repo consumidor)
- [ ] `scripts/` en estructura `dev/ops/migration`
- [ ] Si existen runbooks, los activos y heredados respetan las rutas
      canónicas

## Calidad de nombres

- [ ] `scripts/dev/check_naming_compliance.py` sin errores

## Estado base limpio

- [ ] Sin `__pycache__/`
- [ ] Sin artefactos de prueba fuera de rutas esperadas

## Validación final

- [ ] `scripts/dev/check_state0.py` sin errores
