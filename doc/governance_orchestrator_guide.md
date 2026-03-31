# Guia De Uso — `governance_orchestrator.py`

## Objetivo

`scripts/dev/governance_orchestrator.py` separa la orquestacion del trabajo de
los motores:

- `Codex@repo_fuente` actua como orquestador
- `Claude@repo_objetivo` actua como `motor_activo`
- `Codex@repo_objetivo` actua como `motor_auditor`

El objetivo es evitar un `advance` monolitico y trabajar una fase por comando,
con reanudacion limpia, write-set cerrado y runtime local privado.

## Runtime local

El orquestador crea en primer uso:

- `.orchestrator_local/`

Esa carpeta:

- no forma parte del baseline exportable
- no se commitea
- guarda sesiones, prompts renderizados, outputs crudos y receipts

El bootstrap de runtime es automatico. No hace falta crear la carpeta a mano.

## Flujo esperado

1. `init-session`
2. `status` o `resume`
3. `run-f1`
4. `approve-f2`
5. `run-f3`
6. `freeze-ask`
7. `run-f4`
8. `run-f5`
9. `freeze-plan`
10. `run-f6`
11. `run-f7`
12. `prepare-f8`

Si hay `FAIL`:

- `run-f1-remediation`
- `run-f4-remediation`
- `run-f6-remediation`

## Prompts usados

Base:

- `01_f1_ask.md`
- `03_f3_auditoria_ask.md`
- `04_f4_plan.md`
- `05_f5_auditoria_plan.md`
- `06_f6_ejecucion.md`
- `07_f7_post_auditoria.md`

Remediacion:

- `13_f1_remediacion_ask.md`
- `15_f4_remediacion_plan.md`
- `17_f6_remediacion_ejecucion.md`

Fuera del pipeline orquestado:

- `99 prompt plan a codex.md`
- `99` es un prompt humano pre-`00`, previo a `handoff.md`
- el orquestador no usa `99` en `F1-F8`

## Comandos principales

```bash
python scripts/dev/governance_orchestrator.py --target-repo <repo> --initiative-id <id> init-session
python scripts/dev/governance_orchestrator.py --target-repo <repo> --initiative-id <id> status
python scripts/dev/governance_orchestrator.py --target-repo <repo> --initiative-id <id> resume
python scripts/dev/governance_orchestrator.py --target-repo <repo> --initiative-id <id> show-prompt
python scripts/dev/governance_orchestrator.py --target-repo <repo> --initiative-id <id> last-run
python scripts/dev/governance_orchestrator.py --target-repo <repo> --initiative-id <id> next-step
python scripts/dev/governance_orchestrator.py --target-repo <repo> --initiative-id <id> run-current-step
```

Comandos de fase:

```bash
python scripts/dev/governance_orchestrator.py --target-repo <repo> --initiative-id <id> run-f1
python scripts/dev/governance_orchestrator.py --target-repo <repo> --initiative-id <id> approve-f2 --motor-auditor codex
python scripts/dev/governance_orchestrator.py --target-repo <repo> --initiative-id <id> run-f3
python scripts/dev/governance_orchestrator.py --target-repo <repo> --initiative-id <id> freeze-ask
python scripts/dev/governance_orchestrator.py --target-repo <repo> --initiative-id <id> run-f4
python scripts/dev/governance_orchestrator.py --target-repo <repo> --initiative-id <id> run-f5
python scripts/dev/governance_orchestrator.py --target-repo <repo> --initiative-id <id> freeze-plan
python scripts/dev/governance_orchestrator.py --target-repo <repo> --initiative-id <id> run-f6
python scripts/dev/governance_orchestrator.py --target-repo <repo> --initiative-id <id> run-f7
python scripts/dev/governance_orchestrator.py --target-repo <repo> --initiative-id <id> prepare-f8
```

Reapertura explícita de auditoría:

```bash
python scripts/dev/governance_orchestrator.py --target-repo <repo> --initiative-id <id> reopen-phase --phase F5
python scripts/dev/governance_orchestrator.py --target-repo <repo> --initiative-id <id> run-current-step
```

## Reglas operativas

- Un comando, una fase.
- Un motor, un artefacto principal.
- El orquestador verifica artefacto esperado y metadata.
- Los outputs crudos viven en `.orchestrator_local/`.
- Los artefactos formales viven en el repo objetivo.
- `F2` y `F8` siguen siendo checkpoints humanos.
- `resume` reconstruye el estado desde los artefactos reales de la iniciativa.
- `show-prompt` da visibilidad al prompt base o renderizado de la fase efectiva.
- `last-run` muestra el último intento ejecutado y su resultado local.
- cada intento deja `run_state.json` local con `running`, `completed` o `failed`
- si una fase falla antes del artefacto formal, el orquestador guarda receipt fallido con error y snapshot
- `reopen-phase` permite repetir `F3`, `F5` o `F7` sobre una iniciativa ya empezada.
