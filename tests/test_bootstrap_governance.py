from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.migration import bootstrap_governance as bg


class BootstrapGovernanceTests(unittest.TestCase):
    def test_core_pack_collects_orchestrator_and_governance_templates(self) -> None:
        sources = bg.collect_sources(["core"])
        rel_paths = {path.relative_to(bg.REPO_ROOT) for path in sources}
        # Orchestrator: solo execution_checkpoint.md existe en el kit
        self.assertIn(Path("dev/templates/orchestrator/execution_checkpoint.md"), rel_paths)
        self.assertIn(Path("dev/templates/governance/repo_governance_profile.md"), rel_paths)
        self.assertIn(Path("dev/templates/governance/weekly_briefing.md"), rel_paths)
        self.assertIn(Path("dev/templates/governance/weekly_review.md"), rel_paths)
        self.assertIn(Path("dev/templates/governance/architecture_findings_register.md"), rel_paths)
        self.assertIn(Path("dev/templates/governance/adapter_template.md"), rel_paths)
        self.assertIn(Path("dev/records/reviews/README.md"), rel_paths)
        self.assertIn(Path("dev/records/reviews/weekly/.gitkeep"), rel_paths)
        self.assertIn(Path("doc/governance_prompts/20_weekly_mit_review.md"), rel_paths)
        self.assertIn(Path("dev/policies/weekly_review_policy.md"), rel_paths)

    def test_core_pack_collects_skills_recursively(self) -> None:
        """v0.2.0: dev/skills/ se incluye en core con glob recursivo."""
        sources = bg.collect_sources(["core"])
        rel_paths = {path.relative_to(bg.REPO_ROOT) for path in sources}
        # SKILL_CONTRACT y REGISTRY estan en core.files
        self.assertIn(Path("dev/skills/SKILL_CONTRACT.md"), rel_paths)
        self.assertIn(Path("dev/skills/REGISTRY.md"), rel_paths)
        # Las SKILL.md anidadas se recogen por glob recursivo
        self.assertIn(Path("dev/skills/f1_plan_creation/SKILL.md"), rel_paths)
        self.assertIn(Path("dev/skills/f2_plan_audit/SKILL.md"), rel_paths)
        self.assertIn(Path("dev/skills/f6_closeout/SKILL.md"), rel_paths)
        self.assertIn(Path("dev/skills/f7_lessons/SKILL.md"), rel_paths)

    def test_core_pack_collects_new_canon_scripts(self) -> None:
        """v0.2.0: memory_precheck + check_clock_canon + refresh_*.ps1 viajan en core."""
        sources = bg.collect_sources(["core"])
        rel_paths = {path.relative_to(bg.REPO_ROOT) for path in sources}
        self.assertIn(Path("scripts/dev/memory_precheck.py"), rel_paths)
        self.assertIn(Path("scripts/dev/check_clock_canon.py"), rel_paths)
        self.assertIn(Path("scripts/dev/check_structural_tooling_ready.py"), rel_paths)
        self.assertIn(Path("scripts/dev/refresh_symdex_index.ps1"), rel_paths)
        self.assertIn(Path("scripts/dev/refresh_codebase_memory_index.ps1"), rel_paths)
        self.assertIn(Path("scripts/dev/refresh_governance_retrieval_index.ps1"), rel_paths)
        self.assertIn(Path("scripts/ops/context_mcp/refresh_governance_index.mjs"), rel_paths)
        self.assertIn(Path("dev/governance_guide.md"), rel_paths)

    def test_argparse_accepts_arbitrary_ia_outside_catalog(self) -> None:
        """v0.2.0: --with-ia acepta cualquier string (no esta restringido a IA_CATALOG)."""
        with tempfile.TemporaryDirectory() as tmp:
            argv = [
                "bootstrap_governance.py",
                "--target", tmp,
                "--with-ia", "codex",
                "--with-ia", "kimi",
                "--preferred-working-ia", "kimi",
                "--preferred-auditor-ia", "codex",
            ]
            with mock.patch("sys.argv", argv):
                args = bg.parse_args()
            self.assertEqual(args.with_ia, ["codex", "kimi"])
            self.assertEqual(args.preferred_working_ia, "kimi")
            self.assertEqual(args.preferred_auditor_ia, "codex")

    def test_ia_catalog_contains_minimum_expected_ias(self) -> None:
        """v0.2.0: IA_CATALOG incluye al menos las 10 IAs documentadas."""
        expected = {"claude", "codex", "gpt", "gemini", "kimi",
                    "grok", "deepseek", "qwen", "mistral", "llama"}
        self.assertTrue(expected.issubset(set(bg.IA_CATALOG)))

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

    def test_parse_args_defaults_symdex_semantic_backend_to_local(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            argv = [
                "bootstrap_governance.py",
                "--target",
                tmp,
                "--with-ia",
                "codex",
                "--with-ia",
                "claude",
                "--preferred-working-ia",
                "codex",
                "--preferred-auditor-ia",
                "claude",
            ]
            with mock.patch("sys.argv", argv):
                args = bg.parse_args()
            self.assertEqual(args.symdex_semantic_backend, "local")


if __name__ == "__main__":
    unittest.main()
