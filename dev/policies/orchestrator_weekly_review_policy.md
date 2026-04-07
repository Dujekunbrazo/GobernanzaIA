# Policy: Orchestrator Weekly Review

## Objetivo

Definir como el orquestador debe ejecutar la review semanal canonica sin
confundirla con una iniciativa `M4`.

## Responsabilidades del orquestador

El orquestador debe poder:

- preparar el arbol de artefactos semanales
- generar `weekly_briefing.md`
- renderizar el prompt semanal canonico
- lanzar la review contra el motor designado
- persistir receipts y estado operativo local
- preparar remediaciones supervisadas cuando el usuario las apruebe

## Responsabilidades prohibidas

El orquestador no puede:

- redactar el contenido sustantivo del `weekly_review.md`
- inventar findings sin respaldo del motor revisor
- abrir `M4` sin aprobacion humana explicita

## Modos operativos esperados

- `BASELINE_INICIAL_MIT`
- `DELTA_SEMANAL_MIT`
- preparacion de remediacion supervisada

## Criterio de aceptabilidad

La integracion ejecutiva es correcta cuando:

- la weekly review usa el stack de contexto canonico
- deja runtime y receipts fuera de los artefactos sustantivos
- puede preparar remediacion sin saltarse la aprobacion humana
