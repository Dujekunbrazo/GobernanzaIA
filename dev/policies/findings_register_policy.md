# Policy: Architecture Findings Register

## Objetivo

Mantener un registro vivo y trazable de hallazgos arquitectonicos del repo.

## Reglas

- el registro no es un informe semanal
- el registro persiste entre semanas
- un hallazgo no debe reaparecer como si fuera nuevo si ya existe
- cada hallazgo debe tener estado y via de remediacion sugerida
- un hallazgo material no puede vivir solo en `weekly_review.md`
- cuando una iniciativa cierre un hallazgo, el registro debe actualizarse

## Estados minimos

- `NUEVO`
- `PERSISTENTE`
- `RESUELTO`
- `RECLASIFICADO`

## Vias de remediacion

- `WATCHLIST`
- `M3`
- `M4`

## Criterio de aceptabilidad

El registro es valido cuando:

- evita redescubrir el mismo problema cada semana
- permite decidir que debe corregirse y que solo debe observarse
- permite trazabilidad desde weekly hasta iniciativa o watchlist
