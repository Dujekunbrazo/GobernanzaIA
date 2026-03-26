# Prompt — Audit Handoff

Actúa como `motor_activo`.

Tu tarea es preparar el paquete completo para auditoría formal.

No implementes cambios.
No inventes información.
No generes fixes.
No sobrescribas `dev/records/initiatives/<initiative_id>/handoff.md`; ese
archivo queda reservado al handoff de apertura de `M4`.

## Debes incluir

1. Contexto
- objetivo original
- fase actual
- fases completadas
- estado del Ask y del Plan

2. Plan congelado (resumen)
- commits propuestos
- alcance definido
- referencia al Ask congelado

3. Implementación real
- commits ejecutados
- archivos tocados
- cambios relevantes

4. Validación realizada
- comandos ejecutados
- resultados

5. Error original (si aplica)
- comando
- output

## Salida

Generar bloque listo para:
- incorporar en `dev/records/initiatives/<initiative_id>/post_audit.md`, o
- entregar al `motor_auditor` como resumen de auditoría
