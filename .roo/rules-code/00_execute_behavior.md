# Code Mode Behavior (Implementación)

Objetivo: implementar cambios de forma segura siguiendo el SOP.

## Reglas obligatorias
1) Antes de tocar código, verifica si existe PLAN CONGELADO.
   - Debe estar en `dev/records/initiatives/<initiative_id>/plan.md` y marcado explícitamente como:
     "PLAN CONGELADO".
2) Si NO existe plan congelado:
   - NO implementes.
   - Pide al usuario completar `F4-F5` y congelar el plan.
3) Sigue estrictamente `dev/workflow.md` (`F6`).
4) Respeta `dev/guarantees/implementation_gate.md`.
5) Este modo no define un rol oficial de gobernanza; el rol válido es `motor_activo`.
6) Para código vivo, usa `symdex_search_code` y luego `symdex_read_code`.
7) Para dudas de workflow, gates, prompts o adapters, usa `governance_search`
   antes de cualquier lectura directa.
8) Declara herramienta usada y fuente canónica usada en cada respuesta
   técnica.
9) Si faltan MCPs activos, declara limitación operativa.
10) No uses iniciativas previas como fuente principal de proceso si existe
   fuente canónica.

## Commits
- 1 cambio lógico por commit (atómico).
- Prohibido refactor encubierto.
- Si algo no estaba en el plan: parar y escalar a Fase 4.

## Ejecución
- Aplica los cambios commit a commit.
- Tras cada commit: describe brevemente qué cambió y cómo validar.
- No modifiques documentación fuera del alcance autorizado de la iniciativa.
- Registra ejecución en `dev/records/initiatives/<initiative_id>/execution.md`.

## Salida esperada
- Commits ejecutados o bloqueados
- Para cada commit:
  - Archivos tocados
  - Resumen del cambio
  - Validación (comando/log esperado)
  - Herramienta y fuente canónica usadas
