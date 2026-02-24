# Decision Log

Este archivo registra decisiones técnicas relevantes para evitar
reabrir debates ya resueltos.

Cada entrada debe ser breve, clara y justificada.

---

## Formato de entrada

### YYYY-MM-DD — Título corto de la decisión

**Contexto**
Qué problema o situación llevó a tomar esta decisión.

**Decisión**
Qué se decidió exactamente.

**Motivo**
Por qué se eligió esta solución frente a otras.

**Impacto**
Qué partes del sistema afecta.

**Riesgos asumidos**
Qué trade-offs aceptamos.

**Revisión futura**
Cuándo tendría sentido reconsiderar esta decisión (si aplica).

---

# Registro

---

### 2026-02-XX — Separación Runtime vs Dev Workflow

**Contexto**
Se estaba mezclando configuración de ejecución (KIMI.md, IDENTITY.md)
con reglas de desarrollo.

**Decisión**
Separar claramente:
- Runtime → KIMI.md, IDENTITY.md, personalidades.md, state/*
- Dev workflow → /dev y .roo

**Motivo**
Evitar contaminación del prompt de ejecución y token bloat.

**Impacto**
Estructura del repo y reglas de Roo.

**Riesgos asumidos**
Mayor número de archivos, ligera complejidad inicial.

**Revisión futura**
Si se introduce motor formal de agentes o enforcement real.

---

### 2026-02-XX — Plan Congelado Obligatorio

**Contexto**
Iteraciones excesivas entre planificación e implementación.

**Decisión**
Introducir Fase 3: PLAN CONGELADO obligatorio antes de implementar.

**Motivo**
Reducir deriva semántica y cambios fuera de alcance.

**Impacto**
Workflow completo del repo.

**Riesgos asumidos**
Menor flexibilidad en cambios espontáneos.

**Revisión futura**
Si el equipo crece o se automatiza enforcement.

---

### 2026-02-24 — Contrato Maestro Multi-IA

**Contexto**
Existían reglas repartidas entre varias capas (`dev`, `.roo`, prompts) sin una
directriz universal explícita para todas las IAs.

**Decisión**
Establecer `AGENTS.md` como contrato maestro multi-IA y alinear el resto de
capas a esa fuente.

**Motivo**
Eliminar ambigüedad entre herramientas y evitar divergencia de comportamiento.

**Impacto**
Gobernanza de proceso y adapters de IA en `dev/ai/adapters/`.

**Riesgos asumidos**
Sobrecarga inicial de documentación durante la transición.

**Revisión futura**
Cuando haya automatización de validación de compliance.

---

### 2026-02-24 — Auditoría Codex Interna por Fases

**Contexto**
El workflow histórico hablaba de auditor externo, pero la operación real
requiere auditoría interna sistemática por Codex.

**Decisión**
Fijar auditoría Codex en F2.5 (Ask), F5 (Plan) y F8 (Post-audit/debug).

**Motivo**
Reducir deriva entre planificación y ejecución antes de congelar artefactos.

**Impacto**
`dev/workflow.md`, `.roo/rules/*`, y prompts de auditoría.

**Riesgos asumidos**
Mayor rigor y posible aumento de bloqueos tempranos.

**Revisión futura**
Si se incorpora un segundo auditor independiente.

---

### 2026-02-24 — Cuarentena de Runbooks Heredados

**Contexto**
Los runbooks venían de otro proyecto y mezclaban rutas/módulos no presentes en
el repo actual.

**Decisión**
Clasificarlos formalmente en `dev/runbooks/REGISTRY.md` y excluir del flujo
operativo los marcados `HEREDADO_NO_APLICA`.

**Motivo**
Evitar decisiones basadas en documentación no aplicable.

**Impacto**
Gobernanza documental y gates de ejecución.

**Riesgos asumidos**
Pérdida temporal de runbooks operativos hasta adaptación.

**Revisión futura**
Tras adaptar o reemplazar runbooks por versiones nativas del repo actual.

---

### 2026-02-24 — Reglas duras de documentación y scripts

**Contexto**
Se necesitaba llevar el repo a estado base alineado al nuevo orquestador, con
enforcement explícito para docs y orden operativo en scripts.

**Decisión**
Crear políticas canónicas:
- `dev/policies/documentation_rules.md`
- `dev/policies/scripts_rules.md`

Y enlazarlas desde `AGENTS.md`, `dev/workflow.md`, `docs_gate` y reglas Roo.

**Motivo**
Evitar deriva documental y desorden operativo al ejecutar scripts con distintas
IAs o entornos.

**Impacto**
Gobernanza transversal de documentación y carpeta `scripts/`.

**Riesgos asumidos**
Mayor rigidez inicial en cambios rápidos.

**Revisión futura**
Cuando exista validación automática de cumplimiento en CI.

---

### 2026-02-24 — Orden canónico de scripts con compatibilidad retro

**Contexto**
`scripts/` no tenía jerarquía y mezclaba ruta operativa con compatibilidad.

**Decisión**
Definir estructura fija:
- `scripts/dev/`
- `scripts/ops/`
- `scripts/migration/`

Mover exportación de incidentes a `scripts/ops/export_incident.py` y mantener
wrapper de compatibilidad en `scripts/export_incident.py`.

**Motivo**
Ordenar operación sin romper comandos ya documentados.

**Impacto**
Ruta canónica de scripts y destino de artefactos en `reports/incidents/`.

**Riesgos asumidos**
Posible confusión temporal entre ruta canónica y wrapper.

**Revisión futura**
Retirar wrapper cuando todo el ecosistema use la ruta canónica.

---

### 2026-02-24 — Bitácora diaria automática por IA (capa proceso)

**Contexto**
Se requería trazabilidad diaria de conversaciones de trabajo con IAs de código
sin tocar runtime de Marvin.

**Decisión**
Implantar bitácora en:
- `dev/records/bitacora/`

Con script oficial:
- `scripts/ops/bitacora_append.py`

Y wrapper:
- `scripts/bitacora_append.py`

**Motivo**
Conservar historial operativo por IA/día para auditoría y continuidad.

**Impacto**
Adapters de IA, workflow, policies y gates de documentación.

**Riesgos asumidos**
Dependencia de cumplimiento del append por cada IA/herramienta.

**Revisión futura**
Automatizar validación en CI para detectar turnos no registrados.

---

### 2026-02-24 — Checklist automático de nomenclatura

**Contexto**
Se requería asegurar estructura y nombres homogéneos sin depender de revisión
manual.

**Decisión**
Crear reglas duras en `dev/policies/naming_rules.md` y validador:
`scripts/dev/check_naming_compliance.py`.

**Motivo**
Evitar deriva de estructura entre IAs y mantener cierre auditable.

**Impacto**
`AGENTS.md`, workflow, docs gate y reglas Roo.

**Riesgos asumidos**
Más bloqueos tempranos cuando el naming no cumple.

**Revisión futura**
Integrar este check en CI para enforcement automático por pull request.

---

### 2026-02-24 — Estado 0 de organización verificable

**Contexto**
Se necesitaba dejar el repo en estado base estable y auditable conforme a las
reglas de orquestación.

**Decisión**
Agregar política de layout (`repo_layout_rules.md`), checklist operativo
(`dev/checklists/state0.md`) y validador automático
(`scripts/dev/check_state0.py`).

**Motivo**
Tener criterio objetivo para declarar “estado 0” sin ambigüedad.

**Impacto**
Workflow, docs gate, AGENTS y reglas Roo.

**Riesgos asumidos**
Mayor fricción inicial por checks adicionales.

**Revisión futura**
Integrar check de state0 en CI junto a naming compliance.
