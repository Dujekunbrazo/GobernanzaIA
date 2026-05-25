# Skill Policy

## Proposito

Definir como se crea, usa y depreca la capa canonica `dev/skills/` sin
romper el canon normativo existente.

## Principios

1. Una Skill es operativa, no normativa.
2. Una capability migrada tiene un unico owner canonico.
3. La activacion debe ser progresiva: cargar primero la Skill y sus
   referencias obligatorias.
4. La Skill debe aportar valor nuevo verificable frente al prompt legacy.
5. La Skill no sustituye `AGENTS.md`, `dev/workflow.md`, `dev/guarantees/`
   ni `dev/policies/`.

## Cuando se justifica crear una Skill

Crear una Skill nueva solo cuando se cumplan a la vez estas condiciones:

- la capability es recurrente
- la capability tiene inputs y write set razonablemente estables
- la capability se beneficia de checklist de salida y fallback estructurado
- el prompt legacy o la operativa actual ya no son suficiente empaquetado

## Cuando no se justifica

No crear una Skill nueva si:

- una policy o guarantee ya cubre la necesidad por si sola
- la capability es demasiado puntual o no recurrente
- el write set es demasiado abierto o inestable
- la nueva Skill duplicaria otra existente con diferencias cosméticas

## Owner canonico

Si una capability tiene Skill:

- `dev/skills/<skill_name>/SKILL.md` es la fuente de verdad operativa
- `dev/skills/REGISTRY.md` debe declarar capability, owner, estado,
  compatibilidad, sustitucion y retirada
- `dev/prompts/` puede conservarse solo como compatibilidad de solo lectura
- `dev/ai/adapters/` solo afinan el uso por motor; no mandan sobre la Skill

## Lifecycle

Toda Skill registrada usa uno de estos estados:

- `PROPUESTA`
- `PILOTO_ACTIVO`
- `CANONICA`
- `DEPRECATED`
- `RETIRADA`

Una Skill solo puede considerarse canonica si su entrada de registry esta
completa y no existe prompt legacy compitiendo como fuente operativa primaria.

## Precedencia para capacidades migradas

La precedencia operativa de capacidades migradas es:

`dev/skills/` > `dev/prompts/` > `dev/ai/adapters/`

Reglas:

- si existe Skill para una capacidad, la Skill manda
- si prompt legacy y Skill divergen, se corrige el prompt para converger
- el prompt legacy no puede introducir instrucciones operativas que
  contradigan la Skill

## Clasificacion por motor

Toda Skill debe declarar uno de estos motores:

- `shared`
- `claude_preferred`
- `codex_preferred`

La clasificacion es obligatoria y debe reflejar el owner operativo natural de
la capability.

## Progressive disclosure

- no cargar el cuerpo de una Skill si no aplica
- al activarla, leer primero `SKILL.md`
- abrir referencias opcionales solo si hacen falta para resolver la tarea

## Deprecacion de prompts migrados

Un prompt legacy migrado puede seguir existiendo solo si:

- declara explicitamente que la Skill es la fuente de verdad operativa
- se usa como compatibilidad para tooling o atajos manuales
- no contradice la Skill correspondiente

Si deja de existir consumidor legacy, el prompt debe evaluarse para
deprecacion o eliminacion en una iniciativa posterior.

La compatibilidad legacy indefinida queda prohibida: toda entrada de registry
debe declarar criterio de retirada o justificar `n/a`.
