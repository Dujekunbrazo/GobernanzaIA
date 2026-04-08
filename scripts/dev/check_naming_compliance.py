import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

INITIATIVE_ID_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}_[a-z0-9_]+$")
BITACORA_FILE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}_(codex|claude)\.md$")

INITIATIVE_ALLOWED_FILES = {
    "ask.md",
    "ask_audit.md",
    "plan.md",
    "plan_audit.md",
    "execution.md",
    "post_audit.md",
    "closeout.md",
    "lessons_learned.md",
    "handoff.md",
    "baseline_freeze.md",
    "capability_closure.md",
    "exception_record.md",
    "real_validation.md",
}

TEMPLATE_REQUIRED_FILES = {
    "ask.md",
    "ask_audit.md",
    "plan.md",
    "plan_audit.md",
    "execution.md",
    "post_audit.md",
    "closeout.md",
    "lessons_learned.md",
}

ADAPTER_REQUIRED_FILES = {"codex.md", "claude.md"}


def check_initiatives(errors, warnings):
    base = REPO_ROOT / "dev" / "records" / "initiatives"
    if not base.exists():
        errors.append("Missing folder: dev/records/initiatives")
        return

    for entry in sorted(base.iterdir()):
        if entry.name in {".gitkeep"}:
            continue
        if not entry.is_dir():
            errors.append(f"Invalid entry in initiatives (must be dir): {entry}")
            continue
        if not INITIATIVE_ID_PATTERN.match(entry.name):
            errors.append(f"Invalid initiative_id name: {entry.name}")

        for child in sorted(entry.iterdir()):
            if child.name.startswith("."):
                continue
            if child.is_dir():
                warnings.append(f"Nested directory inside initiative: {child}")
                continue
            if child.name not in INITIATIVE_ALLOWED_FILES:
                warnings.append(f"Non-standard file in initiative {entry.name}: {child.name}")

        ask_path = entry / "ask.md"
        if ask_path.exists():
            try:
                ask_text = ask_path.read_text(encoding="utf-8", errors="ignore")
            except OSError as exc:
                warnings.append(f"Could not read ask.md for {entry.name}: {exc}")
                continue
            if "Modo:" not in ask_text:
                warnings.append(f"ask.md without explicit 'Modo:' in initiative {entry.name}")


def check_bitacora(errors):
    base = REPO_ROOT / "dev" / "records" / "bitacora"
    if not base.exists():
        errors.append("Missing folder: dev/records/bitacora")
        return

    for file in sorted(base.iterdir()):
        if not file.is_file():
            continue
        if file.name in {"README.md", ".gitkeep"}:
            continue
        if not BITACORA_FILE_PATTERN.match(file.name):
            errors.append(f"Invalid bitacora filename: {file.name}")


def check_templates(errors):
    base = REPO_ROOT / "dev" / "templates" / "initiative"
    if not base.exists():
        errors.append("Missing folder: dev/templates/initiative")
        return

    present = {f.name for f in base.iterdir() if f.is_file()}
    for required in sorted(TEMPLATE_REQUIRED_FILES):
        if required not in present:
            errors.append(f"Missing template file: dev/templates/initiative/{required}")


def check_adapters(errors):
    base = REPO_ROOT / "dev" / "ai" / "adapters"
    if not base.exists():
        errors.append("Missing folder: dev/ai/adapters")
        return

    present = {f.name for f in base.iterdir() if f.is_file()}
    for required in sorted(ADAPTER_REQUIRED_FILES):
        if required not in present:
            errors.append(f"Missing adapter file: dev/ai/adapters/{required}")


def main():
    errors = []
    warnings = []

    check_initiatives(errors, warnings)
    check_bitacora(errors)
    check_templates(errors)
    check_adapters(errors)

    print("Naming compliance report")
    print("------------------------")
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

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
