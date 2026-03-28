from __future__ import annotations

import contextlib
import json
import shutil
import unittest
import uuid
from pathlib import Path

from scripts.dev import governance_orchestrator as orch


class GovernanceOrchestratorTests(unittest.TestCase):
    @contextlib.contextmanager
    def make_tempdir(self):
        root = Path.cwd() / ".tmp_governance_orchestrator_tests" / uuid.uuid4().hex
        root.mkdir(parents=True, exist_ok=True)
        try:
            yield root
        finally:
            shutil.rmtree(root, ignore_errors=True)

    def test_ensure_local_runtime_creates_scaffold(self) -> None:
        with self.make_tempdir() as repo_root:
            (repo_root / ".git" / "info").mkdir(parents=True)
            runtime_root = orch.ensure_local_runtime(repo_root)
            self.assertTrue((runtime_root / "config").exists())
            self.assertTrue((runtime_root / "sessions").exists())
            self.assertTrue((runtime_root / ".gitignore").exists())
            exclude = (repo_root / ".git" / "info" / "exclude").read_text(encoding="utf-8")
            self.assertIn(".orchestrator_local/", exclude)

    def test_session_id_is_stable(self) -> None:
        target = Path("C:/tmp/repo")
        self.assertEqual(
            orch.session_id_for(target, "2026-03-28_demo"),
            orch.session_id_for(target, "2026-03-28_demo"),
        )

    def test_build_prompt_includes_base_prompt_and_write_set(self) -> None:
        with self.make_tempdir() as repo_root:
            (repo_root / ".git" / "info").mkdir(parents=True)
            target_repo = repo_root / "target"
            (target_repo / "dev" / "records" / "initiatives" / "2026-03-28_demo").mkdir(parents=True)
            ctx = orch.build_session_context(target_repo, "2026-03-28_demo")
            prompt = orch.build_prompt(ctx, "F1")
            self.assertIn("F1 Ask", prompt)
            self.assertIn("Puedes escribir solo:", prompt)
            self.assertIn("ask.md", prompt)

    def test_snapshot_uses_ping_pong_state_machine(self) -> None:
        with self.make_tempdir() as repo_root:
            root = repo_root / "initiative"
            root.mkdir(parents=True)
            ask = root / "ask.md"
            ask.write_text(
                "# ASK\n\n- Estado: PROPUESTO\n\n## Objetivo y contexto\n\nTexto listo.\n",
                encoding="utf-8",
            )
            paths = orch.gpp.InitiativePaths(
                initiative_id="2026-03-28_demo",
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
            snap = orch.snapshot(paths)
            self.assertEqual(snap["next_step"], "WAITING_FOR_F2")

    def test_persist_session_writes_snapshot(self) -> None:
        with self.make_tempdir() as repo_root:
            (repo_root / ".git" / "info").mkdir(parents=True)
            target_repo = repo_root / "target"
            initiative_root = target_repo / "dev" / "records" / "initiatives" / "2026-03-28_demo"
            initiative_root.mkdir(parents=True)
            ask = initiative_root / "ask.md"
            ask.write_text("# ASK\n\n- Estado: PROPUESTO\n\n## Objetivo y contexto\n\nTexto listo.\n", encoding="utf-8")
            ctx = orch.build_session_context(target_repo, "2026-03-28_demo")
            ctx.paths.ask.write_text(ask.read_text(encoding="utf-8"), encoding="utf-8")
            data = orch.persist_session(ctx)
            stored = json.loads(ctx.session_file.read_text(encoding="utf-8"))
            self.assertEqual(stored["session_id"], ctx.session_id)
            self.assertEqual(data["snapshot"]["next_step"], "WAITING_FOR_F2")


if __name__ == "__main__":
    unittest.main()
