# Prompt — README Update (Incremental)

Actúa como motor activo en actualización documental incremental.

Tu tarea es actualizar `README.md` según cambios reales implementados.

## Reglas obligatorias

- No reescribir el README completo.
- Solo modificar secciones existentes.
- Si necesitas crear sección nueva: marcar que requiere confirmación.
- No inventar rutas, comandos ni features.

## Entrada

Se proporciona:
- lista de archivos modificados
- resumen de cambios
- validación realizada
- referencia a `plan.md` y `closeout.md` si aplica

## Salida

1. Secciones modificadas
2. Texto exacto a añadir o reemplazar
3. Verificación de coherencia técnica
4. Resumen para `dev/records/initiatives/<initiative_id>/closeout.md`
