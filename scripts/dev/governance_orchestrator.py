from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.dev import governance_ping_pong as gpp


CANONICAL_REPO_ROOT = Path(__file__).resolve().parents[2]
PROMPTS_ROOT = CANONICAL_REPO_ROOT / "doc" / "governance_prompts"
LOCAL_RUNTIME_DIRNAME = ".orchestrator_local"
LOCAL_RUNTIME_ROOT = CANONICAL_REPO_ROOT / LOCAL_RUNTIME_DIRNAME
DEFAULT_MAX_AUDITS = gpp.DEFAULT_MAX_AUDITS
GIT_EXCLUDE_ENTRY = f"{LOCAL_RUNTIME_DIRNAME}/"
REOPENABLE_PHASES = ("F3", "F5", "F7")
AUDIT_ARTIFACTS: dict[str, tuple[str, str]] = {
    "F3": ("ask_audit.md", "ask_audit"),
    "F5": ("plan_audit.md", "plan_audit"),
    "F7": ("post_audit.md", "post_audit"),
}

PHASE_PROMPTS: dict[str, str] = {
    "F1": "01_f1_ask.md",
    "F1_REMEDIATION": "13_f1_remediacion_ask.md",
    "F3": "03_f3_auditoria_ask.md",
    "F4": "04_f4_plan.md",
    "F4_REMEDIATION": "15_f4_remediacion_plan.md",
    "F5": "05_f5_auditoria_plan.md",
    "F6": "06_f6_ejecucion.md",
    "F6_REMEDIATION": "17_f6_remediacion_ejecucion.md",
    "F7": "07_f7_post_auditoria.md",
}
PHASE_ENGINES: dict[str, str] = {
    "F1": "claude",
    "F1_REMEDIATION": "claude",
    "F3": "codex",
    "F4": "claude",
    "F4_REMEDIATION": "claude",
    "F5": "codex",
    "F6": "claude",
    "F6_REMEDIATION": "claude",
    "F7": "codex",
}
NEXT_STEP_TO_PHASE: dict[str, str] = {
    "RUN_F1": "F1",
    "RUN_F3": "F3",
    "RUN_F1_F3_REMEDIATION": "F1_REMEDIATION",
    "RUN_F4": "F4",
    "RUN_F5": "F5",
    "RUN_F4_F5_REMEDIATION": "F4_REMEDIATION",
    "RUN_F6_F7": "F6",
    "RUN_F6_F7_REMEDIATION": "F6_REMEDIATION",
}


@dataclass(frozen=True)
class SessionContext:
    target_repo: Path
    initiative_id: str
    runtime_root: Path
    session_id: str
    session_dir: Path
    session_file: Path
    prompts_dir: Path
    outputs_dir: Path
    receipts_dir: Path
    paths: gpp.InitiativePaths


def today_iso() -> str:
    return dt.date.today().isoformat()


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def ensure_git_exclude(repo_root: Path, entry: str) -> None:
    exclude_path = repo_root / ".git" / "info" / "exclude"
    if not exclude_path.parent.exists():
        return
    existing = exclude_path.read_text(encoding="utf-8") if exclude_path.exists() else ""
    lines = {line.strip() for line in existing.splitlines() if line.strip()}
    if entry in lines:
        return
    prefix = "" if existing.endswith("\n") or not existing else "\n"
    exclude_path.write_text(existing + prefix + entry + "\n", encoding="utf-8")


def ensure_local_runtime(base_repo: Path | None = None) -> Path:
    runtime_root = (base_repo or CANONICAL_REPO_ROOT) / LOCAL_RUNTIME_DIRNAME
    for rel in ("config", "sessions", "tmp", "receipts", "prompts_rendered"):
        (runtime_root / rel).mkdir(parents=True, exist_ok=True)
    gitignore = runtime_root / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text("*\n!.gitignore\n!README.md\n", encoding="utf-8")
    readme = runtime_root / "README.md"
    if not readme.exists():
        readme.write_text(
            "# Orchestrator Local Runtime\n\n"
            "Estado operativo local del orquestador. No forma parte del baseline exportable.\n",
            encoding="utf-8",
        )
    ensure_git_exclude(base_repo or CANONICAL_REPO_ROOT, GIT_EXCLUDE_ENTRY)
    return runtime_root


def session_id_for(target_repo: Path, initiative_id: str) -> str:
    digest = hashlib.sha1(str(target_repo).encode("utf-8")).hexdigest()[:10]
    safe_id = initiative_id.replace("\\", "_").replace("/", "_")
    return f"{digest}_{safe_id}"


def build_session_context(target_repo: Path, initiative_id: str) -> SessionContext:
    runtime_root = ensure_local_runtime()
    session_id = session_id_for(target_repo, initiative_id)
    session_dir = runtime_root / "sessions" / session_id
    prompts_dir = session_dir / "prompts"
    outputs_dir = session_dir / "outputs"
    receipts_dir = session_dir / "receipts"
    for path in (session_dir, prompts_dir, outputs_dir, receipts_dir):
        path.mkdir(parents=True, exist_ok=True)
    initiative_root = target_repo / "dev" / "records" / "initiatives" / initiative_id
    paths = gpp.InitiativePaths(
        initiative_id=initiative_id,
        root=initiative_root,
        ask=initiative_root / "ask.md",
        ask_audit=initiative_root / "ask_audit.md",
        handoff=initiative_root / "handoff.md",
        plan=initiative_root / "plan.md",
        plan_audit=initiative_root / "plan_audit.md",
        execution=initiative_root / "execution.md",
        post_audit=initiative_root / "post_audit.md",
        closeout=initiative_root / "closeout.md",
        lessons=initiative_root / "lessons_learned.md",
        real_validation=initiative_root / "real_validation.md",
    )
    return SessionContext(
        target_repo=target_repo,
        initiative_id=initiative_id,
        runtime_root=runtime_root,
        session_id=session_id,
        session_dir=session_dir,
        session_file=session_dir / "session.json",
        prompts_dir=prompts_dir,
        outputs_dir=outputs_dir,
        receipts_dir=receipts_dir,
        paths=paths,
    )


def snapshot(paths: gpp.InitiativePaths) -> dict[str, str]:
    return {
        "initiative_id": paths.initiative_id,
        "ask_state": gpp.get_state(paths.ask) or "<empty>",
        "ask_audit": gpp.get_verdict(paths.ask_audit) or "<empty>",
        "plan_state": gpp.get_state(paths.plan) or "<empty>",
        "plan_audit": gpp.get_verdict(paths.plan_audit) or "<empty>",
        "post_audit": gpp.get_verdict(paths.post_audit) or "<empty>",
        "next_step": gpp.recommend_next_step(paths),
    }


def workflow_state(paths: gpp.InitiativePaths, override_phase: str = "") -> dict[str, str]:
    state = snapshot(paths)
    if override_phase:
        state["recommended_next_step"] = state["next_step"]
        state["next_step"] = f"RUN_{override_phase}"
        state["override_phase"] = override_phase
    phase = override_phase or NEXT_STEP_TO_PHASE.get(state["next_step"], "")
    if phase:
        state["phase"] = phase
        state["engine"] = PHASE_ENGINES[phase]
        state["prompt"] = PHASE_PROMPTS[phase]
    return state


def persist_session(ctx: SessionContext, payload: dict | None = None) -> dict:
    data = payload or read_json(ctx.session_file)
    data.update(
        {
            "session_id": ctx.session_id,
            "target_repo": str(ctx.target_repo),
            "initiative_id": ctx.initiative_id,
            "runtime_root": str(ctx.runtime_root),
            "updated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        }
    )
    data["snapshot"] = workflow_state(ctx.paths, str(data.get("override_phase") or ""))
    write_json(ctx.session_file, data)
    return data


def output_file_for(ctx: SessionContext, phase: str, engine: str) -> Path:
    return ctx.outputs_dir / f"{phase.lower()}_{engine}_raw.txt"


def receipt_file_for(ctx: SessionContext, phase: str) -> Path:
    return ctx.receipts_dir / f"{phase.upper()}.json"


def base_prompt_file_for_phase(phase: str) -> Path:
    return PROMPTS_ROOT / PHASE_PROMPTS[phase]


def load_prompt_text(name: str) -> str:
    prompt_path = PROMPTS_ROOT / name
    if not prompt_path.exists():
        raise SystemExit(f"Missing prompt file: {prompt_path}")
    return prompt_path.read_text(encoding="utf-8").strip()


def allowed_writes_for_phase(paths: gpp.InitiativePaths, phase: str) -> list[Path]:
    if phase == "F1":
        return [paths.ask]
    if phase == "F1_REMEDIATION":
        return [paths.ask]
    if phase == "F3":
        return [paths.ask_audit]
    if phase == "F4":
        return [paths.plan, paths.root / "capability_closure.md"]
    if phase == "F4_REMEDIATION":
        return [paths.plan, paths.root / "capability_closure.md"]
    if phase == "F5":
        return [paths.plan_audit]
    if phase == "F6":
        return [paths.execution]
    if phase == "F6_REMEDIATION":
        return [paths.execution]
    if phase == "F7":
        return [paths.post_audit]
    raise SystemExit(f"Unsupported phase: {phase}")


def read_paths_for_phase(paths: gpp.InitiativePaths, phase: str) -> list[Path]:
    capability = paths.root / "capability_closure.md"
    reads: list[Path]
    if phase in {"F1", "F1_REMEDIATION"}:
        reads = [paths.handoff, paths.ask_audit]
    elif phase == "F3":
        reads = [paths.ask]
    elif phase in {"F4", "F4_REMEDIATION"}:
        reads = [paths.handoff, paths.ask, paths.ask_audit, paths.plan_audit]
    elif phase == "F5":
        reads = [paths.ask, paths.ask_audit, paths.plan, paths.handoff]
        if capability.exists():
            reads.append(capability)
    elif phase in {"F6", "F6_REMEDIATION"}:
        reads = [paths.plan, paths.plan_audit, paths.execution, paths.post_audit]
    elif phase == "F7":
        reads = [paths.handoff, paths.plan, paths.execution]
    else:
        raise SystemExit(f"Unsupported phase: {phase}")
    return [path for path in reads if path.exists()]


def build_prompt(ctx: SessionContext, phase: str) -> str:
    base_prompt = load_prompt_text(PHASE_PROMPTS[phase])
    writes = "\n".join(f"- {path}" for path in allowed_writes_for_phase(ctx.paths, phase))
    reads = "\n".join(f"- {path}" for path in read_paths_for_phase(ctx.paths, phase))
    role = "motor_auditor" if PHASE_ENGINES[phase] == "codex" and phase in {"F3", "F5", "F7"} else "motor_activo"
    artifact = allowed_writes_for_phase(ctx.paths, phase)[0]
    footer = (
        "\n\n[RESULTADO OBLIGATORIO]\n"
        f"- crear o actualizar {artifact}\n"
        "- incluir metadata obligatoria\n"
        "- no tocar otros archivos\n"
        "- si no puedes completar la fase, deja bloqueo con evidencia en el artefacto permitido\n"
    )
    return (
        "[ORCHESTRATOR]\n"
        f"Repo objetivo: {ctx.target_repo}\n"
        f"Initiative ID: {ctx.initiative_id}\n"
        f"Fase operativa: {phase}\n"
        f"Rol esperado: {role}\n"
        f"Motor esperado: {PHASE_ENGINES[phase]}\n\n"
        "Lee solo:\n"
        f"{reads or '- [sin lecturas adicionales]'}\n\n"
        "Puedes escribir solo:\n"
        f"{writes}\n\n"
        "No modifiques otros archivos.\n"
        "Confirma qué iniciativa estás usando antes de trabajar.\n\n"
        f"{base_prompt}"
        f"{footer}"
    )


def write_prompt_copy(ctx: SessionContext, phase: str, prompt: str) -> Path:
    prompt_path = ctx.prompts_dir / f"{phase.lower()}.txt"
    prompt_path.write_text(prompt, encoding="utf-8")
    return prompt_path


def run_claude(ctx: SessionContext, phase: str, prompt: str, dry_run: bool) -> Path:
    output_path = output_file_for(ctx, phase, "claude")
    if dry_run:
        output_path.write_text(prompt, encoding="utf-8")
        return output_path
    settings_path = ctx.target_repo / ".claude" / "settings.local.json"
    command = ["claude", "-p", "--output-format", "text", "--permission-mode", "bypassPermissions"]
    if settings_path.exists():
        command.extend(["--settings", str(settings_path)])
    command.append(prompt)
    result = subprocess.run(
        command,
        cwd=ctx.target_repo,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
        check=False,
    )
    output_path.write_text(result.stdout or "", encoding="utf-8")
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "Claude command failed")
    return output_path


def run_codex(ctx: SessionContext, phase: str, prompt: str, dry_run: bool) -> Path:
    output_path = output_file_for(ctx, phase, "codex")
    if dry_run:
        output_path.write_text(prompt, encoding="utf-8")
        return output_path
    command = [
        "codex",
        "-a",
        "never",
        "-s",
        "workspace-write",
        "exec",
        "-C",
        str(ctx.target_repo),
        "-o",
        str(output_path),
        prompt,
    ]
    result = subprocess.run(
        command,
        cwd=ctx.target_repo,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "Codex command failed")
    return output_path


def ensure_phase_artifact(paths: gpp.InitiativePaths, phase: str) -> None:
    if phase in {"F1", "F1_REMEDIATION"}:
        if not gpp.document_has_meaningful_content(paths.ask, gpp.ASK_HEADINGS):
            raise RuntimeError(f"Expected meaningful ask content in {paths.ask}")
        return
    if phase == "F3":
        gpp.ensure_file_updated(paths.ask_audit, "Veredicto")
        return
    if phase in {"F4", "F4_REMEDIATION"}:
        if not gpp.document_has_meaningful_content(paths.plan, gpp.PLAN_HEADINGS):
            raise RuntimeError(f"Expected meaningful plan content in {paths.plan}")
        return
    if phase == "F5":
        gpp.ensure_file_updated(paths.plan_audit, "Veredicto")
        return
    if phase in {"F6", "F6_REMEDIATION"}:
        if not gpp.document_has_meaningful_content(paths.execution, gpp.EXECUTION_HEADINGS):
            raise RuntimeError(f"Expected meaningful execution content in {paths.execution}")
        return
    if phase == "F7":
        gpp.ensure_file_updated(paths.post_audit, "Veredicto")
        return
    raise SystemExit(f"Unsupported phase: {phase}")


def run_phase(ctx: SessionContext, phase: str, dry_run: bool = False) -> dict:
    prompt = build_prompt(ctx, phase)
    prompt_copy = write_prompt_copy(ctx, phase, prompt)
    if phase in {"F6", "F6_REMEDIATION"}:
        gpp.ensure_f6_branch(ctx.paths, dry_run=dry_run)
        gpp.run_preflight(ctx.initiative_id, allow_dirty_with_ask_exception=False, dry_run=dry_run)
    engine = PHASE_ENGINES[phase]
    output_path = run_claude(ctx, phase, prompt, dry_run=dry_run) if engine == "claude" else run_codex(ctx, phase, prompt, dry_run=dry_run)
    ensure_phase_artifact(ctx.paths, phase)
    receipt = {
        "phase": phase,
        "engine": engine,
        "initiative_id": ctx.initiative_id,
        "target_repo": str(ctx.target_repo),
        "prompt_file": str(prompt_copy),
        "output_file": str(output_path),
        "allowed_writes": [str(path) for path in allowed_writes_for_phase(ctx.paths, phase)],
        "snapshot": snapshot(ctx.paths),
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    write_json(receipt_file_for(ctx, phase), receipt)
    persist_session(ctx, {"last_phase": phase, "last_engine": engine, "override_phase": ""})
    return receipt


def parse_target_repo(value: str) -> Path:
    return Path(value).expanduser().resolve()


def require_paths(ctx: SessionContext) -> None:
    if not gpp.initiative_exists(ctx.paths):
        raise SystemExit(f"Missing initiative folder: {ctx.paths.root}")


def current_workflow_state(ctx: SessionContext) -> dict[str, str]:
    data = read_json(ctx.session_file)
    return workflow_state(ctx.paths, str(data.get("override_phase") or ""))


def latest_receipt(ctx: SessionContext) -> dict:
    data = read_json(ctx.session_file)
    last_phase = str(data.get("last_phase") or "")
    if not last_phase:
        return {}
    path = receipt_file_for(ctx, last_phase)
    if not path.exists():
        return {}
    return read_json(path)


def print_snapshot(payload: dict) -> None:
    for key in ("initiative_id", "ask_state", "ask_audit", "plan_state", "plan_audit", "post_audit", "next_step"):
        print(f"{key}={payload.get(key, '<empty>')}")
    if payload.get("recommended_next_step"):
        print(f"recommended_next_step={payload['recommended_next_step']}")
    if payload.get("override_phase"):
        print(f"override_phase={payload['override_phase']}")
    if payload.get("phase"):
        print(f"phase={payload['phase']}")
    if payload.get("engine"):
        print(f"engine={payload['engine']}")
    if payload.get("prompt"):
        print(f"prompt={payload['prompt']}")


def reset_audit_artifact(ctx: SessionContext, phase: str) -> Path:
    template_name, attr_name = AUDIT_ARTIFACTS[phase]
    template_path = gpp.TEMPLATE_ROOT / template_name
    text = template_path.read_text(encoding="utf-8")
    artifact = getattr(ctx.paths, attr_name)
    auditor = gpp.extract_metadata(gpp.read_text(ctx.paths.ask), "motor_auditor") or "codex"
    for key, value in (
        ("Initiative ID", ctx.initiative_id),
        ("Fase", phase),
        ("Auditor", auditor),
        ("Fecha", today_iso()),
    ):
        text = gpp.replace_metadata_line(text, key, value)
    artifact.write_text(text, encoding="utf-8")
    return artifact


def reopen_phase(args: argparse.Namespace) -> int:
    ctx = build_session_context(parse_target_repo(args.target_repo), args.initiative_id)
    gpp.configure_repo_root(str(ctx.target_repo))
    gpp.ensure_repo_supports_governance()
    require_paths(ctx)
    phase = args.phase.upper()
    if phase not in REOPENABLE_PHASES:
        raise SystemExit(f"Unsupported reopen phase: {phase}")
    reset_audit_artifact(ctx, phase)
    if phase == "F3":
        gpp.set_state(ctx.paths.ask, "VALIDADO")
    elif phase == "F5":
        gpp.set_state(ctx.paths.plan, "PROPUESTO")
    data = persist_session(
        ctx,
        {
            "last_reopened_phase": phase,
            "override_phase": phase,
            "reopened_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        },
    )
    print(f"initiative_id={ctx.initiative_id}")
    print("result=PHASE_REOPENED")
    print(f"phase={phase}")
    print(f"audit_artifact={getattr(ctx.paths, AUDIT_ARTIFACTS[phase][1])}")
    print_snapshot(data["snapshot"])
    return 0


def init_session(args: argparse.Namespace) -> int:
    ctx = build_session_context(parse_target_repo(args.target_repo), args.initiative_id)
    gpp.configure_repo_root(str(ctx.target_repo))
    gpp.ensure_repo_supports_governance()
    require_paths(ctx)
    persist_session(ctx, {"created_at": dt.datetime.now(dt.timezone.utc).isoformat()})
    print(f"session_id={ctx.session_id}")
    print(f"runtime_root={ctx.runtime_root}")
    print_snapshot(current_workflow_state(ctx))
    return 0


def status(args: argparse.Namespace) -> int:
    ctx = build_session_context(parse_target_repo(args.target_repo), args.initiative_id)
    gpp.configure_repo_root(str(ctx.target_repo))
    gpp.ensure_repo_supports_governance()
    require_paths(ctx)
    persist_session(ctx)
    print(f"session_id={ctx.session_id}")
    print_snapshot(current_workflow_state(ctx))
    return 0


def resume(args: argparse.Namespace) -> int:
    ctx = build_session_context(parse_target_repo(args.target_repo), args.initiative_id)
    gpp.configure_repo_root(str(ctx.target_repo))
    gpp.ensure_repo_supports_governance()
    require_paths(ctx)
    persist_session(ctx)
    state = current_workflow_state(ctx)
    print(f"session_id={ctx.session_id}")
    print_snapshot(state)
    return 0


def show_prompt(args: argparse.Namespace) -> int:
    ctx = build_session_context(parse_target_repo(args.target_repo), args.initiative_id)
    gpp.configure_repo_root(str(ctx.target_repo))
    gpp.ensure_repo_supports_governance()
    require_paths(ctx)
    state = current_workflow_state(ctx)
    phase = state.get("phase")
    if not phase:
        raise SystemExit(f"No prompt available for next_step={state['next_step']}")
    base_prompt = base_prompt_file_for_phase(phase)
    rendered_prompt = ctx.prompts_dir / f"{phase.lower()}.txt"
    print(f"initiative_id={ctx.initiative_id}")
    print(f"phase={phase}")
    print(f"engine={PHASE_ENGINES[phase]}")
    print(f"base_prompt={base_prompt}")
    print(f"rendered_prompt={rendered_prompt if rendered_prompt.exists() else '<not_rendered_yet>'}")
    if args.rendered:
        print()
        print((rendered_prompt if rendered_prompt.exists() else base_prompt).read_text(encoding="utf-8"))
    return 0


def last_run(args: argparse.Namespace) -> int:
    ctx = build_session_context(parse_target_repo(args.target_repo), args.initiative_id)
    gpp.configure_repo_root(str(ctx.target_repo))
    gpp.ensure_repo_supports_governance()
    require_paths(ctx)
    receipt = latest_receipt(ctx)
    if not receipt:
        print(f"initiative_id={ctx.initiative_id}")
        print("result=NO_RUNS_YET")
        return 0
    print(f"initiative_id={ctx.initiative_id}")
    for key in ("phase", "engine", "prompt_file", "output_file", "timestamp"):
        print(f"{key}={receipt.get(key, '<empty>')}")
    print_snapshot(receipt.get("snapshot", {}))
    return 0


def next_step_cmd(args: argparse.Namespace) -> int:
    ctx = build_session_context(parse_target_repo(args.target_repo), args.initiative_id)
    gpp.configure_repo_root(str(ctx.target_repo))
    gpp.ensure_repo_supports_governance()
    require_paths(ctx)
    state = current_workflow_state(ctx)
    print(f"session_id={ctx.session_id}")
    print(f"next_step={state['next_step']}")
    if state.get("recommended_next_step"):
        print(f"recommended_next_step={state['recommended_next_step']}")
    if state.get("phase"):
        print(f"phase={state['phase']}")
        print(f"engine={state['engine']}")
        print(f"prompt={state['prompt']}")
    return 0


def approve_f2(args: argparse.Namespace) -> int:
    ctx = build_session_context(parse_target_repo(args.target_repo), args.initiative_id)
    gpp.configure_repo_root(str(ctx.target_repo))
    gpp.ensure_repo_supports_governance()
    require_paths(ctx)
    if not gpp.document_has_meaningful_content(ctx.paths.ask, gpp.ASK_HEADINGS):
        raise SystemExit("ask.md does not contain enough content for F2 validation")
    gpp.set_state(ctx.paths.ask, "VALIDADO")
    for path in (ctx.paths.ask, ctx.paths.plan, ctx.paths.execution, ctx.paths.closeout, ctx.paths.lessons):
        gpp.set_metadata(path, "motor_auditor", args.motor_auditor)
    persist_session(ctx, {"last_phase": "F2", "override_phase": ""})
    print(f"initiative_id={ctx.initiative_id}")
    print("result=F2_VALIDATED")
    print(f"motor_auditor={args.motor_auditor}")
    print(f"next_step={current_workflow_state(ctx)['next_step']}")
    return 0


def freeze_ask(args: argparse.Namespace) -> int:
    ctx = build_session_context(parse_target_repo(args.target_repo), args.initiative_id)
    gpp.configure_repo_root(str(ctx.target_repo))
    require_paths(ctx)
    if gpp.get_verdict(ctx.paths.ask_audit) != "PASS":
        raise SystemExit("ask_audit.md must be PASS before freezing ask.md")
    gpp.set_state(ctx.paths.ask, "CONGELADO")
    persist_session(ctx, {"last_phase": "F3", "override_phase": ""})
    print(f"initiative_id={ctx.initiative_id}")
    print("result=ASK_FROZEN")
    print(f"next_step={current_workflow_state(ctx)['next_step']}")
    return 0


def freeze_plan(args: argparse.Namespace) -> int:
    ctx = build_session_context(parse_target_repo(args.target_repo), args.initiative_id)
    gpp.configure_repo_root(str(ctx.target_repo))
    require_paths(ctx)
    if gpp.get_verdict(ctx.paths.plan_audit) != "PASS":
        raise SystemExit("plan_audit.md must be PASS before freezing plan.md")
    gpp.set_state(ctx.paths.plan, "CONGELADO")
    persist_session(ctx, {"last_phase": "F5", "override_phase": ""})
    print(f"initiative_id={ctx.initiative_id}")
    print("result=PLAN_FROZEN")
    print(f"next_step={current_workflow_state(ctx)['next_step']}")
    return 0


def run_current_step(args: argparse.Namespace) -> int:
    ctx = build_session_context(parse_target_repo(args.target_repo), args.initiative_id)
    gpp.configure_repo_root(str(ctx.target_repo))
    gpp.ensure_repo_supports_governance()
    require_paths(ctx)
    state = current_workflow_state(ctx)
    next_step = state["next_step"]
    if next_step == "WAITING_FOR_F2":
        raise SystemExit("Next step is WAITING_FOR_F2. Use approve-f2 after human validation.")
    if next_step == "WAITING_FOR_F8":
        raise SystemExit("Next step is WAITING_FOR_F8. Use prepare-f8 and execute real validation manually.")
    phase = state.get("phase")
    if not phase:
        raise SystemExit(f"Unsupported next step: {next_step}")
    receipt = run_phase(ctx, phase, dry_run=args.dry_run)
    print(json.dumps(receipt, indent=2, ensure_ascii=True))
    return 0


def run_named_phase(args: argparse.Namespace, phase: str) -> int:
    ctx = build_session_context(parse_target_repo(args.target_repo), args.initiative_id)
    gpp.configure_repo_root(str(ctx.target_repo))
    gpp.ensure_repo_supports_governance()
    require_paths(ctx)
    receipt = run_phase(ctx, phase, dry_run=args.dry_run)
    print(json.dumps(receipt, indent=2, ensure_ascii=True))
    return 0


def prepare_f8(args: argparse.Namespace) -> int:
    ctx = build_session_context(parse_target_repo(args.target_repo), args.initiative_id)
    gpp.configure_repo_root(str(ctx.target_repo))
    gpp.ensure_repo_supports_governance()
    require_paths(ctx)
    if not ctx.paths.real_validation.exists():
        template = (gpp.TEMPLATE_ROOT / "real_validation.md").read_text(encoding="utf-8")
        text = template
        for key, value in (
            ("Initiative ID", ctx.initiative_id),
            ("Modo", "M4"),
            ("Estado", "PROPUESTO"),
            ("Fecha", today_iso()),
            ("motor_activo", "claude"),
            ("motor_auditor", gpp.extract_metadata(gpp.read_text(ctx.paths.ask), "motor_auditor") or "codex"),
            ("Rama", gpp.declared_branch(ctx.paths)),
            ("baseline_mit", gpp.extract_metadata(gpp.read_text(ctx.paths.ask), "baseline_mit") or gpp.DEFAULT_BASELINE_MIT),
        ):
            text = gpp.replace_metadata_line(text, key, value)
        ctx.paths.real_validation.write_text(text, encoding="utf-8")
    persist_session(ctx, {"last_phase": "F8_PREP", "override_phase": ""})
    print(f"initiative_id={ctx.initiative_id}")
    print(f"real_validation={ctx.paths.real_validation}")
    print("next_step=WAITING_FOR_F8")
    return 0


def doctor(args: argparse.Namespace) -> int:
    target_repo = parse_target_repo(args.target_repo)
    ctx = build_session_context(target_repo, args.initiative_id)
    gpp.configure_repo_root(str(target_repo))
    report = {
        "target_repo": str(target_repo),
        "runtime_root": str(ctx.runtime_root),
        "initiative_exists": gpp.initiative_exists(ctx.paths),
        "supports_governance": True,
        "claude_available": shutil_which("claude"),
        "codex_available": shutil_which("codex"),
        "next_step": current_workflow_state(ctx)["next_step"] if gpp.initiative_exists(ctx.paths) else "<missing initiative>",
    }
    try:
        gpp.ensure_repo_supports_governance()
    except SystemExit:
        report["supports_governance"] = False
    print(json.dumps(report, indent=2, ensure_ascii=True))
    return 0


def shutil_which(name: str) -> bool:
    result = subprocess.run(
        ["where", name] if sys.platform.startswith("win") else ["which", name],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
        check=False,
    )
    return result.returncode == 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Orquestador canónico de gobernanza M4: Codex orquesta, Claude actúa y Codex audita dentro del repo objetivo."
    )
    parser.add_argument("--target-repo", required=True, help="Repo objetivo sobre el que se orquesta la iniciativa.")
    parser.add_argument("--initiative-id", required=True, help="Initiative ID canónico.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init-session", help="Inicializa runtime local y registra sesión.")
    init_parser.set_defaults(func=init_session)

    status_parser = subparsers.add_parser("status", help="Muestra el estado real de la iniciativa.")
    status_parser.set_defaults(func=status)

    resume_parser = subparsers.add_parser("resume", help="Retoma una iniciativa ya empezada y muestra el siguiente paso efectivo.")
    resume_parser.set_defaults(func=resume)

    show_prompt_parser = subparsers.add_parser("show-prompt", help="Muestra el prompt base o renderizado de la fase efectiva.")
    show_prompt_parser.add_argument("--rendered", action="store_true", help="Imprime el prompt renderizado si ya existe; si no, imprime el prompt base.")
    show_prompt_parser.set_defaults(func=show_prompt)

    last_run_parser = subparsers.add_parser("last-run", help="Muestra el último intento ejecutado y su snapshot.")
    last_run_parser.set_defaults(func=last_run)

    next_parser = subparsers.add_parser("next-step", help="Calcula el siguiente paso y el prompt asociado.")
    next_parser.set_defaults(func=next_step_cmd)

    reopen_parser = subparsers.add_parser("reopen-phase", help="Reabre F3, F5 o F7 para repetir auditoría sobre una iniciativa a medias.")
    reopen_parser.add_argument("--phase", required=True, choices=REOPENABLE_PHASES)
    reopen_parser.set_defaults(func=reopen_phase)

    approve_parser = subparsers.add_parser("approve-f2", help="Registra la validación humana mínima de F2.")
    approve_parser.add_argument("--motor-auditor", default="codex")
    approve_parser.set_defaults(func=approve_f2)

    freeze_ask_parser = subparsers.add_parser("freeze-ask", help="Congela ask.md tras PASS en F3.")
    freeze_ask_parser.set_defaults(func=freeze_ask)

    freeze_plan_parser = subparsers.add_parser("freeze-plan", help="Congela plan.md tras PASS en F5.")
    freeze_plan_parser.set_defaults(func=freeze_plan)

    prepare_f8_parser = subparsers.add_parser("prepare-f8", help="Prepara real_validation.md para F8.")
    prepare_f8_parser.set_defaults(func=prepare_f8)

    doctor_parser = subparsers.add_parser("doctor", help="Diagnostica disponibilidad del orquestador y del repo objetivo.")
    doctor_parser.set_defaults(func=doctor)

    current_parser = subparsers.add_parser("run-current-step", help="Ejecuta el paso actual sugerido por la máquina de estados.")
    current_parser.add_argument("--dry-run", action="store_true")
    current_parser.set_defaults(func=run_current_step)

    for command, phase in (
        ("run-f1", "F1"),
        ("run-f3", "F3"),
        ("run-f1-remediation", "F1_REMEDIATION"),
        ("run-f4", "F4"),
        ("run-f5", "F5"),
        ("run-f4-remediation", "F4_REMEDIATION"),
        ("run-f6", "F6"),
        ("run-f7", "F7"),
        ("run-f6-remediation", "F6_REMEDIATION"),
    ):
        phase_parser = subparsers.add_parser(command, help=f"Ejecuta {phase} con prompt envelope y receipt local.")
        phase_parser.add_argument("--dry-run", action="store_true")
        phase_parser.set_defaults(func=lambda args, phase=phase: run_named_phase(args, phase))

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
