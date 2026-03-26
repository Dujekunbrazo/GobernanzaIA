# Scripts Policy (Hard)

Fuente canónica:
- `dev/policies/scripts_rules.md`

Reglas mínimas:
- Orden obligatorio en `scripts/dev`, `scripts/ops`, `scripts/migration`.
- No dejar scripts nuevos sueltos en `scripts/` (salvo wrappers de compatibilidad).
- Scripts deben resolver rutas de forma robusta (no depender de `cwd`).
- Si se mueve un script, mantener compatibilidad temporal y documentar ruta nueva.

Si no cumple:
- bloquear cierre
- registrar pendiente de normalización
