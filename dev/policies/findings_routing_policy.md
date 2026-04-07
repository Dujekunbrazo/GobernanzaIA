# Policy: Findings Routing

## Objetivo

Definir como un hallazgo semanal pasa a `WATCHLIST`, `M3` o `M4`.

## Regla principal

La review semanal detecta y enruta.
No implementa correcciones por si misma.

## Routing minimo

- `WATCHLIST`
  - riesgo no material o evidencia insuficiente
  - se mantiene bajo observacion
- `M3`
  - cambio acotado, bajo write set, bajo riesgo de wiring transversal
- `M4`
  - cambio transversal, legacy, impacto observable, owner arquitectonico o
    plan multi-commit

## Señales para `M4`

- capability transversal
- riesgo de convivencia legacy/canonico
- wiring global o blast radius significativo
- cambio observable del producto
- necesidad de auditoria formal o validacion real

## Regla de persistencia

- un hallazgo `PERSISTENTE` no puede permanecer indefinidamente sin decision
  explicita
- si una `WATCHLIST` escala de riesgo, debe reclasificarse

## Criterio de aceptabilidad

El routing es correcto cuando:

- cada hallazgo tiene una via clara
- no quedan observaciones materiales flotando
- el paso a remediacion es gobernable y no ambiguo
