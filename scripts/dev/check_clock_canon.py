"""Guardrail estatico de inyeccion de reloj canonico.

Audita las rutas en denylist y falla si encuentra llamadas directas al reloj
del sistema en modulos de dominio puro.

Uso:
    python scripts/dev/check_clock_canon.py

Exit code 0: denylist limpia (sin violaciones).
Exit code 1: se encontraron violaciones; las imprime en stdout.

Denylist auditada (dominio puro):
  - src/bo_core/core/public_information/  (incluye tracked_project/, store.py,
    polling.py — denylist ampliada 2026-05-24 Fase 1 plan piloto tras
    migrar 5 hits a foundation.time.utcnow())
  - src/bo_core/core/official_signal/
  - src/bo_core/core/daily/
  - src/bo_core/core/procedure/  (denylist ampliada 2026-05-24 Fase 1
    plan piloto tras migrar reconciler.py + sync.py)

Allowlist (borde legitimo, excluido de auditoria):
  - src/bo_core/core/foundation/time.py
  - src/bo_core/core/ledger/
  - src/bo_core/surfaces/
  - scripts/
  - src/bo_delivery/
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

DENYLIST_DIRS: tuple[Path, ...] = (
    REPO_ROOT / "src" / "bo_core" / "core" / "public_information",
    REPO_ROOT / "src" / "bo_core" / "core" / "official_signal",
    REPO_ROOT / "src" / "bo_core" / "core" / "daily",
    REPO_ROOT / "src" / "bo_core" / "core" / "procedure",
)

ALLOWLIST_PREFIXES: tuple[Path, ...] = (
    REPO_ROOT / "src" / "bo_core" / "core" / "foundation" / "time.py",
    REPO_ROOT / "src" / "bo_core" / "core" / "ledger",
    REPO_ROOT / "src" / "bo_core" / "surfaces",
    REPO_ROOT / "scripts",
    REPO_ROOT / "src" / "bo_delivery",
)

def _is_allowlisted(path: Path, allowlist: tuple[Path, ...]) -> bool:
    for prefix in allowlist:
        try:
            path.relative_to(prefix)
            return True
        except ValueError:
            pass
        if path == prefix:
            return True
    return False


def _find_clock_calls(source: str) -> list[int]:
    """Retorna los numeros de linea donde hay llamadas al reloj del sistema."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    hits: list[int] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not isinstance(func, ast.Attribute):
            continue
        obj = func.value
        if not isinstance(obj, ast.Name):
            continue
        pair = (obj.id, func.attr)
        if pair in {
            ("datetime", "now"),
            ("datetime", "utcnow"),
            ("date", "today"),
            ("time", "time"),
            ("time", "monotonic"),
        }:
            hits.append(node.lineno)
    return hits


def check_denylist(
    denylist: tuple[Path, ...] = DENYLIST_DIRS,
    allowlist: tuple[Path, ...] = ALLOWLIST_PREFIXES,
) -> list[str]:
    """Recorre la denylist y devuelve lista de violaciones 'archivo:linea'.

    Acepta denylist y allowlist como argumentos para facilitar el testing.
    """
    violations: list[str] = []
    for denydir in denylist:
        if not denydir.exists():
            continue
        for py_file in sorted(denydir.rglob("*.py")):
            if _is_allowlisted(py_file, allowlist):
                continue
            try:
                source = py_file.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            lines = _find_clock_calls(source)
            for lineno in lines:
                try:
                    label = py_file.relative_to(REPO_ROOT)
                except ValueError:
                    label = py_file
                violations.append(f"{label}:{lineno}")
    return violations


def main() -> int:
    violations = check_denylist()
    if violations:
        print("check_clock_canon: FAIL — llamadas al reloj en dominio puro:")
        for v in violations:
            print(f"  {v}")
        return 1
    print("check_clock_canon: OK — denylist limpia")
    return 0


if __name__ == "__main__":
    sys.exit(main())
