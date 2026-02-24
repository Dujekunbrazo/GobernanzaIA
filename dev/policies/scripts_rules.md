# Scripts Rules (Hard)

Estas reglas gobiernan la carpeta `scripts/`.

## 1) Estructura obligatoria

`scripts/` se organiza así:
- `scripts/dev/` utilities de desarrollo
- `scripts/ops/` operación y soporte
- `scripts/migration/` migraciones puntuales

## 2) Ubicación y alcance

- Ningún script nuevo debe quedar suelto en raíz de `scripts/` (excepto wrappers de compatibilidad).
- Cada script debe vivir en su categoría correcta.

## 3) Contrato de ejecución

- Todo script debe funcionar desde cualquier `cwd` razonable.
- Los paths deben resolverse relativos al repo, no al directorio de ejecución actual.
- Debe fallar con mensajes claros y códigos de salida no-cero.

## 4) Compatibilidad

- Si se mueve un script usado en documentación/comandos previos:
  - mantener wrapper de compatibilidad temporal
  - documentar la ruta canónica nueva

## 5) I/O y artefactos

- Salidas de scripts operativos deben ir a rutas explícitas (`reports/`, `logs/`, etc.).
- Prohibido escribir artefactos temporales en rutas ambiguas sin documentarlo.

## 6) Documentación mínima por script

Cada script debe exponer:
- propósito
- uso (`--help` o bloque de uso)
- output esperado
- errores comunes

## 7) Regla de bloqueo

Si un script no cumple estructura o contrato de ejecución:
- no puede declararse estado operativo
- debe quedar como pendiente de normalización
