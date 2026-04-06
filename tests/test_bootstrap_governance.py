from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.migration import bootstrap_governance as bg


class BootstrapGovernanceTests(unittest.TestCase):
    def test_core_pack_collects_orchestrator_and_governance_templates(self) -> None:
        sources = bg.collect_sources(["core"])
        rel_paths = {path.relative_to(bg.REPO_ROOT) for path in sources}
        self.assertIn(Path("dev/templates/orchestrator/phase_ticket.md"), rel_paths)
        self.assertIn(Path("dev/templates/orchestrator/resume_packet.md"), rel_paths)
        self.assertIn(Path("dev/templates/governance/repo_governance_profile.md"), rel_paths)

    def test_ensure_repo_governance_profile_preserves_existing_overlay(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target_root = Path(tmp)
            overlay = target_root / "dev" / "repo_governance_profile.md"
            overlay.parent.mkdir(parents=True, exist_ok=True)
            overlay.write_text("local overlay\n", encoding="utf-8")
            result = bg.ensure_repo_governance_profile(target_root, dry_run=False)
            self.assertEqual(result, "preserved")
            self.assertEqual(overlay.read_text(encoding="utf-8"), "local overlay\n")

    def test_ensure_repo_governance_profile_writes_from_template_when_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target_root = Path(tmp)
            result = bg.ensure_repo_governance_profile(target_root, dry_run=False)
            self.assertEqual(result, "written")
            overlay = target_root / "dev" / "repo_governance_profile.md"
            self.assertTrue(overlay.exists())
            self.assertIn("# REPO GOVERNANCE PROFILE", overlay.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
