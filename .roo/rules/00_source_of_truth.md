# Source of Truth (Roo)

Regla única:
- La gobernanza oficial vive en `AGENTS.md` y `dev/workflow.md`.

Si hay diferencias entre `.roo` y esas fuentes, prevalecen `AGENTS.md` +
`dev/workflow.md` y `.roo` debe corregirse en el mismo cambio.

## Resumen operativo vigente

- Si el usuario no declara modo, iniciar en `M0`.
- No existen motores por defecto.
- El usuario designa `motor_activo` y, en `M4`, designa `motor_auditor` en `F2`.
- `Roo` puede actuar como motor general bajo el mismo contrato que el resto.
- Los modos nativos de Roo no sustituyen `M0-M4` ni `F1-F9`.
- Los modos nativos `Ask/Architect/Code/Debug/Orchestrator` son solo una capa
  de producto; nunca sustituyen el proceso oficial.
- Políticas transversales obligatorias:
  - `dev/policies/documentation_rules.md`
  - `dev/policies/scripts_rules.md`
  - `dev/policies/bitacora_rules.md`
  - `dev/policies/naming_rules.md`
  - `dev/policies/repo_layout_rules.md`
- Gates obligatorios:
  - `dev/guarantees/ask_gate.md`
  - `dev/guarantees/plan_gate.md`
  - `dev/guarantees/implementation_gate.md`
  - `dev/guarantees/docs_gate.md`

## Reglas mínimas no negociables

- No implementar sin `PLAN CONGELADO`.
- No planificar sin `ASK CONGELADO`.
- No se permite `PASS` con hallazgos pendientes.
- Solo los problemas materiales cuentan como `hallazgos`.
- Las `observaciones` no bloquean.
- Consulta de gobernanza -> `governance_search` y luego lectura canónica.
- Consulta de código -> `semantic_search` y luego `get_symbol` (via symdex_code).
- Si faltan MCPs activos, declarar limitación operativa antes de continuar.
- En respuestas técnicas, declarar herramienta usada y fuente canónica usada.
- `dev/records/initiatives/` no es fuente principal de proceso si existe fuente
  canónica en `dev/`.
- Si una auditoría formal (`F3`, `F5` o `F7`) va a ejecutarse en Roo, preguntar
  antes si el usuario desea cambiar de API/modelo.
- Si no hay confirmación explícita sobre mantener o cambiar la API/modelo para
  esa auditoría, estado = `BLOQUEADO`.
- Un cambio lógico por commit.
- `README.md` solo se actualiza de forma incremental.
- No inventar rutas/comandos/features.

## Autocheck MCP

Al inicio de sesión o tras recarga:

1. Comprobar si están disponibles `governance_search`,
   `semantic_search` y `get_symbol` (via symdex_code).
2. Si faltan, declararse limitado y no fingir gobernanza dinámica ni navegación
   de código por MCP.
3. Si están presentes, usarlos según el routing obligatorio.
4. Si Roo va a auditar en `F3`, `F5` o `F7`, preguntar si se mantiene o cambia
   la API/modelo antes de continuar.

## Python en Windows

Nunca ejecutar `python` a ciegas en Windows porque puede resolver al alias de
`WindowsApps`.

Orden obligatorio:
- Si existe `.venv\Scripts\python.exe`, usar ese ejecutable.
- Si no existe, usar `py -3`.
- Solo usar `python` cuando `python --version` funcione correctamente en la sesión.
