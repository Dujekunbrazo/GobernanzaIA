# Quickstart Humano del Orquestador

Esta guia corta define las frases canonicas para arrancar y operar una
iniciativa `M4` con el orquestador desde chat.

Contrato corto:

- el orquestador coordina estado, fase, continuidad y checkpoints
- los motores escriben los artefactos sustantivos de la iniciativa
- si se abre un chat nuevo, el orquestador rehidrata; el chat no actúa como
  memoria fiable por sí solo

## Abrir una iniciativa nueva desde handoff

Usa esta frase:

```text
GOBERNANZA NUEVA | repo=<repo> | initiative_id=<id> | fuente=handoff | motor_activo=<motor>
```

Ejemplo:

```text
GOBERNANZA NUEVA | repo=Kiminion | initiative_id=2026-04-06_source_router_evolution | fuente=handoff | motor_activo=claude
```

Interpretacion operativa:

- el usuario pide apertura formal de gobernanza
- la iniciativa ya existe en `dev/records/initiatives/<initiative_id>/`
- `handoff.md` ya esta creado
- el orquestador debe abrir `M4`, localizar el handoff y ejecutar `F1`
- la parada natural queda en `F2`

## Aprobar F2

Usa una frase minima como:

```text
F2 aprobado, motor_auditor=codex
```

## Reabrir una fase formal

Usa una frase como:

```text
reabre F5 de la iniciativa <initiative_id>
```

o, si quieres dejar mas contexto:

```text
reabre F5 de la iniciativa <initiative_id> por hallazgos del plan audit
```

## Preparar F8 y rehidratar un chat nuevo

Usa una frase como:

```text
prepara F8 de la iniciativa <initiative_id>
```

Si se abre un chat nuevo del motor, el orquestador debe emitir siempre:

- `phase_ticket`
- `resume_packet`

La orden practica puede ser:

```text
rehidrata F8 de la iniciativa <initiative_id>
```

## Checkpoint lateral de F6

Para ejecucion supervisada por commit o tramo:

```text
lanza checkpoint F6 sobre C3 de la iniciativa <initiative_id>
```

o:

```text
ejecuta F6 solo para C3 y luego checkpoint auditor
```

## Regla de oro

El usuario no necesita recordar comandos internos del script.
Le basta con declarar:

- que es gobernanza
- el repo
- la iniciativa
- el motor activo o auditor cuando aplique
- la fase que quiere abrir o continuar

El orquestador traduce esa orden a:

- fase efectiva
- `phase_ticket`
- `resume_packet`
- siguiente paso permitido

## Review semanal MIT

La review semanal es un control recurrente del repo, separado de `M4`.
No autoriza cambios de codigo por si misma.

Frases canonicas:

```text
REVIEW SEMANAL INICIAL | repo=<repo> | fecha=<yyyy-mm-dd> | motor_activo=claude
```

```text
REVIEW SEMANAL | repo=<repo> | fecha=<yyyy-mm-dd> | motor_activo=claude
```

```text
REHIDRATA REVIEW SEMANAL | repo=<repo> | fecha=<yyyy-mm-dd>
```

La primera corrida valida debe crear una `BASELINE_INICIAL_MIT`.
Las corridas posteriores deben operar como `DELTA_SEMANAL_MIT`.

Primera corrida:

- no bebe de una review semanal anterior
- construye una fotografia profunda del repo
- crea el primer registro vivo de hallazgos
- fija la base de comparacion para las siguientes semanas

Corridas posteriores:

- comparan contra la ultima review semanal valida
- distinguen hallazgos nuevos, persistentes, resueltos y reclasificados
- priorizan delta y tendencia sobre redescubrimiento completo

Outputs esperados:

- `weekly_briefing.md`
- `weekly_review.md`
- `weekly_review_delta.md`
- `architecture_findings_register.md`
- `candidate_initiatives.md`

Si una review ya esta abierta en otro chat, la rehidratacion correcta debe
devolver:

- artefactos ya creados
- modo efectivo (`BASELINE_INICIAL_MIT` o `DELTA_SEMANAL_MIT`)
- ultimo punto aceptado
- siguiente paso permitido

Si una review genera una remediacion aprobable:

```text
APRUEBA REMEDIACION | repo=<repo> | fecha=<yyyy-mm-dd> | candidate_id=<id> | initiative_id=<initiative_id> | modo=M4 | motor_activo=<motor>
```

## Autochequeo dual de capas

Cuando un repo declare `symdex_code` o `codebase-memory-mcp` como
`DISPONIBLE`, el autochequeo correcto debe separar:

- tool expuesta
- capacidad funcional real
- límites metodológicos visibles en la sesión

Regla:

- no basta con ver tools expuestas en la lista del cliente
- hay que ejecutar pruebas mínimas reales sobre cada capa antes de iniciar un
  análisis serio
- el autocheck debe terminar con una decisión operativa:
  - `ESTADO: OK`
  - `ESTADO: FALTA ...`

Frase recomendada:

```text
Haz un autochequeo de MCP local y estructural en esta sesión y confirma:
1. tools expuestas
2. si SymDex tiene semantic_search real, un símbolo ambiguo como classify y un símbolo único como _build_rules
3. si codebase-memory-mcp responde list_projects, index_status y trace_path sobre un nodo real
4. qué limitación metodológica visible existe en cada capa
5. termina con ESTADO: OK o ESTADO: FALTA ...
```

Variante recomendada para comparación explícita:

```text
ANALISIS COMPARATIVO MCP LOCAL + ESTRUCTURAL
Usa symdex_code y codebase-memory-mcp de forma conjunta.
Primero haz autocheck dual de ambas capas.
Después compara qué responde mejor cada una, qué no responde bien ninguna,
y termina con una recomendación de routing canónico basada en evidencia.
```

Referencia de ejecución:

- `dev/policies/structural_analysis_execution_policy.md`
