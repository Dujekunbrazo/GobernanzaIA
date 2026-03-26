# Ask Mode Behavior

Objetivo: producir un Ask útil bajo el contrato de `AGENTS.md` y
`dev/workflow.md`.

## Reglas obligatorias

1) No implementes código.
2) No generes plan final de commits de implementación.
3) No asumas que este modo define una fase oficial distinta a `F1/F2/F3`.
4) Trabaja con evidencia verificable (código, logs, docs del repo).
5) Para gobernanza dinámica, usa `governance_search` antes de cualquier lectura
   directa.
6) Declara herramienta usada y fuente canónica usada en cada respuesta técnica.
7) Si faltan MCPs activos, declara limitación operativa.
8) No uses iniciativas previas como fuente principal de proceso si existe
   fuente canónica.
9) Aplica `dev/guarantees/ask_gate.md`.

## Proceso obligatorio

### 1. Confirmación de entrada
- Resume objetivo, alcance preliminar y restricciones en 3-6 líneas.
- Si la sesión acaba de arrancar o se ha recargado, confirma si están activos
  `governance_search`, `symdex_search_code` y `symdex_read_code`.
- Si Roo va a intervenir como canal de auditoría en `F3`, pregunta antes si el
  usuario desea mantener o cambiar la API/modelo para esa auditoría.
- Si falta contexto material, declara qué fuente canónica necesitas leer.

### 2. Evidencia técnica
- Lista archivos y zonas de código relevantes.
- Lista logs o trazas relevantes (si aplica).
- Señala vacíos de información.

### 3. Preguntas de aclaración (bloqueantes y no bloqueantes)
- Prioriza preguntas que cambian diseño, métricas o aceptación.
- Si no hay bloqueantes, dilo explícitamente.

### 4. Opciones y trade-offs
- Propón 2-3 opciones de abordaje.
- Para cada opción: riesgo, coste y criterio de elección.

### 5. Recomendación Ask
- Recomienda una opción con razonamiento explícito.
- Define precondiciones para planificación.

### 6. Estado del dossier
- Entrega inicial:
  `ASK PROPUESTO — PENDIENTE DE VALIDACIÓN`
- Tras validación del usuario:
  `ASK VALIDADO`
- Tras consolidar cambios aceptados:
  `ASK CONGELADO`

## Salida obligatoria (estructura)

- Objetivo y contexto
- Evidencia técnica
- Supuestos
- Preguntas bloqueantes/no bloqueantes
- Opciones y trade-offs
- Recomendación Ask
- Criterios de aceptación para el `motor_activo`
- Estado del dossier (propuesto/validado/congelado)

## Restricciones

- No tocar código de producción en modo Ask.
- No saltar a `F4` si no existe `ASK CONGELADO`.
- Cualquier cambio posterior al Ask congelado obliga a reabrir F1.
- Usa solo terminología activa: `motor_activo` y `motor_auditor`.
- Los modos nativos de Roo no redefinen `M0-M4` ni `F1-F9`.
