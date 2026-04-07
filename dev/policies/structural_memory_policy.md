# Structural Memory Policy (Hard)

Propósito:
- regular la integración canónica de `codebase-memory-mcp` como capa
  estructural primaria del sistema.

## 1) Rol canónico

`codebase-memory-mcp` es la capacidad estructural prevista para:

- wiring global
- call paths
- blast radius
- impact analysis
- legacy y dead code
- arquitectura estructural

## 2) Regla de uso

- cuando esté disponible y validado localmente, pasa a ser la vía estructural
  primaria
- `symdex_code` permanece como capa de detalle local, no como sustituto
  estructural global
- la búsqueda textual queda solo como fallback de último nivel

## 3) Cuándo debe usarse

Debe priorizarse en:

- iniciativas con capability transversal
- dudas de wiring canónico
- análisis de legacy o paths paralelos
- auditorías `F5` y `F7` con impacto multiarchivo
- `F8` cuando haya que contrastar runtime observado contra wiring esperado

## 4) Fallback permitido

Si la capacidad no está disponible o no está validada localmente:

- degradar a `symdex_code` más lectura canónica del repo
- dejar trazado en el perfil local del repo
- no simular que la capacidad existe

## 5) Prohibiciones

- prohibido tratar `codebase-memory-mcp` como ayuda opcional lateral cuando ya
  esté validado
- prohibido mantener dos vías estructurales primarias en paralelo
- prohibido declararlo como disponible si no está realmente operativo

## 6) Criterio de aceptabilidad

La integración estructural es aceptable cuando:

- el perfil del repo declara su disponibilidad real
- el routing canónico lo prioriza donde corresponde
- existe fallback explícito
- no crea rutas paralelas de análisis estructural
