"""Memory precheck gate (Regla 32 AGENTS.md §5).

Compuerta CLI minima que inventaria 6 fuentes canonicas del repo antes
de proponer canon nuevo (nueva BX.Y, nuevo `access_pattern`, nuevo
arquetipo, nueva capability seed o renombrado canonico).

Veredicto binario:

- ALLOW (exit 0): no hay matches activos ni fallo de fuente, y, si
  `--strict` no esta activo, los matches retirados no bloquean.
- BLOCK (exit 1): hay matches activos, o `--strict` y existe al menos
  un match retirado, o falta una fuente requerida.

La salida stdout es determinista y termina con una linea literal
`Verdict: ALLOW` o `Verdict: BLOCK`.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_SOURCE_PATHS: tuple[str, ...] = (
    "dev/records/reviews/initiative_backlog.md",
    "dev/records/reviews/architecture_findings_register.md",
    "dev/records/reviews/initiative_architecture_backlog.md",
)
# Las rutas por defecto son la memoria operativa viva canonica del kit
# (declarada en AGENTS.md §11). El consumidor debe anadir sus propias fuentes
# canon project-specific via `--canon-source` repetible o via la variable de
# entorno `MEMORY_PRECHECK_SOURCES` (separada por os.pathsep). Si ninguna
# fuente adicional se declara, el scan solo cubre la memoria estructural.

RETIRED_HEADING_WINDOW = 25
RETIRED_INLINE_WINDOW = 5

RETIRED_LEXEMS: tuple[str, ...] = (
    "saneamiento",
    "retirad",
    "carecia de evidencia",
    "antipattern",
    "propuesta intermedia",
    "propuesta retirada",
)

HEADING_RE = re.compile(r"^#{1,6}\s+(.*)$")
TOKEN_RE = re.compile(r"^[A-Za-z][\w\.]*$")


@dataclass(frozen=True)
class Match:
    path: str
    line_number: int
    line: str
    classification: str


@dataclass(frozen=True)
class SourceError:
    path: str
    reason: str


def _has_retired_lexem(text: str) -> bool:
    low = text.lower()
    return any(lex in low for lex in RETIRED_LEXEMS)


def _is_retired_context(lines: list[str], match_index: int) -> bool:
    if _has_retired_lexem(lines[match_index]):
        return True

    heading_start = max(0, match_index - RETIRED_HEADING_WINDOW)
    for back in range(match_index - 1, heading_start - 1, -1):
        m = HEADING_RE.match(lines[back])
        if m is None:
            continue
        if _has_retired_lexem(m.group(1)):
            return True
        break

    inline_start = max(0, match_index - RETIRED_INLINE_WINDOW)
    for back in range(match_index - 1, inline_start - 1, -1):
        if _has_retired_lexem(lines[back]):
            return True
    return False


def build_term_regex(term: str) -> re.Pattern[str]:
    """Compila regex case-insensitive para `term`.

    Si `term` parece identificador (un token alfanumerico con puntos),
    exige limite de token defensivo: el caracter anterior y posterior no
    puede ser alfanumerico, underscore ni punto. Asi se evita matchear
    `TOKEN` dentro de `TOKENX`, `xTOKEN`, `TOKEN_otro` o `2026TOKEN`.
    """
    escaped = re.escape(term)
    if TOKEN_RE.fullmatch(term):
        pattern = rf"(?<![\w\.]){escaped}(?![\w\.])"
    else:
        pattern = escaped
    return re.compile(pattern, re.IGNORECASE)


def scan_source(
    term_re: re.Pattern[str],
    path: Path,
    repo_root: Path,
) -> tuple[list[Match], SourceError | None]:
    try:
        rel = str(path.relative_to(repo_root)).replace("\\", "/")
    except ValueError:
        rel = str(path).replace("\\", "/")
    if not path.exists():
        return [], SourceError(path=rel, reason="missing")
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return [], SourceError(path=rel, reason=f"unreadable: {exc}")
    lines = text.splitlines()
    matches: list[Match] = []
    for i, line in enumerate(lines):
        if term_re.search(line):
            classification = (
                "retired" if _is_retired_context(lines, i) else "active"
            )
            matches.append(
                Match(
                    path=rel,
                    line_number=i + 1,
                    line=line.rstrip(),
                    classification=classification,
                )
            )
    return matches, None


def build_report(
    *,
    term: str,
    matches: list[Match],
    source_errors: list[SourceError],
    strict: bool,
    sources_scanned: int,
) -> tuple[str, bool]:
    active = [m for m in matches if m.classification == "active"]
    retired = [m for m in matches if m.classification == "retired"]

    block = False
    block_reason = ""
    if source_errors:
        block = True
        block_reason = "SOURCE_MISSING"
    elif active:
        block = True
        block_reason = "ACTIVE_MATCH"
    elif strict and retired:
        block = True
        block_reason = "STRICT_RETIRED_MATCH"

    out: list[str] = []
    out.append("Memory precheck report")
    out.append("----------------------")
    out.append(f"candidate={term}")
    out.append(f"sources_scanned={sources_scanned}")
    out.append(f"active_matches={len(active)}")
    out.append(f"retired_matches={len(retired)}")
    out.append(f"source_errors={len(source_errors)}")
    out.append(f"strict={'yes' if strict else 'no'}")
    if block_reason:
        out.append(f"block_reason={block_reason}")

    if source_errors:
        out.append("")
        out.append("Source errors:")
        for err in sorted(source_errors, key=lambda e: e.path):
            out.append(f"- {err.path} reason={err.reason}")

    if matches:
        out.append("")
        out.append("Matches:")
        ordered = sorted(matches, key=lambda m: (m.path, m.line_number))
        for m in ordered:
            out.append(
                f"- {m.path}:{m.line_number} classification={m.classification}"
            )
            out.append(f"  > {m.line}")

    out.append("")
    out.append(f"Verdict: {'BLOCK' if block else 'ALLOW'}")
    return "\n".join(out), block


def build_json_report(
    *,
    term: str,
    matches: list[Match],
    source_errors: list[SourceError],
    strict: bool,
    sources_scanned: int,
) -> tuple[str, bool]:
    """Variante JSON de `build_report`. Mismo dato, formato parseable.

    El stdout queda como `json.dumps(..., indent=2, ensure_ascii=False)`
    con clave terminal `verdict` igual a `ALLOW` o `BLOCK`. Los matches
    van ordenados por `(path, line_number)` para que el output sea
    determinista (igual que el reporte humano).
    """
    active = [m for m in matches if m.classification == "active"]
    retired = [m for m in matches if m.classification == "retired"]

    block = False
    block_reason: str | None = None
    if source_errors:
        block = True
        block_reason = "SOURCE_MISSING"
    elif active:
        block = True
        block_reason = "ACTIVE_MATCH"
    elif strict and retired:
        block = True
        block_reason = "STRICT_RETIRED_MATCH"

    ordered_matches = sorted(matches, key=lambda m: (m.path, m.line_number))
    ordered_errors = sorted(source_errors, key=lambda e: e.path)

    payload: dict[str, object] = {
        "candidate": term,
        "sources_scanned": sources_scanned,
        "active_matches": len(active),
        "retired_matches": len(retired),
        "source_errors": len(source_errors),
        "strict": strict,
        "block_reason": block_reason,
        "matches": [
            {
                "path": m.path,
                "line_number": m.line_number,
                "line": m.line,
                "classification": m.classification,
            }
            for m in ordered_matches
        ],
        "errors": [
            {"path": e.path, "reason": e.reason} for e in ordered_errors
        ],
        "verdict": "BLOCK" if block else "ALLOW",
    }
    return json.dumps(payload, indent=2, ensure_ascii=False), block


def run(
    term: str,
    strict: bool,
    repo_root: Path | None = None,
    sources: Iterable[str] | None = None,
    as_json: bool = False,
) -> tuple[str, int]:
    """Ejecuta el precheck. Devuelve (stdout_text, exit_code).

    `repo_root` y `sources` son inyectables para tests con fixtures
    sinteticas; por defecto usan REPO_ROOT y SOURCE_PATHS canonicos.
    Si `as_json=True`, stdout es JSON parseable; si no, texto humano.
    """
    if repo_root is None:
        repo_root = REPO_ROOT
    if sources is None:
        sources_list = list(DEFAULT_SOURCE_PATHS)
    else:
        sources_list = list(sources)

    term_re = build_term_regex(term)
    all_matches: list[Match] = []
    all_errors: list[SourceError] = []
    for rel in sources_list:
        path = repo_root / rel
        matches, err = scan_source(term_re, path, repo_root)
        if err is not None:
            all_errors.append(err)
        all_matches.extend(matches)

    builder = build_json_report if as_json else build_report
    text, block = builder(
        term=term,
        matches=all_matches,
        source_errors=all_errors,
        strict=strict,
        sources_scanned=len(sources_list),
    )
    return text, 1 if block else 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Memory precheck gate (Regla 32 AGENTS.md §5). "
            "Inventaria canon vivo antes de proponer canon nuevo."
        ),
    )
    parser.add_argument(
        "term",
        help="Termino candidato a buscar en el canon vivo.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Tratar matches retirados/historicos como bloqueantes.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Emitir reporte como JSON parseable en lugar de texto humano.",
    )
    parser.add_argument(
        "--canon-source",
        action="append",
        default=[],
        dest="canon_sources",
        help=(
            "Ruta adicional a archivo .md canon que se incluye en el scan. "
            "Repetir el flag para anadir multiples fuentes. Tambien se aceptan "
            "via variable de entorno MEMORY_PRECHECK_SOURCES (separadas por "
            "os.pathsep). Las rutas son relativas al repo_root."
        ),
    )
    return parser.parse_args(argv)


def resolve_sources(canon_sources_cli: list[str]) -> list[str]:
    """Combina default + variable de entorno + CLI flags en una lista ordenada
    sin duplicados, preservando orden de aparicion (default → env → cli)."""
    env_value = os.environ.get("MEMORY_PRECHECK_SOURCES", "").strip()
    env_sources: list[str] = []
    if env_value:
        env_sources = [s.strip() for s in env_value.split(os.pathsep) if s.strip()]
    combined: list[str] = []
    seen: set[str] = set()
    for src in (*DEFAULT_SOURCE_PATHS, *env_sources, *canon_sources_cli):
        if src not in seen:
            combined.append(src)
            seen.add(src)
    return combined


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    resolved_sources = resolve_sources(args.canon_sources)
    text, exit_code = run(
        args.term,
        args.strict,
        sources=resolved_sources,
        as_json=args.as_json,
    )
    # Escribir bytes UTF-8 directamente para no depender de la encoding
    # nativa de stdout (cp1252 en Windows rompe con `✓` y similares
    # que aparecen en las fuentes canonicas).
    sys.stdout.buffer.write((text + "\n").encode("utf-8", errors="replace"))
    sys.stdout.flush()
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
