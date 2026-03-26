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

### 2026-03-11 — Separación formal entre gobernanza recuperable y SymDex de código

**Contexto**
La gobernanza activa consumía demasiado contexto y mezclaba en la misma capa
reglas de procedimiento, histórico documental y navegación de código. Además,
la operación con múltiples motores exigía una gobernanza neutral por rol y una
auditoría menos burocrática.

**Decisión**
Adoptar una arquitectura de contexto con tres piezas:
- capa estática mínima siempre presente
- gobernanza textual recuperable bajo demanda mediante recuperación híbrida
- `SymDex` reservado exclusivamente para código vivo del producto

Además:
- el modo por defecto pasa de `M1` a `M0`
- no existen motores por defecto
- `Codex`, `Claude`, `Gemini` y `Roo` pueden actuar como `motor_activo` o
  `motor_auditor` si el usuario los designa
- las auditorías formales separan `hallazgos` bloqueantes de `observaciones`
  no bloqueantes

**Motivo**
Reducir tokens, separar proceso de sustancia técnica, mantener auditabilidad
real y evitar que detalles editoriales bloqueen fases formales.

**Impacto**
`AGENTS.md`, `dev/workflow.md`, adapters de motor, compatibilidad `.roo/`,
prompts/templates de auditoría y documentación de arquitectura del repo.

**Riesgos asumidos**
Necesidad de mantener consistencia estricta entre fuentes canónicas y capas de
compatibilidad, especialmente en Roo y en los artefactos de auditoría.

**Revisión futura**
Si la recuperación de gobernanza sigue trayendo ruido o ambigüedad, evaluar
endurecer más el filtro determinista o incorporar configuración técnica
dedicada del retrieval.

---

### 2026-03-11 — Solución operativa para contexto MCP

**Contexto**
La iniciativa `2026-03-11_integracion_operativa_contexto` exige dejar
operativos `SymDex` para código vivo y el retrieval semántico de gobernanza.
En el entorno actual no existe binario/package verificable de `symdex` o
`symdex-mcp`.

**Decisión**
Implementar dos servidores MCP locales en `scripts/ops/context_mcp/`:
- `symdex-code` para código vivo con índice local acotado al perímetro canónico
- `governance-retrieval` para gobernanza textual con recuperación híbrida

Para embeddings:
- usar `OpenAI Embeddings` si existe `OPENAI_API_KEY`
- usar `Google Gemini Embeddings` como fallback si la clave operativa es
  `GOOGLE_API_KEY` o `GEMINI_API_KEY`

**Motivo**
Cerrar la iniciativa con integración real, usando capacidades verificables del
entorno actual, sin depender de un binario externo no localizable.

**Impacto**
`scripts/ops/context_mcp/`, `AGENTS.md`, `dev/workflow.md`,
`dev/ai/adapters/*`, `doc/architecture/context_retrieval_architecture.md`,
`%APPDATA%\\Claude\\claude_desktop_config.json`.

**Riesgos asumidos**
La primera indexación semántica depende de disponibilidad de la API de
embeddings configurada en `.env` y la activación final en UI requiere reinicio
de Claude Desktop.

**Revisión futura**
Si aparece un `symdex-mcp` canónico y verificable, reevaluar si conviene
sustituir la implementación repo-local.

---

### 2026-03-11 — El cliente objetivo real para MCP en este repo es VS Code

**Contexto**
La integración operativa del sistema de contexto se había conectado a
`claude_desktop_config.json`, pero el flujo real del usuario opera en
`VS Code + Antigravity + extensiones`.

**Decisión**
Usar:
- `.mcp.json` en raíz del proyecto para `Claude Code for VS Code`
- `.claude/settings.local.json` para aprobación local de servidores MCP
- `.vscode/mcp.json` para configuración MCP del workspace real en VS Code

Y retirar la integración declarada en `Claude Desktop` como ruta principal.

**Motivo**
Una integración MCP solo cuenta como operativa si está conectada al cliente
real donde trabajan los agentes.

**Impacto**
`.mcp.json`, `.claude/settings.local.json`, `.vscode/mcp.json` y limpieza de
`%APPDATA%\\Claude\\claude_desktop_config.json`.

**Riesgos asumidos**
La visibilidad efectiva de los servidores en cada extensión concreta depende de
recargar VS Code / la extensión correspondiente.

**Revisión futura**
Si Codex requiere una ruta adicional específica distinta del MCP workspace de
VS Code, documentarla y separarla explícitamente.

---

### 2026-03-10 — Correo persistente y lectura limpia como pipeline general de producto

**Contexto**
El workstation actual permite recuperar listas de mails y abrir detalles, pero
trata el material como salida efimera del turno y muestra el cuerpo del mail
sin una separacion semantica clara entre contenido util, firma, disclaimer,
historico citado o ruido del cliente. El problema se agrava al mezclar correos
humanos, notificaciones administrativas y alertas automaticas.

**Decisión**
Plantear la evolucion del correo como una capacidad general de producto basada
en dos piezas coordinadas: material persistente dentro del asunto y lectura
limpia/trazable del detalle de mail. La direccion tecnica propuesta es un
pipeline general de clasificacion de tipo de mail y segmentacion por bloques,
no una coleccion de hardcodes por empresa ni una solucion principal apoyada en
RAG o LLM por cada correo.

**Motivo**
Permite mantener alineacion con MIT y Krug, reducir carga cognitiva sin perder
trazabilidad y evitar tanto la fragilidad de reglas puras como la opacidad de
una solucion enteramente generativa. El corpus dominante disponible del usuario
sirve para validacion inicial, pero no define el modelo conceptual del
producto.

**Impacto**
Proyeccion del workstation, contrato interno del material de correo, render de
detalle de mail, futura estrategia de validacion con corpus real y formulacion
de la iniciativa `2026-03-10_material_correo_persistente`.

**Riesgos asumidos**
Mayor esfuerzo inicial de diseño y validacion, especialmente para evitar
falsos positivos al plegar contenido en notificaciones oficiales o mensajes
automaticos.

**Revisión futura**
Revisar en F4/F5 si la primera iteracion necesita una capa secundaria de
perfiles por remitente o si basta con el pipeline general.

---

### 2026-02-26 — Grounding obligatorio anti-alucinación para factual externo multi-MCP

**Contexto**
Se detectó una brecha estructural: en chat libre, consultas factuales externas podían resolverse sin ejecución obligatoria de herramientas, causando riesgo de alucinación.

**Decisión**
Adoptar como política de sistema: cero respuestas factuales externas sin evidencia ejecutada por tools, con pipeline único para 5 MCP (Intent Router -> Capability Resolver -> Planner -> Policy Gate -> Executor -> Evidence Store -> Composer grounded).

**Motivo**
Eliminar soluciones por parche y garantizar un comportamiento consistente, trazable y auditable para cualquier integración MCP presente o futura.

**Impacto**
Contratos de acción/evidencia, orquestación del runtime en `core/sync`, política de writes con confirmación explícita, suite de regresión anti-alucinación y observabilidad por `flow_id/trace_id`.

**Riesgos asumidos**
Mayor complejidad inicial y potencial aumento de latencia por ejecución de tools y validaciones adicionales.

**Revisión futura**
Tras completar F8/F9 de la iniciativa `2026-02-26_antialucinacion_multi_mcp`, revisar métricas de latencia y tasa de bloqueos para ajustar presupuesto/planificación sin relajar invariantes.

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

---

### 2026-03-09 — Bootstrap M365 desde sesion persistida del vendor local

**Contexto**
Kiminion seguia dependiendo de bearers MCP manuales aunque MCP Desktop mantuviera una sesion Microsoft 365 valida en `localhost:3000`. El token MCP caducaba, pero el usuario no podia volver a abrir una nueva sesion Microsoft por restricciones de IT.

**Decisión**
Adoptar como ruta operativa principal un bootstrap local entre Kiminion y el vendor `MCP-Microsoft-Office`: Kiminion intenta recuperar un bearer MCP desde la sesion persistida del vendor local y el vendor persiste suficiente estado MSAL/SQLite para reemitir ese bearer sin relogin Microsoft.

**Motivo**
Es la unica via que elimina el copy/paste manual sin exigir una nueva autenticacion de Microsoft al usuario. Ademas separa mejor configuracion estable, sesion web del vendor y bearer MCP de transporte.

**Impacto**
`core/app/runtime.py`, `core/concepts/auth/m365_auth.py`, `integrations/MCP-Microsoft-Office/src/api/controllers/local-session-bootstrap-controller.cjs`, `integrations/MCP-Microsoft-Office/src/auth/msal-service.cjs`, `integrations/MCP-Microsoft-Office/src/core/database-factory.cjs` y la operativa documentada en `README.md`.

**Riesgos asumidos**
Dependencia explicita del vendor local en `localhost:3000` y de su almacenamiento persistente (`SQLite` + cache MSAL) como fuente de recuperacion para Kiminion. Si el usuario borra esa sesion o cambia el entorno del vendor, Kiminion puede volver a requerir recuperacion manual.

**Revisión futura**
Si se introduce un store MSAL compartido o un flujo formal de cuenta de servicio, reevaluar si Kiminion debe seguir dependiendo del vendor local o pasar a una sesion Graph propia con refresh token persistido.

---

### 2026-03-06 — Cerrar base pre-workstation antes de cualquier rediseño UI

**Contexto**
Tras completar el desacople y la semántica base de la UI, el sistema ya no depende de Flet en las rules, pero aún conserva deuda técnica estructural: colisión de entries por `flow_token`, bootstrap con bypasses directos, store insuficiente para inspector futuro y deuda operativa en alertas/budget/provider status.

**Decisión**
Abrir una iniciativa específica de hardening de base pre-workstation y bloquear cualquier rediseño visual hasta cerrar esa deuda.

**Motivo**
Separar claramente trabajo estructural y trabajo visual. Evita construir la workstation sobre un modelo semántico incompleto y reduce el riesgo de regresiones mezcladas con cambios de diseño.

**Impacto**
Afecta a `core/app/ui_state_store.py`, `core/app/ui_port.py`, `core/app/flet_ui_adapter.py`, `core/app/runtime.py`, `kiminion_ui.py`, reglas UI y suite de tests de integración.

**Riesgos asumidos**
Se retrasa el rediseño visual, pero se gana una base más estable y auditable para hacerlo después sin arrastrar deuda oculta.

**Revisión futura**
Cuando la iniciativa de hardening base pre-workstation cierre en verde, se podrá abrir la iniciativa de workstation profesional como cambio separado.

---

### 2026-03-06 — Base pre-workstation cerrada antes de abrir la workstation profesional

**Contexto**
La iniciativa `2026-03-06_hardening_base_pre_workstation` se completó con transcript multi-entry, snapshots por flujo, bootstrap sin bypasses y deuda operativa mínima cerrada en alertas/budget/provider status.

**Decisión**
Dar por cerrada la deuda técnica pre-workstation y tratar cualquier trabajo posterior de workstation como una iniciativa nueva, separada y puramente de producto/UI sobre esta base ya auditada.

**Motivo**
Evitar reabrir deuda estructural ya resuelta y mantener la separación entre hardening de base y rediseño visual/profesionalización de la interfaz.

**Impacto**
Afecta al punto de partida de la futura iniciativa de workstation y al criterio de no volver a mezclar refactor estructural con diseño visual.

**Riesgos asumidos**
La futura workstation heredará las decisiones semánticas cerradas aquí; si se quisiera cambiar el modelo base, habría que abrir una iniciativa específica y no modificarlo de forma incidental durante el rediseño.

**Revisión futura**
Cuando se abra la iniciativa de workstation profesional, revisar solo necesidades de proyección UI y ergonomía, no la base semántica ya consolidada en esta fase.
 
---

### 2026-03-06 — Workstation profesional implantada sin reabrir la base semántica

**Contexto**
La iniciativa `2026-03-06_workstation_profesional` se abrió tras cerrar la base pre-workstation. El objetivo era sustituir la UI visible por una workstation operativa en Flet, manteniendo la base semántica ya auditada y sin ampliar `UiPort` por defecto.

**Decisión**
Dar por implantada y cerrada la workstation profesional como nueva ruta principal de producción, usando `WorkstationUiAdapter`, `TurnCard`, inspector contextual, chrome observable, command surface y alertas integradas visualmente.

**Motivo**
Separar claramente la evolución visual/profesionalización de la interfaz de la deuda estructural ya resuelta, y consolidar una experiencia de trabajo más adecuada al runtime real del sistema.

**Impacto**
Afecta a `kiminion_ui.py`, `core/app/workstation_*`, `core/app/components/turn_card.py`, la suite específica de workstation y la superficie visual principal de la aplicación.

**Riesgos asumidos**
La workstation v1 resuelve implantación y ergonomía base, pero no agota futuras optimizaciones visuales o de rendimiento para sesiones largas.

**Revisión futura**
Si se abre una nueva iteración de UI, deberá tratarse como evolución de la workstation ya implantada, no como reapertura de la base semántica o del desacople previo.

---

### 2026-03-07 — Detalle de mail M365 como flujo independiente del transcript

**Contexto**
Se quería mejorar la lectura de mails M365 ya disponible en chat sin introducir todavía reply, forward, drafts ni envío, y sin abrir una vista paralela fuera de la workstation.

**Decisión**
Implementar la mejora en dos fases funcionales:
- lista de mails enriquecida con contexto visible (`Para`, `CC`, `Para ti` / `En copia`)
- acción estructurada `Ver completo` que abre el detalle del mail como un flujo nuevo e independiente en el transcript

**Motivo**
Mantener el cambio dentro del perímetro MIT actual: evolución incremental, transcript como superficie principal, metadatos operativos internos y mínima superficie nueva.

**Impacto**
Afecta a `core/sync/rules/evidence_compose_rule.py`, `core/sync/rules/assistant_reply_rule.py`, `core/sync/rules/mail_detail_rule.py`, `core/app/components/turn_card.py`, `core/app/workstation_ui_adapter.py`, `core/contracts/events.py` y `manifests/m365.yaml`.

**Riesgos asumidos**
El detalle del mail queda solo en lectura en esta iniciativa; responder, reenviar y enviar requerirán una iteración posterior con su propio control de riesgo.

**Revisión futura**
Cuando se abra la siguiente iniciativa de correo, reutilizar los metadatos internos ya conservados en `UiTurn.metadata` para construir reply/reply-all/forward sin rehacer el flujo de lectura.

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

---

### 2026-02-25 — Baseline congelado: chat + memoria persistente

**Contexto**
Tras retirar MCP y estabilizar slash commands, el sistema quedó funcional en su
mínimo operativo (chat, `/update`, `/end`, persistencia dual).

**Decisión**
Congelar este baseline y exigir smoke test antes de cambios de arquitectura.
Script canónico: `scripts/dev/smoke_chat_memory.py`.

**Motivo**
Evitar regresiones sobre un punto estable y reducir retrabajo en sesiones
siguientes.

**Impacto**
Flujo de desarrollo diario y criterio de entrada a cambios estructurales.

**Riesgos asumidos**
Puede aumentar el tiempo previo a cambios grandes por validaciones adicionales.

**Revisión futura**
Cuando existan tests de integración automáticos equivalentes en CI.

---

### 2026-02-26 — Manejo de servidores persistentes en Windows

**Contexto**
Durante el arranque de MCP en Windows se interpretó como cuelgue ejecutar
`node src/main/dev-server.cjs` con `cmd /c` en foreground, cuando en realidad
es un proceso persistente por diseño.

**Decisión**
Tratar servidores (`dev-server`, APIs locales, watchers) como procesos de larga
vida: lanzarlos en terminal separada/background (`start` o `Start-Process`) y
evitar `cmd /c` en foreground para flujos que esperan finalización.

**Motivo**
Eliminar falsos diagnósticos de bloqueo y evitar interrupciones manuales de
procesos sanos que están sirviendo correctamente.

**Impacto**
Scripts de arranque (`start_kiminion.bat`) y troubleshooting operativo de MCP
local en Windows.

**Riesgos asumidos**
Mayor cantidad de ventanas/procesos activos y necesidad de cierre explícito al
terminar sesión.

**Revisión futura**
Si se migra a un supervisor único de procesos (por ejemplo, `npm-run-all`,
`concurrently` o servicio de Windows) con gestión de ciclo de vida centralizada.

---

### 2026-03-07 — Gobernanza multi-IA simplificada y neutral por rol

**Contexto**
La gobernanza activa tenía fases y roles heredados (`F2.5`, `Architect`,
`Orchestrator`) y estados de auditoría blandos (`PASS_WITH_OBSERVATIONS`) que
ya no reflejaban la forma real de trabajo.

**Decisión**
Simplificar el proceso formal a `F1-F9` con:
- `F3` y `F5` como auditoría + congelado
- `F8` para docs/cierre y `F9` para `lessons_learned.md`
- solo dos roles operativos: `motor_activo` y `motor_auditor`
- auditorías formales con decisión binaria `PASS` o `FAIL`

Además:
- MIT Concept-Sync se fija como baseline por defecto.
- Se incorpora política Git/GitHub canónica en
  `dev/policies/git_workflow_rules.md`.
- Se definen artefactos mínimos distintos para `M3` y `M4`.

**Motivo**
Reducir ambigüedad operativa, eliminar acoplamientos a motores concretos y
mejorar trazabilidad real entre iniciativa, auditoría y cierre.

**Impacto**
Afecta a `AGENTS.md`, `dev/workflow.md`, `dev/guarantees/*`,
`dev/policies/*`, `dev/templates/initiative/*`, `dev/prompts/*`,
`dev/ai/adapters/*` y documentación operativa de `dev/`.

**Riesgos asumidos**
Necesidad de mantener compatibilidad conceptual con histórico ya cerrado que
usa terminología previa (`F2.5`, roles heredados).

**Revisión futura**
Cuando se estabilice este modelo, evaluar una segunda iniciativa para
enforcement automático (`check_governance_compliance.py`) en CI.

---

### 2026-03-07 — Gobernanza de ingeniería multi-capa con carga condicional

**Contexto**
La gobernanza activa ya estaba simplificada por fases (`F1-F9`) pero solo
declaraba MIT como baseline técnico explícito. Faltaba una capa operativa para
Clean Code, usabilidad cognitiva (Krug), excepciones por rendimiento y reglas
de validación, además de límite de convergencia para auditorías formales.

**Decisión**
Introducir una gobernanza de ingeniería en tres niveles:
- resumen ejecutivo en `AGENTS.md`
- reglas técnicas auditables en
  `dev/policies/ai_engineering_governance.md`
- referencia larga no obligatoria en
  `doc/architecture/ai_engineering_dossier.md`

Además:
- añadir convergencia formal de auditorías en `dev/workflow.md`
  (`1` auditoría + máximo `2` re-auditorías por fase).
- extender `dev/policies/git_workflow_rules.md` con:
  - commit formal final al terminar `F9` con `closeout.md` y
    `lessons_learned.md`
  - prohibición de abrir nueva iniciativa formal sobre working tree con cambios
    sin commit de otra iniciativa, salvo excepción documentada.

**Motivo**
Evitar deriva de criterios técnicos entre motores, reducir coste de contexto por
sesión y cortar iteraciones de auditoría indefinidas sin perder rigor.

**Impacto**
`AGENTS.md`, `dev/workflow.md`, `dev/policies/git_workflow_rules.md`,
`dev/policies/ai_engineering_governance.md`, `doc/architecture/`,
`dev/ai/adapters/*`, `dev/ai/README.md`.

**Riesgos asumidos**
Mayor volumen documental en la capa de gobernanza y necesidad de mantener
coherencia entre resumen ejecutivo, policy corta y dosier largo.

**Revisión futura**
Si aparece fricción operativa, evaluar enforcement automatizado ligero para
validar terminología activa y presencia de reglas mínimas por fase.

---

### 2026-03-09 — M365 vendor-only como única fuente de verdad operativa

**Contexto**
Kiminion mantenía un flujo OAuth paralelo en Python (refresh/access token
Microsoft) además de la sesión real del vendor local en `localhost:3000`,
provocando estados inconsistentes y recuperación frágil tras reinicios.

**Decisión**
Fijar el modelo `vendor_local_session` como única fuente de verdad operativa
para M365 en runtime. Kiminion consume estado/sesión del vendor, elimina
vestigios de `MICROSOFT_AUTH_FLOW` y evita side-effects de bootstrap en
consultas de estado.

**Motivo**
Reducir complejidad accidental, eliminar doble autoridad de sesión y alinear el
comportamiento técnico con la ruta de recuperación realmente disponible para el
usuario.

**Impacto**
`core/app/runtime.py`, `core/concepts/auth/m365_auth.py`,
`core/config/{validator.py,schema.py,env_loader.py,README.md}`,
`core/sync/rules/slash_command_rule.py`, tests M365/runtime/config y la
iniciativa `dev/records/initiatives/2026-03-09_unificar_sesion_m365/`.

**Riesgos asumidos**
Si el vendor arranca sin sesión web reutilizable, `/api/auth/status` puede
devolver `authenticated=false` y exigir recuperación manual vía
`http://localhost:3000` + `/m365 reconnect`.

**Revisión futura**
Si reaparecen incidencias de sesión en frío, evaluar endurecimiento adicional
del contrato de estado del vendor sin reintroducir OAuth paralelo en Python.

---

### 2026-03-09 — Cierre Git con elevación temprana y sin bucles

**Contexto**
En cierres recientes de iniciativa se repitieron intentos de `git add`/`commit`
en contexto sin permisos efectivos sobre `.git`, produciendo iteraciones largas
antes de solicitar elevación del operador. Además, el append tardío de bitácora
generó commits/push adicionales de cierre.

**Decisión**
Formalizar un protocolo anti-bucle para `F8/F9`:
- preflight de permisos efectivos antes del primer `git add` en cierre;
- secuencia obligatoria: bitácora de cierre -> commit formal -> push -> árbol
  limpio;
- límite de reintentos: ante primer `Permission denied`, cambiar de contexto y
  evitar repetir en bucle.

**Motivo**
Reducir fricción operativa en cierres y evitar pérdida de tiempo por reintentos
inútiles cuando el problema real es ACL/sandbox.

**Impacto**
`dev/policies/git_workflow_rules.md`, `dev/workflow.md`,
`dev/policies/bitacora_rules.md`, `dev/guarantees/docs_gate.md`,
`dev/ai/adapters/codex.md`, e iniciativa M3
`dev/records/initiatives/2026-03-09_cierre_git_sin_bucle/`.

**Riesgos asumidos**
La elevación sigue dependiendo de confirmación explícita del operador (`Yes`),
por diseño de seguridad del entorno.

**Revisión futura**
Si reaparecen incidencias, evaluar automatización de preflight ACL para avisar
antes de entrar en staging de cierre.

---

### 2026-03-10 — Reapertura de F4 en material de correo persistente

**Contexto**
La prueba real de la iniciativa `2026-03-10_material_correo_persistente`
mostró que el plan congelado no respetaba el modelo de trabajo deseado:
`Material` actuaba como mini-workspace con detalle embebido, el transcript
seguía funcionando como visor secundario de mails y la persistencia quedaba
demasiado acoplada al flujo conversacional visible.

**Decisión**
Mantener `ask.md` como valido y reabrir `F4` sobre el mismo `plan.md`, sin crear
`plan2.md`.

El nuevo plan debe imponer estas reglas:
- `Material` es inventario persistente minimo del asunto;
- la zona de trabajo es el unico visor real del mail activo;
- el chat deja solo trazas breves de incorporacion o trabajo, sin renderizar
  mails completos;
- la limpieza semantica del mail debe existir una sola vez y reutilizarse desde
  un estado canonico del asunto.

**Motivo**
Evitar duplicidad documental y, sobre todo, duplicidad conceptual en runtime:
un mismo mail no puede seguir viviendo a la vez como reply conversacional,
detalle en Material y artefacto de trabajo.

**Impacto**
`dev/records/initiatives/2026-03-10_material_correo_persistente/plan.md`
queda reescrito y vuelve a `PROPUESTO`. `plan_audit.md` pasa a ser historial del
plan anterior y no habilita `F6` hasta nueva auditoria `F5`.

**Riesgos asumidos**
La reescritura del plan amplía el saneamiento estructural del subsistema mail,
pero reduce deuda tecnica futura y evita consolidar un modelo espagueti.

**Revisión futura**
En la siguiente auditoria `F5`, verificar expresamente que el plan elimina la
dualidad transcript/material y que no deja rutas legadas de apertura de mail
como deuda dormida.
