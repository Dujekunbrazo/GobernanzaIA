# SKILL REGISTRY

`dev/skills/` es una libreria interna versionada de capacidades operativas de
gobernanza. Este registry es el indice canonico de resolucion: si una
capability esta registrada como `CANONICA`, su `SKILL.md` es el owner operativo.

## Estados

- `PROPUESTA`: candidata aun no usada como canon.
- `PILOTO_ACTIVO`: usable, pero pendiente de estabilizacion.
- `CANONICA`: owner operativo de la capability.
- `DEPRECATED`: sustituida, conservada solo por compatibilidad temporal.
- `RETIRADA`: no usar.

## Registry

| Skill | Capability | Motor | Agent ID | Perfil operativo | Fase | Estado | Owner canonico | Sustituye | Compatibilidad | Retirada |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `f1_plan_creation` | crear/remediar `plan.md` | `claude_preferred` | `m4.f1.claude.plan_architect` | `claude_plan_architect` | `F1` | `CANONICA` | `dev/skills/f1_plan_creation/SKILL.md` | `dev/prompts/plan_create.md`, `doc/governance_prompts/01_f1_plan.md` | prompts legacy solo lectura | evaluar retirada cuando no haya consumidor legacy |
| `f2_plan_audit` | auditar `plan.md` | `codex_preferred` | `m4.f2.codex.plan_auditor` | `codex_plan_auditor` | `F2` | `CANONICA` | `dev/skills/f2_plan_audit/SKILL.md` | `dev/prompts/plan_audit.md`, `doc/governance_prompts/02_f2_auditoria_plan.md` | prompts legacy solo lectura | evaluar retirada cuando no haya consumidor legacy |
| `f2_auditor_autofix` | autofix mecanico de expediente tras `F2 FAIL` | `codex_preferred` | `m4.audit.codex.safe_autofix` | `codex_auditor_autofix` | `F2` | `CANONICA` | `dev/skills/f2_auditor_autofix/SKILL.md` | `dev/prompts/audit_autofix.md`, `doc/governance_prompts/03_f2_remediacion_plan.md` | prompts legacy solo lectura | evaluar retirada cuando no haya consumidor legacy |
| `f3_implementation_execute` | ejecutar `plan.md` congelado | `claude_preferred` | `m4.f3.claude.implementation_executor` | `claude_implementation_executor` | `F3` | `CANONICA` | `dev/skills/f3_implementation_execute/SKILL.md` | `dev/prompts/implementation_execute.md`, `doc/governance_prompts/04_f3_implementacion.md` | prompts legacy solo lectura | evaluar retirada cuando no haya consumidor legacy |
| `f4_post_audit` | auditar implementacion | `codex_preferred` | `m4.f4.codex.bug_structural_auditor` | `codex_bug_structural_auditor` | `F4` | `CANONICA` | `dev/skills/f4_post_audit/SKILL.md` | `dev/prompts/post_audit.md`, `doc/governance_prompts/05_f4_post_auditoria.md` | prompts legacy solo lectura | evaluar retirada cuando no haya consumidor legacy |
| `f5_real_validation` | validar evidencia real guiada | `codex_preferred` | `m4.f5.codex.real_validation_guide` | `codex_real_validation_guide` | `F5` | `CANONICA` | `dev/skills/f5_real_validation/SKILL.md` | `dev/prompts/real_validation.md` | prompt legacy solo lectura | evaluar retirada cuando no haya consumidor legacy |
| `f6_closeout` | cierre documental, README y Git | `codex_preferred` | `m4.f6.codex.closeout_auditor` | `codex_closeout_auditor` | `F6` | `CANONICA` | `dev/skills/f6_closeout/SKILL.md` | `dev/prompts/readme_update.md`, `doc/governance_prompts/06_f6_f7_cierre_y_lecciones.md` | prompts legacy solo lectura | evaluar retirada cuando no haya consumidor legacy |
| `f7_lessons` | lecciones finales y backlogs | `codex_preferred` | `m4.f7.codex.lessons_curator` | `codex_lessons_curator` | `F7` | `CANONICA` | `dev/skills/f7_lessons/SKILL.md` | `doc/governance_prompts/06_f6_f7_cierre_y_lecciones.md` | prompt legacy solo lectura | evaluar retirada cuando no haya consumidor legacy |
| `skill_lifecycle_audit` | auditar contrato/lifecycle de Skills | `codex_preferred` | n/a | `codex_skill_lifecycle_auditor` | `meta` | `CANONICA` | `dev/skills/skill_lifecycle_audit/SKILL.md` | n/a | n/a | n/a |
