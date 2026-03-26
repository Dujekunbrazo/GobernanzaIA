# Scripts

Estructura oficial:

- `scripts/dev/`: utilidades de desarrollo local
- `scripts/ops/`: scripts operativos y soporte
- `scripts/migration/`: migraciones puntuales

Reglas:
- La ruta canónica se define por categoría.
- No dejar scripts nuevos sueltos en `scripts/` (excepto wrappers de compatibilidad).
- Los scripts deben resolver paths contra el repo y no depender del `cwd`.

## Script operativo actual

### Export incident bundle

Ruta canónica:
- `scripts/ops/export_incident.py`

Wrapper de compatibilidad:
- `scripts/export_incident.py`

Uso:

```bash
python scripts/export_incident.py <trace_id>
```

Opciones avanzadas:

```bash
python scripts/ops/export_incident.py <trace_id> --log-file logs/kiminion_trace.jsonl --output-dir reports/incidents
```

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

### Smoke baseline chat + memoria

Script canónico:
- `scripts/dev/smoke_chat_memory.py`

Uso local (sin red):

```bash
python scripts/dev/smoke_chat_memory.py
```

Uso completo (incluye llamada real a Kimi):

```bash
python scripts/dev/smoke_chat_memory.py --probe-api
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

Con `Roo` + `SymDex` externo desde GitHub:

```bash
python scripts/migration/bootstrap_governance.py --target <ruta_repo_destino> --with-ia codex --with-ia roo --preferred-working-ia codex --preferred-auditor-ia roo --include-pack symdex
```

Con `Claude` + `Roo` + `governance_search` + `SymDex`:

```bash
python scripts/migration/bootstrap_governance.py --target <ruta_repo_destino> --with-ia codex --with-ia claude --with-ia roo --preferred-working-ia codex --preferred-auditor-ia claude --include-pack governance_search --include-pack symdex
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
- `claude` instala solo `CLAUDE.md`; no instala `.claude/settings.local.json`.
- `codex` y `gemini` existen como packs explícitos de perfil multi-IA, aunque hoy no añaden superficie raíz adicional porque su capa normativa ya viaja en `core` dentro de `dev/ai/adapters/`.
- `roo` instala solo reglas Markdown reusables; no instala `.roo/mcp.json`.
- `governance_search` instala el MCP local de retrieval de gobernanza, ejecuta instalación `npm` en `scripts/ops/context_mcp` y, si también se instala `roo`, añade `governance_retrieval` a `.roo/mcp.json`.
- `symdex` no copia código desde `Kiminion`: instala `SymDex` desde `https://github.com/husnainpk/SymDex`, genera `.symdexignore` y, si también se instala `roo`, prepara `.roo/mcp.json` con `uvx --from <source> symdex serve`.
- `roo + symdex` exige `uvx` en el entorno destino para que el wiring MCP funcione.
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

Con wiring Roo:

```bash
python scripts/ops/install_symdex.py --repo-root <ruta_repo_destino> --write-roo-mcp
```

### Trabajo en `GobernanzaIA` y reimportación en `Kiminion`

Flujo recomendado:

1. Abrir `GobernanzaIA` en un VSCode separado y hacer allí las mejoras
   reusables del baseline.
2. Desde ese repo fuente, ejecutar:

```bash
python scripts/migration/bootstrap_governance.py --target <ruta_kiminion> --force --with-ia codex --with-ia claude --with-ia roo --preferred-working-ia codex --preferred-auditor-ia claude --include-pack governance_search --include-pack symdex
```

3. Revisar el diff en `Kiminion` y validar gates locales.

