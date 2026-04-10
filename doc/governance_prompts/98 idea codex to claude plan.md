Actua como `Claude` bajo la gobernanza canonica del repositorio.

## Fuentes de verdad obligatorias
1. `AGENTS.md`
2. `dev/workflow.md`
3. `dev/guarantees/plan_gate.md`
4. `dev/ai/adapters/claude.md`
5. `dev/policies/*.md`

## Routing obligatorio
- Gobernanza: `governance_search`
- Codigo vivo: `symdex_code`
- Wiring e impacto: `codebase-memory-mcp`
- No uses lectura bruta como via primaria si el routing canonico responde

## Mision
Voy a darte un `input de planificacion` ya trabajado en `M0` con Codex.
Tu trabajo es convertir ese input en un `plan.md` ejecutable, auditable,
acotado y listo para auditoria formal.

## Lo que debes hacer
1. Entender el problema real y el resultado buscado
2. Separar hechos, supuestos y huecos
3. Aterrizar alcance y no-alcance
4. Identificar restricciones, riesgos y modulos afectados
5. Diseñar estrategia de implementacion incremental
6. Diseñar validacion global y validacion por tramos
7. Diseñar rollback
8. Dejar el plan listo para auditoria, sin narrativa sobrante

## Restricciones
- no implementes codigo
- no inventes evidencia faltante
- no recrees la conversacion completa dentro del plan
- no recrees artefactos intermedios del flujo anterior
- si falta informacion material, dejala explicita dentro del plan
- si detectas alcance ambiguo, declaralo como bloqueo o duda abierta

## Salida obligatoria
Genera un documento listo para guardar en:

`dev/records/initiatives/<initiative_id>/plan.md`

Con esta estructura minima:
1. Objetivo
2. Problema real
3. Resultado esperado
4. Evidencia base
5. Contexto tecnico relevante
6. Alcance
7. No-alcance
8. Restricciones
9. Supuestos
10. Riesgos principales
11. Superficies y modulos afectados
12. Decisiones ya tomadas
13. Dudas abiertas
14. Estrategia de implementacion
15. Plan por tramos
16. Validacion global prevista
17. Rollback
18. Definition of Done
19. Referencias

Marca final:
- `Estado: PROPUESTO`
- `Etiqueta: PENDIENTE_DE_AUDITORIA`

## Input de planificacion
[PEGAR AQUI]
