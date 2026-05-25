# Canonical Clock Injection Policy

## Regla MIT transversal

> El reloj se lee **una sola vez, en el borde**. El dominio recibe tiempo
> como dato explícito.

Ningún módulo de dominio puro llama a funciones que lean el reloj del sistema
(`datetime.now`, `date.today`, `time.time`, `time.monotonic`, `utcnow`). El
tiempo llega como parámetro obligatorio declarado en la firma.

El único reloj canónico del sistema es la función libre `utcnow()` definida en
`src/bo_core/core/foundation/time.py`. No se introduce ningún segundo reloj,
`ClockService`, factory ni abstracción pesada de inyección.

## Vocabulario temporal canónico

Los campos de tiempo que aparecen en contratos y dataclasses del sistema se
nombran únicamente con los términos siguientes. Introducir un nombre nuevo
requiere actualizar este policy.

| Campo | Semántica |
|---|---|
| `as_of` | instante de referencia para una decisión o priorización |
| `computed_at` | instante en que se calculó un resultado derivado |
| `retrieved_at` | instante en que se recuperó un artefacto externo |
| `generated_at` | instante en que se generó un artefacto de salida (snapshot/export) |
| `started_at` | inicio de una operación de adquisición o fetch |
| `finished_at` | fin de una operación de adquisición o fetch |
| `last_checked_at` | último instante en que se comprobó un estado |
| `next_check_at` | instante programado para la siguiente comprobación |

## Definición de borde vs. dominio

**Borde** — sitio donde el reloj del sistema puede leerse legítimamente:
- conectores y adaptadores HTTP (`surfaces/**`)
- ledger de trazabilidad (`ledger/**`)
- scripts de orquestación, smokes y CI (`scripts/**`)
- exporters y snapshots de delivery que estampan `generated_at` en el momento
  de render (`bo_delivery/**`)
- CLI y punto de entrada del orquestador

**Dominio** — módulo que toma decisiones sobre el estado del mundo. El dominio
**nunca** llama al reloj; recibe `as_of`, `computed_at` u otro campo canónico
como parámetro obligatorio de su firma.

Ejemplos de borde legítimo:
```python
# conector: estampa el hecho en el momento de la petición
retrieved_at = utcnow()
record = FetchRecord(started_at=started, finished_at=utcnow(), ...)

# exporter: sella el artefacto en el momento de render
generated_at = utcnow()
```

Ejemplos de dominio correcto:
```python
# prioritizer recibe as_of como dato; no llama al reloj
def prioritize(signals, as_of: datetime) -> list[OfficialSignal]: ...

# builder recibe now como dato; no llama al reloj
def build_tracked_project_case(..., now: datetime) -> TrackedProjectCase: ...
```

## Allowlist (uso permitido, no auditado por el guardrail)

Las rutas siguientes pueden invocar `utcnow()` o equivalentes sin ser marcadas
como violación:

- `src/bo_core/core/foundation/time.py` — definición del reloj canónico
- `src/bo_core/core/ledger/**` — estampa hechos de trazabilidad
- `src/bo_core/surfaces/**` — conectores y adaptadores de superficie
- `scripts/**` — orquestación, smokes y CI
- `src/bo_delivery/**` — exporters y snapshots (borde de render)

## Denylist (dominio auditado, debe estar limpio)

Las rutas siguientes son dominio puro. El guardrail
`scripts/dev/check_clock_canon.py` las audita y falla ante cualquier llamada
directa al reloj:

- `src/bo_core/core/public_information/tracked_project/**`
- `src/bo_core/core/official_signal/**`

El guardrail debe retornar exit 0 sobre estas rutas. Cualquier expansión de
la denylist requiere reapertura de F1 en la iniciativa correspondiente.

## Zona gris / deuda controlada (NO auditada por este guardrail)

Los módulos siguientes contienen llamadas directas al reloj que no se migran
en esta iniciativa. Están registrados explícitamente como deuda controlada;
una iniciativa posterior decidirá su clasificación final y migración.

| Módulo | Hits | Clasificación provisional |
|---|---|---|
| `src/bo_core/core/procedure/reconciler.py:69` | 1 | dominio con deuda |
| `src/bo_core/core/procedure/sync.py:71` | 1 | dominio con deuda |
| `src/bo_core/core/public_information/store.py` | 4 | frontera persistencia |
| `src/bo_core/core/public_information/polling.py:151` | 1 | frontera scheduling |

El guardrail no audita estas rutas para no forzar refactor masivo ni producir
falsos positivos en código fuera del alcance de la iniciativa actual.

## Guardrail

El script `scripts/dev/check_clock_canon.py` implementa un AST walker que:

1. Recorre todos los archivos `.py` bajo las rutas de la denylist.
2. Detecta llamadas a `datetime.now`, `date.today`, `time.time`,
   `time.monotonic` en cualquier forma de invocación.
3. Excluye explícitamente los archivos bajo la allowlist.
4. Devuelve exit code 1 con lista de violaciones si encuentra alguna,
   exit code 0 si el dominio está limpio.

Ejecutar antes de cada merge de rama que toque módulos de dominio:
```
python scripts/dev/check_clock_canon.py
```

## Historial

- 2026-04-28: canon inicial establecido en iniciativa
  `2026-04-28_canonical_clock_injection_contract` (F2 PASS).
  Inventario base: 11 hits en `src/`; 1 reloj canónico, 2 borde delivery,
  1 hotspot corregido (`tracked_project/builder.py:208`), 7 zona gris.
