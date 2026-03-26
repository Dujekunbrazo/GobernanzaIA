# Action Policy (Hard)

Esta policy define el contrato canónico para capacidades que afectan el modelo
de acción y su ejecución transversal. Complementa `AGENTS.md` y
`dev/policies/ai_engineering_governance.md`; no sustituye gates ni workflow.

## 1) Alcance

Aplica cuando un cambio toca cualquiera de estos planos:

- `planner`
- `generator`
- `router`
- `execute`
- contratos de acción
- registros, descriptores o policies que gobiernan ejecución

## 2) Transversal capability

Definición:
- Una `transversal capability` es una capacidad que condiciona, enriquece,
  resuelve, valida o aprende sobre la ejecución de acciones a través de
  múltiples `tools`, `paths`, `channels` o superficies semánticamente
  equivalentes.

Reglas:
- Toda `transversal capability` debe tener owner arquitectónico explícito.
- Toda `transversal capability` debe exponer contrato canónico y punto de
  extensión único dentro del modelo de acción.
- La integración de una `transversal capability` debe resolverse mediante
  `descriptor`, `policy`, `registry` o mecanismo común equivalente.
- `planner`, `generator`, `router` y `execute` solo pueden consumir la
  capability a través del mecanismo canónico.

## 3) Capability closure

Definición:
- Una capability queda en `closure` solo cuando su contrato canónico está
  conectado mediante el wiring común previsto y resulta consumible desde todas
  las superficies incluidas en alcance.

Requisitos:
- Toda capability debe declarar:
  - owner arquitectónico
  - contrato canónico
  - mecanismo de adhesión (`descriptor`, `policy`, `registry` o equivalente)
  - punto de wiring canónico
  - criterio de validación estructural end-to-end

Prohibiciones:
- Queda prohibido considerar completa una capability si existe implementación
  sin wiring efectivo.
- Queda prohibido cerrar una capability con wiring parcial por herramienta o
  path.
- Quedan prohibidas las integraciones huérfanas.
- Queda prohibida la convivencia entre fallback legacy y capability canónica
  activa.
- Queda prohibida la activación por branching local fuera del mecanismo
  canónico.

## 4) Descriptor adhesion

- Cada acción o herramienta que participe en una `transversal capability` debe
  declararlo en su `descriptor` o registro canónico.
- La ausencia de adhesión explícita implica que la capability no está
  soportada para esa superficie.
- No se permite soporte implícito mediante wiring manual o ramas locales.

## 5) Validación

- Toda implementación que toque una `transversal capability` debe demostrar
  wiring común.
- Cuando aplique, las pruebas deben verificar ausencia de branching
  oportunista, ausencia de convivencia legacy/canónico y cobertura estructural
  sobre las superficies afectadas.
- No basta con validar el caso feliz de una sola herramienta si la capability
  declarada es transversal.
