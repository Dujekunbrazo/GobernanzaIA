import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
INITIATIVE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}_[a-z0-9_]+$")

REQUIRED_FILES_BY_MODE = {
    "M3": {"ask.md", "execution.md", "closeout.md", "lessons_learned.md"},
    "M4": {
        "ask.md",
        "ask_audit.md",
        "plan.md",
        "plan_audit.md",
        "execution.md",
        "post_audit.md",
        "closeout.md",
        "lessons_learned.md",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preflight de iniciativa para gobernanza formal."
    )
    parser.add_argument("--initiative-id", required=True)
    parser.add_argument("--mode", required=True, choices=sorted(REQUIRED_FILES_BY_MODE))
    parser.add_argument(
        "--allow-dirty-with-ask-exception",
        action="store_true",
        help="Permite working tree sucio si ask.md registra excepción operativa.",
    )
    return parser.parse_args()


def git_output(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def ask_has_dirty_exception(ask_path: Path) -> bool:
    if not ask_path.exists():
        return False
    text = ask_path.read_text(encoding="utf-8", errors="ignore").lower()
    return "excepción operativa" in text and "worktree" in text and "sucio" in text


def print_report(errors: list[str], warnings: list[str], info: list[str]) -> None:
    print("Initiative preflight report")
    print("--------------------------")
    for item in info:
        print(f"- {item}")
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


def main() -> int:
    args = parse_args()
    errors: list[str] = []
    warnings: list[str] = []
    info: list[str] = []

    if not INITIATIVE_PATTERN.match(args.initiative_id):
        errors.append(f"Invalid initiative id: {args.initiative_id}")
        print_report(errors, warnings, info)
        return 1

    initiative_dir = REPO_ROOT / "dev" / "records" / "initiatives" / args.initiative_id
    ask_path = initiative_dir / "ask.md"

    info.append(f"initiative_id={args.initiative_id}")
    info.append(f"mode={args.mode}")

    if not initiative_dir.exists():
        errors.append(f"Missing initiative folder: {initiative_dir}")
    else:
        for name in sorted(REQUIRED_FILES_BY_MODE[args.mode]):
            if not (initiative_dir / name).exists():
                errors.append(f"Missing required file for {args.mode}: {name}")

    if ask_path.exists():
        ask_text = ask_path.read_text(encoding="utf-8", errors="ignore")
        if f"Modo: `{args.mode}`" not in ask_text and f"Modo: {args.mode}" not in ask_text:
            warnings.append(f"ask.md does not explicitly declare mode {args.mode}")

    try:
        branch = git_output("branch", "--show-current")
        dirty = git_output("status", "--porcelain")
    except RuntimeError as exc:
        errors.append(str(exc))
        print_report(errors, warnings, info)
        return 1

    info.append(f"branch={branch or '<detached>'}")
    info.append(f"dirty={'yes' if dirty else 'no'}")

    if not branch.startswith("initiative/"):
        warnings.append("Current branch does not use 'initiative/' prefix")
    else:
        expected_slug = args.initiative_id.replace("_", "-")
        if branch != f"initiative/{expected_slug}":
            warnings.append(
                f"Branch does not match initiative slug: expected initiative/{expected_slug}"
            )

    if dirty:
        if args.allow_dirty_with_ask_exception and ask_has_dirty_exception(ask_path):
            warnings.append("Dirty worktree allowed by explicit exception in ask.md")
        else:
            errors.append(
                "Working tree is dirty. Clean it or register explicit exception and rerun with --allow-dirty-with-ask-exception"
            )

    print_report(errors, warnings, info)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
