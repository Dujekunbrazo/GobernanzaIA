# GobernanzaIA

Baseline canónico de gobernanza **multi-IA** para repositorios de software.
Define cómo se trabaja un repo con dos IAs colaborando (motor activo + motor
auditor), cómo se distribuye la gobernanza a otros repos y qué reglas aplican
a cualquier repo consumidor.

El canon es **agnóstico de motor**: los nombres concretos de las IAs (Claude,
Codex, Kimi, Gemini, etc.) se eligen durante la instalación, no están
hardcoded en la normativa.

![Version](https://img.shields.io/badge/version-v0.2.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10+-blue?logo=python)
![Motores](https://img.shields.io/badge/IAs-multi--IA%20%7C%2010%2B%20cat%C3%A1logo-informational)
![Tests](https://img.shields.io/badge/tests-21%20OK-brightgreen)

## Tabla de contenidos

- [¿Qué es?](#qué-es)
- [Novedades v0.2.0](#novedades-v020)
- [Quickstart — Instalar en un repo nuevo](#quickstart--instalar-en-un-repo-nuevo)
- [Estructura del repo](#estructura-del-repo)
- [Workflow canónico](#workflow-canónico)
  - [Modos M0-M4](#modos-m0-m4)
  - [Carril iniciativa F1-F7](#carril-iniciativa-f1-f7)
  - [Carril weekly review W1-W4](#carril-weekly-review-w1-w4)
- [Capa de Skills (`dev/skills/`)](#capa-de-skills-devskills)
- [Regla 32 — memory_precheck](#regla-32--memory_precheck)
- [Stack canónico de contexto](#stack-canónico-de-contexto)
- [Soporte multi-IA](#soporte-multi-ia)
  - [Catálogo de IAs](#catálogo-de-ias)
  - [Adapters por motor](#adapters-por-motor)
  - [Añadir una IA nueva al catálogo](#añadir-una-ia-nueva-al-catálogo)
- [Packs opcionales](#packs-opcionales)
- [Distribución a repos consumidores](#distribución-a-repos-consumidores)
- [Dependencias externas y atribución](#dependencias-externas-y-atribución)
- [Validación del baseline](#validación-del-baseline)
- [Tests](#tests)
- [Changelog](#changelog)
- [Licencia](#licencia)

---

## ¿Qué es?

`GobernanzaIA` concentra la parte que debe ser:

- canónica
- repetible
- auditable
- distribuible
- separada del runtime del producto

Su objetivo es que cualquier repo consumidor pueda heredar:

- reglas duras (32 reglas en `AGENTS.md`)
- workflow de modos `M0-M4`
- carril de iniciativa `F1-F7`
- carril de weekly review `W1-W4`
- 9 Skills operativas migradas en `dev/skills/`
- templates, prompts y guarantees
- baseline exportable + overlay local mínima
- tooling MCP canónicamente integrado

sin arrastrar:

- iniciativas reales del repo origen
- históricos de producto
- caches, logs o runtime efímero
- configuraciones locales acopladas a una máquina concreta

---

## Novedades v0.2.0

Refresh sustantivo del kit publicado el 2026-05-25. Detalles completos en
[`CHANGELOG.md`](./CHANGELOG.md).

- **Canon motor-agnóstico**: el sistema describe los roles como `motor activo`
  y `motor auditor` en abstracto; los nombres concretos viven en
  `dev/governance_baseline.json` durante la instalación.
- **AGENTS.md: 22 → 32 reglas** duras no negociables.
- **Capa nueva `dev/skills/`** con 9 Skills migradas (F1-F7 + autofix +
  skill_lifecycle_audit), `SKILL_CONTRACT.md` y `REGISTRY.md`.
- **Regla 32** operacionalizada vía `scripts/dev/memory_precheck.py`.
- **IA libre en bootstrap**: catálogo de 10 IAs conocidas (Claude, Codex,
  GPT, Gemini, Kimi, Grok, DeepSeek, Qwen, Mistral, Llama); cualquier otra
  se acepta con WARN.
- **Plantilla `adapter_template.md`** para crear adapters de IAs nuevas.
- **Cadena de prompts F1-F7** + cadena `96.x` de M0 investigada multi-agente.
- **8 policies nuevas** + 3 scripts nuevos (`memory_precheck`,
  `check_clock_canon`, `check_structural_tooling_ready`) + 3 refresh `.ps1`.

---

## Quickstart — Instalar en un repo nuevo

Clona este repo y ejecuta el bootstrap apuntando al repo destino.

### Instalación canónica (Claude + Codex)

```bash
git clone https://github.com/Dujekunbrazo/GobernanzaIA.git
cd GobernanzaIA
python scripts/migration/bootstrap_governance.py \
  --target /ruta/a/tu/repo \
  --with-ia codex --with-ia claude \
  --preferred-working-ia claude \
  --preferred-auditor-ia codex
```

### Instalación con IAs no canónicas (ej. Codex + Kimi)

```bash
python scripts/migration/bootstrap_governance.py \
  --target /ruta/a/tu/repo \
  --with-ia codex --with-ia kimi \
  --preferred-working-ia kimi \
  --preferred-auditor-ia codex \
  --generate-adapter-template-for kimi
```

El flag `--generate-adapter-template-for <ia>` (repetible) genera
`dev/ai/adapters/<ia>.md` desde `dev/templates/governance/adapter_template.md`
para que el consumidor lo rellene.

### Dry-run (sin escribir archivos)

```bash
python scripts/migration/bootstrap_governance.py \
  --target /ruta/a/tu/repo \
  --with-ia codex --with-ia claude \
  --preferred-working-ia claude --preferred-auditor-ia codex \
  --dry-run
```

### Listar packs disponibles

```bash
python scripts/migration/bootstrap_governance.py --list-packs
```

---

## Estructura del repo

```text
GobernanzaIA/
├─ AGENTS.md                # contrato maestro (32 reglas duras)
├─ CHANGELOG.md             # historial de versiones
├─ CLAUDE.md                # bootstrap para Claude (re-exporta AGENTS.md)
├─ README.md                # este archivo
├─ dev/
│  ├─ workflow.md           # workflow operativo compacto
│  ├─ governance_guide.md   # guía operativa completa
│  ├─ repo_governance_profile.md  # perfil local del repo (overlay)
│  ├─ ai/
│  │  ├─ README.md
│  │  └─ adapters/          # adapters por motor concreto (claude, codex, ...)
│  ├─ checklists/           # state0.md y otros
│  ├─ guarantees/           # gates F2/F4/M3/docs
│  ├─ logs/                 # log de decisiones interno
│  ├─ policies/             # 35+ policies operativas
│  ├─ prompts/              # atajos manuales a Skills (plan_create, plan_audit, ...)
│  ├─ records/              # scaffolding (initiatives/, reviews/, bitacora/)
│  ├─ runbooks/             # runbooks y registry de estado
│  ├─ skills/               # 9 Skills canónicas migradas + REGISTRY + CONTRACT
│  └─ templates/
│     ├─ governance/        # weekly, backlogs, repo_profile, adapter_template
│     ├─ initiative/        # plan.md, plan_audit, execution, post_audit, ...
│     └─ orchestrator/      # execution_checkpoint.md
├─ doc/
│  ├─ architecture/         # ai_engineering_dossier, context_retrieval
│  ├─ governance_prompts/   # cadena F1-F7 + 96.x M0 investigada + weekly
│  └─ governance_ping_pong_guide.md
├─ scripts/
│  ├─ dev/                  # validadores: check_*, memory_precheck, refresh_*
│  ├─ migration/            # bootstrap_governance + sync_governance_consumers
│  └─ ops/                  # instaladores MCP, bitácora, context_mcp/
└─ tests/                   # 21 tests cubriendo bootstrap, sync, MCP installs
```

---

## Workflow canónico

### Modos M0-M4

| Modo | Propósito |
|------|-----------|
| `M0 CONVERSACION` | ideación, lectura de código, aterrizaje técnico sin ejecución |
| `M1 ANALISIS` | diagnóstico técnico sin cambios de código |
| `M2 DEBUG` | reproducción y aislamiento de fallos sin implementar fix |
| `M3 IMPLEMENTACION_MENOR` | cambio acotado y trazable |
| `M4 INICIATIVA_COMPLETA` | cambio mediano/grande con trazabilidad formal |

Reglas clave:

- si el usuario no declara modo, se empieza en `M0`
- para entrar en `M3` o `M4` hace falta aprobación explícita
- los motores concretos se declaran al instalar (`installation_profile`)
- en `M4`, el motor auditor conduce `F2`, `F4` y `F5`-`F7`

### Carril iniciativa F1-F7

| Fase | Salida principal | Conduce |
|------|------------------|---------|
| `F1` | `plan.md` propuesto | motor activo |
| `F2` | `plan_audit.md` + plan congelado | motor auditor |
| `F3` | `execution.md` | motor activo |
| `F4` | `post_audit.md` | motor auditor |
| `F5` | `real_validation.md` (si aplica) | motor auditor |
| `F6` | `closeout.md` | motor auditor |
| `F7` | `lessons_learned.md` | motor auditor |

Reglas duras:

- el primer artefacto formal es `plan.md` (no hay fases ASK ni input formal)
- no se implementa sin `PLAN CONGELADO`
- las auditorías formales son solo `PASS` o `FAIL`
- `F5` es obligatoria cuando hay comportamiento observable del producto
- no se cierra con wiring parcial, legacy vivo o paths paralelos

### Carril weekly review W1-W4

| Fase | Propósito |
|------|-----------|
| `W1` | briefing factual |
| `W2` | review estratégica (MIT + Krug) |
| `W3` | actualización de findings y backlog |
| `W4` | promoción opcional a iniciativa |

Reglas duras:

- el weekly **no** genera `plan.md`
- el weekly descubre y prioriza; la iniciativa formal nace después en `M0`
- el primer weekly de un repo nuevo se ejecuta como `BASELINE_INICIAL_MIT`

Artefactos semanales en `dev/records/reviews/weekly/<yyyy-mm-dd>/`:
`weekly_briefing.md`, `weekly_review.md`, `weekly_review_delta.md`,
`weekly_review_audit.md`, `candidate_initiatives.md`.

---

## Capa de Skills (`dev/skills/`)

Las **Skills** son la capa operativa canónica del kit. Tienen precedencia
sobre los adapters por motor (`AGENTS.md` §1 carveout operativo): si una
capability está migrada a una Skill, esa Skill es el owner operativo y un
adapter no puede sustituirla.

### Skills canónicas migradas

| Skill | Capability | Fase |
|-------|------------|------|
| [`f1_plan_creation`](./dev/skills/f1_plan_creation/SKILL.md) | crear/remediar `plan.md` | F1 |
| [`f2_plan_audit`](./dev/skills/f2_plan_audit/SKILL.md) | auditar `plan.md` | F2 |
| [`f2_auditor_autofix`](./dev/skills/f2_auditor_autofix/SKILL.md) | autofix mecánico tras `F2 FAIL` | F2 |
| [`f3_implementation_execute`](./dev/skills/f3_implementation_execute/SKILL.md) | ejecutar `plan.md` congelado | F3 |
| [`f4_post_audit`](./dev/skills/f4_post_audit/SKILL.md) | auditar implementación | F4 |
| [`f5_real_validation`](./dev/skills/f5_real_validation/SKILL.md) | validar evidencia real guiada | F5 |
| [`f6_closeout`](./dev/skills/f6_closeout/SKILL.md) | cierre documental, README y Git | F6 |
| [`f7_lessons`](./dev/skills/f7_lessons/SKILL.md) | lecciones finales y backlogs | F7 |
| [`skill_lifecycle_audit`](./dev/skills/skill_lifecycle_audit/SKILL.md) | auditar contrato/lifecycle de Skills | meta |

Más:
- [`dev/skills/SKILL_CONTRACT.md`](./dev/skills/SKILL_CONTRACT.md): contrato de qué tiene que cumplir una Skill.
- [`dev/skills/REGISTRY.md`](./dev/skills/REGISTRY.md): índice canónico de resolución (estados `CANONICA`, `PILOTO_ACTIVO`, `DEPRECATED`, `RETIRADA`).

`dev/prompts/*.md` y `doc/governance_prompts/*.md` son atajos manuales a
estas Skills (compatibilidad con flujos pre-Skills); las Skills son la
fuente de verdad operativa.

---

## Regla 32 — memory_precheck

`AGENTS.md` §5 R32 obliga: **antes de proponer canon nuevo** (nueva
capability, identificador, `access_pattern`, arquetipo, seed o renombrado
de algo ya canonizado), ejecutar:

```bash
python scripts/dev/memory_precheck.py <termino_candidato>
```

Debe aparecer en chat `Verdict: ALLOW` (exit 0) o `Verdict: BLOCK`
(exit 1). Si es `BLOCK`, la propuesta no avanza hasta inventariar matches
activos y decidir si lo propuesto es **reconciliación** con canon
existente (no canon nuevo) o si **se retira**.

Las fuentes de canon escaneadas son parametrizables:

```bash
# Anadir fuentes ad-hoc via CLI
python scripts/dev/memory_precheck.py mi_termino \
  --canon-source doc/mi_doc_canon.md \
  --canon-source doc/otro_doc.md

# O via variable de entorno (separadas por os.pathsep)
export MEMORY_PRECHECK_SOURCES="doc/canon1.md:doc/canon2.md"
python scripts/dev/memory_precheck.py mi_termino
```

Por defecto cubre la memoria estructural del kit:
`dev/records/reviews/{initiative_backlog,architecture_findings_register,initiative_architecture_backlog}.md`.

---

## Stack canónico de contexto

La gobernanza opera sobre **cuatro capas** explícitamente separadas:

| Capa | Resuelve | Tool canónica |
|------|----------|---------------|
| 1. Gobernanza normativa | reglas, workflow, guarantees, policies, adapters, skills | `governance_search` MCP |
| 2. Código vivo local | lectura fina de símbolos y bloques concretos | `symdex_code` MCP |
| 3. Memoria estructural | wiring global, impacto, legacy, dead code | `codebase-memory-mcp` MCP |
| 4. Evidencia runtime real | comportamiento observable, trazas, terminal | producto + `trace on` |

La memoria conversacional **no** cuenta como continuidad válida. Detalle
completo del routing en [`AGENTS.md`](./AGENTS.md) §10.

---

## Soporte multi-IA

### Catálogo de IAs

`scripts/migration/bootstrap_governance.py` mantiene un `IA_CATALOG`
extensible. Catálogo inicial v0.2.0:

| IA | Vendor | Adapter en kit |
|----|--------|----------------|
| `claude` | Anthropic | ✓ ([`dev/ai/adapters/claude.md`](./dev/ai/adapters/claude.md)) |
| `codex` | OpenAI | ✓ ([`dev/ai/adapters/codex.md`](./dev/ai/adapters/codex.md)) |
| `gpt` | OpenAI | — (generar desde plantilla) |
| `gemini` | Google | — (generar desde plantilla) |
| `kimi` | Moonshot | — (generar desde plantilla) |
| `grok` | xAI | — (generar desde plantilla) |
| `deepseek` | DeepSeek | — (generar desde plantilla) |
| `qwen` | Alibaba | — (generar desde plantilla) |
| `mistral` | Mistral | — (generar desde plantilla) |
| `llama` | Meta | — (generar desde plantilla) |

`--with-ia` acepta **cualquier string**. Las IAs fuera del catálogo emiten
un WARN pero el install continúa.

### Adapters por motor

Un adapter (`dev/ai/adapters/<motor>.md`) afina detalles concretos del
motor (modelos, continuidad durable, routing MCP soportado, convenciones,
fallbacks). **No crea workflow ni routing paralelos al canon**.

Si el motor instalado no tiene adapter, el bootstrap puede generarlo:

```bash
python scripts/migration/bootstrap_governance.py \
  --target /ruta/a/repo \
  --with-ia codex --with-ia kimi \
  --preferred-working-ia kimi --preferred-auditor-ia codex \
  --generate-adapter-template-for kimi
```

Esto copia [`dev/templates/governance/adapter_template.md`](./dev/templates/governance/adapter_template.md) →
`dev/ai/adapters/kimi.md` con placeholders para rellenar.

### Añadir una IA nueva al catálogo

En `scripts/migration/bootstrap_governance.py`, añade una línea al dict
`IA_CATALOG`:

```python
IA_CATALOG: dict[str, dict[str, str | bool]] = {
    # ... entradas existentes ...
    "mi_nueva_ia": {"vendor": "MiVendor", "has_adapter_in_kit": False},
}
```

Y opcionalmente, en `dev/ai/adapters/mi_nueva_ia.md`, crea el adapter
canónico desde la plantilla.

---

## Packs opcionales

| Pack | Para qué sirve |
|------|----------------|
| `core` | baseline canónico (siempre instalado por defecto) |
| `governance_search` | MCP local de retrieval canónico de gobernanza |
| `symdex` | lectura fina de código vivo y búsqueda semántica local |
| `codebase_memory` | memoria estructural persistente vía `codebase-memory-mcp` |
| `claude` | `CLAUDE.md` raíz reusable |
| `codex`, `gpt`, `gemini`, `kimi`, `grok`, `deepseek`, `qwen`, `mistral`, `llama` | packs vacíos extensibles por IA |

Ejemplo con los 3 MCPs:

```bash
python scripts/migration/bootstrap_governance.py \
  --target /ruta/a/repo \
  --with-ia codex --with-ia claude \
  --preferred-working-ia claude --preferred-auditor-ia codex \
  --include-pack governance_search \
  --include-pack symdex \
  --include-pack codebase_memory
```

Los packs MCP ejecutan post-copy actions que instalan los servidores
locales (npm/uv) y registran wiring en `.mcp.json` del repo destino.

---

## Distribución a repos consumidores

Modelo:

- **`GobernanzaIA`** = fuente de verdad viva
- **Repo consumidor** = baseline distribuido + overlay local mínima

### Lo que viaja al baseline exportable

- `AGENTS.md`, `dev/workflow.md`, `dev/governance_guide.md`
- `dev/guarantees/`, `dev/policies/`, `dev/skills/`, `dev/prompts/`
- `dev/templates/initiative/`, `dev/templates/governance/`
- `dev/ai/adapters/*.md`
- `scripts/dev/` (validadores + memory_precheck + refresh `.ps1`)
- `scripts/migration/` (bootstrap + sync)
- `scripts/ops/` (instaladores MCP + context_mcp/)
- `doc/architecture/`, `doc/governance_prompts/`, `doc/governance_ping_pong_guide.md`
- Scaffolding vacío de `dev/records/`

### Lo que NO viaja

- Iniciativas reales del repo origen
- `dev/records/initiatives/`, `dev/records/bitacora/`, `dev/records/reviews/` con contenido
- `dev/logs/decisions.md` (log histórico interno)
- Caches, logs, sesiones, outputs generados
- `tests/` (son tests del kit, no del consumidor)
- Configuraciones locales (`.symdex`, `node_modules/`, `__pycache__/`)

### Overlay local mínima

- `dev/repo_governance_profile.md`

El bootstrap preserva esta overlay con `PRESERVE_IF_EXISTS` en
actualizaciones del baseline. Si no existe, se genera desde la plantilla
`dev/templates/governance/repo_governance_profile.md` para que el
consumidor lo rellene.

### Sync entre múltiples consumidores

`scripts/migration/sync_governance_consumers.py` puede sincronizar el
baseline a varios repos consumidores declarados en `KNOWN_CONSUMERS` del
propio script:

```python
KNOWN_CONSUMERS: dict[str, ConsumerProfile] = {
    "mi_consumidor": ConsumerProfile(
        key="mi_consumidor",
        repo_dir="MiRepo",
        installed_ias=("codex", "claude"),
        preferred_working_ia="claude",
        preferred_auditor_ia="codex",
        include_packs=("governance_search", "symdex", "codebase_memory"),
    ),
}
```

Por defecto el dict está vacío (es overlay del propio mantenedor del kit).
El consumidor puede invocar `bootstrap_governance.py` directamente sin
pasar por sync.

---

## Dependencias externas y atribución

`GobernanzaIA` define el canon, el wiring y los instaladores. **No reclama
autoría** sobre herramientas externas integradas:

- [`SymDex`](https://github.com/husnainpk/SymDex): motor semántico de código.
- [`codebase-memory-mcp`](https://github.com/DeusData/codebase-memory-mcp/): memoria estructural persistente.

Lo que vive aquí: política de uso, routing canónico, instaladores, wiring
MCP común, integración operativa.

Nota sobre backend semántico de SymDex:

- baseline canónico usa backend `local` por defecto
- `voyage` es opcional
- la búsqueda semántica solo se considera disponible cuando backend e
  indexado están validados de verdad

---

## Validación del baseline

```bash
# Validadores estructurales del kit
python scripts/dev/check_naming_compliance.py
python scripts/dev/check_state0.py

# Compilación sintáctica de scripts críticos
python -m py_compile \
  scripts/migration/bootstrap_governance.py \
  scripts/migration/sync_governance_consumers.py \
  scripts/dev/memory_precheck.py

# Smoke de instalación con dry-run
python scripts/migration/bootstrap_governance.py \
  --target /tmp/test_dst \
  --with-ia codex --with-ia claude \
  --preferred-working-ia claude --preferred-auditor-ia codex \
  --dry-run
```

El baseline se considera sano cuando:

- el bootstrap exporta solo lo exportable
- la weekly review funciona como control separado del carril iniciativa
- la remediación semanal entra por `M3/M4` con aprobación humana explícita
- no hay records reales dentro del repo canónico (solo scaffolding)
- la instalación con cualquier par de IAs distintas produce manifest válido

---

## Tests

```bash
python -m unittest discover -s tests -v
```

21 tests en verde tras v0.2.0:

- `tests/test_bootstrap_governance.py` (8): incluye glob recursivo de
  skills, scripts nuevos en core, argparse acepta IA fuera de catálogo,
  IA_CATALOG mantiene mínimo las 10 IAs documentadas.
- `tests/test_sync_governance_consumers.py` (1): comando bootstrap
  construido correctamente.
- `tests/test_install_symdex.py` (varios): instalación de SymDex con
  backend semántico.
- `tests/test_install_codebase_memory_mcp.py` (varios).
- `tests/test_governance_ping_pong.py` (varios).

Los tests son del kit, **no viajan al consumidor**.

---

## Changelog

Detalle completo de cambios por versión: [`CHANGELOG.md`](./CHANGELOG.md).

Versión actual: **v0.2.0** (2026-05-25).

---

## Licencia

MIT. Ver [LICENSE](./LICENSE) si existe, o el header de los archivos
fuente. Las dependencias externas (SymDex, codebase-memory-mcp) mantienen
sus propias licencias en sus repos upstream.
