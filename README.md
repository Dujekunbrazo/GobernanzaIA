# GobernanzaIA

Baseline reusable de gobernanza multi-IA para proyectos de software.

`GobernanzaIA` extrae del ecosistema de `Kiminion` la parte que debe ser
canonica, repetible e instalable en cualquier repo nuevo, sin arrastrar
runtime de producto, historicos de iniciativas ni configuraciones locales
acopladas a una herramienta concreta.

![Version](https://img.shields.io/badge/version-baseline--dev-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10+-blue?logo=python)
![Motores](https://img.shields.io/badge/ias-codex%20%7C%20claude%20%7C%20gemini%20%7C%20roo-informational)

## Tabla de contenidos

- [Sobre el proyecto](#sobre-el-proyecto)
- [Que instala](#que-instala)
- [Arquitectura de gobernanza](#arquitectura-de-gobernanza)
- [Estructura del repo](#estructura-del-repo)
- [Instalacion en otro proyecto](#instalacion-en-otro-proyecto)
- [Packs opcionales](#packs-opcionales)
- [Flujo de sincronizacion con Kiminion](#flujo-de-sincronizacion-con-kiminion)
- [Requisitos](#requisitos)
- [FAQ](#faq)

---

## Sobre el proyecto

`GobernanzaIA` no es una aplicacion de negocio. Es el baseline operativo que
define como trabajan varias IAs sobre un repositorio compartido con proceso
cerrado, trazable y auditable.

El baseline actual prioriza:

- `AGENTS.md` como contrato universal y fuente primaria de verdad.
- Workflow canonico `M0-M4` y pipeline formal `F1-F9`.
- Gates de proceso reutilizables para `ask`, `plan`, `implementacion` y
  `docs`.
- Adaptadores por motor para `Codex`, `Claude`, `Gemini` y `Roo`.
- Bootstrap oficial para instalar la gobernanza en repos nuevos.
- Perfil multi-IA de instalacion con minimo dos IAs y preferencia separada de
  trabajo y auditoria.
- Packs operativos opcionales para `governance_search` y `SymDex`.
- Frontera explicita entre gobernanza reusable y runtime del producto
  consumidor.

---

## Que instala

El baseline instala:

- `AGENTS.md`
- `dev/workflow.md`
- `dev/guarantees/`
- `dev/policies/`
- `dev/prompts/`
- `dev/ai/adapters/`
- `dev/templates/initiative/`
- scaffolding vacio de `dev/records/`
- scripts de validacion y bitacora
- bootstrap oficial de instalacion

El baseline no instala:

- runtime de `Kiminion`
- historicos reales de `dev/records/`
- `state/`, `logs/`, `sessions/`, `content/`, `reports/`
- settings locales como `.claude/settings.local.json`
- wiring MCP legado o paths hardcodeados de otro repo

---

## Arquitectura de gobernanza

La arquitectura se apoya en cuatro piezas:

1. Contrato normativo:
   `AGENTS.md` define precedencia, modos, pipeline, bloqueos y reglas duras.
2. Workflow operativo:
   `dev/workflow.md` convierte ese contrato en fases ejecutables.
3. Gates y policies:
   `dev/guarantees/` y `dev/policies/` fijan criterios de aceptacion y
   restricciones transversales.
4. Adaptadores por motor:
   `dev/ai/adapters/` traduce el contrato canonico a superficies concretas sin
   convertirlas en fuente normativa primaria.

Principios estructurales:

- No existe motor por defecto.
- El usuario designa `motor_activo`.
- En `M4`, el usuario designa `motor_auditor`.
- Las superficies nativas de producto son adaptadores, no gobernanza canonica.
- Las capabilities transversales deben resolverse mediante abstraccion
  comun, owner explicito y wiring unico.

---

## Estructura del repo

```text
GobernanzaIA/
|-- AGENTS.md
|-- CLAUDE.md
|-- README.md
|-- dev/
|   |-- workflow.md
|   |-- ai/
|   |   |-- README.md
|   |   `-- adapters/
|   |-- guarantees/
|   |-- policies/
|   |-- prompts/
|   |-- templates/
|   |   `-- initiative/
|   `-- records/
|       |-- README.md
|       |-- bitacora/
|       `-- initiatives/
|-- doc/
|   `-- architecture/
`-- scripts/
    |-- dev/
    |-- ops/
    `-- migration/
```

Rutas importantes:

- `scripts/migration/bootstrap_governance.py`: instalador canonico del baseline
- `scripts/ops/install_governance_mcp.py`: instalador local de
  `governance_search`
- `scripts/ops/install_symdex.py`: instalador local de `SymDex`
- `scripts/dev/check_naming_compliance.py`: validador de nomenclatura
- `scripts/dev/check_state0.py`: validador de estado base

---

## Instalacion en otro proyecto

### Uso interactivo

Si ejecutas el bootstrap sin flags de IA, el script pregunta con que IAs vas a
trabajar, exige minimo dos y te pide una preferencia separada para trabajo y
auditoria.

```bash
python scripts/migration/bootstrap_governance.py --target <ruta_repo_destino>
```

### Uso no interactivo minimo

```bash
python scripts/migration/bootstrap_governance.py \
  --target <ruta_repo_destino> \
  --with-ia codex \
  --with-ia claude \
  --preferred-working-ia codex \
  --preferred-auditor-ia claude
```

### Con governance_search y SymDex

```bash
python scripts/migration/bootstrap_governance.py \
  --target <ruta_repo_destino> \
  --with-ia codex \
  --with-ia claude \
  --with-ia roo \
  --preferred-working-ia codex \
  --preferred-auditor-ia claude \
  --include-pack governance_search \
  --include-pack symdex
```

### Que deja instalado

- baseline en el repo destino
- `dev/governance_baseline.json` con metadata de instalacion
- perfil multi-IA instalado
- `governance_search` opcional con wiring MCP para `Roo`
- `SymDex` opcional desde su GitHub oficial

Nota importante:

Las preferencias guardadas en `dev/governance_baseline.json` son solo metadata
de instalacion. No asignan `motor_activo` ni `motor_auditor` por defecto en
runtime.

---

## Packs opcionales

### `core`

Obligatorio. Instala la gobernanza canonica reusable.

### `claude`

Instala `CLAUDE.md` como superficie reusable de compatibilidad.

### `codex`

Pack explicito de perfil multi-IA. No necesita superficie raiz adicional
porque la capa normativa de `Codex` ya viaja en `dev/ai/adapters/codex.md`.

### `gemini`

Pack explicito de perfil multi-IA. No necesita superficie raiz adicional
porque la capa normativa de `Gemini` ya viaja en `dev/ai/adapters/gemini.md`.

### `roo`

Instala reglas Markdown reusables de `Roo`, pero no copia `.roo/mcp.json`
local del repo fuente.

### `governance_search`

Instala el MCP local de retrieval de gobernanza y, si tambien se instala
`roo`, fusiona `governance_retrieval` en `.roo/mcp.json`.

### `symdex`

Instala `SymDex` desde `https://github.com/husnainpk/SymDex`, genera
`.symdexignore` repo-agnostico y, si tambien se instala `roo`, fusiona
`symdex` en `.roo/mcp.json` usando `uvx --from <source> symdex serve`.

---

## Flujo de sincronizacion con Kiminion

Modelo recomendado:

1. Mejorar lo reusable en `GobernanzaIA`.
2. Publicar una version o snapshot limpio del baseline.
3. Reimportarlo en `Kiminion` o en otro repo consumidor con
   `bootstrap_governance.py`.
4. Mantener en cada proyecto solo overlays locales y `dev/records/` propios.

Regla operativa:

- si una mejora es reusable, nace o se promociona a `GobernanzaIA`
- si es especifica del runtime de `Kiminion`, se queda en `Kiminion`

Ejemplo de reimportacion en `Kiminion`:

```bash
python scripts/migration/bootstrap_governance.py \
  --target <ruta_kiminion> \
  --force \
  --with-ia codex \
  --with-ia claude \
  --with-ia roo \
  --preferred-working-ia codex \
  --preferred-auditor-ia claude \
  --include-pack governance_search \
  --include-pack symdex
```

---

## Requisitos

Base:

- Python 3.10+

Segun packs:

- `governance_search`: `node` + `npm`
- `roo + symdex`: `uv`/`uvx`
- `symdex` sin `uv`: puede instalar runtime por `pip`, pero el wiring MCP de
  `Roo` sigue requiriendo `uvx`

---

## FAQ

### Esto sustituye el runtime de Kiminion

No. `GobernanzaIA` solo contiene gobernanza reusable y tooling asociado.

### Puedo instalar solo una IA

No. El instalador exige minimo dos IAs para que el repo nazca preparado para
trabajo y auditoria separados.

### Las preferencias de instalacion fijan motores por defecto

No. Solo dejan constancia de tooling instalado. La designacion real de
`motor_activo` y `motor_auditor` sigue siendo explicita por usuario.

### Puedo usarlo fuera de Kiminion

Si. Esa es precisamente la finalidad del baseline.
