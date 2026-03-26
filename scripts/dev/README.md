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
python scripts/dev/check_bitacora_compliance.py --ia codex --initiative-id 2026-03-26_demo --phase F8
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
