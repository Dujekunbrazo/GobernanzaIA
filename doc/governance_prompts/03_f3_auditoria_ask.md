# F3 Auditoría Ask

Quiero auditar el Ask de esta iniciativa.

Usa la iniciativa activa y el `motor_auditor` ya designado en la iniciativa.

Audita el `ask.md` según la gobernanza del repo y deja el resultado en
`ask_audit.md` dentro de la misma carpeta.

Antes de seguir, confirma qué iniciativa estás auditando,luego crea ask_audit.md con el resultado de la auditoría.

Reglas adicionales obligatorias:
- no uses la categoría `observaciones`
- toda debilidad, riesgo, ambigüedad material o recomendación correctiva debe ir a `Hallazgos`
- si emites `PASS`, justifica explícitamente por qué no existe ningún hallazgo material ni pendiente
- el artefacto debe incluir obligatoriamente `## Hallazgos`, `## Justificación del veredicto`, `## Escalado de remediacion` y `## Condición para F3`
- además de escribir `ask_audit.md`, replica el artefacto completo al final de tu respuesta en un bloque ```md``` para recuperación del orquestador si la escritura falla
