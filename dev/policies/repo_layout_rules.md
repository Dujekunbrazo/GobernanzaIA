# Repo Layout Rules (Hard)

Estas reglas definen el estado base de organización del repositorio.

## 1) Estructura raíz mínima esperada

En la raíz solo deben existir:
- archivos de arranque/configuración (`README.md`, `AGENTS.md`, `CLAUDE.md`, `.gitignore`, `.env.example`, `requirements.txt`, `start_kiminion.bat`)
- código runtime temporalmente heredado (`kiminion_ui.py`, `memory_concept.py`, `kiminion_logging.py`)
- carpetas de dominio (`dev/`, `scripts/`, `doc/`, `state/`, `logs/`, `reports/`, `sessions/`, `content/`)

## 2) Gobernanza centralizada

- Reglas: `AGENTS.md`, `dev/workflow.md`, `dev/policies/*.md`
- Gates: `dev/guarantees/*.md`
- Evidencia: `dev/records/*`
- No mezclar gobernanza con runtime: artefactos de proceso (reglas, gates, plantillas, bitácora, iniciativas) deben vivir en `dev/` y nunca en rutas runtime de la app.

## 3) Scripts

- Orden obligatorio en `scripts/dev`, `scripts/ops`, `scripts/migration`
- En `scripts/` raíz solo wrappers y `README.md`

## 4) Runbooks heredados

- Activos solo: `dev/runbooks/README.md`, `dev/runbooks/REGISTRY.md`
- Heredados en cuarentena: `dev/records/legacy/runbooks/`

## 5) Artefactos transitorios

- `__pycache__/` no forma parte del estado base.
- reportes de prueba ad-hoc no forman parte del estado base.

## 6) Validación obligatoria

Script oficial:
- `scripts/dev/check_state0.py`

Si falla:
- no hay cierre formal de iniciativa.

## 7) Frontera proyecto Python vs gobernanza

- Código y artefactos runtime del proyecto: raíz Python, `state/`, `logs/`, `sessions/`, `reports/`, `content/`.
- Gobernanza IA y proceso: `dev/` (`workflow`, `policies`, `guarantees`, `templates`, `records`, `ai/adapters`).
- Prohibido mover reglas de gobernanza a carpetas runtime o mezclar código de aplicación dentro de `dev/`.

