# AI Engineering Governance (Hard)

Esta policy define reglas técnicas de ingeniería para cambios de código y
producto. No define fases del workflow de iniciativa, gates ni convergencia de
auditorías; eso vive en `AGENTS.md` y `dev/workflow.md`.

## 1) Alcance y precedencia técnica

Precedencia:
1. MIT Concept-Sync (macroarquitectura).
2. Clean Code (microimplementación).
3. Krug / Don't Make Me Think (usabilidad cognitiva).
4. Rendimiento (excepción acotada sobre Clean Code en hot paths).
5. Validación (evidencia para aceptar cambios).

Regla de desempate:
- MIT manda en decisiones inter-concepto.
- Clean Code manda dentro de cada concepto.
- Krug manda en superficies orientadas a usuario.
- Rendimiento solo excepciona Clean Code cuando hay evidencia técnica.
- Si hay zona gris, el plan debe explicitar resolución auditable.

## 2) Macroarquitectura (MIT)

- Separar funcionalidades por unidades con valor claro para el usuario.
- Evitar acoplamiento directo entre conceptos salvo excepción documentada.
- Coordinar por eventos/sincronizaciones o mecanismo equivalente explícito.
- Mantener trazabilidad causal de flujos cuando aplique.
- Clausula anti-sobrediseño: MIT no obliga a atomizar por defecto.
  Si una separación añade complejidad sin mejorar integridad,
  incrementabilidad o trazabilidad, se simplifica.

## 3) Capacidades transversales y extensión canónica

- Si una capability afecta varias herramientas, canales, paths o superficiescon la misma responsabilidad semántica, se considera transversal y debe resolverse horizontalmente.
- Toda capability transversal debe declarar owner arquitectónico claro,
  contrato o abstracción canónica, punto de extensión único y mecanismo común de wiring (`descriptor`, `policy`, `registry` o equivalente).
- `planner`, `generator`, `router` y `execute` deben consumir la abstracción canónica; no deben convertirse en acumuladores de excepciones por herramienta o path.
- Está prohibido dar por resuelta una capability transversal mediante ramas locales del tipo `if tool == ...`, `if channel == ...`,
  `if filters.get(...)`, flags path-specific, bypass o hacks equivalentes.
- Está prohibida la coexistencia de múltiples caminos activos para la misma capability: coverage vertical aislada por herramienta, paths paralelos o fallback legacy conviviendo con el camino canónico.

## 4) Capability closure, wiring y retiro de legacy

- Una capability no se considera completada mientras no esté conectada en su wiring canónico sobre todas las superficies incluidas en alcance.
- Queda prohibido cerrar una iniciativa con integraciones huérfanas: handler, regla, descriptor, policy, registry o wiring añadido sin consumo real.
- Si una iniciativa introduce un camino canónico nuevo para una capability, el legacy equivalente debe eliminarse, quedar desactivado o declararse fuera de alcance con justificación explícita.
- La validación debe comprobar estructura y no solo el caso puntual: ausencia de branching oportunista fuera del owner arquitectónico, ausencia de convivencia entre camino canónico y legacy, y cobertura del wiring común sobre las superficies afectadas.
- Cuando el cambio toque el modelo de acción o el plano `planner`/`generator`/`router`/`execute`, debe leerse además `dev/policies/action_policy.md`.

## 5) Microimplementación (Clean Code)

- Nombres deben revelar intención y ser buscables.
- Una función debe tener responsabilidad principal clara.
- Evitar flags booleanos que mezclen caminos de lógica.
- Evitar comentarios compensatorios para justificar código confuso.
- Al tocar código existente, aplicar mejora incremental dentro del alcance real del cambio (regla Boy Scout acotada).

## 6) Usabilidad cognitiva (Krug)

Aplica a UI, CLI, DX y respuestas API orientadas a usuario:
- Priorizar claridad inmediata y convenciones reconocibles.
- Evitar fricción cognitiva y texto innecesario.
- Mensajes de error deben ser accionables y facilitar recuperación.
- Evitar creatividad de navegación/interacción sin beneficio claro y medible.

## 7) Rendimiento y hot paths

- No aplicar Clean Code de forma dogmática en rutas críticas.
- Se permite diseño más directo (menos abstracción) en hot paths si reduce
  coste real.
- Toda excepción por rendimiento requiere evidencia verificable:
  benchmark, perfilado, métricas o restricción técnica observable.
- Sin evidencia, prevalece legibilidad/mantenibilidad.

## 8) Validación y pruebas

- Todo cambio debe tener validación proporcional al riesgo.
- Cuando aplique, pruebas deben seguir `FIRST`:
  - Fast
  - Independent
  - Repeatable
  - Self-validating
  - Timely
- Cambios de usabilidad deben incluir comprobación orientada a tareas de
  usuario (manual o automatizada) cuando el impacto lo justifique.
- Cuando una capability transversal esté en alcance, la validación debe
  incluir evidencia estructural de wiring real, no-convivencia legacy/canónico
  y ausencia de branching oportunista cuando aplique.

## 9) Carga condicional de contexto

Lectura mínima por tarea:
- arquitectura/runtime: esta policy; dosier largo solo si hace falta.
- implementación interna: esta policy.
- UI/CLI/DX/API: esta policy con foco en usabilidad.
- hot paths: esta policy con foco en rendimiento y evidencia.
- acciones/capabilities transversales: esta policy y
  `dev/policies/action_policy.md`.

Dosier largo de apoyo:
- `doc/architecture/ai_engineering_dossier.md`

## 10) Terminología activa

- En gobernanza activa no usar nombres de roles heredados del esquema previo.
- Los roles válidos son motor activo y motor auditor.
