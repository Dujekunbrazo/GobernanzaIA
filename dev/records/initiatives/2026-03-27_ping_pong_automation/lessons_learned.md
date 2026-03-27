# LESSONS LEARNED

- Initiative ID: 2026-03-27_ping_pong_automation
- Modo: M3
- Fecha: 2026-03-27
- motor_activo: codex
- motor_auditor:

## Resumen de la iniciativa

Se pudo traducir la conversacion de gobernanza a un autómata acotado sin tocar
runtime de producto, reutilizando prompts y templates canónicos ya presentes.

## Que funciono bien

1. Reusar `dev/prompts/` y `dev/templates/initiative/` redujo bastante la
   invencion de wiring.
2. Separar `init`, `approve-f2`, `status` y `advance` deja el flujo mas claro
   que un comando monolitico.

## Que no funciono

1. Los directorios temporales de pruebas dieron problemas de permisos en
   Windows y dejaron basura bloqueada en la raiz.

## Lecciones tecnicas

1. Para este tipo de automatizacion conviene mantener el contador de intentos
   en memoria por corrida y detenerse en el checkpoint humano, en lugar de
   inventar estado paralelo persistente.
2. El `preflight` exige la frase exacta de "excepción operativa" para aceptar
   worktree sucio.
3. La metadata `Rama` puede reservar la rama prevista desde `F1`, mientras que
   la materializacion real de la rama debe aplazarse a `F6` si asi lo exige el
   proceso.
4. Para multi-repo en Windows, la UX mejora mucho si el repo destino lo deduce
   un launcher desde `Iniciar en`, en lugar de obligar al usuario a recordar
   flags.

## Lecciones de proceso

1. La iteracion real por parejas de fases (`F1/F3`, `F4/F5`, `F6/F7`) era la
   especificacion clave; sin esa precision el script habria quedado demasiado
   lineal.

## Propuestas de cambio a gobernanza

1. Considerar una ruta oficial para scratch de tests operativos dentro del repo
   de gobernanza.

## Decision por propuesta

1. REVISAR_MAS_ADELANTE
