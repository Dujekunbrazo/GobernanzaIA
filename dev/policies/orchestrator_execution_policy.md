# Orchestrator Execution Policy (Hard)

Propósito:
- definir la gobernanza ejecutiva del orquestador como segunda pata canónica
  del sistema.

## 1) Rol ejecutivo

El orquestador es el sistema operativo de la gobernanza.

Su función es:

- abrir y cerrar sesiones
- calcular fase efectiva y siguiente paso permitido
- verificar precondiciones y gates mecánicos
- emitir `phase_ticket` y `resume_packet`
- controlar intentos, reentradas, excepciones y receipts
- preparar checkpoints y validación guiada cuando corresponda
- coordinar motores, no sustituirlos

## 2) Responsabilidades permitidas

El orquestador puede:

- inicializar runtime local
- renderizar prompts de fase
- lanzar fases contra el `motor_activo` o `motor_auditor`
- persistir estado operativo y receipts
- preparar `F8` y bootstrap de reentrada
- lanzar checkpoints laterales de `F6`
- reparar formato o metadata solo ante fallo mecánico trazado

## 3) Responsabilidades prohibidas

El orquestador no puede:

- redactar `ask.md`, `plan.md`, `execution.md`, `ask_audit.md`,
  `plan_audit.md`, `post_audit.md` o `real_validation.md`
- sustituir juicio técnico del `motor_auditor`
- inventar validación observable
- asumir memoria conversacional como continuidad válida
- reabrir alcance o replanificar por su cuenta

## 4) Runtime ejecutivo

El runtime del orquestador vive fuera del baseline exportable y fuera de los
artefactos sustantivos de iniciativa.

Su contenido típico incluye:

- sesiones
- prompts renderizados
- receipts
- `phase_tickets`
- `resume_packets`
- checkpoints
- estado de último intento y último error

## 5) Interfaz humana mínima

El usuario no necesita recordar comandos internos.

La interfaz humana mínima consiste en declarar:

- que la intención es de gobernanza
- el repo objetivo
- la iniciativa
- el `motor_activo` o `motor_auditor` cuando aplique
- la fase a abrir, continuar o rehidratar

## 6) Criterio de aceptabilidad

La gobernanza ejecutiva del orquestador se considera correcta cuando:

- el estado de fase no depende del chat
- toda reentrada queda rehidratada
- ningún motor recibe autorización ambigua
- el runtime operativo no contamina los artefactos sustantivos
- el usuario puede continuar una iniciativa desde una orden humana corta
