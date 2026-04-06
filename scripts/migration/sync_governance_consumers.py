"""
Sync the canonical governance baseline from GobernanzaIA into known consumers.

This script is intentionally run from the source repository. It reuses
bootstrap_governance.py and preserves an existing consumer installation profile
when a governance manifest is already present. The local repo capabilities
profile remains consumer-owned overlay.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
BOOTSTRAP_PATH = REPO_ROOT / "scripts" / "migration" / "bootstrap_governance.py"
MANIFEST_PATH = Path("dev/governance_baseline.json")


@dataclass(frozen=True)
class ConsumerProfile:
    key: str
    repo_dir: str
    installed_ias: tuple[str, ...]
    preferred_working_ia: str
    preferred_auditor_ia: str
    include_packs: tuple[str, ...]


KNOWN_CONSUMERS: dict[str, ConsumerProfile] = {
    "kiminion": ConsumerProfile(
        key="kiminion",
        repo_dir="Kiminion",
        installed_ias=("codex", "claude", "roo"),
        preferred_working_ia="codex",
        preferred_auditor_ia="claude",
        include_packs=("governance_search", "symdex"),
    ),
    "mcp_boletinesoficiales": ConsumerProfile(
        key="mcp_boletinesoficiales",
        repo_dir="MCP_Boletinesoficiales",
        installed_ias=("codex", "claude"),
        preferred_working_ia="codex",
        preferred_auditor_ia="claude",
        include_packs=("governance_search", "symdex"),
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync governance baseline from GobernanzaIA into known consumers."
    )
    parser.add_argument(
        "--consumer",
        action="append",
        choices=sorted(KNOWN_CONSUMERS),
        help="Known consumer to sync. Repeat the flag to sync multiple consumers.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing baseline files in the consumer.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned actions without modifying consumer repositories.",
    )
    return parser.parse_args()


def load_existing_manifest(target_root: Path) -> dict | None:
    manifest_path = target_root / MANIFEST_PATH
    if not manifest_path.exists():
        return None
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def effective_profile(profile: ConsumerProfile, target_root: Path) -> ConsumerProfile:
    manifest = load_existing_manifest(target_root)
    if manifest is None:
        return profile

    installation_profile = manifest.get("installation_profile") or {}
    packs = tuple(
        pack
        for pack in (manifest.get("packs") or [])
        if pack not in {"core", "claude", "codex", "gemini", "roo"}
    )
    installed_ias = tuple(installation_profile.get("installed_ias") or profile.installed_ias)
    preferred_working_ia = installation_profile.get("preferred_working_ia") or profile.preferred_working_ia
    preferred_auditor_ia = installation_profile.get("preferred_auditor_ia") or profile.preferred_auditor_ia

    return ConsumerProfile(
        key=profile.key,
        repo_dir=profile.repo_dir,
        installed_ias=installed_ias,
        preferred_working_ia=preferred_working_ia,
        preferred_auditor_ia=preferred_auditor_ia,
        include_packs=packs or profile.include_packs,
    )


def resolve_target_root(profile: ConsumerProfile) -> Path:
    return (REPO_ROOT.parent / profile.repo_dir).resolve()


def build_bootstrap_command(
    *,
    target_root: Path,
    profile: ConsumerProfile,
    force: bool,
    dry_run: bool,
) -> list[str]:
    command = [sys.executable, str(BOOTSTRAP_PATH), "--target", str(target_root)]
    for ia_name in profile.installed_ias:
        command.extend(["--with-ia", ia_name])
    command.extend(["--preferred-working-ia", profile.preferred_working_ia])
    command.extend(["--preferred-auditor-ia", profile.preferred_auditor_ia])
    for pack_name in profile.include_packs:
        command.extend(["--include-pack", pack_name])
    if force:
        command.append("--force")
    if dry_run:
        command.append("--dry-run")
    return command


def main() -> int:
    args = parse_args()
    consumer_keys = args.consumer or list(KNOWN_CONSUMERS)

    print("Governance consumer sync")
    print("------------------------")
    print(f"Source: {REPO_ROOT}")
    print(f"Consumers: {', '.join(consumer_keys)}")
    print(f"Mode: {'dry-run' if args.dry_run else 'write'}")

    for consumer_key in consumer_keys:
        base_profile = KNOWN_CONSUMERS[consumer_key]
        target_root = resolve_target_root(base_profile)
        if not target_root.exists():
            raise FileNotFoundError(
                f"Known consumer '{consumer_key}' not found at expected path: {target_root}"
            )

        profile = effective_profile(base_profile, target_root)
        command = build_bootstrap_command(
            target_root=target_root,
            profile=profile,
            force=args.force,
            dry_run=args.dry_run,
        )
        print(f"\nSYNC {consumer_key}: {target_root}")
        print(" ".join(command))
        subprocess.run(command, check=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
