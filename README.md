# GobernanzaIA

Baseline reutilizable de gobernanza multi-IA para proyectos de software.

## Contenido

- `AGENTS.md`: contrato universal multi-IA
- `dev/workflow.md`: SOP operativo
- `dev/guarantees/`: gates de proceso
- `dev/policies/`: reglas duras
- `dev/ai/adapters/`: adaptadores por motor
- `dev/templates/initiative/`: plantillas de iniciativa
- `scripts/ops/bitacora_append.py`: bitacora diaria por IA
- `scripts/dev/check_naming_compliance.py`: validacion de nomenclatura
- `scripts/dev/check_state0.py`: validacion de estado base
- `scripts/migration/bootstrap_governance.py`: bootstrap para nuevos repos

## Uso rapido

```bash
python scripts/migration/bootstrap_governance.py --target <ruta_repo_destino>
```

## Nota

Este repositorio contiene gobernanza y proceso. No contiene runtime de una app de negocio.
