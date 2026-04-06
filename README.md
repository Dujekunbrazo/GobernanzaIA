# GobernanzaIA

Baseline reusable de gobernanza multi-IA para proyectos de software.

`GobernanzaIA` concentra la parte que debe ser
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
- [Como usar la gobernanza](#como-usar-la-gobernanza)
- [Pipeline operativo F1-F10](#pipeline-operativo-f1-f10)
- [Artefactos y reglas de paso](#artefactos-y-reglas-de-paso)
- [Como trabajar una iniciativa paso a paso](#como-trabajar-una-iniciativa-paso-a-paso)
- [Estructura del repo](#estructura-del-repo)
- [Instalacion en otro proyecto](#instalacion-en-otro-proyecto)
- [Packs opcionales](#packs-opcionales)
- [Flujo de sincronizacion con repos consumidores](#flujo-de-sincronizacion-con-repos-consumidores)
- [Requisitos](#requisitos)
- [FAQ](#faq)

---

## Sobre el proyecto

`GobernanzaIA` no es una aplicacion de negocio. Es el baseline operativo que
define como trabajan varias IAs sobre un repositorio compartido con proceso
cerrado, trazable y auditable.

El baseline actual prioriza:

- `AGENTS.md` como contrato universal y fuente primaria de verdad.
- Workflow canonico `M0-M4` y pipeline formal `F1-F10`.
- Gates de proceso reutilizables para `ask`, `plan`, `implementacion` y
  `docs`.
- Adaptadores por motor para `Codex`, `Claude`, `Gemini` y `Roo`.
- Bootstrap oficial para instalar la gobernanza en repos nuevos.
- Orquestador canónico por fases para separar ejecución, auditoría y runtime local.
- Perfil multi-IA de instalacion con minimo dos IAs y preferencia separada de
  trabajo y auditoria.
- Packs operativos opcionales para `governance_search` y `SymDex`.
- Capa estructural prevista para `codebase-memory-mcp` con fallback explícito.
- Frontera explicita entre gobernanza reusable y runtime del producto
  consumidor.

Orden canónico de evolución:

1. gobernanza normativa
2. gobernanza ejecutiva del orquestador
3. integración de memoria estructural
4. expansión segura a repos consumidores

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

En reimportaciones sobre repos ya vivos, el bootstrap preserva overlays locales
que no deben pisarse ciegamente, como:

- `.gitignore`
- `dev/logs/decisions.md`
- `dev/repo_governance_profile.md`

El baseline no instala:

- runtime de una aplicacion consumidora
- historicos reales de `dev/records/`
- `state/`, `logs/`, `sessions/`, `content/`, `reports/`
- settings locales como `.claude/settings.local.json`
- wiring MCP legado o paths hardcodeados de otro repo

El baseline puede crear runtime local en primer uso de ciertas utilidades
canónicas. Ese runtime no forma parte del baseline exportable y se materializa
solo en la máquina donde se ejecuta la herramienta.

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

## Como usar la gobernanza

La gobernanza no es un conjunto de notas sueltas. Es un protocolo de trabajo.

La idea base es esta:

1. el usuario plantea una necesidad
2. la IA declara o confirma el modo correcto
3. se sigue el pipeline correspondiente
4. se generan artefactos trazables en `dev/records/initiatives/`
5. no se avanza de fase sin cumplir la precondicion anterior

### Modos de trabajo

- `M0 CONVERSACION`
  - ideacion, aclaraciones, alcance, dudas
  - no se crea codigo ni artefactos de iniciativa
- `M1 ANALISIS`
  - diagnostico tecnico sin cambios de codigo
  - puede leer repo y producir analisis
- `M2 DEBUG`
  - reproduccion y aislamiento de fallos sin implementar fix
- `M3 IMPLEMENTACION_MENOR`
  - cambio acotado, trazable y de bajo riesgo
  - no abre auditoria formal completa
- `M4 INICIATIVA_COMPLETA`
  - cambio mediano/grande con pipeline formal completo

### Regla de activacion

- si el usuario no declara modo, se empieza en `M0`
- para entrar en `M3` o `M4`, hace falta aprobacion explicita del usuario
- el usuario designa siempre `motor_activo`
- en `M4`, el usuario designa `motor_auditor` en `F2`

### Que debe decir el usuario

Ejemplos utiles:

- `TRANSICION: M0 -> M3 | fix acotado de gobernanza | impacto bajo | aprobar`
- `motor_activo: Codex`
- `TRANSICION: M0 -> M4 | nueva iniciativa transversal | trazabilidad completa | aprobar`
- `F2 VALIDADO | motor_auditor: Claude`

### Regla de oro

- una conversacion no sustituye a la gobernanza
- si el trabajo requiere trazabilidad, se abre iniciativa
- si cambia materialmente el alcance, se reabre la fase anterior

---

## Pipeline operativo F1-F10

`M4` trabaja con diez fases formales.

| Fase | Proposito | Salida principal |
| ---- | --------- | ---------------- |
| `F1` | Ask propuesto | `ask.md` |
| `F2` | Validacion usuario + designacion de auditor | `ask.md` en `VALIDADO` o `BLOQUEADO` |
| `F3` | Auditoria y congelado de ask | `ask_audit.md` + `ask.md` en `CONGELADO` |
| `F4` | Plan propuesto | `plan.md` |
| `F5` | Auditoria y congelado de plan | `plan_audit.md` + `plan.md` en `CONGELADO` |
| `F6` | Implementacion | `execution.md` |
| `F7` | Post-auditoria / debug | `post_audit.md` |
| `F8` | Validacion real guiada | `real_validation.md` |
| `F9` | Docs + cierre | `closeout.md` |
| `F10` | Lecciones finales | `lessons_learned.md` |

### Reglas de avance

- no se planifica sin `ASK CONGELADO`
- no se implementa sin `PLAN CONGELADO`
- solo `F3`, `F5` y `F7` tienen auditoria formal `PASS` o `FAIL`
- `F8` no es auditoria formal, pero puede bloquear el cierre
- si `F8` detecta fallos materiales, se reabre `F6`
- si se reabre `F6`, luego deben repetirse `F7` y `F8`

### Cuando aplica F8

`F8` aplica cuando la iniciativa toca:

- comportamiento observable del producto
- UX verificable en ejecucion
- integraciones reales que deban probarse en la app viva

Si no aplica:

- debe quedar trazado como `NO_APLICA`
- no se inventa prueba real solo para cumplir una formalidad

### Que cambia F8 frente al workflow anterior

Antes era facil:

- terminar `F7`
- lanzar pruebas manuales
- arreglar el primer fallo en caliente
- perder vision global

Ahora `F8` obliga a:

- preparar un barrido completo
- ejecutar todas las pruebas reales
- registrar resultados estructurados
- consolidar hallazgos antes de volver a tocar codigo

---

## Artefactos y reglas de paso

Ruta canonica:

`dev/records/initiatives/<initiative_id>/`

### Artefactos obligatorios en M4

- `ask.md`
- `ask_audit.md`
- `plan.md`
- `plan_audit.md`
- `execution.md`
- `post_audit.md`
- `closeout.md`
- `lessons_learned.md`

### Artefactos opcionales mas utiles

- `handoff.md`
  - apertura durable pre-`F1`
- `capability_closure.md`
  - cuando la iniciativa toca una capability transversal
- `exception_record.md`
  - si hace falta una excepcion formal
- `real_validation.md`
  - fase `F8` cuando aplica

### Reglas practicas por artefacto

- `handoff.md`
  - conserva analisis previo
  - no sustituye `ask.md` ni `plan.md`
- `ask.md`
  - fija problema, evidencia, alcance, supuestos y trade-offs
- `plan.md`
  - define implementacion por commits y validaciones
- `execution.md`
  - registra lo que realmente se implemento y valido
- `post_audit.md`
  - decide si la implementacion es apta tecnicamente
- `real_validation.md`
  - registra pruebas reales, expected, observed, evidencia y decision
- `closeout.md`
  - declara cierre estructural y estado final
- `lessons_learned.md`
  - captura mejoras de proceso y decisiones sobre gobernanza

### Gates minimos

- Ask gate antes de planificar
- Plan gate antes de implementar
- Implementation gate antes de cerrar
- Docs gate antes de declarar cierre formal

---

## Como trabajar una iniciativa paso a paso

Esta es la forma recomendada de uso diario.

### 1. Conversacion y apertura

Empieza en `M0`.

Haz:

- delimitar el problema
- decidir si es `M3` o `M4`
- designar `motor_activo`

Si va a ser `M4`, puedes abrir `handoff.md` para no perder analisis previo.

### 2. F1-F3: Ask

Objetivo:

- dejar claro que se va a hacer
- que queda fuera
- que evidencia existe
- que preguntas siguen abiertas

No se debe:

- implementar
- meter ya el plan final de commits
- vender como cerrado algo que aun es ambiguo

### 3. F4-F5: Plan

Objetivo:

- convertir el ask congelado en plan ejecutable
- definir validaciones
- fijar wiring, owner y mecanismo comun si hay capability transversal

No se debe:

- ampliar alcance sin reabrir ask
- esconder refactors dentro de commits funcionales

### 4. F6-F7: Implementacion y post-auditoria

Objetivo:

- ejecutar el plan congelado
- validar tecnica y estructuralmente
- confirmar ausencia de wiring parcial o branching oportunista

`F7` decide si la implementacion es tecnicamente apta o no.

### 5. F8: Validacion real guiada

Objetivo:

- probar el comportamiento real en la app
- registrar todos los resultados antes de arreglar nada

Flujo:

1. el `motor_activo` prepara el script de pruebas
2. el usuario ejecuta frases o acciones reales
3. la IA registra:
   - caso
   - esperado
   - observado
   - resultado
   - evidencia
4. al final decide:
   - `APTA_PARA_F9`
   - `REABRIR_F6`
   - `NO_APLICA`

Regla critica:

- no se toca codigo tras el primer fallo material salvo bloqueo critico que
  impida seguir el barrido

### 6. F9-F10: Cierre y lecciones

`F9` cierra documentalmente:

- `closeout.md`
- checks en verde
- estado estructural declarado

`F10` captura:

- lecciones tecnicas
- lecciones de proceso
- propuestas de cambio a gobernanza
- decision por propuesta

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
  --preferred-working-ia codex \
  --preferred-auditor-ia claude \
  --include-pack governance_search \
  --include-pack symdex
```

### Que deja instalado

- baseline en el repo destino
- `dev/governance_baseline.json` con metadata de instalacion
- perfil multi-IA instalado
- `governance_search` opcional con wiring MCP en `.mcp.json`
- `SymDex` opcional desde su GitHub oficial
- `symdex_code` opcional con wiring MCP en `.mcp.json`
- `doc/governance_prompts/` como playbook reusable de prompts de proceso

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
fusiona `governance_retrieval` en `.mcp.json`. Si tambien se instala `roo`,
añade el mismo servidor a `.roo/mcp.json`.

### `symdex`

Instala `SymDex` desde `https://github.com/husnainpk/SymDex`, genera
`.symdexignore`, prepara `.symdex/` como directorio de estado, ejecuta un
warm-up best effort y fusiona `symdex_code` en `.mcp.json` mediante el wrapper
repo-local `scripts/ops/run_symdex_mcp.py`. Si tambien se instala `roo`,
añade el mismo servidor a `.roo/mcp.json`.

---

## Flujo de sincronizacion con repos consumidores

Modelo recomendado:

1. Mejorar lo reusable en `GobernanzaIA`.
2. Publicar una version o snapshot limpio del baseline.
3. Reimportarlo en un repo consumidor con
   `bootstrap_governance.py`.
4. Mantener en cada proyecto solo overlays locales y `dev/records/` propios.

Regla operativa:

- si una mejora es reusable, nace o se promociona a `GobernanzaIA`
- si es especifica del runtime de un producto, se queda en ese repo consumidor

Ejemplo de reimportacion en un repo consumidor:

```bash
python scripts/migration/bootstrap_governance.py \
  --target <ruta_repo_consumidor> \
  --force \
  --with-ia codex \
  --with-ia claude \
  --preferred-working-ia codex \
  --preferred-auditor-ia claude \
  --include-pack governance_search \
  --include-pack symdex
```

Si trabajas con los consumidores conocidos del workspace actual, puedes usar el
wrapper de sync:

```bash
python scripts/migration/sync_governance_consumers.py --force
```

Por defecto intenta sincronizar:

- `Kiminion`
- `MCP_Boletinesoficiales`

resolviendolos como repos hermanos de `GobernanzaIA`.

---

## Requisitos

Base:

- Python 3.10+

Segun packs:

- `governance_search`: `node` + `npm`
- `symdex`: `python` en PATH para el wrapper MCP y preferiblemente `uv`/`uvx`
  o `symdex` ya instalado para warm-up/fallback

---

## FAQ

### Esto sustituye el runtime de una aplicacion de producto

No. `GobernanzaIA` solo contiene gobernanza reusable y tooling asociado.

### Puedo instalar solo una IA

No. El instalador exige minimo dos IAs para que el repo nazca preparado para
trabajo y auditoria separados.

### Las preferencias de instalacion fijan motores por defecto

No. Solo dejan constancia de tooling instalado. La designacion real de
`motor_activo` y `motor_auditor` sigue siendo explicita por usuario.

### Puedo usarlo fuera del repo donde nacio originalmente

Si. Esa es precisamente la finalidad del baseline.

### Donde debo hacer cambios de gobernanza

Si el cambio es reusable, debe nacer en `GobernanzaIA`.

Luego se sincroniza o reinstala en los repos consumidores.

Si el cambio es especifico del runtime de un producto, se queda en ese repo
consumidor.

### Un cambio en GobernanzaIA llega automaticamente al repo consumidor

No.

`GobernanzaIA` es la fuente canónica, pero cada repo consumidor necesita:

1. instalar o reimportar el baseline
2. revisar el diff
3. validar sus gates locales

### Como debe comportarse el usuario durante F8

No dando feedback caotico y arreglando sobre la marcha.

La operativa correcta es:

- ejecutar el barrido completo
- registrar cada resultado
- consolidar hallazgos
- solo entonces decidir reapertura a `F6`
