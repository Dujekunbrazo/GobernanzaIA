import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BITACORA_DIR = REPO_ROOT / "dev" / "records" / "bitacora"
ENTRY_SPLIT = re.compile(r"(?=^###\s+\d{2}:\d{2}:\d{2}\s*$)", re.MULTILINE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Valida que exista evidencia de bitacora para una IA o iniciativa."
    )
    parser.add_argument("--initiative-id", default="", help="Filter entries by initiative id")
    parser.add_argument("--ia", default="", help="Filter files by IA slug, for example codex")
    parser.add_argument("--phase", default="", help="Require matching phase within the entry")
    parser.add_argument("--date", default="", help="Restrict search to YYYY-MM-DD")
    parser.add_argument("--require-count", type=int, default=1, help="Minimum matching entries")
    return parser.parse_args()


def list_target_files(date_filter: str, ia_filter: str) -> list[Path]:
    if not BITACORA_DIR.exists():
        return []
    pattern = "*.md"
    files = sorted(path for path in BITACORA_DIR.glob(pattern) if path.is_file())
    targets: list[Path] = []
    for path in files:
        stem = path.stem
        if "_" not in stem:
            continue
        file_date, file_ia = stem.split("_", 1)
        if date_filter and file_date != date_filter:
            continue
        if ia_filter and file_ia != ia_filter:
            continue
        targets.append(path)
    return targets


def split_entries(text: str) -> list[str]:
    chunks = [chunk.strip() for chunk in ENTRY_SPLIT.split(text) if chunk.strip()]
    return [chunk for chunk in chunks if chunk.startswith("### ")]


def entry_matches(entry: str, initiative_id: str, phase: str) -> bool:
    if initiative_id and f"- Initiative ID: `{initiative_id}`" not in entry:
        return False
    if phase and f"- Fase: `{phase}`" not in entry:
        return False
    return True


def main() -> int:
    args = parse_args()
    ia_filter = args.ia.strip().lower()
    initiative_id = args.initiative_id.strip()
    phase = args.phase.strip()
    date_filter = args.date.strip()

    errors: list[str] = []
    info: list[str] = []
    matches: list[str] = []

    if not BITACORA_DIR.exists():
        errors.append(f"Missing bitacora directory: {BITACORA_DIR}")
    target_files = list_target_files(date_filter=date_filter, ia_filter=ia_filter)
    if not target_files:
        errors.append("No bitacora files matched the requested filters")

    for path in target_files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for index, entry in enumerate(split_entries(text), start=1):
            if entry_matches(entry, initiative_id=initiative_id, phase=phase):
                matches.append(f"{path.name}#entry{index}")

    info.append(f"filters: ia={ia_filter or '*'} initiative={initiative_id or '*'} phase={phase or '*'} date={date_filter or '*'}")
    info.append(f"matched_entries={len(matches)}")

    if len(matches) < args.require_count:
        errors.append(
            f"Expected at least {args.require_count} matching bitacora entries but found {len(matches)}"
        )

    print("Bitacora compliance report")
    print("-------------------------")
    for item in info:
        print(f"- {item}")
    print(f"Errors: {len(errors)}")
    if matches:
        print("\nMatches:")
        for item in matches:
            print(f"- {item}")
    if errors:
        print("\nErrors:")
        for item in errors:
            print(f"- {item}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
