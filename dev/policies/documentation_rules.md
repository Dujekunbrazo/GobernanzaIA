# Documentation Rules (Hard)

Estas reglas son obligatorias para cualquier IA y cualquier contribución humana.

## 1) Verificabilidad absoluta

- Prohibido documentar rutas, comandos, archivos o features inexistentes.
- Toda afirmación técnica debe poder verificarse en el repo actual.

## 2) Cambios incrementales

- `README.md` solo se actualiza de forma incremental.
- Prohibido reescribir README completo sin aprobación explícita.

## 3) Coherencia con el workflow

- La documentación de iniciativa vive en:
  `dev/records/initiatives/<initiative_id>/`.
- Los gates en `dev/guarantees/*.md` son plantillas, no bitácora histórica.
- El historial se guarda en `dev/records/`.

## 4) Estado documental por iniciativa

Cada iniciativa debe cerrar con:
- `closeout.md`
- estado de fases F1-F9
- evidencia de gates en verde o bloqueos aceptados explícitamente

## 5) Runbooks heredados

- Runbooks marcados `HEREDADO_NO_APLICA` no pueden guiar ejecución.
- Runbooks `PENDIENTE_ADAPTACION` solo pueden usarse con disclaimer explícito.

## 6) Calidad mínima de redacción técnica

- Títulos claros y consistentes.
- Fechas en formato ISO (`YYYY-MM-DD`).
- Decisiones con contexto, motivo e impacto.
- Evitar duplicación si ya existe una fuente canónica.

## 7) Regla de bloqueo

Si no se puede verificar una afirmación documental:
- la IA debe parar
- marcar `BLOQUEADO`
- pedir evidencia o corrección de contexto
