# Scripts

Estructura oficial:

- `scripts/dev/`: utilidades de desarrollo local
- `scripts/ops/`: scripts operativos y soporte
- `scripts/migration/`: migraciones puntuales

Reglas:
- La ruta canónica se define por categoría.
- No dejar scripts nuevos sueltos en `scripts/` (excepto wrappers de compatibilidad).
- Los scripts deben resolver paths contra el repo y no depender del `cwd`.

## Scripts operativos actuales

### Bitacora diaria por IA

Ruta canónica:
- `scripts/ops/bitacora_append.py`

Wrapper de compatibilidad:
- `scripts/bitacora_append.py`

Uso:

```bash
python scripts/bitacora_append.py --ia codex --pregunta "..." --respuesta "..."
```

Con metadatos de workflow:

```bash
python scripts/ops/bitacora_append.py --ia codex --pregunta "..." --respuesta "..." --initiative-id 2026-02-24_bitacora --phase F1
```

Con payload JSON por `stdin`:

```bash
echo '{"ia":"codex","pregunta":"...","respuesta":"...","initiative_id":"2026-03-26_demo","phase":"F6"}' | python scripts/ops/bitacora_append.py --stdin-json
```

### Bitacora compliance

Script canónico:
- `scripts/dev/check_bitacora_compliance.py`

Uso:

```bash
python scripts/dev/check_bitacora_compliance.py --initiative-id 2026-03-26_demo
```

Filtrando por IA y fase:

```bash
python scripts/dev/check_bitacora_compliance.py --ia codex --initiative-id 2026-03-26_demo --phase F9
```

### Naming compliance

Script canónico:
- `scripts/dev/check_naming_compliance.py`

Uso:

```bash
python scripts/dev/check_naming_compliance.py
```

### State0 compliance

Script canónico:
- `scripts/dev/check_state0.py`

Uso:

```bash
python scripts/dev/check_state0.py
```

### Governance bootstrap (repos nuevos)

Script canónico:
- `scripts/migration/bootstrap_governance.py`

Uso base con perfil multi-IA interactivo (`core` obligatorio):

```bash
python scripts/migration/bootstrap_governance.py --target <ruta_repo_destino>
```

Uso no interactivo minimo (`core` + dos IAs):

```bash
python scripts/migration/bootstrap_governance.py --target <ruta_repo_destino> --with-ia codex --with-ia claude --preferred-working-ia codex --preferred-auditor-ia claude
```

Con `SymDex` externo desde GitHub:

```bash
python scripts/migration/bootstrap_governance.py --target <ruta_repo_destino> --with-ia codex --with-ia claude --preferred-working-ia codex --preferred-auditor-ia claude --include-pack symdex
```

Con `Claude` + `Codex` + `governance_search` + `SymDex`:

```bash
python scripts/migration/bootstrap_governance.py --target <ruta_repo_destino> --with-ia codex --with-ia claude --preferred-working-ia codex --preferred-auditor-ia claude --include-pack governance_search --include-pack symdex
```

Simulación sin escritura:

```bash
python scripts/migration/bootstrap_governance.py --target <ruta_repo_destino> --dry-run
```

Si no pasas flags `--with-ia`, el script preguntará interactivamente qué IAs
quieres instalar y exigirá al menos dos.

Listado de packs:

```bash
python scripts/migration/bootstrap_governance.py --list-packs
```

Reglas:

- `core` instala la gobernanza canónica reusable y el scaffolding vacío de `dev/records/`.
- en reimportaciones, `core` preserva overlays locales como `.gitignore` y
  `dev/logs/decisions.md` si ya existen en el consumidor.
- en reimportaciones con `--force`, el bootstrap elimina aliases legacy
  conocidos de `doc/governance_prompts/` para mantener un único prompt canónico
  por fase y un único cierre conjunto `F9/F10`.
- `claude` instala solo `CLAUDE.md`; no instala `.claude/settings.local.json`.
- `codex` y `gemini` existen como packs explícitos de perfil multi-IA, aunque hoy no añaden superficie raíz adicional porque su capa normativa ya viaja en `core` dentro de `dev/ai/adapters/`.
- `roo` instala solo reglas Markdown reusables; no instala `.roo/mcp.json`.
- `governance_search` instala el MCP local de retrieval de gobernanza, ejecuta instalación `npm` en `scripts/ops/context_mcp` y escribe `governance_retrieval` en `.mcp.json`. Si también se instala `roo`, añade además el mismo servidor a `.roo/mcp.json`.
- `symdex` no copia código desde un repo consumidor: instala `SymDex` desde `https://github.com/husnainpk/SymDex`, genera `.symdexignore`, prepara `.symdex/`, hace warm-up best effort y escribe `symdex_code` en `.mcp.json` usando `scripts/ops/run_symdex_mcp.py`. Si también se instala `roo`, añade además el mismo servidor a `.roo/mcp.json`.
- el wrapper de `symdex` prioriza un binario local `symdex` y solo cae a `uvx --from <source> ...` si hace falta.
- El instalador exige un perfil de al menos dos IAs y una preferencia separada para trabajo y auditoría.
- Ese perfil se guarda en `dev/governance_baseline.json` como metadata de instalación; no asigna `motor_activo` ni `motor_auditor` por defecto.
- Toda instalación escribe metadata en `dev/governance_baseline.json`.

### Instalador canónico de governance_search

Ruta:
- `scripts/ops/install_governance_mcp.py`

Uso:

```bash
python scripts/ops/install_governance_mcp.py --repo-root <ruta_repo_destino>
```

Con wiring MCP raíz:

```bash
python scripts/ops/install_governance_mcp.py --repo-root <ruta_repo_destino> --write-root-mcp
```

Con wiring Roo:

```bash
python scripts/ops/install_governance_mcp.py --repo-root <ruta_repo_destino> --write-roo-mcp
```

### Instalador canónico de SymDex

Ruta:
- `scripts/ops/install_symdex.py`

Uso:

```bash
python scripts/ops/install_symdex.py --repo-root <ruta_repo_destino>
```

Con wiring MCP raíz:

```bash
python scripts/ops/install_symdex.py --repo-root <ruta_repo_destino> --write-root-mcp
```

Con wiring Roo:

```bash
python scripts/ops/install_symdex.py --repo-root <ruta_repo_destino> --write-roo-mcp
```

### Sync desde `GobernanzaIA` hacia consumidores conocidos

Script canónico:
- `scripts/migration/sync_governance_consumers.py`

Uso:

```bash
python scripts/migration/sync_governance_consumers.py --force
```

Modo simulación:

```bash
python scripts/migration/sync_governance_consumers.py --force --dry-run
```

Consumidores específicos:

```bash
python scripts/migration/sync_governance_consumers.py --consumer kiminion --consumer mcp_boletinesoficiales --force
```

### Trabajo en `GobernanzaIA` y reimportación en repos consumidores

Flujo recomendado:

1. Abrir `GobernanzaIA` en un VSCode separado y hacer allí las mejoras
   reusables del baseline.
2. Desde ese repo fuente, ejecutar el wrapper de sync o el bootstrap directo:

```bash
python scripts/migration/sync_governance_consumers.py --force
```

o bien:

```bash
python scripts/migration/bootstrap_governance.py --target <ruta_repo_consumidor> --force --with-ia codex --with-ia claude --with-ia roo --preferred-working-ia codex --preferred-auditor-ia claude --include-pack governance_search --include-pack symdex
```

3. Revisar el diff en el repo consumidor y validar sus gates locales.

