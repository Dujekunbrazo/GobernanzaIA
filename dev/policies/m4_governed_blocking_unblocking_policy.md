# M4 Governed Blocking And Unblocking Policy

Proposito:
- completar la policy de `first-pass quality` con una gobernanza canónica de
  `BLOQUEADO`
- detener loops ciegos sin paralizar la iniciativa sin protocolo de salida
- fijar desbloqueo válido y reentrada segura con una sola capa primaria

## 1) Ambito

- esta policy aplica al carril iniciativa `M4`
- complementa `dev/policies/m4_first_pass_quality_policy.md`
- no redefine weekly review ni automatiza `F5`

## 2) Semantica de BLOQUEADO

- `BLOQUEADO` detiene la automatización del script `ping_pong`
- `BLOQUEADO` no cancela ni cierra la iniciativa
- `BLOQUEADO` exige:
  - razón explícita
  - siguiente paso mínimo seguro
  - no invocación de motor mientras la causa siga activa

## 3) blocked_reason_code canonicos

La taxonomía mínima congelada es:

- `REPEATED_FAILURE_SIGNATURE`
- `MISSING_EVIDENCE`
- `MECHANICAL_ARTIFACT_CONFLICT`
- `PRE_GATE_FAILURE`
- `OUT_OF_SCOPE_WRITESET`
- `MODEL_ESCALATION_EXHAUSTED`
- `FINAL_VALIDATION_FAILED`

## 4) Clases canónicas de desbloqueo válido

Solo existen estas clases:

- evidencia nueva
- corrección mecánica segura
- cambio de estrategia
- escalado de modelo justificado
- reapertura de fase previa

Sin una de esas causas, no existe desbloqueo válido.

## 5) Artefacto canónico de desbloqueo

- `unblock_context.json` es la única capa primaria para decidir desbloqueo y
  reentrada
- `status` y `advance` solo pueden decidir reentrada desde ese sidecar
- `execution.md` y `real_validation.md` solo resumen el desbloqueo ya
  aceptado; no autorizan reentrada

## 6) Schema mínimo de unblock_context.json

Campos obligatorios:

- `blocked_reason_code`
- `failure_signature`
- `phase`
- `layer`
- `new_evidence_type`
- `new_evidence_ref`
- `approved_action`
- `resume_state`
- `model_override`
- `created_at_utc`

Reglas:

- `approved_action` solo puede ser:
  - `SAFE_MECHANICAL_FIX`
  - `RESUME_SAME_PHASE`
  - `REOPEN_PREVIOUS_PHASE`
  - `ESCALATE_MODEL`
  - `WAIT_FOR_HUMAN_EVIDENCE`
- `resume_state` no es libre; debe ser coherente con la matriz canónica
- `model_override` puede ser `null` si no aplica

## 7) Matriz mínima canónica

- `REPEATED_FAILURE_SIGNATURE`
  - `approved_action`: `REOPEN_PREVIOUS_PHASE` o `ESCALATE_MODEL`
  - `resume_state`: `REOPEN_F1` | `REOPEN_F3` | `RUNNING_F3` | `RUNNING_F3_FINAL`
- `MISSING_EVIDENCE`
  - `approved_action`: `WAIT_FOR_HUMAN_EVIDENCE`
  - `resume_state`: `null`
- `MECHANICAL_ARTIFACT_CONFLICT`
  - `approved_action`: `SAFE_MECHANICAL_FIX`
  - `resume_state`: `WAITING_FOR_F2_AUDIT_RESULT` | `WAITING_FOR_F4_AUDIT_RESULT` | `WAITING_FOR_F4_FINAL_AUDIT_RESULT`
- `PRE_GATE_FAILURE`
  - `approved_action`: `SAFE_MECHANICAL_FIX` o `REOPEN_PREVIOUS_PHASE`
  - `resume_state`: `READY_FOR_F1` | `RUNNING_F3` | `RUNNING_F3_FINAL`
- `OUT_OF_SCOPE_WRITESET`
  - `approved_action`: `REOPEN_PREVIOUS_PHASE`
  - `resume_state`: `REOPEN_F1` | `REOPEN_F3`
- `MODEL_ESCALATION_EXHAUSTED`
  - `approved_action`: `REOPEN_PREVIOUS_PHASE`
  - `resume_state`: `REOPEN_F1` | `REOPEN_F3`
- `FINAL_VALIDATION_FAILED`
  - `approved_action`: `REOPEN_PREVIOUS_PHASE`
  - `resume_state`: `REOPEN_F3`

## 8) Autoridad mínima del desbloqueo

- evidencia humana verificable:
  - `new_evidence_ref` debe apuntar a evidencia viva o artefacto formal ya
    existente del expediente
- corrección mecánica segura:
  - la emite el propio script tras verificación determinista
- escalado o reapertura:
  - deben quedar trazados en `unblock_context.json`
  - no se aceptan desbloqueos implícitos ni por texto libre

## 9) Reconciliación sidecar -> expediente

- primero se valida `unblock_context.json`
- si es válido, el script actualiza el resumen mínimo en `execution.md`
  antes de reentrar
- si es inválido, incompleto o incoherente con el bloqueo activo, el estado
  correcto sigue siendo `BLOQUEADO`
- no existe reconciliación expediente -> sidecar para esta responsabilidad

## 10) Regla anti-loop de desbloqueo

Si reaparecen el mismo `blocked_reason_code` y la misma `failure_signature`
sin cambio material trazado en `unblock_context.json`, el estado correcto
sigue siendo `BLOQUEADO`.
