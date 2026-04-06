from __future__ import annotations

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


if __name__ == "__main__":
    unittest.main()
