# Guia De Uso — `governance_ping_pong.py`

## Objetivo

Esta guia explica como usar el script
`scripts/dev/governance_ping_pong.py` para automatizar el ping-pong de una
iniciativa `M4` entre `Claude` y `Codex` sin tener que ir copiando prompts o
mensajes entre chats.

El objetivo del script no es sustituir la gobernanza. El objetivo es ejecutar
de forma automatizada las fases iterables del pipeline formal, manteniendo como
fuente de verdad los artefactos canónicos de la iniciativa.

## Que automatiza y que no

Automatiza:

- `F1 <-> F3`
- `F4 <-> F5`
- `F6 <-> F7`

No automatiza:

- `F2` porque es checkpoint manual del usuario
- `F8` porque es validación real guiada del usuario
- `F9/F10` porque quedan fuera de este primer alcance

## Idea mental correcta

El script no conecta dos chats entre sí.

Lo que hace es:

1. usar `Claude` CLI como `motor_activo`
2. usar `Codex` CLI como `motor_auditor`
3. hacer que ambos lean y escriban sobre los mismos artefactos dentro de
   `dev/records/initiatives/<initiative_id>/`
4. parar cuando toca una decisión humana o cuando una fase supera el número
   máximo de reintentos

## Flujo general

El flujo operativo es este:

1. crear la iniciativa `M4`
2. preparar `handoff.md` si aplica
3. lanzar el primer `advance`
4. revisar `ask.md` en `F2`
5. aprobar `F2`
6. relanzar `advance`
7. dejar que el script itere automáticamente hasta `F8` o bloqueo
8. ejecutar tú `F8`
9. si `F8` reabre `F6`, relanzar `advance`

## Mapa de fases

### `F1 <-> F3`

- `Claude` escribe o corrige `ask.md`
- `Codex` audita en `ask_audit.md`
- si `FAIL`, vuelve a `Claude`
- si `PASS`, `ask.md` queda `CONGELADO`

### `F4 <-> F5`

- `Claude` escribe o corrige `plan.md`
- `Codex` audita en `plan_audit.md`
- si `FAIL`, vuelve a `Claude`
- si `PASS`, `plan.md` queda `CONGELADO`

### `F6 <-> F7`

- el script crea o activa la rama de iniciativa
- ejecuta preflight
- `Claude` implementa y actualiza `execution.md`
- `Codex` audita en `post_audit.md`
- si `FAIL`, vuelve a `Claude`
- si `PASS`, el script se detiene en `WAITING_FOR_F8`

## Requisitos previos

Antes de usar el script necesitas:

- estar en la raiz del repo
- tener `claude` disponible en terminal
- tener `codex` disponible en terminal
- tener permisos para editar el repo
- tener claro un `initiative_id` válido

Formato esperado para `initiative_id`:

- `YYYY-MM-DD_tema_corto`
- ejemplo: `2026-03-27_demo`

## Cómo arrancar `Claude` y `Codex` en terminal

Esta sección responde a una duda muy concreta: cómo comprobar que ambos CLIs
están listos y cómo arrancarlos manualmente.

### Importante

Para usar `governance_ping_pong.py` no necesitas mantener dos terminales
abiertas con `Claude` y `Codex` corriendo al mismo tiempo.

El script los lanza por dentro cuando toca:

- usa `claude -p` para el trabajo no interactivo de `Claude`
- usa `codex exec` para el trabajo no interactivo de `Codex`

Lo que sí necesitas es:

- que ambos comandos existan
- que ambos estén autenticados

### Paso 1: abrir una terminal en la raíz del repo

En VS Code:

1. abre el repo `GobernanzaIA`
2. abre `Terminal -> New Terminal`
3. comprueba que estés en la raíz del repo

Deberías ver algo equivalente a:

```powershell
PS C:\Users\Jorge Ferrer\Documents\GobernanzaIA>
```

### Paso 2: comprobar que `Claude` existe

Ejecuta:

```bash
claude --version
```

Si todo va bien, verás una versión parecida a:

```text
2.1.76 (Claude Code)
```

Si no existe el comando, el problema no es el script: primero tienes que tener
`Claude Code` disponible en tu sistema.

### Paso 3: comprobar que `Codex` existe

Ejecuta:

```bash
codex --version
```

Si todo va bien, verás algo parecido a:

```text
codex-cli 0.117.0-alpha.24
```

Si no existe el comando, primero tienes que tener `codex` instalado y visible
en `PATH`.

### Windows: si `codex` no entra por `PATH`

En algunos entornos Windows, `codex` está instalado dentro de la extensión de
VS Code pero no queda disponible como comando corto en PowerShell.

En ese caso, puedes lanzarlo por ruta completa.

Ejemplo real:

```powershell
& "C:\Users\Jorge Ferrer\.vscode\extensions\openai.chatgpt-26.325.21211-win32-x64\bin\windows-x86_64\codex.exe" --version
```

Si eso funciona, el problema no es `codex`: el problema es solo `PATH`.

#### Opción A: usar siempre la ruta completa

```powershell
& "C:\Users\Jorge Ferrer\.vscode\extensions\openai.chatgpt-26.325.21211-win32-x64\bin\windows-x86_64\codex.exe" exec "explica este repo"
```

#### Opción B: añadirlo al `PATH` solo en esa terminal

```powershell
$env:PATH += ";C:\Users\Jorge Ferrer\.vscode\extensions\openai.chatgpt-26.325.21211-win32-x64\bin\windows-x86_64"
codex --version
```

Esto solo afecta a la terminal actual.

#### Opción C: crear un alias temporal en PowerShell

```powershell
Set-Alias codex "C:\Users\Jorge Ferrer\.vscode\extensions\openai.chatgpt-26.325.21211-win32-x64\bin\windows-x86_64\codex.exe"
codex --version
```

Esto también aplica solo a la sesión actual.

### Paso 4: comprobar login de `Claude`

Ejecuta:

```bash
claude auth status
```

Si no estás autenticado, inicia sesión con:

```bash
claude auth login
```

Esto abre el flujo de login de tu cuenta Anthropic.

### Paso 5: comprobar login de `Codex`

Ejecuta:

```bash
codex login status
```

Si no estás autenticado, puedes iniciar sesión con:

```bash
codex login
```

Si en tu entorno necesitas forzar flujo por dispositivo:

```bash
codex login --device-auth
```

Si usas API key en otro contexto, existe también:

```bash
codex login --with-api-key
```

Pero para tu caso normal con cuenta interactiva, lo habitual es `codex login`
o `codex login --device-auth`.

Si `codex` no entra por `PATH`, sustituye `codex` por la ruta completa o por el
alias temporal que hayas creado antes.

Ejemplo:

```powershell
& "C:\Users\Jorge Ferrer\.vscode\extensions\openai.chatgpt-26.325.21211-win32-x64\bin\windows-x86_64\codex.exe" login --device-auth
```

### Paso 6: comprobar que ambos responden de forma básica

Una vez logados, puedes hacer una comprobación rápida:

```bash
claude --help
codex --help
```

Si ambos responden, ya están listos para que el script los invoque.

### Paso 7: arrancarlos manualmente, si quieres usarlos tú fuera del script

Esto es opcional. Sirve solo si quieres hablar manualmente con ellos desde la
terminal.

#### Claude interactivo

```bash
claude
```

O con un prompt directo:

```bash
claude "resume este repo"
```

#### Codex interactivo

```bash
codex
```

O con ejecución puntual:

```bash
codex exec "explica este repositorio"
```

### Paso 8: entender qué pasa cuando usas el script

Cuando ejecutas:

```bash
python scripts/dev/governance_ping_pong.py advance --initiative-id 2026-03-27_demo
```

el script no espera que tú tengas `Claude` y `Codex` abiertos a mano.

Lo que hace internamente es:

1. construir el prompt de fase
2. lanzar `Claude` o `Codex`
3. dejar que escriban sobre los artefactos del repo
4. leer el resultado
5. decidir si avanza, itera o se bloquea

### Paso 9: secuencia mínima recomendada para comprobar entorno

Si quieres una rutina simple antes de usar el script, esta es la buena:

```bash
claude --version
codex --version
claude auth status
codex login status
python scripts/dev/governance_ping_pong.py status --initiative-id 2026-03-27_demo
python scripts/dev/governance_ping_pong.py advance --initiative-id 2026-03-27_demo --dry-run
```

### Fallos típicos en este punto

#### `claude` no se reconoce

El sistema no encuentra `Claude Code`. No es un problema del script.

#### `codex` no se reconoce

El sistema no encuentra `codex`. No es un problema del script.

En Windows, primero prueba la ruta completa del `codex.exe` que instala la
extensión de VS Code.

#### `auth status` dice que no estás logado

Tienes que autenticarte primero antes de usar `advance`.

#### El script falla aunque los comandos existen

Suele significar una de estas cosas:

- falta login
- hay permisos insuficientes
- el artefacto de iniciativa no existe
- el `initiative_id` no coincide
- el preflight de `F6` está bloqueando

## Dónde vive todo

Script:

- `scripts/dev/governance_ping_pong.py`
- `scripts/dev/governance_ping_pong_launcher.bat`

Artefactos reales de una iniciativa:

- `dev/records/initiatives/<initiative_id>/ask.md`
- `dev/records/initiatives/<initiative_id>/ask_audit.md`
- `dev/records/initiatives/<initiative_id>/plan.md`
- `dev/records/initiatives/<initiative_id>/plan_audit.md`
- `dev/records/initiatives/<initiative_id>/execution.md`
- `dev/records/initiatives/<initiative_id>/post_audit.md`
- `dev/records/initiatives/<initiative_id>/closeout.md`
- `dev/records/initiatives/<initiative_id>/lessons_learned.md`

Opcionales:

- `dev/records/initiatives/<initiative_id>/handoff.md`
- `dev/records/initiatives/<initiative_id>/real_validation.md`

No debes trabajar en carpetas temporales de test como:

- `.tmp_governance_ping_pong_tests/`

## Launcher `.bat` para Windows

Si trabajas con varios repos en paralelo y no quieres escribir comandos a mano,
la forma recomendada en Windows es usar:

- `scripts/dev/governance_ping_pong_launcher.bat`

### Qué hace el launcher

- toma como repo destino la carpeta desde la que se lanza
- llama al script Python por debajo con ese repo ya resuelto
- detecta `claude`
- intenta encontrar `codex` aunque no este en `PATH`
- te enseña un menu para:
  - listar iniciativas
  - ver `status`
  - hacer `advance`
  - hacer `advance --dry-run`
  - hacer `approve-f2`
  - hacer `init`

### Cómo usarlo bien con varios repos

La idea buena es crear un acceso directo por repo.

Ejemplo:

- acceso directo `PingPong Kiminio`
- acceso directo `PingPong McpBoletines`

Ambos apuntan al mismo `.bat`, pero cada acceso directo tiene un `Iniciar en`
distinto.

### Configuración recomendada del acceso directo

#### Destino

```text
C:\Users\Jorge Ferrer\Documents\GobernanzaIA\scripts\dev\governance_ping_pong_launcher.bat
```

#### Iniciar en

Para Kiminio:

```text
C:\Users\Jorge Ferrer\Documents\Kiminio
```

Para McpBoletines:

```text
C:\Users\Jorge Ferrer\Documents\McpBoletines
```

Con eso, el launcher entiende automaticamente contra que repo debe trabajar.

## Concepto de rama prevista vs rama real

Esta distinción es importante.

### Rama prevista

Desde `F1`, los artefactos guardan una metadata `Rama:` con la rama prevista
de la iniciativa. Por ejemplo:

- `initiative/2026-03-27-demo`

Esto sirve para que `ask.md` y `plan.md` tengan clara la identidad operativa de
la iniciativa incluso antes de implementar.

### Rama real

La rama Git no se crea ni se activa en `init`.

La rama se crea o se activa solo al entrar en `F6`:

- si la rama ya existe: `git checkout <rama>`
- si la rama no existe: `git checkout -b <rama>`

Esto permite reservar la rama desde `F1-F5` sin materializarla antes de tiempo.

## Comandos disponibles

El script tiene cuatro subcomandos:

- `init`
- `approve-f2`
- `status`
- `advance`

## 1. `init`

Sirve para crear el esqueleto de la iniciativa `M4`.

Ejemplo mínimo:

```bash
python scripts/dev/governance_ping_pong.py init --initiative-id 2026-03-27_demo
```

Ejemplo habitual con handoff:

```bash
python scripts/dev/governance_ping_pong.py init --initiative-id 2026-03-27_demo --with-handoff
```

Ejemplo más completo:

```bash
python scripts/dev/governance_ping_pong.py init ^
  --initiative-id 2026-03-27_demo ^
  --motor-activo claude ^
  --motor-auditor codex ^
  --with-handoff ^
  --summary "Automatizar pipeline M4 entre Claude y Codex"
```

### Qué hace `init`

- crea la carpeta de iniciativa
- copia los templates canónicos
- rellena metadata base
- deja `ask.md` en `PROPUESTO`
- deja `plan.md` en `PROPUESTO`
- reserva la rama prevista en `Rama:`

### Qué no hace `init`

- no ejecuta `Claude`
- no ejecuta `Codex`
- no crea la rama Git real
- no valida `F2`

### Flags útiles de `init`

- `--initiative-id`: obligatorio
- `--motor-activo`: por defecto `claude`
- `--motor-auditor`: por defecto `codex`
- `--baseline-mit`: por defecto `MIT Concept-Sync`
- `--branch`: fuerza la rama prevista en metadata
- `--summary`: inyecta un resumen inicial en `ask.md`
- `--with-handoff`: crea `handoff.md`
- `--with-real-validation`: crea `real_validation.md`
- `--force`: permite regenerar si la iniciativa ya existe

## 2. Qué haces tú después de `init`

Tienes dos caminos.

### Camino A: con `handoff.md`

1. creas la iniciativa con `--with-handoff`
2. editas `handoff.md`
3. lanzas `advance`

Este es el camino recomendado cuando vienes de conversación previa o de un
análisis ya razonado.

### Camino B: sin `handoff.md`

1. creas la iniciativa sin handoff
2. lanzas `advance`
3. `Claude` intenta construir `ask.md` con el contexto disponible

## 3. `status`

Sirve para saber en qué punto estás y cuál es el siguiente paso esperado.

Ejemplo:

```bash
python scripts/dev/governance_ping_pong.py status --initiative-id 2026-03-27_demo
```

Salida típica:

```text
initiative_id=2026-03-27_demo
ask_state=PROPUESTO
ask_audit=<empty>
plan_state=<empty>
plan_audit=<empty>
post_audit=<empty>
next_step=WAITING_FOR_F2
```

### Significado de `next_step`

- `RUN_F1`: falta Ask útil
- `WAITING_FOR_F2`: el usuario debe revisar/validar `ask.md`
- `RUN_F3`: toca auditoría Ask
- `RUN_F1_F3_REMEDIATION`: hubo `FAIL` en `F3`
- `RUN_F4`: toca preparar plan
- `RUN_F5`: toca auditoría Plan
- `RUN_F4_F5_REMEDIATION`: hubo `FAIL` en `F5`
- `RUN_F6_F7`: toca implementación/post-auditoría
- `WAITING_FOR_F8`: la implementación quedó lista para tu validación real

## 4. `advance`

Es el comando principal. Avanza automáticamente hasta el siguiente checkpoint
humano o hasta bloqueo por exceso de fallos.

Ejemplo base:

```bash
python scripts/dev/governance_ping_pong.py advance --initiative-id 2026-03-27_demo
```

Ejemplo seguro en seco:

```bash
python scripts/dev/governance_ping_pong.py advance --initiative-id 2026-03-27_demo --dry-run
```

Ejemplo con excepción operativa de worktree sucio:

```bash
python scripts/dev/governance_ping_pong.py advance --initiative-id 2026-03-27_demo --allow-dirty-with-ask-exception
```

### Qué hace `advance`

Dependiendo del estado actual:

- si falta contenido real en `ask.md`, intenta `F1`
- si `ask.md` está `PROPUESTO`, se detiene en `F2`
- si `ask.md` está `VALIDADO`, arranca el bucle `F1 <-> F3`
- si `ask.md` queda `CONGELADO`, arranca el bucle `F4 <-> F5`
- si `plan.md` queda `CONGELADO`, entra a `F6 <-> F7`
- si `post_audit.md` da `PASS`, se detiene en `WAITING_FOR_F8`

### Límite de reintentos

Por defecto cada fase auditada admite hasta `3` intentos:

- `1` intento inicial
- `2` reintentos

Puedes cambiarlo con:

```bash
python scripts/dev/governance_ping_pong.py advance --initiative-id 2026-03-27_demo --max-audits 3
```

Si se agotan los intentos:

- `BLOCKED_AFTER_F3`
- `BLOCKED_AFTER_F5`
- `BLOCKED_AFTER_F7`

## 5. `approve-f2`

Este es tu checkpoint manual.

Cuando `advance` deja la iniciativa en `WAITING_FOR_F2`, abres:

- `ask.md`

Revisas alcance, supuestos y preguntas. Si está bien, apruebas:

```bash
python scripts/dev/governance_ping_pong.py approve-f2 --initiative-id 2026-03-27_demo --motor-auditor codex
```

### Qué hace `approve-f2`

- comprueba que `ask.md` tenga contenido mínimo real
- cambia `Estado: VALIDADO`
- fija `motor_auditor`

Después relanzas:

```bash
python scripts/dev/governance_ping_pong.py advance --initiative-id 2026-03-27_demo
```

## Ejemplo completo de punta a punta

### Caso

Quieres abrir una iniciativa `M4` para automatizar un cambio mediano y usar:

- `Claude` como `motor_activo`
- `Codex` como `motor_auditor`

### Paso 1: crear iniciativa

```bash
python scripts/dev/governance_ping_pong.py init --initiative-id 2026-03-27_demo --with-handoff
```

### Paso 2: escribir handoff

Editas:

- `dev/records/initiatives/2026-03-27_demo/handoff.md`

Ahí dejas:

- contexto
- alcance
- riesgos
- supuestos
- restricciones

### Paso 3: primer avance

```bash
python scripts/dev/governance_ping_pong.py advance --initiative-id 2026-03-27_demo
```

Comportamiento esperado:

- `Claude` trabaja `F1`
- el script detecta que `ask.md` quedó en `PROPUESTO`
- el script responde `WAITING_FOR_F2`

### Paso 4: revisar `F2`

Abres:

- `dev/records/initiatives/2026-03-27_demo/ask.md`

Compruebas:

- objetivo
- evidencia
- supuestos
- preguntas
- trade-offs

### Paso 5: aprobar `F2`

```bash
python scripts/dev/governance_ping_pong.py approve-f2 --initiative-id 2026-03-27_demo --motor-auditor codex
```

### Paso 6: relanzar automatización

```bash
python scripts/dev/governance_ping_pong.py advance --initiative-id 2026-03-27_demo
```

Ahora el script hace:

- `F3`: Codex audita `ask.md`
- si `FAIL`, Claude corrige `ask.md`
- cuando `PASS`, congela `ask.md`
- `F4`: Claude propone `plan.md`
- `F5`: Codex audita `plan.md`
- si `FAIL`, Claude corrige `plan.md`
- cuando `PASS`, congela `plan.md`
- al entrar en `F6`, crea o activa la rama `initiative/...`
- ejecuta preflight
- Claude implementa
- Codex audita en `F7`
- si `PASS`, responde `WAITING_FOR_F8`

### Paso 7: ejecutar `F8`

Cuando veas:

```text
WAITING_FOR_F8
```

entras tú.

Abres:

- `dev/records/initiatives/2026-03-27_demo/real_validation.md`

Y decides:

- `APTA_PARA_F9`
- `REABRIR_F6`
- `NO_APLICA`

### Paso 8: si `F8` reabre implementación

Si decides `REABRIR_F6`, simplemente vuelves a ejecutar:

```bash
python scripts/dev/governance_ping_pong.py advance --initiative-id 2026-03-27_demo
```

## Cómo sabe el script qué hacer

El script no usa una base de datos externa ni estado paralelo complejo.

Decide el siguiente paso leyendo:

- `Estado:` de `ask.md`
- `Estado:` de `plan.md`
- `Veredicto:` de `ask_audit.md`
- `Veredicto:` de `plan_audit.md`
- `Veredicto:` de `post_audit.md`
- si hay contenido real dentro de `ask.md`, `plan.md` y `execution.md`

Esto es importante porque el estado real vive en los artefactos, no en memoria
de chat.

## Cómo invoca a Claude y Codex

### Claude

`Claude` se usa como proceso no interactivo:

- `claude -p`

El script le pasa prompts construidos para:

- `F1`
- remediación de `F3`
- `F4`
- remediación de `F5`
- `F6`
- remediación de `F7`

### Codex

`Codex` se usa como proceso no interactivo:

- `codex exec`

El script lo usa para:

- auditoría de `F3`
- auditoría de `F5`
- post-auditoría de `F7`

## Cómo trata la rama

### En `F1-F5`

No toca tu rama Git actual.

Solo deja escrita la rama prevista en metadata:

- `Rama: initiative/2026-03-27-demo`

### En `F6`

Hace esto:

1. lee la rama prevista
2. comprueba tu rama actual
3. si ya estás en la rama prevista, no hace nada
4. si no estás:
   - si la rama existe, hace `git checkout <rama>`
   - si no existe, hace `git checkout -b <rama>`

## Cómo usar `dry-run`

`dry-run` es la forma segura de inspeccionar el flujo antes de ejecutar cambios
reales.

Ejemplo:

```bash
python scripts/dev/governance_ping_pong.py advance --initiative-id 2026-03-27_demo --dry-run
```

Con `dry-run`:

- no se lanza `Claude`
- no se lanza `Codex`
- no se cambia de rama
- no se implementa código
- el script imprime qué haría

Úsalo siempre la primera vez que abras una iniciativa nueva.

## Excepción operativa por worktree sucio

En `F6`, el script ejecuta:

- `scripts/dev/initiative_preflight.py`

Si tu worktree está sucio, el preflight bloqueará salvo que:

1. `ask.md` incluya la justificación de "excepción operativa" con referencia a
   worktree sucio
2. lances `advance` con:

```bash
python scripts/dev/governance_ping_pong.py advance --initiative-id 2026-03-27_demo --allow-dirty-with-ask-exception
```

## Situaciones típicas

### Quiero ver dónde estoy

```bash
python scripts/dev/governance_ping_pong.py status --initiative-id 2026-03-27_demo
```

### Quiero preparar la iniciativa pero no ejecutar todavía

```bash
python scripts/dev/governance_ping_pong.py init --initiative-id 2026-03-27_demo --with-handoff
```

### Quiero revisar el flujo antes de lanzar nada real

```bash
python scripts/dev/governance_ping_pong.py advance --initiative-id 2026-03-27_demo --dry-run
```

### El script se paró en `WAITING_FOR_F2`

Abre `ask.md`, revisa y luego:

```bash
python scripts/dev/governance_ping_pong.py approve-f2 --initiative-id 2026-03-27_demo --motor-auditor codex
```

### El script se paró en `WAITING_FOR_F8`

Haz tú `F8`.

### El script se paró en `BLOCKED_AFTER_F3`

Has agotado intentos de auditoría Ask. Tienes que intervenir tú.

### El script se paró en `BLOCKED_AFTER_F5`

Has agotado intentos de auditoría Plan. Tienes que intervenir tú.

### El script se paró en `BLOCKED_AFTER_F7`

Has agotado intentos de post-auditoría. Tienes que intervenir tú.

## Buenas prácticas

- usa `--with-handoff` cuando vienes de conversación larga
- usa `status` antes de asumir en qué fase estás
- usa `--dry-run` la primera vez
- no trabajes sobre carpetas de test temporales
- deja `F2` y `F8` como checkpoints humanos reales
- no uses el script para saltarte la gobernanza; úsalo para ejecutarla mejor

## Limitaciones actuales

- no automatiza `F9/F10`
- no persiste un historial complejo de iteraciones fuera de los artefactos
- depende de que `Claude` y `Codex` estén disponibles por CLI
- si el entorno Git/ACL de Windows está raro, la parte de branch checkout puede
  requerir intervención manual

## Checklist de uso rápido

1. `init`
2. preparar `handoff.md` si aplica
3. `advance`
4. revisar `F2`
5. `approve-f2`
6. `advance`
7. esperar `WAITING_FOR_F8`
8. hacer `F8`
9. si reabre `F6`, volver a `advance`

## Referencias

- `scripts/dev/governance_ping_pong.py`
- `scripts/dev/README.md`
- `dev/workflow.md`
- `AGENTS.md`
- `dev/templates/initiative/`
- `dev/prompts/`
