# Governance Starter

Base reutilizable para aplicar esta gobernanza multi-IA en un repo nuevo.

## Comando principal

```bash
python scripts/migration/bootstrap_governance.py --target <ruta_repo_destino>
```

Ejemplo Windows:

```bash
python scripts/migration/bootstrap_governance.py --target "C:\Users\Jorge Ferrer\Documents\MiNuevoProyecto"
```

## Opciones

- `--dry-run`: simula copia sin escribir archivos.
- `--force`: sobrescribe archivos existentes en destino.
- `--skip-claude-root`: no copia `CLAUDE.md` en raíz.

## Qué instala

- Contrato y workflow: `AGENTS.md`, `dev/workflow.md`
- Gates: `dev/guarantees/*.md`
- Políticas: `dev/policies/*.md`
- Adaptadores: `dev/ai/adapters/*.md`
- Plantillas de iniciativa: `dev/templates/initiative/*.md`
- Bitácora base: `dev/records/bitacora/*`, `dev/records/initiatives/.gitkeep`
- Validadores/scripts clave: `scripts/ops/bitacora_append.py`, `scripts/dev/check_naming_compliance.py`, `scripts/dev/check_state0.py`
