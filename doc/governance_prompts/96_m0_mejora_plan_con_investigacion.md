# M0 — Mejora Del Input De Planificación Con Investigación
> [!IMPORTANT]
> Bootstrap obligatorio de gobernanza antes de usar este prompt:
> leer `AGENTS.md`, cargar la Skill canonica si existe, usar `governance_search`
> para gobernanza con `phase`/`document_type` cuando aplique, usar `symdex_code`
> para codigo vivo y `codebase-memory-mcp` para wiring/impacto/legacy cuando
> toque codigo, y declarar cualquier degradacion antes de recurrir a lectura
> bruta.

Usa este prompt cuando ya existe una idea o un borrador de plan y quieres que
Codex lo refuerce con investigación externa y mejores prácticas actuales antes
de pasar a `F1`.

Objetivo:

- encontrar papers o fuentes fuertes sobre el problema real
- destilar implicaciones prácticas para esta iniciativa
- devolver un input de planificación más sólido para `Claude`

Prompt base:

> Analiza esta iniciativa en profundidad.
>
> 1. Identifica primero qué preguntas técnicas o de producto requieren
>    investigación externa real.
> 2. Busca bibliografía primaria y reciente realmente relevante para esas
>    preguntas, priorizando papers, documentación oficial, benchmarks y
>    publicaciones con evidencia sólida.
> 3. Extrae solo los hallazgos que cambien decisiones del plan: arquitectura,
>    riesgos, validación, métricas, secuenciación, tradeoffs o límites
>    conocidos.
> 4. Reescribe y mejora el plan original incorporando esas conclusiones de
>    forma concreta, trazable y sin romper el alcance aprobado.
>
> Reglas:
> - No metas investigación decorativa.
> - No cites por prestigio institucional; cita por relevancia y calidad de
>   evidencia.
> - No amplíes el alcance sin justificarlo explícitamente.
> - Si la evidencia es débil, contradictoria o no concluyente, dilo de forma
>   explícita.
> - Toda mejora del plan debe quedar conectada con un hallazgo externo
>   verificable.
> - La investigación debe mejorar el plan, no sustituirlo ni convertirlo en un
>   ensayo académico.
> - Si una línea del plan original ya es correcta, consérvala; no la
>   reescribas solo por estilo.
>
> Entrega:
> - resumen de preguntas investigadas
> - fuentes clave y por qué importan
> - hallazgos accionables
> - plan reescrito y mejorado
> - cambios principales respecto al plan original
> - riesgos, supuestos y puntos aún no resueltos

Reglas:

- úsalo en `M0`, no dentro de `F1-F4`
- sirve para fortalecer el input, no para sustituir `plan.md`
- el resultado debe volver a aterrizarse en el canon del repo antes de pasarlo
  a `Claude`
