"""
Bootstrap governance files into a target repository.

Usage:
    python scripts/migration/bootstrap_governance.py --target <path>
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def collect_sources(include_claude_root: bool) -> list[Path]:
    required_files = [
        Path("AGENTS.md"),
        Path("dev/workflow.md"),
        Path("dev/ai/README.md"),
        Path("dev/checklists/state0.md"),
        Path("dev/logs/decisions.md"),
        Path("dev/records/README.md"),
        Path("dev/records/bitacora/README.md"),
        Path("dev/records/bitacora/.gitkeep"),
        Path("dev/records/initiatives/.gitkeep"),
        Path("scripts/README.md"),
        Path("scripts/ops/bitacora_append.py"),
        Path("scripts/dev/check_naming_compliance.py"),
        Path("scripts/dev/check_state0.py"),
        Path("scripts/bitacora_append.py"),
    ]

    if include_claude_root:
        required_files.insert(1, Path("CLAUDE.md"))

    required_dirs = [
        Path("dev/guarantees"),
        Path("dev/policies"),
        Path("dev/ai/adapters"),
        Path("dev/templates/initiative"),
    ]

    sources = [REPO_ROOT / rel for rel in required_files]
    for rel_dir in required_dirs:
        abs_dir = REPO_ROOT / rel_dir
        for file in sorted(abs_dir.glob("*.md")):
            sources.append(file)

    missing = [src for src in sources if not src.exists()]
    if missing:
        lines = ["Missing source files in governance pack:"]
        lines.extend(f"- {path}" for path in missing)
        raise FileNotFoundError("\n".join(lines))

    return sources


def copy_sources(sources: list[Path], target_root: Path, force: bool, dry_run: bool) -> tuple[int, int]:
    copied = 0
    skipped = 0

    for src in sources:
        rel = src.relative_to(REPO_ROOT)
        dst = target_root / rel

        if dst.exists() and not force:
            skipped += 1
            print(f"SKIP (exists): {rel}")
            continue

        if dry_run:
            action = "OVERWRITE" if dst.exists() else "COPY"
            print(f"{action}: {rel}")
            copied += 1
            continue

        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied += 1
        print(f"COPIED: {rel}")

    return copied, skipped


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy governance baseline into another repository."
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Target repository path where governance files will be copied.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite files that already exist in target.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be copied without writing files.",
    )
    parser.add_argument(
        "--skip-claude-root",
        action="store_true",
        help="Do not copy CLAUDE.md to target root.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target_root = Path(args.target).expanduser().resolve()

    if not args.dry_run:
        target_root.mkdir(parents=True, exist_ok=True)

    sources = collect_sources(include_claude_root=not args.skip_claude_root)
    copied, skipped = copy_sources(
        sources=sources,
        target_root=target_root,
        force=args.force,
        dry_run=args.dry_run,
    )

    print("\nGovernance bootstrap summary")
    print("----------------------------")
    print(f"Target: {target_root}")
    print(f"Copied: {copied}")
    print(f"Skipped: {skipped}")
    print(f"Mode: {'dry-run' if args.dry_run else 'write'}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
