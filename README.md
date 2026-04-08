# GobernanzaIA

Baseline canonico de gobernanza multi-IA para repositorios de software.

`GobernanzaIA` define como se trabaja, como se distribuye la gobernanza a
otros repos y que reglas aplican a cualquier repo consumidor.

Los motores directos (`Claude` y `Codex`) comparten la misma gobernanza
sustantiva a traves de `AGENTS.md`.

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
- pipeline `F1-F10`
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

- gobernanza normativa consolidada para motores directos
- `AGENTS.md` como contrato compartido entre Claude y Codex
- stack de 4 capas de contexto con routing MCP canonico
- `F8` live con evidencia runtime real
- perfil local de capacidades por repo
- presupuesto de contexto/tokens
- baseline exportable + overlay local minima
- soporte canonico para `codebase-memory-mcp`
- review semanal MIT con baseline inicial, delta semanal, findings register,
  candidatas de remediacion y handoff supervisado

El runtime ejecutivo del orquestador vive en su propio repo:
[Orquestador](https://github.com/Dujekunbrazo/Orquestador)

---

## Piezas principales

| Pieza | Responsabilidad |
| --- | --- |
| `AGENTS.md` | contrato maestro, reglas duras y routing MCP |
| `dev/workflow.md` | referencia operativa compacta para motores directos |
| `dev/guarantees/` | gates y criterios de paso |
| `dev/policies/` | restricciones transversales y contratos operativos |
| `dev/templates/initiative/` | artefactos de `M3/M4` |
| `dev/templates/governance/` | perfiles, weekly review y remediacion |
| `doc/governance_prompts/` | prompts de fase y prompts recurrentes |
| `scripts/dev/` | validadores y enforcement |
| `scripts/migration/` | bootstrap y sync de consumidores |
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
- `dev/records/reviews/architecture_findings_register.md`

### Flujo de remediacion

1. la review detecta hallazgos
2. el findings register los mantiene vivos
3. se agrupan en `candidate_initiatives.md`
4. el usuario aprueba la remediacion
5. se abre una iniciativa `M3` o `M4` formal

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
│  ├─ repo_governance_profile.md
│  ├─ ai/
│  │  └─ adapters/
│  ├─ guarantees/
│  ├─ policies/
│  ├─ prompts/
│  ├─ templates/
│  │  ├─ initiative/
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

Usa los prompts de `doc/governance_prompts/`:

1. `00_abrir_m4_y_handoff.md` — abrir M4 y crear handoff
2. `01_f1_ask.md` — generar ask
3. `02_f2_validacion_ask.md` — validar ask
4. `03_f3_auditoria_ask.md` — auditar ask
5. (y asi sucesivamente hasta `09_f9_f10_cierre_y_lecciones.md`)

### Lanzar review semanal

Usa el prompt `doc/governance_prompts/20_weekly_mit_review.md` con un
briefing tecnico generado previamente.

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
| `symdex` | lectura fina de codigo vivo local y busqueda semantica local cuando este validada |
| `codebase_memory` | memoria estructural persistente (`codebase-memory-mcp`) |
| `claude` | `CLAUDE.md` reusable |

Ejemplo con todos los packs:

```bash
python scripts/migration/bootstrap_governance.py --target <ruta_repo_destino> --with-ia codex --with-ia claude --preferred-working-ia codex --preferred-auditor-ia claude --include-pack governance_search --include-pack symdex --include-pack codebase_memory
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
