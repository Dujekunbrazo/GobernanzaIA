import argparse
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
    parser.add_argument("--ia", required=True, help="AI name. Example: codex, claude, gemini, roo")
    parser.add_argument("--pregunta", required=True, help="User question")
    parser.add_argument("--respuesta", required=True, help="AI response")
    parser.add_argument("--initiative-id", default="", help="Optional initiative id")
    parser.add_argument("--phase", default="", help="Optional phase (F1..F9)")
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Output directory for bitacora files",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv if argv is not None else sys.argv[1:])
    path = append_entry(
        ia=args.ia,
        question=args.pregunta,
        answer=args.respuesta,
        initiative_id=args.initiative_id,
        phase=args.phase,
        output_dir=args.output_dir,
    )
    print(f"OK: bitacora updated at {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
