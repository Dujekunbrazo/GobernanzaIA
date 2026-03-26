import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_FIELDS = {
    "Initiative ID": "exact",
    "Modo": "non_empty",
    "Capability": "non_empty",
    "Estado": {"PENDIENTE", "PASS", "FAIL"},
    "Owner arquitectónico": "non_empty",
    "Contrato canónico": "non_empty",
    "Wiring canónico": "non_empty",
    "Legacy afectado": "non_empty",
    "Fecha": "non_empty",
}

REQUIRED_SECTIONS = [
    "Superficies incluidas",
    "Evidencia estructural",
    "No-convivencia legacy/canónico",
    "No-branching oportunista",
    "Decisión de cierre",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Valida capability_closure.md para una iniciativa."
    )
    parser.add_argument(
        "--initiative-id",
        required=True,
        help="Initiative ID en dev/records/initiatives/<initiative_id>/",
    )
    parser.add_argument(
        "--required",
        action="store_true",
        help="Falla si capability_closure.md no existe.",
    )
    return parser.parse_args()


def normalize_scalar(value: str) -> str:
    return value.strip().strip("`").strip()


def extract_field(text: str, label: str) -> str | None:
    pattern = rf"^- {re.escape(label)}:\s*(.*)$"
    match = re.search(pattern, text, flags=re.MULTILINE)
    if not match:
        return None
    return normalize_scalar(match.group(1))


def section_body(text: str, title: str) -> str:
    pattern = rf"^## {re.escape(title)}\s*$"
    match = re.search(pattern, text, flags=re.MULTILINE)
    if not match:
        return ""
    start = match.end()
    next_match = re.search(r"^##\s+.+$", text[start:], flags=re.MULTILINE)
    end = start + next_match.start() if next_match else len(text)
    return text[start:end].strip()


def has_meaningful_content(body: str) -> bool:
    meaningful_lines = []
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if re.fullmatch(r"(?:[-*]|\d+\.)\s*", line):
            continue
        if re.fullmatch(r"(?:[-*]|\d+\.)\s*Pendiente\.?", line, flags=re.IGNORECASE):
            continue
        meaningful_lines.append(line)
    return bool(meaningful_lines)


def main() -> int:
    args = parse_args()
    initiative_dir = REPO_ROOT / "dev" / "records" / "initiatives" / args.initiative_id
    closure_path = initiative_dir / "capability_closure.md"

    errors: list[str] = []
    warnings: list[str] = []

    if not initiative_dir.exists():
        errors.append(f"Initiative not found: {initiative_dir}")
    if errors:
        print_report(errors, warnings)
        return 1

    if not closure_path.exists():
        message = f"Missing file: {closure_path}"
        if args.required:
            errors.append(message)
            print_report(errors, warnings)
            return 1
        warnings.append(message)
        print_report(errors, warnings)
        return 0

    text = closure_path.read_text(encoding="utf-8", errors="ignore")

    for field, rule in REQUIRED_FIELDS.items():
        value = extract_field(text, field)
        if value is None:
            errors.append(f"Missing field: {field}")
            continue
        if rule == "exact":
            if value != args.initiative_id:
                errors.append(
                    f"Field '{field}' must match initiative id '{args.initiative_id}', found '{value}'"
                )
        elif rule == "non_empty":
            if not value or value in {"PENDIENTE", "|"}:
                errors.append(f"Field '{field}' must not be empty")
        elif isinstance(rule, set):
            if value not in rule:
                errors.append(f"Field '{field}' has invalid value '{value}'")

    for title in REQUIRED_SECTIONS:
        body = section_body(text, title)
        if not body:
            errors.append(f"Missing section: {title}")
            continue
        if not has_meaningful_content(body):
            errors.append(f"Section '{title}' has no meaningful content")

    print_report(errors, warnings)
    return 1 if errors else 0


def print_report(errors: list[str], warnings: list[str]) -> None:
    print("Capability closure report")
    print("-------------------------")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    if errors:
        print("\nErrors:")
        for item in errors:
            print(f"- {item}")
    if warnings:
        print("\nWarnings:")
        for item in warnings:
            print(f"- {item}")


if __name__ == "__main__":
    sys.exit(main())
