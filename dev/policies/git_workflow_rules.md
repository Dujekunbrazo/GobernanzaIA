# Git Workflow Rules (Hard)

Estas reglas definen la operativa obligatoria de Git/GitHub para trabajo con IA.

## 1) Rama activa obligatoria

- Antes de cualquier modificación, verificar rama activa.
- Prohibido trabajar directamente en `main` o `master`.
- Si la rama activa es `main/master`, crear rama de trabajo antes de continuar.

## 2) Nomenclatura de rama por tipo de tarea

Prefijos obligatorios:
- `feature/` -> nueva funcionalidad
- `refactor/` -> reestructuración sin cambio de comportamiento
- `fix/` -> corrección de bug
- `hotfix/` -> bug urgente en producción
- `chore/` -> mantenimiento, dependencias o configuración
- `initiative/` -> trabajo ligado a `dev/records/initiatives/`

Formato:
- `<prefijo>/<fecha>_<descripcion-corta>`

Ejemplo:
- `refactor/2026-02-26_context-recovery`

## 3) Commits atómicos y descriptivos

- Cada commit representa una sola unidad lógica de cambio.
- Mensaje obligatorio:
  - `<tipo>(<scope>): <descripcion en infinitivo>`
- Tipos válidos:
  - `feat` | `fix` | `refactor` | `chore` | `docs` | `test`

Prohibido:
- mensajes genéricos (`cambios`, `fix`, `wip`)
- mezclar `refactor` + `feature` en el mismo commit

## 4) Rama protegida en solo lectura para la IA

- Prohibido `git push origin main` y `git push origin master`.
- La rama protegida recibe cambios solo mediante PR o merge desde rama de trabajo.

Antes de merge:
- `git status` en clean working tree
- tests relevantes en código de salida `0`
- rama sincronizada con troncal (`git fetch` + `git rebase origin/main` o equivalente)

## 5) Push como checkpoint operativo

- Hacer push de la rama de trabajo al finalizar cada sesión o bloque lógico.
- Objetivo: backup y recuperación ante corte de contexto/sesión.

Comando típico:
- `git push origin <rama-actual>`

## 6) Sincronización con iniciativas

Si el trabajo está ligado a `dev/records/initiatives/<initiative_id>/`:
- la rama debe usar prefijo `initiative/`
- el slug de rama debe coincidir con la initiative (con separadores válidos)

Ejemplo:
- Initiative: `2026-02-26_context_recovery`
- Rama: `initiative/2026-02-26_context-recovery`

## 7) Límite de contexto y handoff de sesión

Si una sesión supera:
- 10 archivos modificados, o
- 15 commits

Se debe iniciar nueva sesión con handoff mínimo:
- rama activa
- último commit completado
- próximo commit pendiente
- archivos en staging

## 8) Cierre de rama e informe

Al finalizar una rama:
1. Completar auditoría/post-auditoría de la iniciativa.
2. Merge por PR o estrategia aprobada de squash merge.
3. Borrar rama local/remota cuando el merge esté confirmado.
4. Registrar resultado en artefactos de iniciativa (`closeout.md` y `lessons_learned.md`).
5. Generar commit formal de cierre al terminar `F9`, incluyendo como mínimo:
   - `closeout.md`
   - `lessons_learned.md`

## 9) Apertura de nuevas iniciativas con working tree limpio

- Prohibido abrir una nueva iniciativa formal (`M3` o `M4`) sobre working tree
  con cambios sin commit pertenecientes a otra iniciativa.
- Si existe restricción técnica real, registrar excepción explícita en el `ask.md`
  y luego en `execution.md` o `closeout.md` con justificación.

## 10) Excepciones

Si no hay remoto disponible o hay restricción de permisos:
- registrar la excepción en `execution.md` o `closeout.md`
- no inventar comandos no ejecutados

## 11) Protocolo anti-bucle para cierre Git (`F8/F9`)

Objetivo:
- evitar iteraciones largas de `git add/commit/push` en entornos con ACL
  restrictiva o sandbox.

Preflight obligatorio de cierre (antes del primer `git add`):
- pedir ejecución con permisos efectivos para escribir en `.git` cuando el
  entorno ya tenga historial de `Permission denied` o bloqueo por sandbox.
- no iniciar staging de cierre en contexto sin permisos efectivos.

Secuencia obligatoria de cierre:
1. ejecutar bitácora de cierre (`scripts/ops/bitacora_append.py`) antes del
   commit final para que quede incluida en el mismo bloque de cierre.
2. staging de artefactos de cierre.
3. commit formal de cierre.
4. push de checkpoint remoto.
5. verificación final de working tree limpio.

Regla de reintentos:
- ante el primer `Permission denied` en `git add`, `git commit` o `git push`,
  no repetir el mismo comando en el mismo contexto.
- cambiar inmediatamente a ejecución con permisos efectivos (confirmación del
  operador si aplica).
- tras elevar permisos, se permite como máximo un pase de remediación ACL
  (`takeown`/`icacls`) y un único reintento de la secuencia de cierre.
- si persiste el fallo, no iterar en bucle: documentar incidencia en
  `closeout.md` y escalar ejecución manual al operador con comandos concretos.
