# Changelog

Todas las versiones siguen [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v0.2.0 — 2026-05-25

Refresh sustantivo del kit para alinearlo con el canon vivo (rev 9.7.7),
convertirlo en kit limpio sin contaminacion de project-domain y soportar
instalaciones con cualquier par de IAs.

### Sustantivo

- **Canon motor-agnostico**. El sistema describe los roles como `motor activo`
  y `motor auditor` en abstracto. Los nombres concretos viven en
  `dev/governance_baseline.json` (`installation_profile.preferred_working_ia`
  y `preferred_auditor_ia`) durante la instalacion. Antes el canon hablaba
  literalmente de `Claude` y `Codex`.
- **AGENTS.md 22 → 32 reglas duras no negociables**.
  - R1: motor activo carga AGENTS.md y respeta routing MCP antes de degradar
    a lectura bruta.
  - R24: hallazgos F2/F4 deben ser cerrables (Tipo/Artefacto/Seccion/Cambio
    minimo/Criterio cierre/Rerun scope/Reapertura).
  - R25: `SAFE_AUDITOR_AUTOFIX` lo conduce el motor auditor sin devolver al
    motor activo para reconciliaciones mecanicas.
  - R26: legacy, dualidad canonica o evidencia material pendiente escala a
    hallazgo bloqueante.
  - R27: una iniciativa no queda cerrada sin working tree limpio, commits
    finales y estado Git trazado.
  - R28: README incremental obligatorio si la iniciativa cambia superficie.
  - R29: integracion a troncal y borrado de ramas declarados en `closeout.md`.
  - R30: SymDex y codebase-memory representan baseline integrado de
    `main/master`.
  - R31: tras F5 APTA_PARA_F6, autoriza cierre completo estandar.
  - R32: `python scripts/dev/memory_precheck.py <termino>` obligatorio antes
    de proponer canon nuevo.
- **`dev/skills/` como capa operativa canonica nueva** (9 Skills migradas):
  `f1_plan_creation`, `f2_plan_audit`, `f2_auditor_autofix`,
  `f3_implementation_execute`, `f4_post_audit`, `f5_real_validation`,
  `f6_closeout`, `f7_lessons`, `skill_lifecycle_audit` + `SKILL_CONTRACT.md`
  y `REGISTRY.md`. AGENTS.md §1 carveout operativo: la Skill canonica de
  una capability migrada tiene precedencia sobre los adapters.
- **8 policies nuevas**: `skill_policy`, `canonical_clock_injection_policy`,
  `audit_finding_contract_policy`, `m4_artifact_shape_contract_policy`,
  `m4_first_pass_quality_policy`, `m4_governed_blocking_unblocking_policy`,
  `scoped_validation_policy`, ampliacion `tooling_quality_policy`.
- **Cadena de prompts F1-F7 nueva** en `doc/governance_prompts/`:
  `01_f1_plan`, `02_f2_auditoria_plan`, `03_f2_remediacion_plan`,
  `04_f3_implementacion`, `05_f4_post_auditoria`, `06_f6_f7_cierre_y_lecciones`.
  Sustituye el esquema F4-F10 viejo borrado.
- **Cadena `96.x` M0 investigada multi-agente** anadida en
  `doc/governance_prompts/`: `96.1, 96.2, 96.3, 96.3.1, 96.5, 96.6, 96_m0`.
- **§7.1 Cierre F6/F7** nuevo en AGENTS.md: motor auditor conduce el
  cierre completo estandar (commit/push/merge/borrado ramas/refresh MCP).
- **Scripts nuevos**:
  - `scripts/dev/memory_precheck.py` (operacionaliza Regla 32; rutas canon
    parametrizables via `--canon-source` o variable `MEMORY_PRECHECK_SOURCES`).
  - `scripts/dev/check_clock_canon.py`.
  - `scripts/dev/check_structural_tooling_ready.py`.
  - `scripts/dev/refresh_symdex_index.ps1`.
  - `scripts/dev/refresh_codebase_memory_index.ps1`.
  - `scripts/dev/refresh_governance_retrieval_index.ps1`.
  - `scripts/ops/context_mcp/refresh_governance_index.mjs`.

### Bootstrap multi-IA

- `IA_CHOICES` (tupla cerrada de 2 IAs) → `IA_CATALOG` con 10 IAs conocidas:
  `claude`, `codex`, `gpt`, `gemini`, `kimi`, `grok`, `deepseek`, `qwen`,
  `mistral`, `llama`. Anadir una IA nueva = una linea mas en el dict.
- `argparse` ya no restringe con `choices=`: cualquier string es valido para
  `--with-ia`. Las IAs fuera del catalogo emiten WARN pero no bloquean.
- `IA_PACKS` ampliado: cada IA del catalogo tiene su pack registrado (vacios
  son placeholder extensible).
- Flag nuevo `--generate-adapter-template-for <ia>` (repetible) que crea
  `dev/ai/adapters/<ia>.md` desde `dev/templates/governance/adapter_template.md`
  si el adapter no existe.
- Plantilla `dev/templates/governance/adapter_template.md` nueva con
  contrato de adapter (identidad, modelos, continuidad durable, routing MCP,
  convenciones, excepciones, fallbacks).
- `dev/skills/` se incluye en `core.globs` con glob **recursivo** para
  recoger SKILL.md anidados por capability.
- `REMOVE_ON_FORCE_IF_EXISTS` incluye los 9 prompts F4-F10 legacy borrados.
- `dev/logs/decisions.md` excluido del bootstrap (log historico interno del
  repo origen, no debe viajar al consumidor).

### Limpieza project-domain

- **LEG-DISCOVERY removido completamente**. Era investigacion legislativa
  especifica del repo origen `MCP_Boletinesoficiales` (boletines oficiales
  espanoles), no gobernanza generica:
  - AGENTS.md `Carril LEG-DISCOVERY` (§6) eliminado.
  - 2 Skills `m4_legislation_profile` y `leg_discovery_omnibus_instrumento_paraguas` NO importadas.
  - 1 policy `omnibus_instrumento_paraguas_provisional_policy.md` NO importada.
  - 2 prompts `99_m4_leg_arranque.md` y `99.1_leg_discovery_arranque.md` NO importados.
- **Rutas project-specific generalizadas**: `doc/project/` → `doc/` o
  `<carpeta_doc>/`; `MCP_Boletinesoficiales` → `<nombre_repo>`.
- **Refs Kiminion eliminadas** de `dev/policies/git_workflow_rules.md`:
  `2026-02-26_kiminion-recovery` → `2026-mm-dd_descripcion-corta`.
- **Ejemplos `B2.6→B2.7→B2.7.1`** generalizados a "regla anti-deuda
  historica" en SKILL.md de fase 2 y 6.
- **Modelos hardcoded** (`Claude Opus`, `Claude Sonnet`) generalizados a
  "modelo de mayor capacidad" / "modelo de menor coste" en governance_guide,
  workflow, weekly_briefing_policy, etc.

### Compatibilidad

- Los `agent_id` historicos del kit (`m4.f1.claude.plan_architect`,
  `m4.f2.codex.plan_auditor`, etc.) mantienen el sufijo nominal
  `claude`/`codex` como legacy nominal. El sufijo NO impone el motor
  concreto que ejecuta el rol; lo aclara `dev/governance_guide.md` §7.3.
- `sync_governance_consumers.py.KNOWN_CONSUMERS` vaciado. Las entradas
  hardcoded `kiminion` y `mcp_boletinesoficiales` del repo origen no son
  parte del kit limpio. El consumidor anade sus propios destinos.
- Esquema F1-F7 reemplaza el viejo F4-F10. Los 9 prompts viejos se borran
  con `--force` automatica del bootstrap.

### Tests

- Test roto `phase_ticket.md` / `resume_packet.md` corregido (esos archivos
  nunca existieron en orchestrator/).
- Tests nuevos: glob recursivo de skills, scripts nuevos en core, argparse
  acepta IA fuera de catalogo, IA_CATALOG mantiene minimo 10 IAs documentadas.
- 21 tests del repo en verde.

### Validacion real F5

Bootstrap ejecutado en repo desechable con perfil `codex` + `kimi`,
`preferred_working_ia=kimi`, `preferred_auditor_ia=codex`. Verificado:

- 135 archivos copiados, manifest correcto.
- 0 menciones literales `Claude`/`Codex` en cuerpo normativo del kit instalado.
- 0 menciones LEG/M4-LEG/legislation_profile.
- 11 archivos en `dev/skills/` instalados via glob recursivo.
- Adapter `dev/ai/adapters/kimi.md` generado desde plantilla.
- `dev/logs/decisions.md` NO instalado (excluido).
- `check_naming_compliance.py`: 0 errors, 0 warnings.

### Migracion desde v0.1.x

Si tu repo consumidor instalo `v0.1.x`:

```bash
# Sincroniza el baseline; --force purga prompts viejos F4-F10 obsoletos.
python scripts/migration/bootstrap_governance.py \
  --target <ruta_repo_destino> \
  --with-ia <tu_motor_activo> --with-ia <tu_motor_auditor> \
  --preferred-working-ia <tu_motor_activo> \
  --preferred-auditor-ia <tu_motor_auditor> \
  --force
```

El adapter local en `dev/ai/adapters/<motor>.md` se preserva si existe.
El manifest `dev/governance_baseline.json` se reescribe con la nueva forma.
