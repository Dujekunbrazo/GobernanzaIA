# ASK

- Initiative ID: 2026-03-27_ping_pong_automation
- Modo: M3
- Estado: PROPUESTO
- Fecha: 2026-03-27
- motor_activo: codex
- motor_auditor:
- Rama: initiative/2026-03-27-gobernanza-sync-fuente-consumidores
- baseline_mit: MIT Concept-Sync

## Objetivo y contexto

Crear un script local en `scripts/dev/` que automatice el ping-pong de una
iniciativa `M4` entre Claude y Codex para los bucles `F1 <-> F3`, `F4 <-> F5`
y `F6 <-> F7`, dejando `F2` y `F8` como checkpoints manuales del usuario.

## Evidencia técnica

- Existen templates canonicos en `dev/templates/initiative/` para `ask.md`,
  `ask_audit.md`, `plan.md`, `plan_audit.md`, `execution.md`, `post_audit.md`,
  `closeout.md`, `lessons_learned.md`, `handoff.md` y `real_validation.md`.
- Existen prompts canonicos en `dev/prompts/` para `ask_discovery.md`,
  `plan_create.md`, `plan_audit.md`, `implementation_execute.md` y
  `post_audit.md`.
- Estan disponibles `claude` y `codex` como CLIs locales autenticados.
- `scripts/dev/initiative_preflight.py` ya valida precondiciones de iniciativas.

## Supuestos

- La automatizacion debe vivir en `scripts/dev/` como utilidad de desarrollo
  local, no en runtime de producto.
- El flujo debe respetar limites de re-auditoria y checkpoints manuales.
- El usuario activara el orquestador desde terminal o task de VS Code.
- Excepción operativa: el worktree actual esta sucio por cambios previos ajenos
  a esta iniciativa; la frase canonica "excepción operativa de worktree
  sucio" debe quedar registrada de forma explicita y trazable.

## Preguntas bloqueantes / no bloqueantes

- No bloqueante: el script puede limitarse a terminal y README sin crear task
  de VS Code en esta primera iteracion.

## Opciones y trade-offs

- Script unico con subcomandos `init`, `approve-f2`, `status` y `advance`.
  Simplifica activacion y evita estado paralelo fuera de artefactos canonicos.
- Anadir task de VS Code ahora mismo.
  Mejor UX, pero aumenta superficie no esencial para el primer corte.

## Recomendacion Ask

Implementar un unico script Python con subcomandos operativos y documentar su
uso en `scripts/dev/README.md`, manteniendo el cambio acotado y trazable.

## Criterios de aceptacion para el motor_activo

- Existe un script ejecutable en `scripts/dev/` con ayuda CLI.
- Permite inicializar una iniciativa `M4`.
- Permite marcar `F2` como checkpoint manual aprobado.
- Permite avanzar automaticamente hasta `F2`, `F8` o bloqueo por exceso de
  `FAIL`.
- Usa prompts y artefactos canonicos del repo.
- Queda documentado como activarlo y validado con pruebas basicas.
