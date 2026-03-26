# Repo Layout Rules (Hard)

Estas reglas definen el estado base de organización del repositorio.

## 1) Estructura raíz mínima esperada

En un repo con gobernanza instalada, la raíz debe contener como mínimo:
- archivos base (`README.md`, `AGENTS.md`, `.gitignore`)
- superficies opcionales de compatibilidad según packs instalados
  (`CLAUDE.md` y equivalentes)
- carpetas de gobernanza (`dev/`, `scripts/`)
- `doc/` cuando exista documentación arquitectónica compartida

Los artefactos de runtime del proyecto consumidor pueden existir en la raíz o
en carpetas propias del producto, pero no forman parte del baseline mínimo de
gobernanza.

## 2) Gobernanza centralizada

- Reglas: `AGENTS.md`, `dev/workflow.md`, `dev/policies/*.md`
- Gates: `dev/guarantees/*.md`
- Evidencia: `dev/records/*`
- Política Git/GitHub: `dev/policies/git_workflow_rules.md`
- No mezclar gobernanza con runtime: artefactos de proceso (reglas, gates, plantillas, bitácora, iniciativas) deben vivir en `dev/` y nunca en rutas runtime de la app.

## 3) Scripts

- Orden obligatorio en `scripts/dev`, `scripts/ops`, `scripts/migration`
- En `scripts/` raíz solo wrappers y `README.md`

## 4) Runbooks heredados

- Si existen runbooks activos, solo se admiten `dev/runbooks/README.md` y
  `dev/runbooks/REGISTRY.md`
- Si el repositorio conserva runbooks heredados, deben vivir en
  `dev/records/legacy/runbooks/`
- Un baseline reusable puede omitir runbooks por completo

## 5) Artefactos transitorios

- `__pycache__/` no forma parte del estado base.
- reportes de prueba ad-hoc no forman parte del estado base.

## 6) Validación obligatoria

Script oficial:
- `scripts/dev/check_state0.py`

Si falla:
- no hay cierre formal de iniciativa.

## 7) Frontera producto vs gobernanza

- Código y artefactos runtime del proyecto consumidor: rutas del producto,
  cualesquiera que sean (`core/`, `src/`, raíz Python, `state/`, `logs/`,
  `sessions/`, `reports/`, `content/`, etc.).
- Gobernanza IA y proceso: `dev/` (`workflow`, `policies`, `guarantees`,
  `templates`, `records`, `ai/adapters`) y `scripts/` de soporte.
- Prohibido mover reglas de gobernanza a carpetas runtime o mezclar código de
  aplicación dentro de `dev/`.

