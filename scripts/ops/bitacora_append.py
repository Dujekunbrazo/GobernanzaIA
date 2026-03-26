import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = REPO_ROOT / "dev" / "records" / "bitacora"

SENSITIVE_PATTERNS = [
    re.compile(r"(sk-[A-Za-z0-9]{20,})"),
    re.compile(r"(AKIA[0-9A-Z]{16})"),
    re.compile(r"(?i)(api[_-]?key\s*[:=]\s*[^\s]+)"),
    re.compile(r"(?i)(token\s*[:=]\s*[^\s]+)"),
]


def slugify(value):
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value)
    value = value.strip("_")
    return value or "ia"


def sanitize_text(value):
    text = (value or "").strip()
    if not text:
        return "(sin contenido)"

    sanitized = text
    for pattern in SENSITIVE_PATTERNS:
        sanitized = pattern.sub("[REDACTED]", sanitized)
    return sanitized


def read_optional_text(value, file_path, label):
    direct = (value or "").strip()
    if direct:
        return direct
    path_value = (file_path or "").strip()
    if path_value:
        return Path(path_value).read_text(encoding="utf-8").strip()
    return ""


def load_stdin_json(enabled):
    if not enabled:
        return {}
    raw = sys.stdin.read().strip()
    if not raw:
        raise ValueError("--stdin-json requires JSON content on stdin")
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError("--stdin-json expects a JSON object")
    return payload


def ensure_header(path, ia_name, day):
    if path.exists():
        return
    header = (
        f"# Bitacora {day} - {ia_name}\n\n"
        f"- IA: {ia_name}\n"
        f"- Fecha: {day}\n\n"
        "## Conversacion\n"
    )
    path.write_text(header, encoding="utf-8")


def append_entry(ia, question, answer, initiative_id=None, phase=None, output_dir=DEFAULT_OUTPUT_DIR):
    now = datetime.now()
    day = now.strftime("%Y-%m-%d")
    ia_slug = slugify(ia)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{day}_{ia_slug}.md"

    ensure_header(path, ia, day)

    safe_question = sanitize_text(question)
    safe_answer = sanitize_text(answer)
    metadata = []
    if initiative_id:
        metadata.append(f"- Initiative ID: `{initiative_id}`")
    if phase:
        metadata.append(f"- Fase: `{phase}`")

    block = [f"\n### {now.strftime('%H:%M:%S')}"]
    if metadata:
        block.extend(metadata)
    block.extend(
        [
            "",
            "**Usuario**",
            "",
            safe_question,
            "",
            f"**{ia}**",
            "",
            safe_answer,
            "",
        ]
    )

    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(block))

    return path


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Append one conversation turn to the daily AI bitacora file."
    )
    parser.add_argument("--stdin-json", action="store_true", help="Read payload from stdin JSON")
    parser.add_argument("--ia", help="AI name. Example: codex, claude, gemini, roo")
    parser.add_argument("--pregunta", help="User question")
    parser.add_argument("--pregunta-file", default="", help="Read user question from file")
    parser.add_argument("--respuesta", help="AI response")
    parser.add_argument("--respuesta-file", default="", help="Read AI response from file")
    parser.add_argument("--initiative-id", default="", help="Optional initiative id")
    parser.add_argument("--phase", default="", help="Optional phase (F1..F9)")
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Output directory for bitacora files",
    )
    parser.add_argument("--print-path-only", action="store_true", help="Print only the output path")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv if argv is not None else sys.argv[1:])
    payload = load_stdin_json(args.stdin_json)

    ia = (args.ia or payload.get("ia") or "").strip()
    question = read_optional_text(
        args.pregunta or payload.get("pregunta", ""),
        args.pregunta_file or payload.get("pregunta_file", ""),
        "pregunta",
    )
    answer = read_optional_text(
        args.respuesta or payload.get("respuesta", ""),
        args.respuesta_file or payload.get("respuesta_file", ""),
        "respuesta",
    )
    initiative_id = (args.initiative_id or payload.get("initiative_id") or "").strip()
    phase = (args.phase or payload.get("phase") or "").strip()
    output_dir = args.output_dir or payload.get("output_dir") or str(DEFAULT_OUTPUT_DIR)

    if not ia:
        raise ValueError("Missing required field: ia")
    if not question:
        raise ValueError("Missing required field: pregunta")
    if not answer:
        raise ValueError("Missing required field: respuesta")

    path = append_entry(
        ia=ia,
        question=question,
        answer=answer,
        initiative_id=initiative_id,
        phase=phase,
        output_dir=output_dir,
    )
    if args.print_path_only:
        print(path)
    else:
        print(f"OK: bitacora updated at {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
