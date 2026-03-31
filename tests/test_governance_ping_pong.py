from __future__ import annotations

import contextlib
import shutil
import unittest
import uuid
from pathlib import Path
from unittest import mock

from scripts.dev import governance_ping_pong as gpp


class GovernancePingPongTests(unittest.TestCase):
    @contextlib.contextmanager
    def make_tempdir(self):
        root = Path.cwd() / ".tmp_governance_ping_pong_tests" / uuid.uuid4().hex
        root.mkdir(parents=True, exist_ok=True)
        try:
            yield str(root)
        finally:
            shutil.rmtree(root, ignore_errors=True)

    def test_replace_metadata_line_updates_existing_field(self) -> None:
        text = "# ASK\n\n- Estado: PROPUESTO\n"
        result = gpp.replace_metadata_line(text, "Estado", "VALIDADO")
        self.assertIn("- Estado: VALIDADO", result)
        self.assertNotIn("- Estado: PROPUESTO", result)

    def test_recommend_next_step_waits_for_f2_after_seeded_ask(self) -> None:
        with self.make_tempdir() as tmpdir:
            root = Path(tmpdir)
            ask = root / "ask.md"
            ask.write_text(
                "# ASK\n\n- Estado: PROPUESTO\n\n## Objetivo y contexto\n\nTexto listo.\n",
                encoding="utf-8",
            )
            paths = gpp.InitiativePaths(
                initiative_id="2026-03-27_demo",
                root=root,
                ask=ask,
                ask_audit=root / "ask_audit.md",
                handoff=root / "handoff.md",
                plan=root / "plan.md",
                plan_audit=root / "plan_audit.md",
                execution=root / "execution.md",
                post_audit=root / "post_audit.md",
                closeout=root / "closeout.md",
                lessons=root / "lessons_learned.md",
                real_validation=root / "real_validation.md",
            )
            self.assertEqual(gpp.recommend_next_step(paths), "WAITING_FOR_F2")

    def test_init_creates_required_artifacts(self) -> None:
        with self.make_tempdir() as tmpdir:
            repo_root = Path(tmpdir)
            initiatives_root = repo_root / "dev" / "records" / "initiatives"
            template_root = repo_root / "dev" / "templates" / "initiative"
            template_root.mkdir(parents=True)
            for name in gpp.M4_ARTIFACTS:
                (template_root / name).write_text("# TEMPLATE\n- Initiative ID:\n", encoding="utf-8")
            for name in gpp.OPTIONAL_ARTIFACTS:
                (template_root / name).write_text("# TEMPLATE\n- Initiative ID:\n", encoding="utf-8")
            with mock.patch.object(gpp, "REPO_ROOT", repo_root), mock.patch.object(
                gpp, "INITIATIVES_ROOT", initiatives_root
            ), mock.patch.object(gpp, "TEMPLATE_ROOT", template_root), mock.patch.object(
                gpp, "get_git_branch", return_value="initiative/2026-03-27-demo"
            ):
                parser = gpp.build_parser()
                args = parser.parse_args(
                    [
                        "init",
                        "--initiative-id",
                        "2026-03-27_demo",
                        "--with-handoff",
                    ]
                )
                exit_code = args.func(args)
                self.assertEqual(exit_code, 0)
                created = initiatives_root / "2026-03-27_demo"
                for name in gpp.M4_ARTIFACTS:
                    self.assertTrue((created / name).exists(), name)
                self.assertTrue((created / "handoff.md").exists())
                ask_text = (created / "ask.md").read_text(encoding="utf-8")
                self.assertIn("- Rama: initiative/2026-03-27-demo", ask_text)

    def test_declared_branch_defaults_to_planned_slug(self) -> None:
        with self.make_tempdir() as tmpdir:
            root = Path(tmpdir)
            paths = gpp.InitiativePaths(
                initiative_id="2026-03-27_demo",
                root=root,
                ask=root / "ask.md",
                ask_audit=root / "ask_audit.md",
                handoff=root / "handoff.md",
                plan=root / "plan.md",
                plan_audit=root / "plan_audit.md",
                execution=root / "execution.md",
                post_audit=root / "post_audit.md",
                closeout=root / "closeout.md",
                lessons=root / "lessons_learned.md",
                real_validation=root / "real_validation.md",
            )
            self.assertEqual(gpp.declared_branch(paths), "initiative/2026-03-27-demo")

    def test_configure_repo_root_switches_runtime_paths(self) -> None:
        with self.make_tempdir() as tmpdir:
            repo_root = Path(tmpdir).resolve()
            original_repo = gpp.REPO_ROOT
            original_initiatives = gpp.INITIATIVES_ROOT
            original_templates = gpp.TEMPLATE_ROOT
            try:
                gpp.configure_repo_root(str(repo_root))
                self.assertEqual(gpp.REPO_ROOT, repo_root)
                self.assertEqual(gpp.INITIATIVES_ROOT, repo_root / "dev" / "records" / "initiatives")
                self.assertEqual(gpp.TEMPLATE_ROOT, repo_root / "dev" / "templates" / "initiative")
            finally:
                gpp.REPO_ROOT = original_repo
                gpp.INITIATIVES_ROOT = original_initiatives
                gpp.TEMPLATE_ROOT = original_templates


if __name__ == "__main__":
    unittest.main()
