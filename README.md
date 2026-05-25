# GobernanzaIA

Baseline canonico de gobernanza multi-IA para repositorios de software.

`GobernanzaIA` define como se trabaja, como se distribuye la gobernanza a
otros repos y que reglas aplican a cualquier repo consumidor.

Los motores directos del repo destino (motor activo + motor auditor)
comparten la misma gobernanza sustantiva a traves de `AGENTS.md`,
independientemente de las IAs concretas que se elijan en la instalacion.

![Version](https://img.shields.io/badge/version-baseline--dev-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10+-blue?logo=python)
![Motores](https://img.shields.io/badge/ias-codex%20%7C%20claude-informational)

## Tabla de contenidos

- [Que es](#que-es)
- [Dependencias externas y atribucion](#dependencias-externas-y-atribucion)
- [Estado actual del canon](#estado-actual-del-canon)
- [Piezas principales](#piezas-principales)
- [Stack canonico de contexto](#stack-canonico-de-contexto)
- [Workflow canonico](#workflow-canonico)
- [Review semanal MIT](#review-semanal-mit)
- [Distribucion a repos consumidores](#distribucion-a-repos-consumidores)
- [Estructura del repo](#estructura-del-repo)
- [Quickstart](#quickstart)
- [Instalacion en un repo nuevo](#instalacion-en-un-repo-nuevo)
- [Packs opcionales](#packs-opcionales)
- [Validacion del baseline](#validacion-del-baseline)

---

## Que es

`GobernanzaIA` concentra la parte que debe ser:

- canonica
- repetible
- auditable
- distribuible
- separada del runtime del producto

Su objetivo es que cualquier repo consumidor pueda heredar:

- reglas duras
- workflow `M0-M4`
- carril de iniciativa `F1-F7`
- carril de weekly review `W1-W4`
- templates y prompts
- baseline + overlay local
- tooling MCP canonicamente integrado

sin arrastrar:

- iniciativas reales
- historicos de producto
- caches o runtime efimero
- configuraciones locales acopladas a una maquina concreta

---

## Dependencias externas y atribucion

`GobernanzaIA` define el canon, el wiring y los instaladores.
No reclama autoria sobre herramientas externas integradas por el baseline.

En particular:

- `SymDex` es una dependencia externa instalada desde su proyecto upstream:
  `https://github.com/husnainpk/SymDex`
- `codebase-memory-mcp` es una dependencia externa instalada desde su proyecto
  upstream oficial `https://github.com/DeusData/codebase-memory-mcp/`

Lo que vive en este repo es:

- la politica de uso
- el routing canonico
- los instaladores
- el wiring MCP comun
- la integracion operativa en repos consumidores

No vive aqui la autoria del motor semantico ni de la memoria estructural.

Nota operativa sobre `SymDex`:

- el baseline canonico usa backend semantico `local` por defecto
- `voyage` es opcional
- que la tool `semantic_search` exista no basta; la busqueda semantica solo se
  considera disponible cuando backend e indexado quedan validados de verdad

---

## Estado actual del canon

El estado real incluye:

- gobernanza normativa canon **motor-agnostica**: el sistema habla de "motor
  activo" y "motor auditor" como roles abstractos; los nombres concretos se
  declaran durante la instalacion en `dev/governance_baseline.json`
- `AGENTS.md` como contrato compartido con **32 reglas duras no negociables**
- carril de iniciativa `F1-F7` con `plan.md` como primer artefacto formal
- carril de weekly review `W1-W4` separado de la iniciativa
- `dev/skills/` como capa operativa canonica con 9 Skills migradas
  (`f1_plan_creation`, `f2_plan_audit`, `f2_auditor_autofix`,
  `f3_implementation_execute`, `f4_post_audit`, `f5_real_validation`,
  `f6_closeout`, `f7_lessons`, `skill_lifecycle_audit`) + `SKILL_CONTRACT.md`
  y `REGISTRY.md`
- Regla 32 operacionalizada via `scripts/dev/memory_precheck.py`: antes de
  proponer canon nuevo, ejecutar precheck contra fuentes canonicas declaradas
- memoria operativa viva (`initiative_backlog.md`, `architecture_findings_register.md`, `initiative_architecture_backlog.md`)
- stack de 4 capas de contexto con routing MCP canonico
- validacion real guiada con evidencia runtime real
- perfil local de capacidades por repo
- presupuesto de contexto/tokens
- baseline exportable + overlay local minima
- soporte canonico para `codebase-memory-mcp`

## Piezas principales

| Pieza | Responsabilidad |
| --- | --- |
| `AGENTS.md` | contrato maestro, 32 reglas duras y routing MCP |
| `dev/workflow.md` | referencia operativa compacta multi-IA |
| `dev/governance_guide.md` | guia operativa completa del sistema |
| `dev/guarantees/` | gates y criterios de paso |
| `dev/policies/` | restricciones transversales y contratos operativos |
| `dev/skills/` | capacidades operativas canonicas migradas por fase |
| `dev/prompts/` | prompts de fase canonicos (atajos manuales a Skills) |
| `dev/ai/adapters/` | adapters por motor concreto (claude, codex, + extensible via plantilla) |
| `dev/templates/initiative/` | artefactos de `M3/M4` |
| `dev/templates/governance/` | perfiles, weekly review, backlogs, adapter template y remediacion |
| `scripts/dev/` | validadores, enforcement y memory_precheck (Regla 32) |
| `scripts/migration/` | bootstrap multi-IA y sync de consumidores |
| `scripts/ops/` | instaladores MCP y soporte operativo |

---

## Stack canonico de contexto

La gobernanza trabaja con cuatro capas explicitamente separadas:

1. `gobernanza normativa`
2. `codigo vivo local`
3. `memoria estructural persistente`
4. `evidencia runtime real`

Routing oficial:

- gobernanza -> `governance_search`
- codigo vivo local -> `symdex_code`
- wiring, impacto, legacy, dead code -> `codebase-memory-mcp`
- validacion observable -> chat del producto, `trace on`, terminal y evidencia real

La memoria conversacional no cuenta como continuidad valida.

---

## Workflow canonico

### Modos

- `M0 CONVERSACION`
- `M1 ANALISIS`
- `M2 DEBUG`
- `M3 IMPLEMENTACION_MENOR`
- `M4 INICIATIVA_COMPLETA`

Reglas clave:

- si el usuario no declara modo, se empieza en `M0`
- para entrar en `M3` o `M4` hace falta aprobacion explicita
- no existe motor por defecto
- el usuario designa `motor_activo`
- en `M4`, el usuario designa `motor_auditor` en `F2`

### Carril iniciativa `F1-F7`

| Fase | Salida principal |
| --- | --- |
| `F1` | `plan.md` propuesto |
| `F2` | `plan_audit.md` y congelado de plan |
| `F3` | `execution.md` |
| `F4` | `post_audit.md` |
| `F5` | `real_validation.md` cuando aplique |
| `F6` | `closeout.md` |
| `F7` | `lessons_learned.md` |

Reglas fuertes:

- el primer artefacto formal es `plan.md` (no hay fases ASK)
- no se implementa sin `PLAN CONGELADO`
- las auditorias formales son solo `PASS` o `FAIL`
- `F5` es obligatoria cuando hay comportamiento observable
- no se cierra con wiring parcial, legacy vivo o paths paralelos

### Carril weekly review `W1-W4`

| Fase | Proposito |
| --- | --- |
| `W1` | briefing factual |
| `W2` | review estrategica |
| `W3` | actualizacion de findings y backlog |
| `W4` | promocion opcional a iniciativa |

Reglas fuertes:

- el weekly no genera `plan.md`
- el weekly descubre y prioriza; la iniciativa formal nace en `M0`
- el primer weekly de un repo nuevo se ejecuta como `BASELINE`

---

## Review semanal MIT

La review semanal es una capacidad canonica separada de `M4`.

No sirve para implementar.
Sirve para detectar, clasificar y preparar trabajo gobernable.

### Modos de review

- `BASELINE_INICIAL_MIT`
  - primera corrida profunda
  - crea la linea base del repo
  - crea el registro vivo inicial de hallazgos

- `DELTA_SEMANAL_MIT`
  - compara contra la ultima review valida
  - distingue hallazgos nuevos, persistentes, resueltos y reclasificados

### Artefactos semanales

- `dev/records/reviews/weekly/<yyyy-mm-dd>/weekly_briefing.md`
- `dev/records/reviews/weekly/<yyyy-mm-dd>/weekly_review.md`
- `dev/records/reviews/weekly/<yyyy-mm-dd>/weekly_review_delta.md`
- `dev/records/reviews/weekly/<yyyy-mm-dd>/weekly_review_audit.md`
- `dev/records/reviews/weekly/<yyyy-mm-dd>/candidate_initiatives.md`

### Memoria operativa viva

- `dev/records/reviews/architecture_findings_register.md` — hallazgos persistentes
- `dev/records/reviews/initiative_backlog.md` — ideas y candidatas accionables
- `dev/records/reviews/initiative_architecture_backlog.md` — remanentes de iniciativas cerradas

### Flujo de remediacion

1. la review detecta hallazgos
2. el findings register los mantiene vivos
3. se agrupan en `candidate_initiatives.md`
4. el usuario aprueba y se abre una iniciativa `M3` o `M4` en `M0`

No se abre `M4` automaticamente sin aprobacion humana explicita.

---

## Distribucion a repos consumidores

El modelo es:

- `GobernanzaIA` = fuente de verdad viva
- repo consumidor = baseline distribuido + overlay local minima

### Entra en el baseline exportable

- `AGENTS.md`
- `dev/workflow.md`
- `dev/guarantees/`
- `dev/policies/`
- `dev/prompts/`
- `dev/templates/initiative/`
- `dev/templates/governance/`
- scripts canonicos
- documentacion reusable
- scaffolding vacio de `dev/records/`

### No entra en el baseline exportable

- iniciativas reales
- historicos reales de `dev/records/`
- caches, logs, sesiones y outputs generados
- configuraciones locales efimeras
- artefactos de una capa ejecutiva externa

### Overlay local minima

- `dev/repo_governance_profile.md`

Esa overlay se preserva en actualizaciones del baseline.

---

## Estructura del repo

```text
GobernanzaIA/
├─ AGENTS.md
├─ CLAUDE.md
├─ README.md
├─ dev/
│  ├─ workflow.md
│  ├─ governance_guide.md
│  ├─ repo_governance_profile.md
│  ├─ ai/
│  │  └─ adapters/         # adapters por motor concreto (claude, codex, ...)
│  ├─ checklists/
│  ├─ guarantees/
│  ├─ policies/
│  ├─ prompts/             # atajos manuales a las Skills canonicas
│  ├─ runbooks/
│  ├─ skills/              # capacidades operativas canonicas por fase
│  ├─ templates/
│  │  ├─ initiative/
│  │  └─ governance/       # incluye adapter_template.md
│  └─ records/
│     ├─ bitacora/
│     ├─ initiatives/
│     └─ reviews/
├─ doc/
│  └─ architecture/
├─ scripts/
│  ├─ dev/
│  ├─ migration/
│  └─ ops/
└─ tests/
```

---

## Quickstart

### Abrir una iniciativa `M4`

1. Trabajar la idea en `M0` con el motor auditor (lectura de codigo y aterrizaje tecnico)
2. Generar un `input de planificacion` transitorio
3. Usar `dev/skills/f1_plan_creation/SKILL.md` (o `dev/prompts/plan_create.md` como atajo) para generar `plan.md`
4. Auditar con `dev/skills/f2_plan_audit/SKILL.md`
5. Implementar con `dev/skills/f3_implementation_execute/SKILL.md`
6. Post-auditar con `dev/skills/f4_post_audit/SKILL.md`
7. Validar con `dev/skills/f5_real_validation/SKILL.md` si aplica
8. Cerrar con `dev/skills/f6_closeout/SKILL.md` + `dev/skills/f7_lessons/SKILL.md`

### Lanzar review semanal

1. Generar `weekly_briefing.md` con el motor activo (modelo de menor coste si aplica)
2. Ejecutar la review estrategica con el motor activo (modelo de mayor capacidad si aplica)
3. Actualizar `architecture_findings_register.md` e `initiative_backlog.md`
4. Opcional: promover candidatas a iniciativa via `M0`

---

## Instalacion en un repo nuevo

El bootstrap acepta **cualquier IA** como motor activo y auditor (no solo
Claude+Codex). El catalogo conocido por defecto incluye 10 IAs: `claude`,
`codex`, `gpt`, `gemini`, `kimi`, `grok`, `deepseek`, `qwen`, `mistral`,
`llama`. Otras IAs se aceptan con un WARN pero el install continua.

Bootstrap canonico (codex + claude):

```bash
python scripts/migration/bootstrap_governance.py --target <ruta_repo_destino> \
  --with-ia codex --with-ia claude \
  --preferred-working-ia claude --preferred-auditor-ia codex
```

Bootstrap con IAs no canonicas (ej. codex + kimi):

```bash
python scripts/migration/bootstrap_governance.py --target <ruta_repo_destino> \
  --with-ia codex --with-ia kimi \
  --preferred-working-ia kimi --preferred-auditor-ia codex \
  --generate-adapter-template-for kimi
```

El flag `--generate-adapter-template-for <ia>` (repetible) genera
`dev/ai/adapters/<ia>.md` desde la plantilla
`dev/templates/governance/adapter_template.md` para que el consumidor la
rellene. Util cuando la IA elegida no tiene adapter en el kit.

Dry run:

```bash
python scripts/migration/bootstrap_governance.py --target <ruta_repo_destino> --dry-run
```

Sync de consumidores (el dict `KNOWN_CONSUMERS` esta vacio por defecto;
el consumidor del kit anade sus propios destinos):

```bash
python scripts/migration/sync_governance_consumers.py --dry-run
```

---

## Packs opcionales

| Pack | Para que sirve |
| --- | --- |
| `governance_search` | retrieval canonico de gobernanza |
| `symdex` | lectura fina de codigo vivo local y busqueda semantica local cuando este validada |
| `codebase_memory` | memoria estructural persistente (`codebase-memory-mcp`) |
| `claude` | `CLAUDE.md` reusable en la raiz del repo destino |
| `codex`, `gpt`, `gemini`, `kimi`, `grok`, `deepseek`, `qwen`, `mistral`, `llama` | packs vacios extensibles por IA del catalogo (placeholder para futuras superficies nativas) |

Ejemplo con todos los MCPs:

```bash
python scripts/migration/bootstrap_governance.py --target <ruta_repo_destino> \
  --with-ia codex --with-ia claude \
  --preferred-working-ia claude --preferred-auditor-ia codex \
  --include-pack governance_search --include-pack symdex --include-pack codebase_memory
```

---

## Validacion del baseline

Comandos utiles:

```bash
python scripts/dev/check_naming_compliance.py
python scripts/dev/check_state0.py
python -m py_compile scripts/migration/bootstrap_governance.py scripts/migration/sync_governance_consumers.py
```

El baseline se considera sano cuando:

- el bootstrap exporta solo lo exportable
- la weekly review funciona como control separado
- la remediacion semanal entra por `M3/M4` con aprobacion humana
- no hay records reales dentro del repo canonico
