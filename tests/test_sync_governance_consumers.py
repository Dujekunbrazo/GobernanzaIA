from __future__ import annotations

import unittest
from pathlib import Path

from scripts.migration import sync_governance_consumers as sync


class SyncGovernanceConsumersTests(unittest.TestCase):
    def test_build_bootstrap_command_includes_profile_and_packs(self) -> None:
        profile = sync.ConsumerProfile(
            key="kiminion",
            repo_dir="Kiminion",
            installed_ias=("codex", "claude"),
            preferred_working_ia="codex",
            preferred_auditor_ia="claude",
            include_packs=("governance_search", "symdex", "codebase_memory"),
        )
        target_root = Path("C:/repos/Kiminion")
        command = sync.build_bootstrap_command(
            target_root=target_root,
            profile=profile,
            force=True,
            dry_run=True,
        )
        rendered = " ".join(command)
        self.assertIn("--with-ia codex", rendered)
        self.assertIn("--with-ia claude", rendered)
        self.assertIn("--include-pack governance_search", rendered)
        self.assertIn("--include-pack symdex", rendered)
        self.assertIn("--include-pack codebase_memory", rendered)
        self.assertIn("--force", rendered)
        self.assertIn("--dry-run", rendered)


if __name__ == "__main__":
    unittest.main()
