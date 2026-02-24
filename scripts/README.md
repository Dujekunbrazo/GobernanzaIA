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

### Governance bootstrap (repos nuevos)

Script canónico:
- `scripts/migration/bootstrap_governance.py`

Uso:

```bash
python scripts/migration/bootstrap_governance.py --target <ruta_repo_destino>
```

Simulación sin escritura:

```bash
python scripts/migration/bootstrap_governance.py --target <ruta_repo_destino> --dry-run
```

