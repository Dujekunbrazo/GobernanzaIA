# Guia De Gobernanza

## 1. Que Es Este Sistema

Esta gobernanza existe para trabajar el repo con un proceso simple, repetible,
auditable y barato en tokens.

Optimiza:
- claridad
- convergencia
- trazabilidad
- coste total por tarea

No existe para generar burocracia ni para reescribir la misma comprension varias
veces.

## 2. Principios Rectores

- una iniciativa tiene un solo artefacto de planificacion: `plan.md`
- una weekly review no sustituye una iniciativa
- un hecho se escribe una vez
- retrieval dirigido antes que lectura masiva
- `Claude` produce y `Codex` audita
- MIT rige arquitectura y seguridad de evolucion
- Krug rige claridad para producto, UI, CLI y DX
- la validacion real decide la aceptabilidad final

## 3. Mapa General Del Sistema

El sistema tiene tres piezas:
- carril de iniciativa
- carril de weekly review
- memoria operativa viva

La weekly descubre y prioriza.
La iniciativa ejecuta.
La memoria viva conecta conversaciones, weeklies e iniciativas cerradas.

## 4. Carril Iniciativa

### 4.1 Cuándo usarlo

- cuando quieres ejecutar un cambio concreto
- cuando una idea ya es lo bastante clara como para aterrizarla
- cuando un hallazgo weekly merece trabajo propio

### 4.2 Flujo completo

1. conversacion tecnica en `M0` con Codex
2. `input de planificacion` transitorio
3. `plan.md` con Claude Opus
4. `plan_audit.md` con Codex
5. `execution.md` con Claude Sonnet
6. `post_audit.md` con Codex
7. `real_validation.md` si aplica
8. `closeout.md`
9. `lessons_learned.md`

### 4.3 Primer artefacto formal

El primer artefacto formal de iniciativa es `plan.md`.

El `input de planificacion` no es un artefacto formal.
Es solo un puente transitorio entre la conversacion `M0` y Claude.

### 4.4 Qué ya no existe

- artefactos intermedios de apertura del workflow anterior

## 5. Carril Weekly Review

### 5.1 Cuándo usarlo

- cuando quieres revisar la salud del repo
- cuando quieres detectar deuda, riesgos o candidatos
- cuando quieres reanclar prioridades sin abrir aun una iniciativa

### 5.2 Flujo completo

1. `Claude Sonnet` produce `weekly_briefing.md`
2. `Claude Opus` produce la review estrategica
3. se actualizan findings y backlog
4. salen candidate initiatives

### 5.3 Weekly normal vs baseline weekly

- `DELTA_WEEKLY`
  usa la ultima review valida y se centra en delta
- `BASELINE_WEEKLY`
  primera review profunda de un repo o de una gobernanza exportada

### 5.4 Qué el weekly no hace

- no genera `plan.md`
- no sustituye `M0`
- no abre una iniciativa por si solo
- no produce un pseudoplan por commits

## 6. Memoria Operativa Viva

### 6.1 `initiative_backlog.md`

Recoge ideas vivas y candidatas accionables.

Origen permitido:
- `conversation`
- `weekly`
- `closeout`

### 6.2 `architecture_findings_register.md`

Recoge hallazgos estructurales persistentes con evidencia.

### 6.3 `initiative_architecture_backlog.md`

Recoge remanentes y follow-ups de iniciativas cerradas.

### 6.4 Movimiento entre registros

- conversacion -> `initiative_backlog.md`
- weekly -> `candidate_initiatives.md` -> `initiative_backlog.md`
- backlog -> iniciativa real
- closeout -> `initiative_architecture_backlog.md` o cierre limpio

## 7. Modelos Y Roles

### 7.1 Claude

- `Opus`, `medium` para `plan.md`
- `Sonnet`, `medium` para implementacion
- `Sonnet`, `low` para validacion, cierre y lecciones
- `Sonnet` factual y `Opus` estrategico en weekly

### 7.2 Codex

- companero tecnico en `M0`
- auditor formal de planes
- auditor formal de implementacion
- apoyo para convertir hallazgos o ideas en iniciativas

### 7.3 Canon activo

El canon activo de esta gobernanza es solo:
- `Claude`
- `Codex`

## 8. Tooling Y Routing

- gobernanza -> `governance_search`
- codigo vivo -> `symdex_code`
- wiring e impacto -> `codebase-memory-mcp`
- lectura directa y `rg` solo como fallback

Regla maestra:
- retrieval dirigido primero
- lectura masiva solo si el routing canonico falla o no basta

## 9. MIT Y Krug

### 9.1 MIT

- Incrementality
- Integrity
- Transparency

### 9.2 Krug

- clarity
- feedback
- cognitive load
- affordance
- recoverability

### 9.3 Cómo se usan juntos

- MIT decide si la arquitectura evoluciona bien
- Krug decide si la experiencia se entiende bien
- un hallazgo puede ser `MIT-FIRST`, `KRUG-FIRST` o `MIXTO`

## 10. Cómo Empezar Una Iniciativa

Tu frase de arranque normal es:

`Vamos a preparar una iniciativa sobre X. Haz M0 conmigo.`

Cuando la idea ya está madura:

`Convierte esta conversación en input de planificación para Claude.`

Yo te devuelvo un bloque listo para pegar en Claude.

Luego:

`Audítame este plan.`

## 11. Cómo Hacer Un Weekly

Tu frase de arranque normal es:

`Quiero hacer el weekly MIT/Krug review.`

Si es la primera vez o un repo nuevo:

`Quiero hacer el baseline weekly MIT/Krug de este repo.`

Si una candidata te convence:

`Quiero convertir esta candidata en iniciativa.`

## 12. Reglas Anti-Duplicidad

- un hecho se escribe una vez
- weekly no produce plan
- backlog no contiene plan operativo
- `execution.md` no reexplica `plan.md`
- `closeout.md` no reescribe diagnostico completo
- no preservar conversaciones o weeklies completos si basta un extracto

## 13. Reglas Anti-Coste

- usar el modelo adecuado para cada fase
- limpiar contexto al pasar de plan a implementacion si viene cargado
- no releer `plan.md` entero si basta la cabecera o el tramo activo
- no pegar logs completos
- no usar `Opus` para lectura factual que puede hacer `Sonnet`

## 14. Criterios De Calidad

Un buen `plan.md`:
- aterriza problema, evidencia, alcance y riesgos
- propone tramos ejecutables
- define validacion y rollback
- no deriva en ensayo narrativo

Una buena auditoria:
- enumera hallazgos reales
- no usa `observaciones`
- no da `PASS` con pendientes

Una buena weekly:
- compara
- prioriza
- deja findings y candidatas vivos
- no intenta implementar

## 15. Errores Comunes

- usar weekly para planificar implementacion
- rehacer el plan en otro artefacto
- usar backlog como pseudoplan
- usar `Opus` para leer bruto
- mezclar ideas, hallazgos y remanentes en un mismo sitio
- reinyectar toda la historia por comodidad

## 16. Casos Especiales

- primer weekly en repo nuevo -> `BASELINE_WEEKLY`
- idea nacida de conversacion -> backlog o M0 directo
- remanente de iniciativa cerrada -> `initiative_architecture_backlog.md`
- cambio de alcance durante implementacion -> volver al plan

## 17. Glosario Operativo

- iniciativa
- weekly
- baseline weekly
- candidate initiative
- backlog
- hallazgo
- remanente
- plan audit
- post-audit
- validacion real

## 18. Ruta Rapida

- si quieres ejecutar algo ya: iniciativa
- si quieres revisar salud del repo: weekly
- si tienes una idea suelta: backlog
- si tienes un hallazgo weekly: candidata -> backlog -> iniciativa

## 19. Referencias Canonicas

- `AGENTS.md`
- `dev/workflow.md`
- `dev/policies/`
- `dev/guarantees/`
- `dev/prompts/`
- `doc/governance_prompts/`
- `dev/repo_governance_profile.md`

## 20. Evolucion De La Gobernanza

Esta gobernanza se cambia por reemplazo en sitio.

No se crea una `v2` paralela.
No se deja legado activo conviviendo con el canon.
Si algo queda obsoleto, se reescribe o se borra.
