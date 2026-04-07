# GobernanzaIA

Baseline canonico de gobernanza multi-IA para repositorios de software.

`GobernanzaIA` no es una app de negocio. Es la fuente de verdad que define
como se trabaja, como se distribuye la gobernanza a otros repos y como se
opera con varias IAs sin depender de memoria de chat, prompts sueltos ni
runtime local mezclado con producto.

![Version](https://img.shields.io/badge/version-baseline--dev-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10+-blue?logo=python)
![Motores](https://img.shields.io/badge/ias-codex%20%7C%20claude%20%7C%20gemini%20%7C%20roo-informational)

## Tabla de contenidos

- [Que es](#que-es)
- [Dependencias externas y atribucion](#dependencias-externas-y-atribucion)
- [Estado actual del canon](#estado-actual-del-canon)
- [Piezas principales](#piezas-principales)
- [Stack canonico de contexto](#stack-canonico-de-contexto)
- [Workflow canonico](#workflow-canonico)
- [Review semanal MIT](#review-semanal-mit)
- [Orquestador canonico](#orquestador-canonico)
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
- pipeline `F1-F10`
- orquestacion ejecutiva
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
  upstream oficial

Lo que vive en este repo es:

- la politica de uso
- el routing canonico
- los instaladores
- el wiring MCP comun
- la integracion operativa en repos consumidores

No vive aqui la autoria del motor semantico ni de la memoria estructural.

Nota operativa sobre `SymDex`:

- el baseline canónico usa backend semántico `local` por defecto
- `voyage` es opcional
- que la tool `semantic_search` exista no basta; la búsqueda semántica solo se
  considera disponible cuando backend e indexado quedan validados de verdad

---

## Estado actual del canon

Esta rama ya refleja un salto importante respecto al baseline anterior.

El estado real ahora incluye:

- gobernanza normativa consolidada
- orquestador como segunda pata canonica
- `phase_ticket` y `resume_packet` para rehidratacion
- `F6` supervisada por commit o tramo cuando aplica
- `F8` live con evidencia runtime real
- perfil local de capacidades por repo
- stack de contexto y routing canonico
- presupuesto de contexto/tokens
- baseline exportable + overlay local minima
- soporte canonico para `codebase-memory-mcp`
- review semanal MIT con baseline inicial, delta semanal, findings register,
  candidatas de remediacion y handoff supervisado

En otras palabras: este repo ya no documenta solo un workflow de iniciativas.
Documenta tambien la supervision ejecutiva, la memoria estructural y el control
recurrente de salud del repo.

---

## Piezas principales

| Pieza | Responsabilidad |
| --- | --- |
| `AGENTS.md` | contrato maestro y reglas duras |
| `dev/workflow.md` | SOP operativo canonico |
| `dev/guarantees/` | gates y criterios de paso |
| `dev/policies/` | restricciones transversales y contratos operativos |
| `dev/templates/initiative/` | artefactos de `M3/M4` |
| `dev/templates/orchestrator/` | runtime rehidratable |
| `dev/templates/governance/` | perfiles, weekly review y remediacion |
| `doc/governance_prompts/` | prompts de fase y prompts recurrentes |
| `scripts/dev/` | validadores, ping-pong y orquestador |
| `scripts/migration/` | bootstrap y sync de consumidores |
| `scripts/ops/` | instaladores MCP y soporte operativo |

---

## Stack canonico de contexto

La gobernanza ya trabaja con cinco capas explicitamente separadas:

1. `gobernanza normativa`
2. `gobernanza ejecutiva del orquestador`
3. `codigo vivo local`
4. `memoria estructural persistente`
5. `evidencia runtime real`

Routing oficial:

- gobernanza -> `governance_search`
- estado operativo -> runtime del orquestador
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

### Pipeline `F1-F10`

| Fase | Salida principal |
| --- | --- |
| `F1` | `ask.md` |
| `F2` | validacion humana del ask |
| `F3` | `ask_audit.md` |
| `F4` | `plan.md` |
| `F5` | `plan_audit.md` |
| `F6` | `execution.md` |
| `F7` | `post_audit.md` |
| `F8` | `real_validation.md` |
| `F9` | `closeout.md` |
| `F10` | `lessons_learned.md` |

Reglas fuertes:

- no se planifica sin `ASK CONGELADO`
- no se implementa sin `PLAN CONGELADO`
- las auditorias formales son solo `PASS` o `FAIL`
- `F8` es obligatoria cuando hay comportamiento observable
- no se cierra con wiring parcial, legacy vivo o paths paralelos

---

## Review semanal MIT

La review semanal ya es una capacidad canonica separada de `M4`.

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
- `dev/records/reviews/architecture_findings_register.md`

### Flujo de remediacion supervisada

1. la review detecta hallazgos
2. el findings register los mantiene vivos
3. se agrupan en `candidate_initiatives.md`
4. el orquestador puede generar `handoff.md`
5. el usuario aprueba la remediacion
6. se abre una iniciativa `M3` o `M4` formal

No se abre `M4` automaticamente sin aprobacion humana explicita.

---

## Orquestador canonico

El orquestador ya no es un helper lateral. Es la capa ejecutiva del sistema.

Responsabilidades:

- abrir y retomar sesiones
- calcular fase efectiva
- verificar precondiciones mecanicas
- emitir `phase_ticket` y `resume_packet`
- persistir receipts y estado operativo
- preparar `F8`
- lanzar checkpoints laterales de `F6`
- ejecutar la review semanal canonica
- preparar remediaciones supervisadas

No puede:

- redactar artefactos sustantivos de motor
- sustituir la auditoria formal
- inventar validacion observable
- abrir `M4` sin aprobacion humana

Ruta:

- [governance_orchestrator.py](/c:/Users/Jorge%20Ferrer/Documents/GobernanzaIA/scripts/dev/governance_orchestrator.py)

Guia humana:

- [orchestrator_human_quickstart.md](/c:/Users/Jorge%20Ferrer/Documents/GobernanzaIA/dev/policies/orchestrator_human_quickstart.md)

---

## Distribucion a repos consumidores

El modelo actual ya es:

- `GobernanzaIA` = fuente de verdad viva
- repo consumidor = baseline distribuido + overlay local minima

### Entra en el baseline exportable

- `AGENTS.md`
- `dev/workflow.md`
- `dev/guarantees/`
- `dev/policies/`
- `dev/prompts/`
- `dev/templates/initiative/`
- `dev/templates/orchestrator/`
- `dev/templates/governance/`
- scripts canónicos
- documentacion reusable
- scaffolding vacio de `dev/records/`

### No entra en el baseline exportable

- iniciativas reales
- historicos reales de `dev/records/`
- `.orchestrator_local/`
- caches, logs, sesiones y outputs generados
- configuraciones locales efimeras

### Overlay local minima

- `dev/repo_governance_profile.md`

Esa overlay se preserva en actualizaciones del baseline.

---

## Estructura del repo

```text
GobernanzaIA/
├─ AGENTS.md
├─ README.md
├─ dev/
│  ├─ workflow.md
│  ├─ guarantees/
│  ├─ policies/
│  ├─ prompts/
│  ├─ templates/
│  │  ├─ initiative/
│  │  ├─ orchestrator/
│  │  └─ governance/
│  └─ records/
│     ├─ bitacora/
│     ├─ initiatives/
│     └─ reviews/
├─ doc/
│  ├─ architecture/
│  └─ governance_prompts/
├─ scripts/
│  ├─ dev/
│  ├─ migration/
│  └─ ops/
└─ tests/
```

---

## Quickstart

### Abrir una iniciativa `M4`

```text
GOBERNANZA NUEVA | repo=<repo> | initiative_id=<id> | fuente=handoff | motor_activo=<motor>
```

### Aprobar `F2`

```text
F2 aprobado, motor_auditor=codex
```

### Rehidratar `F8`

```text
rehidrata F8 de la iniciativa <initiative_id>
```

### Lanzar review semanal inicial

```text
REVIEW SEMANAL INICIAL | repo=<repo> | fecha=<yyyy-mm-dd> | motor_activo=claude
```

### Lanzar review semanal recurrente

```text
REVIEW SEMANAL | repo=<repo> | fecha=<yyyy-mm-dd> | motor_activo=claude
```

### Aprobar remediacion semanal

```text
APRUEBA REMEDIACION | repo=<repo> | fecha=<yyyy-mm-dd> | candidate_id=<id> | initiative_id=<initiative_id> | modo=M4 | motor_activo=<motor>
```

---

## Instalacion en un repo nuevo

Bootstrap minimo:

```bash
python scripts/migration/bootstrap_governance.py --target <ruta_repo_destino> --with-ia codex --with-ia claude --preferred-working-ia codex --preferred-auditor-ia claude
```

Dry run:

```bash
python scripts/migration/bootstrap_governance.py --target <ruta_repo_destino> --dry-run
```

Sync de consumidores conocidos:

```bash
python scripts/migration/sync_governance_consumers.py --dry-run
```

---

## Packs opcionales

| Pack | Para que sirve |
| --- | --- |
| `governance_search` | retrieval canonico de gobernanza |
| `symdex` | lectura fina de codigo vivo local y búsqueda semántica local cuando esté validada |
| `codebase_memory` | memoria estructural persistente (`codebase-memory-mcp`) |
| `roo` | superficie reusable de Roo |
| `claude` | `CLAUDE.md` reusable |

Ejemplo con memoria estructural:

```bash
python scripts/migration/bootstrap_governance.py --target <ruta_repo_destino> --with-ia codex --with-ia claude --preferred-working-ia codex --preferred-auditor-ia claude --include-pack governance_search --include-pack symdex --include-pack codebase_memory
```

---

## Validacion del baseline

Comandos utiles:

```bash
python -m unittest tests.test_governance_orchestrator tests.test_bootstrap_governance tests.test_sync_governance_consumers
python -m py_compile scripts/dev/governance_orchestrator.py scripts/migration/bootstrap_governance.py scripts/migration/sync_governance_consumers.py
```

El baseline se considera sano cuando:

- el bootstrap exporta solo lo exportable
- el orquestador mantiene continuidad sin chat
- la weekly review funciona como control separado
- la remediacion semanal entra por `M3/M4` supervisada
- no hay records reales dentro del repo canonico
