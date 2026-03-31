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
            original_ensure_runtime = orch.ensure_local_runtime
            try:
                orch.ensure_local_runtime = lambda base_repo=None: original_ensure_runtime(repo_root)
                ctx = orch.build_session_context(target_repo, "2026-03-28_demo")
                prompt = orch.build_prompt(ctx, "F1")
                self.assertIn("F1 Ask", prompt)
                self.assertIn("Puedes escribir solo:", prompt)
                self.assertIn("ask.md", prompt)
            finally:
                orch.ensure_local_runtime = original_ensure_runtime

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
            original_ensure_runtime = orch.ensure_local_runtime
            try:
                orch.ensure_local_runtime = lambda base_repo=None: original_ensure_runtime(repo_root)
                ctx = orch.build_session_context(target_repo, "2026-03-28_demo")
                ctx.paths.ask.write_text(ask.read_text(encoding="utf-8"), encoding="utf-8")
                data = orch.persist_session(ctx)
                stored = json.loads(ctx.session_file.read_text(encoding="utf-8"))
                self.assertEqual(stored["session_id"], ctx.session_id)
                self.assertEqual(data["snapshot"]["next_step"], "WAITING_FOR_F2")
            finally:
                orch.ensure_local_runtime = original_ensure_runtime

    def test_workflow_state_uses_override_phase(self) -> None:
        with self.make_tempdir() as repo_root:
            root = repo_root / "initiative"
            root.mkdir(parents=True)
            plan = root / "plan.md"
            plan.write_text("# PLAN\n\n- Estado: CONGELADO\n\n## Objetivo\n\nTexto listo.\n", encoding="utf-8")
            plan_audit = root / "plan_audit.md"
            plan_audit.write_text("# PLAN AUDIT\n\n- Veredicto: PASS\n", encoding="utf-8")
            paths = orch.gpp.InitiativePaths(
                initiative_id="2026-03-28_demo",
                root=root,
                ask=root / "ask.md",
                ask_audit=root / "ask_audit.md",
                handoff=root / "handoff.md",
                plan=plan,
                plan_audit=plan_audit,
                execution=root / "execution.md",
                post_audit=root / "post_audit.md",
                closeout=root / "closeout.md",
                lessons=root / "lessons_learned.md",
                real_validation=root / "real_validation.md",
            )
            state = orch.workflow_state(paths, override_phase="F5")
            self.assertEqual(state["next_step"], "RUN_F5")
            self.assertEqual(state["recommended_next_step"], "RUN_F6_F7")
            self.assertEqual(state["phase"], "F5")

    def test_reopen_f5_resets_plan_audit_and_plan_state(self) -> None:
        with self.make_tempdir() as repo_root:
            (repo_root / ".git" / "info").mkdir(parents=True)
            target_repo = repo_root / "target"
            template_root = target_repo / "dev" / "templates" / "initiative"
            template_root.mkdir(parents=True)
            (template_root / "plan_audit.md").write_text(
                "# PLAN AUDIT\n\n- Initiative ID:\n- Fase: F5\n- Auditor:\n- Fecha:\n- Veredicto: PASS | FAIL\n",
                encoding="utf-8",
            )
            (target_repo / "AGENTS.md").write_text("x\n", encoding="utf-8")
            (target_repo / "scripts" / "dev").mkdir(parents=True)
            (target_repo / "scripts" / "dev" / "initiative_preflight.py").write_text("print('ok')\n", encoding="utf-8")
            initiative_root = target_repo / "dev" / "records" / "initiatives" / "2026-03-28_demo"
            initiative_root.mkdir(parents=True)
            (initiative_root / "ask.md").write_text("# ASK\n\n- motor_auditor: codex\n", encoding="utf-8")
            (initiative_root / "plan.md").write_text("# PLAN\n\n- Estado: CONGELADO\n\n## Objetivo\n\nTexto listo.\n", encoding="utf-8")
            (initiative_root / "plan_audit.md").write_text("# PLAN AUDIT\n\n- Veredicto: PASS\n", encoding="utf-8")
            original_template_root = orch.gpp.TEMPLATE_ROOT
            original_ensure_runtime = orch.ensure_local_runtime
            try:
                orch.gpp.TEMPLATE_ROOT = template_root
                orch.ensure_local_runtime = lambda base_repo=None: original_ensure_runtime(repo_root)
                parser = orch.build_parser()
                args = parser.parse_args(
                    [
                        "--target-repo",
                        str(target_repo),
                        "--initiative-id",
                        "2026-03-28_demo",
                        "reopen-phase",
                        "--phase",
                        "F5",
                    ]
                )
                exit_code = args.func(args)
                self.assertEqual(exit_code, 0)
                self.assertIn("- Estado: PROPUESTO", (initiative_root / "plan.md").read_text(encoding="utf-8"))
                self.assertIn("- Fase: F5", (initiative_root / "plan_audit.md").read_text(encoding="utf-8"))
                ctx = orch.build_session_context(target_repo, "2026-03-28_demo")
                session = json.loads(ctx.session_file.read_text(encoding="utf-8"))
                self.assertEqual(session["override_phase"], "F5")
                self.assertEqual(session["snapshot"]["next_step"], "RUN_F5")
            finally:
                orch.gpp.TEMPLATE_ROOT = original_template_root
                orch.ensure_local_runtime = original_ensure_runtime


if __name__ == "__main__":
    unittest.main()
