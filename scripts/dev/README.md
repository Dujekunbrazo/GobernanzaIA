# Development Scripts

## check_dr1_imports.py

Verifica que los conceptos no se importen entre sí (Design Rule 1 del MIT).

```bash
python scripts/dev/check_dr1_imports.py
```

**DR1**: Ningún archivo en `core/concepts/` puede importar de otro concept.

Ejemplo de violación:

```python
# ❌ VIOLACIÓN: core/concepts/memory/dual_memory.py
from core.concepts.grounding import IntentCompiler  # Importa otro concept
```

Ejemplo correcto:

```python
# ✅ BIEN: core/concepts/memory/dual_memory.py
from core.contracts.events import EventEnvelope  # Solo contracts permitidos
```

## check_capability_closure.py

Valida `capability_closure.md` de una iniciativa.

```bash
python scripts/dev/check_capability_closure.py --initiative-id 2026-03-26_demo
```

Usa `--required` si la initiative debe tener ese artefacto.

## check_bitacora_compliance.py

Valida que exista evidencia de bitácora para una IA o una iniciativa.

```bash
python scripts/dev/check_bitacora_compliance.py --initiative-id 2026-03-26_demo
```

Filtrando por IA y fase:

```bash
python scripts/dev/check_bitacora_compliance.py --ia codex --initiative-id 2026-03-26_demo --phase F9
```

## check_exception_record.py

Valida `exception_record.md` de una iniciativa.

```bash
python scripts/dev/check_exception_record.py --initiative-id 2026-03-26_demo
```

Usa `--required` si la initiative declara excepción formal.

## initiative_preflight.py

Hace preflight de una iniciativa formal antes de implementar o cerrar.

```bash
python scripts/dev/initiative_preflight.py --initiative-id 2026-03-26_demo --mode M3
```

Si el worktree está sucio pero hay excepción explícita en `ask.md`:

```bash
python scripts/dev/initiative_preflight.py --initiative-id 2026-03-26_demo --mode M3 --allow-dirty-with-ask-exception
```

## governance_ping_pong.py

Orquesta el ping-pong `M4` entre `Claude` y `Codex` hasta el siguiente
checkpoint humano.

Subcomandos:

- `init`: crea los artefactos canonicos de una iniciativa `M4`
- `approve-f2`: registra el checkpoint manual de `F2`
- `status`: muestra el estado resumido y el siguiente paso
- `advance`: automatiza `F1 <-> F3`, `F4 <-> F5` y `F6 <-> F7`

Uso recomendado:

```bash
python scripts/dev/governance_ping_pong.py init --initiative-id 2026-03-27_demo --with-handoff
python scripts/dev/governance_ping_pong.py advance --initiative-id 2026-03-27_demo
python scripts/dev/governance_ping_pong.py approve-f2 --initiative-id 2026-03-27_demo --motor-auditor codex
python scripts/dev/governance_ping_pong.py advance --initiative-id 2026-03-27_demo
```

Notas:

- `advance` se detiene en `F2`, en `F8` o cuando una fase auditada acumula
  `3` intentos fallidos en la misma corrida.
- `F2` y `F8` siguen siendo checkpoints manuales del usuario.
- `F1-F5` guardan en `Rama` la rama prevista de la iniciativa.
- Al entrar en `F6`, el script crea o cambia a esa rama prevista y luego
  ejecuta `initiative_preflight.py`.

## governance_ping_pong_launcher.bat

Lanzador interactivo para Windows del ping-pong de gobernanza.

Uso recomendado:

- crea un acceso directo por repo consumidor
- en el acceso directo, apunta a este `.bat`
- en `Iniciar en`, pon la carpeta del repo destino

El launcher:

- detecta el repo destino desde la carpeta de arranque
- intenta localizar `codex` aunque no este en `PATH`
- lista iniciativas del repo destino
- permite `init`, `status`, `approve-f2`, `advance` y `advance --dry-run`

Uso recomendado:

- usar el launcher contra repos consumidores
- evitar poblar `dev/records/initiatives/` en `GobernanzaIA`

## governance_orchestrator.py

Orquestador canónico por fases y capa ejecutiva de la gobernanza.

No redacta artefactos sustantivos de iniciativa.
Coordina:

- sesión y fase vigente
- continuidad operativa
- `phase_ticket` y `resume_packet`
- checkpoints de `F6`
- preparación de `F8`
- receipts e intentos

Los motores siguen siendo responsables de escribir los artefactos de fase.

Uso base:

```bash
python scripts/dev/governance_orchestrator.py --target-repo <repo> --initiative-id 2026-03-28_demo init-session
python scripts/dev/governance_orchestrator.py --target-repo <repo> --initiative-id 2026-03-28_demo next-step
python scripts/dev/governance_orchestrator.py --target-repo <repo> --initiative-id 2026-03-28_demo run-current-step
```

Puntos clave:

- crea `.orchestrator_local/` en primer uso
- guarda runtime local fuera del baseline exportable
- trabaja una fase por comando
- no depende de memoria conversacional para reentrada
- usa prompts `01-07` y prompts de remediación `13/15/17`
- mantiene `F2` y `F8` como checkpoints humanos
