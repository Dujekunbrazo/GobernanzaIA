from __future__ import annotations

import contextlib
import json
import shutil
import unittest
import uuid
from pathlib import Path
from unittest import mock

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
                self.assertIn("dev/records/initiatives/2026-03-28_demo/ask.md", prompt)
                self.assertNotIn(str(ctx.paths.ask), prompt)
            finally:
                orch.ensure_local_runtime = original_ensure_runtime

    def test_f4_remediation_prompt_does_not_include_pre00_prompt_99(self) -> None:
        with self.make_tempdir() as repo_root:
            (repo_root / ".git" / "info").mkdir(parents=True)
            target_repo = repo_root / "target"
            initiative_root = target_repo / "dev" / "records" / "initiatives" / "2026-03-28_demo"
            initiative_root.mkdir(parents=True)
            (initiative_root / "handoff.md").write_text("# handoff\n", encoding="utf-8")
            (initiative_root / "ask.md").write_text("# ASK\n\n- Estado: CONGELADO\n", encoding="utf-8")
            (initiative_root / "ask_audit.md").write_text("# ASK AUDIT\n\n- Veredicto: PASS\n", encoding="utf-8")
            (initiative_root / "plan_audit.md").write_text("# PLAN AUDIT\n\n- Veredicto: FAIL\n", encoding="utf-8")
            original_ensure_runtime = orch.ensure_local_runtime
            try:
                orch.ensure_local_runtime = lambda base_repo=None: original_ensure_runtime(repo_root)
                ctx = orch.build_session_context(target_repo, "2026-03-28_demo")
                prompt = orch.build_prompt(ctx, "F4_REMEDIATION")
                self.assertIn("15_f4_remediacion_plan", str(orch.base_prompt_file_for_phase("F4_REMEDIATION")))
                self.assertNotIn("A continuación, el plan a analizar:", prompt)
                self.assertNotIn("99 prompt plan a codex", prompt)
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

    def test_build_phase_ticket_includes_repo_profile_when_present(self) -> None:
        with self.make_tempdir() as repo_root:
            (repo_root / ".git" / "info").mkdir(parents=True)
            target_repo = repo_root / "target"
            initiative_root = target_repo / "dev" / "records" / "initiatives" / "2026-03-28_demo"
            initiative_root.mkdir(parents=True)
            (target_repo / "dev").mkdir(parents=True, exist_ok=True)
            (target_repo / "dev" / "repo_governance_profile.md").write_text(
                "# REPO GOVERNANCE PROFILE\n\n- governance_search: DISPONIBLE\n- symdex_code: DISPONIBLE\n",
                encoding="utf-8",
            )
            (initiative_root / "ask.md").write_text("# ASK\n\n- Estado: PROPUESTO\n\n## Objetivo y contexto\n\nTexto listo.\n", encoding="utf-8")
            original_ensure_runtime = orch.ensure_local_runtime
            try:
                orch.ensure_local_runtime = lambda base_repo=None: original_ensure_runtime(repo_root)
                ctx = orch.build_session_context(target_repo, "2026-03-28_demo")
                ticket = orch.build_phase_ticket_content(ctx, "F1")
                self.assertIn("dev/repo_governance_profile.md", ticket)
            finally:
                orch.ensure_local_runtime = original_ensure_runtime

    def test_resume_packet_populates_capabilities_from_repo_profile(self) -> None:
        with self.make_tempdir() as repo_root:
            (repo_root / ".git" / "info").mkdir(parents=True)
            target_repo = repo_root / "target"
            initiative_root = target_repo / "dev" / "records" / "initiatives" / "2026-03-28_demo"
            initiative_root.mkdir(parents=True)
            (target_repo / "dev").mkdir(parents=True, exist_ok=True)
            (target_repo / "dev" / "repo_governance_profile.md").write_text(
                "\n".join(
                    [
                        "# REPO GOVERNANCE PROFILE",
                        "",
                        "- governance_search: DISPONIBLE",
                        "- symdex_code: DISPONIBLE",
                        "- codebase-memory-mcp: NO_DISPONIBLE",
                        "- F8 observable: SI",
                        "- trace on o equivalente: SI",
                        "- terminal/logs observables: SI",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            (initiative_root / "ask.md").write_text("# ASK\n\n- Estado: PROPUESTO\n\n## Objetivo y contexto\n\nTexto listo.\n", encoding="utf-8")
            original_ensure_runtime = orch.ensure_local_runtime
            try:
                orch.ensure_local_runtime = lambda base_repo=None: original_ensure_runtime(repo_root)
                ctx = orch.build_session_context(target_repo, "2026-03-28_demo")
                packet = orch.build_resume_packet_content(ctx, "F1")
                self.assertIn("Governance retrieval: DISPONIBLE", packet)
                self.assertIn("Memoria estructural (codebase-memory-mcp): NO_DISPONIBLE", packet)
                self.assertIn("Perfil local: dev/repo_governance_profile.md", packet)
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

    def test_last_receipt_reads_latest_phase_receipt(self) -> None:
        with self.make_tempdir() as repo_root:
            (repo_root / ".git" / "info").mkdir(parents=True)
            target_repo = repo_root / "target"
            initiative_root = target_repo / "dev" / "records" / "initiatives" / "2026-03-28_demo"
            initiative_root.mkdir(parents=True)
            original_ensure_runtime = orch.ensure_local_runtime
            try:
                orch.ensure_local_runtime = lambda base_repo=None: original_ensure_runtime(repo_root)
                ctx = orch.build_session_context(target_repo, "2026-03-28_demo")
                orch.write_json(
                    orch.receipt_file_for(ctx, "F5"),
                    {"phase": "F5", "engine": "codex", "snapshot": {"next_step": "RUN_F4_F5_REMEDIATION"}},
                )
                orch.persist_session(ctx, {"last_phase": "F5"})
                receipt = orch.latest_receipt(ctx)
                self.assertEqual(receipt["phase"], "F5")
                self.assertEqual(receipt["engine"], "codex")
            finally:
                orch.ensure_local_runtime = original_ensure_runtime

    def test_run_phase_failure_writes_failed_receipt_and_run_state(self) -> None:
        with self.make_tempdir() as repo_root:
            (repo_root / ".git" / "info").mkdir(parents=True)
            target_repo = repo_root / "target"
            initiative_root = target_repo / "dev" / "records" / "initiatives" / "2026-03-28_demo"
            initiative_root.mkdir(parents=True)
            (initiative_root / "handoff.md").write_text("# handoff\n", encoding="utf-8")
            (initiative_root / "ask.md").write_text("# ASK\n\n- Estado: CONGELADO\n", encoding="utf-8")
            (initiative_root / "ask_audit.md").write_text("# ASK AUDIT\n\n- Veredicto: PASS\n", encoding="utf-8")
            (initiative_root / "plan_audit.md").write_text("# PLAN AUDIT\n\n- Veredicto: FAIL\n", encoding="utf-8")
            original_ensure_runtime = orch.ensure_local_runtime
            try:
                orch.ensure_local_runtime = lambda base_repo=None: original_ensure_runtime(repo_root)
                ctx = orch.build_session_context(target_repo, "2026-03-28_demo")
                with mock.patch.object(orch, "run_claude", return_value=orch.output_file_for(ctx, "F4_REMEDIATION", "claude")):
                    with self.assertRaisesRegex(RuntimeError, "Expected meaningful plan content"):
                        orch.run_phase(ctx, "F4_REMEDIATION", dry_run=False)
                receipt = orch.read_json(orch.receipt_file_for(ctx, "F4_REMEDIATION"))
                run_state = orch.read_json(orch.run_state_file_for(ctx))
                session = orch.read_json(ctx.session_file)
                self.assertEqual(receipt["status"], "failed")
                self.assertEqual(run_state["status"], "failed")
                self.assertEqual(session["last_attempt_phase"], "F4_REMEDIATION")
                self.assertIn("Expected meaningful plan content", receipt["error"])
            finally:
                orch.ensure_local_runtime = original_ensure_runtime

    def test_ensure_phase_artifact_requires_fresh_update(self) -> None:
        with self.make_tempdir() as repo_root:
            plan = repo_root / "plan.md"
            plan.write_text("# PLAN\n\n- Estado: PROPUESTO\n\n## 1. Objetivo\n\nTexto valido.\n", encoding="utf-8")
            paths = orch.gpp.InitiativePaths(
                initiative_id="2026-03-28_demo",
                root=repo_root,
                ask=repo_root / "ask.md",
                ask_audit=repo_root / "ask_audit.md",
                handoff=repo_root / "handoff.md",
                plan=plan,
                plan_audit=repo_root / "plan_audit.md",
                execution=repo_root / "execution.md",
                post_audit=repo_root / "post_audit.md",
                closeout=repo_root / "closeout.md",
                lessons=repo_root / "lessons_learned.md",
                real_validation=repo_root / "real_validation.md",
            )
            with self.assertRaisesRegex(RuntimeError, "Expected updated artifact"):
                orch.ensure_phase_artifact(paths, "F4", previous_mtime_ns=plan.stat().st_mtime_ns)

    def test_recover_audit_artifact_writes_markdown_block_from_raw_output(self) -> None:
        with self.make_tempdir() as repo_root:
            (repo_root / ".git" / "info").mkdir(parents=True)
            target_repo = repo_root / "target"
            initiative_root = target_repo / "dev" / "records" / "initiatives" / "2026-03-28_demo"
            initiative_root.mkdir(parents=True)
            original_ensure_runtime = orch.ensure_local_runtime
            try:
                orch.ensure_local_runtime = lambda base_repo=None: original_ensure_runtime(repo_root)
                ctx = orch.build_session_context(target_repo, "2026-03-28_demo")
                output = orch.output_file_for(ctx, "F5", "codex")
                output.write_text(
                    "texto previo\n```md\n# PLAN AUDIT\n\n- Initiative ID: 2026-03-28_demo\n- Veredicto: FAIL\n```\n",
                    encoding="utf-8",
                )
                recovered = orch.recover_audit_artifact(ctx, "F5", output)
                self.assertTrue(recovered)
                self.assertIn("# PLAN AUDIT", ctx.paths.plan_audit.read_text(encoding="utf-8"))
            finally:
                orch.ensure_local_runtime = original_ensure_runtime

    def test_run_phase_recovers_f5_audit_when_raw_output_contains_artifact(self) -> None:
        with self.make_tempdir() as repo_root:
            (repo_root / ".git" / "info").mkdir(parents=True)
            target_repo = repo_root / "target"
            initiative_root = target_repo / "dev" / "records" / "initiatives" / "2026-03-28_demo"
            initiative_root.mkdir(parents=True)
            (initiative_root / "ask.md").write_text("# ASK\n\n- Estado: CONGELADO\n", encoding="utf-8")
            (initiative_root / "ask_audit.md").write_text("# ASK AUDIT\n\n- Veredicto: PASS\n", encoding="utf-8")
            (initiative_root / "plan.md").write_text("# PLAN\n\n- Estado: PROPUESTO\n\n## 1. Objetivo\n\nTexto valido.\n", encoding="utf-8")
            (initiative_root / "handoff.md").write_text("# HANDOFF\n", encoding="utf-8")
            (initiative_root / "plan_audit.md").write_text("# PLAN AUDIT\n\n- Veredicto: FAIL\n", encoding="utf-8")
            original_ensure_runtime = orch.ensure_local_runtime
            try:
                orch.ensure_local_runtime = lambda base_repo=None: original_ensure_runtime(repo_root)
                ctx = orch.build_session_context(target_repo, "2026-03-28_demo")
                output = orch.output_file_for(ctx, "F5", "codex")
                output.write_text(
                    "```md\n"
                    "# PLAN AUDIT\n\n"
                    "- Initiative ID: 2026-03-28_demo\n"
                    "- Fase: F5\n"
                    "- Auditor: codex\n"
                    "- Fecha: 2026-03-28\n"
                    "- Veredicto: PASS\n"
                    "- Motor sugerido: N/A\n"
                    "- Esfuerzo sugerido: n/a\n"
                    "\n## Hallazgos\n\n"
                    "- Sin hallazgos materiales ni pendientes.\n"
                    "\n## Justificación del veredicto\n\n"
                    "- No quedan hallazgos materiales ni pendientes.\n"
                    "\n## Escalado de remediacion\n\n"
                    "- Motor sugerido: N/A\n"
                    "- Esfuerzo sugerido: n/a\n"
                    "- Motivo: No aplica.\n"
                    "\n## Condición para F5\n\n"
                    "- Puede congelarse el plan.\n"
                    "```\n",
                    encoding="utf-8",
                )
                with mock.patch.object(orch, "run_codex", return_value=output):
                    receipt = orch.run_phase(ctx, "F5", dry_run=False)
                self.assertEqual(receipt["status"], "completed")
                self.assertTrue(receipt["recovered_artifact"])
                self.assertIn("- Veredicto: PASS", ctx.paths.plan_audit.read_text(encoding="utf-8"))
            finally:
                orch.ensure_local_runtime = original_ensure_runtime


if __name__ == "__main__":
    unittest.main()
