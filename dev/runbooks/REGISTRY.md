# Runbook Registry

Este registro etiqueta el estado de cada runbook heredado.

Estados:
- `APLICA`
- `PENDIENTE_ADAPTACION`
- `HEREDADO_NO_APLICA`

## Estado vigente

| Runbook | Estado | Motivo |
| --- | --- | --- |

_(Sin runbooks registrados aún. Añadir entradas cuando aplique.)_

## Regla de uso

- Los `HEREDADO_NO_APLICA` no pueden usarse en ejecución.
- Los `PENDIENTE_ADAPTACION` solo pueden usarse con disclaimer explícito.
- Ningún runbook heredado puede aprobar gates del workflow sin adaptación formal.
