from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.dev import governance_ping_pong as gpp


CANONICAL_REPO_ROOT = Path(__file__).resolve().parents[2]
PROMPTS_ROOT = CANONICAL_REPO_ROOT / "doc" / "governance_prompts"
RUNTIME_TEMPLATE_ROOT = CANONICAL_REPO_ROOT / "dev" / "templates" / "orchestrator"
LOCAL_RUNTIME_DIRNAME = ".orchestrator_local"
LOCAL_RUNTIME_ROOT = CANONICAL_REPO_ROOT / LOCAL_RUNTIME_DIRNAME
DEFAULT_MAX_AUDITS = gpp.DEFAULT_MAX_AUDITS
GIT_EXCLUDE_ENTRY = f"{LOCAL_RUNTIME_DIRNAME}/"
REOPENABLE_PHASES = ("F3", "F5", "F7")
CHECKPOINT_PROMPT = "18_f6_checkpoint_audit.md"
AUDIT_ARTIFACTS: dict[str, tuple[str, str]] = {
    "F3": ("ask_audit.md", "ask_audit"),
    "F5": ("plan_audit.md", "plan_audit"),
    "F7": ("post_audit.md", "post_audit"),
}
AUDIT_TITLES: dict[str, str] = {
    "F3": "# ASK AUDIT",
    "F5": "# PLAN AUDIT",
    "F7": "# POST AUDIT",
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
    "RUN_F7": "F7",
    "RUN_F6_F7_REMEDIATION": "F6_REMEDIATION",
}


@dataclass(frozen=True)
class RepoCapabilities:
    profile_path: Path
    exists: bool
    governance_search: str
    symdex_code: str
    structural_memory: str
    f8_observable: str
    trace_on: str
    terminal_logs: str


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
    phase_tickets_dir: Path
    resume_packets_dir: Path
    checkpoints_dir: Path
    paths: gpp.InitiativePaths
    repo_capabilities: RepoCapabilities


@dataclass(frozen=True)
class WeeklyReviewPaths:
    root: Path
    weekly_root: Path
    review_dir: Path
    briefing: Path
    review: Path
    delta: Path
    audit: Path
    candidates: Path
    findings_register: Path


@dataclass(frozen=True)
class WeeklyReviewContext:
    target_repo: Path
    review_date: str
    runtime_root: Path
    session_id: str
    session_dir: Path
    prompts_dir: Path
    outputs_dir: Path
    receipts_dir: Path
    session_file: Path
    repo_capabilities: RepoCapabilities
    paths: WeeklyReviewPaths


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
    for rel in ("config", "sessions", "tmp", "receipts", "prompts_rendered", "phase_tickets", "resume_packets", "checkpoints"):
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
    phase_tickets_dir = session_dir / "phase_tickets"
    resume_packets_dir = session_dir / "resume_packets"
    checkpoints_dir = session_dir / "checkpoints"
    for path in (session_dir, prompts_dir, outputs_dir, receipts_dir, phase_tickets_dir, resume_packets_dir, checkpoints_dir):
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
    repo_capabilities = load_repo_capabilities(target_repo / "dev" / "repo_governance_profile.md")
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
        phase_tickets_dir=phase_tickets_dir,
        resume_packets_dir=resume_packets_dir,
        checkpoints_dir=checkpoints_dir,
        paths=paths,
        repo_capabilities=repo_capabilities,
    )


def weekly_review_session_id_for(target_repo: Path, review_date: str) -> str:
    digest = hashlib.sha1(str(target_repo).encode("utf-8")).hexdigest()[:10]
    return f"{digest}_weekly_{review_date}"


def build_weekly_review_context(target_repo: Path, review_date: str) -> WeeklyReviewContext:
    runtime_root = ensure_local_runtime()
    session_id = weekly_review_session_id_for(target_repo, review_date)
    session_dir = runtime_root / "sessions" / session_id
    prompts_dir = session_dir / "prompts"
    outputs_dir = session_dir / "outputs"
    receipts_dir = session_dir / "receipts"
    for path in (session_dir, prompts_dir, outputs_dir, receipts_dir):
        path.mkdir(parents=True, exist_ok=True)
    reviews_root = target_repo / "dev" / "records" / "reviews"
    weekly_root = reviews_root / "weekly"
    review_dir = weekly_root / review_date
    review_dir.mkdir(parents=True, exist_ok=True)
    repo_capabilities = load_repo_capabilities(target_repo / "dev" / "repo_governance_profile.md")
    return WeeklyReviewContext(
        target_repo=target_repo,
        review_date=review_date,
        runtime_root=runtime_root,
        session_id=session_id,
        session_dir=session_dir,
        prompts_dir=prompts_dir,
        outputs_dir=outputs_dir,
        receipts_dir=receipts_dir,
        session_file=session_dir / "session.json",
        repo_capabilities=repo_capabilities,
        paths=WeeklyReviewPaths(
            root=reviews_root,
            weekly_root=weekly_root,
            review_dir=review_dir,
            briefing=review_dir / "weekly_briefing.md",
            review=review_dir / "weekly_review.md",
            delta=review_dir / "weekly_review_delta.md",
            audit=review_dir / "weekly_review_audit.md",
            candidates=review_dir / "candidate_initiatives.md",
            findings_register=reviews_root / "architecture_findings_register.md",
        ),
    )


def parse_profile_value(text: str, key: str) -> str:
    pattern = rf"(?im)^\s*-\s*{re.escape(key)}\s*:\s*(.+?)\s*$"
    match = re.search(pattern, text)
    if not match:
        return "NO_DECLARADO"
    return match.group(1).strip()


def normalize_profile_flag(value: str) -> str:
    raw = value.strip().upper()
    return raw or "NO_DECLARADO"


def load_repo_capabilities(profile_path: Path) -> RepoCapabilities:
    if not profile_path.exists():
        return RepoCapabilities(
            profile_path=profile_path,
            exists=False,
            governance_search="NO_DECLARADO",
            symdex_code="NO_DECLARADO",
            structural_memory="NO_DECLARADO",
            f8_observable="NO_DECLARADO",
            trace_on="NO_DECLARADO",
            terminal_logs="NO_DECLARADO",
        )
    text = profile_path.read_text(encoding="utf-8", errors="ignore")
    return RepoCapabilities(
        profile_path=profile_path,
        exists=True,
        governance_search=normalize_profile_flag(parse_profile_value(text, "governance_search")),
        symdex_code=normalize_profile_flag(parse_profile_value(text, "symdex_code")),
        structural_memory=normalize_profile_flag(parse_profile_value(text, "codebase-memory-mcp")),
        f8_observable=normalize_profile_flag(parse_profile_value(text, "F8 observable")),
        trace_on=normalize_profile_flag(parse_profile_value(text, "trace on o equivalente")),
        terminal_logs=normalize_profile_flag(parse_profile_value(text, "terminal/logs observables")),
    )


def repo_capabilities_summary(capabilities: RepoCapabilities) -> list[str]:
    return [
        f"Governance retrieval: {capabilities.governance_search}",
        f"Codigo vivo local (symdex_code): {capabilities.symdex_code}",
        f"Memoria estructural (codebase-memory-mcp): {capabilities.structural_memory}",
        f"F8 observable: {capabilities.f8_observable}",
        f"trace on: {capabilities.trace_on}",
        f"Terminal/logs observables: {capabilities.terminal_logs}",
    ]


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


def write_text_if_missing(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return
    path.write_text(text, encoding="utf-8")


def previous_weekly_review_date(ctx: WeeklyReviewContext) -> str:
    if not ctx.paths.weekly_root.exists():
        return ""
    dates: list[str] = []
    for path in ctx.paths.weekly_root.iterdir():
        if not path.is_dir():
            continue
        if path.name >= ctx.review_date:
            continue
        if (path / "weekly_review.md").exists():
            dates.append(path.name)
    return max(dates) if dates else ""


def weekly_review_mode(ctx: WeeklyReviewContext, initial_baseline: bool = False) -> str:
    if initial_baseline:
        return "BASELINE_INICIAL_MIT"
    return "DELTA_SEMANAL_MIT" if previous_weekly_review_date(ctx) else "BASELINE_INICIAL_MIT"


def replace_or_insert_metadata_line(text: str, key: str, value: str) -> str:
    return gpp.replace_metadata_line(text, key, value)


def seeded_weekly_template(path: Path, metadata: dict[str, str]) -> str:
    text = path.read_text(encoding="utf-8")
    for key, value in metadata.items():
        text = replace_or_insert_metadata_line(text, key, value)
    return text


def scaffold_weekly_review_artifacts(ctx: WeeklyReviewContext, *, initial_baseline: bool = False) -> dict[str, str]:
    mode = weekly_review_mode(ctx, initial_baseline=initial_baseline)
    repo_name = ctx.target_repo.name
    metadata = {
        "Repo": repo_name,
        "Fecha": ctx.review_date,
        "Review mode": mode,
        "Estado": "PROPUESTO",
        "Generado por": "governance_orchestrator",
        "Fuente de verdad": "GobernanzaIA",
        "Motor revisor": "claude",
        "Compara contra": previous_weekly_review_date(ctx) or "BASELINE_INICIAL_MIT",
        "Fecha de actualizacion": ctx.review_date,
        "Estado general": "PROPUESTO",
        "Fuente": f"weekly/{ctx.review_date}",
    }
    governance_template_root = CANONICAL_REPO_ROOT / "dev" / "templates" / "governance"
    write_text_if_missing(
        ctx.paths.briefing,
        seeded_weekly_template(governance_template_root / "weekly_briefing.md", metadata),
    )
    write_text_if_missing(
        ctx.paths.review,
        seeded_weekly_template(governance_template_root / "weekly_review.md", metadata),
    )
    write_text_if_missing(
        ctx.paths.delta,
        seeded_weekly_template(governance_template_root / "weekly_review_delta.md", metadata),
    )
    write_text_if_missing(
        ctx.paths.audit,
        seeded_weekly_template(governance_template_root / "weekly_review_audit.md", metadata),
    )
    write_text_if_missing(
        ctx.paths.candidates,
        seeded_weekly_template(governance_template_root / "candidate_initiatives.md", metadata),
    )
    write_text_if_missing(
        ctx.paths.findings_register,
        seeded_weekly_template(governance_template_root / "architecture_findings_register.md", metadata),
    )
    return {
        "review_mode": mode,
        "compare_against": previous_weekly_review_date(ctx) or "BASELINE_INICIAL_MIT",
    }


def safe_git_log(target_repo: Path, *, since_date: str = "", until_date: str = "") -> list[str]:
    command = ["git", "log", "--pretty=format:%h %ad %s", "--date=short", "--max-count", "20"]
    if since_date:
        command.extend(["--since", since_date])
    if until_date:
        command.extend(["--until", until_date])
    result = subprocess.run(
        command,
        cwd=target_repo,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def safe_relative_to_target(ctx: WeeklyReviewContext, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ctx.target_repo.resolve())).replace("\\", "/")
    except ValueError:
        return str(path)


def repo_identity_from_profile(ctx: WeeklyReviewContext) -> tuple[str, str, str]:
    if not ctx.repo_capabilities.exists:
        return (ctx.target_repo.name, "NO_EVIDENCIA_EN_PROFILE", "NO_EVIDENCIA_EN_PROFILE")
    text = ctx.repo_capabilities.profile_path.read_text(encoding="utf-8", errors="ignore")
    return (
        parse_profile_value(text, "Repo"),
        parse_profile_value(text, "Propósito"),
        parse_profile_value(text, "Superficie principal"),
    )


def render_weekly_briefing(ctx: WeeklyReviewContext, review_mode: str, compare_against: str) -> str:
    repo_name, purpose, primary_surface = repo_identity_from_profile(ctx)
    since_date = compare_against if compare_against not in {"", "BASELINE_INICIAL_MIT"} else ""
    commit_lines = safe_git_log(ctx.target_repo, since_date=since_date, until_date=ctx.review_date)
    commit_block = "\n".join(f"- {line}" for line in commit_lines[:10]) if commit_lines else "- NO EVIDENCIA EN REPO"
    compare_label = compare_against if compare_against else "BASELINE_INICIAL_MIT"
    if review_mode == "BASELINE_INICIAL_MIT":
        from_label = "<sin review semanal previa>"
        delta_note = "- Esta corrida funda la linea base semanal."
    else:
        from_label = compare_against or "<sin review valida previa>"
        delta_note = f"- Compara contra la revision semanal previa: {compare_label}."
    routing_lines = "\n".join(f"- {line}" for line in repo_capabilities_summary(ctx.repo_capabilities))
    profile_line = (
        f"- Perfil local de capacidades: {safe_relative_to_target(ctx, ctx.repo_capabilities.profile_path)}"
        if ctx.repo_capabilities.exists
        else "- Perfil local de capacidades: NO_ENCONTRADO"
    )
    return (
        "# WEEKLY BRIEFING\n\n"
        f"- Repo: {repo_name}\n"
        f"- Fecha: {ctx.review_date}\n"
        f"- Review mode: {review_mode}\n"
        "- Generado por: governance_orchestrator\n"
        "- Fuente de verdad: GobernanzaIA\n\n"
        "## Identidad del repo\n\n"
        f"- Propósito: {purpose}\n"
        f"- Superficie principal: {primary_surface}\n"
        f"{profile_line}\n\n"
        "## Alcance temporal\n\n"
        f"- Desde: {from_label}\n"
        f"- Hasta: {ctx.review_date}\n"
        f"- Motivo del rango: {review_mode}\n\n"
        "## Delta semanal\n\n"
        f"- Commits o cambios relevantes:\n{commit_block}\n"
        "- Superficies tocadas:\n"
        f"- {primary_surface}\n"
        f"{delta_note}\n\n"
        "## Capas de contexto y evidencia usada\n\n"
        "- Gobernanza normativa: `governance_search` + lectura canónica cuando aplique.\n"
        "- Runtime del orquestador: runtime local y receipts.\n"
        "- Codigo vivo local: `symdex_code` cuando esté disponible.\n"
        "- Memoria estructural persistente: `codebase-memory-mcp` cuando esté disponible.\n"
        "- Evidencia runtime real: tests, logs, CI o señales observables si existen.\n\n"
        "## Behaviors y superficies observadas\n\n"
        f"- Behavior 1: Superficie principal declarada -> {primary_surface}\n"
        "- Behavior 2: NO EVIDENCIA EN BRIEFING\n\n"
        "## Wiring, impacto y legacy\n\n"
        "- Call paths o rutas estructurales relevantes: derivar de la memoria estructural si esta disponible.\n"
        "- Blast radius esperado: contrastar con el delta semanal y las areas tocadas.\n"
        "- Legacy o dead code sospechoso: contrastar con findings persistentes si los hubiera.\n"
        "- Integraciones huerfanas o paths paralelos: NO EVIDENCIA EN BRIEFING.\n\n"
        "## Calidad operativa y validacion\n\n"
        "- Tests y CI: NO EVIDENCIA EN BRIEFING.\n"
        "- Logs / incidentes / errores: NO EVIDENCIA EN BRIEFING.\n"
        "- Cambios observables o riesgos de validacion: derivar de hallazgos y deltas.\n\n"
        "## Riesgos y preguntas abiertas para la review\n\n"
        "- Riesgo 1: confirmar que el delta no esconde paths paralelos o legacy vivo.\n"
        "- Pregunta 1: que capability o boundary acumula mayor tension MIT esta semana.\n\n"
        "## Instrucciones para el motor revisor\n\n"
        "- Anclar toda afirmacion importante al briefing.\n"
        "- Declarar `NO EVIDENCIA EN BRIEFING` cuando falte soporte.\n"
        "- Priorizar MIT: Incrementality, Integrity, Transparency.\n\n"
        "## Resumen de capacidades\n\n"
        f"{routing_lines}\n"
    )


def weekly_output_file_for(ctx: WeeklyReviewContext, engine: str) -> Path:
    return ctx.outputs_dir / f"weekly_review_{ctx.review_date}_{engine}.txt"


def weekly_receipt_file_for(ctx: WeeklyReviewContext) -> Path:
    return ctx.receipts_dir / f"WEEKLY_REVIEW_{ctx.review_date}.json"


def weekly_prompt_copy_for(ctx: WeeklyReviewContext) -> Path:
    return ctx.prompts_dir / f"weekly_review_{ctx.review_date}.txt"


def build_weekly_review_prompt(ctx: WeeklyReviewContext, review_mode: str) -> str:
    base_prompt = load_prompt_text("20_weekly_mit_review.md")
    writes = "\n".join(
        f"- {safe_relative_to_target(ctx, path)}"
        for path in (ctx.paths.review, ctx.paths.delta, ctx.paths.findings_register, ctx.paths.candidates)
    )
    reads = "\n".join(
        f"- {safe_relative_to_target(ctx, path)}"
        for path in (
            ctx.paths.briefing,
            ctx.repo_capabilities.profile_path if ctx.repo_capabilities.exists else ctx.paths.briefing,
        )
    )
    return (
        "[ORCHESTRATOR]\n"
        f"Repo objetivo: {ctx.target_repo}\n"
        f"Review date: {ctx.review_date}\n"
        f"Review mode: {review_mode}\n"
        "Motor esperado: claude\n\n"
        "Lee solo:\n"
        f"{reads}\n\n"
        "Puedes escribir solo:\n"
        f"{writes}\n\n"
        "No toques otros archivos.\n"
        "No abras una iniciativa ni implementes codigo.\n"
        "Confirma repo y review_date antes de trabajar.\n\n"
        f"{base_prompt}\n"
    )


def weekly_artifact_mtimes(ctx: WeeklyReviewContext) -> dict[Path, int | None]:
    return {
        path: artifact_mtime_ns(path)
        for path in (ctx.paths.review, ctx.paths.delta, ctx.paths.findings_register, ctx.paths.candidates)
    }


def ensure_weekly_artifacts_updated(ctx: WeeklyReviewContext, previous_mtimes: dict[Path, int | None]) -> None:
    required = (ctx.paths.review, ctx.paths.findings_register, ctx.paths.candidates)
    for path in required:
        if artifact_mtime_ns(path) == previous_mtimes.get(path):
            raise RuntimeError(f"Expected updated weekly artifact in {path}")


def findings_register_summary(path: Path) -> dict[str, int]:
    if not path.exists():
        return {"total": 0, "NUEVO": 0, "PERSISTENTE": 0, "RESUELTO": 0, "RECLASIFICADO": 0}
    text = path.read_text(encoding="utf-8", errors="ignore")
    states = re.findall(r"(?im)^\s*-\s*Estado:\s*(NUEVO|PERSISTENTE|RESUELTO|RECLASIFICADO)\s*$", text)
    summary = {"total": len(states), "NUEVO": 0, "PERSISTENTE": 0, "RESUELTO": 0, "RECLASIFICADO": 0}
    for state in states:
        summary[state] += 1
    return summary


def candidate_initiatives_summary(path: Path) -> dict[str, object]:
    if not path.exists():
        return {"total": 0, "candidate_ids": []}
    text = path.read_text(encoding="utf-8", errors="ignore")
    candidate_ids = re.findall(r"(?im)^###\s+(CANDIDATE-[0-9A-Za-z_-]+)\s*$", text)
    return {"total": len(candidate_ids), "candidate_ids": candidate_ids}


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
    data = read_json(ctx.session_file)
    if payload:
        data.update(payload)
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


def run_state_file_for(ctx: SessionContext) -> Path:
    return ctx.session_dir / "run_state.json"


def safe_slug(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
    cleaned = cleaned.strip("._-")
    return cleaned or "default"


def scoped_name(phase: str, commit_scope: str = "") -> str:
    base = phase.lower()
    if commit_scope.strip():
        return f"{base}_{safe_slug(commit_scope)}"
    return base


def phase_ticket_file_for(ctx: SessionContext, phase: str, commit_scope: str = "") -> Path:
    return ctx.phase_tickets_dir / f"{scoped_name(phase, commit_scope)}.md"


def resume_packet_file_for(ctx: SessionContext, phase: str, commit_scope: str = "") -> Path:
    return ctx.resume_packets_dir / f"{scoped_name(phase, commit_scope)}.md"


def checkpoint_file_for(ctx: SessionContext, commit_scope: str) -> Path:
    return ctx.checkpoints_dir / f"{safe_slug(commit_scope)}.md"


def normalize_effort(value: str) -> str:
    raw = value.strip().strip("`").lower()
    if raw in {"na", "n/a"}:
        return "n/a"
    if raw in {"medium", "high", "max"}:
        return raw
    return ""


def phase_role_for(phase: str) -> str:
    return "motor_auditor" if PHASE_ENGINES.get(phase) == "codex" and phase in {"F3", "F5", "F7"} else "motor_activo"


def effective_reads_for_phase(paths: gpp.InitiativePaths, phase: str) -> list[Path]:
    if phase == "F8":
        reads = [paths.plan, paths.plan_audit, paths.execution, paths.post_audit, paths.real_validation]
        exception_record = paths.root / "exception_record.md"
        return [path for path in [*reads, exception_record] if path.exists()]
    return read_paths_for_phase(paths, phase)


def audit_artifact_for_phase(paths: gpp.InitiativePaths, phase: str) -> Path | None:
    mapping = {
        "F1_REMEDIATION": paths.ask_audit,
        "F4_REMEDIATION": paths.plan_audit,
        "F6_REMEDIATION": paths.post_audit,
    }
    return mapping.get(phase)


def extract_section(text: str, heading: str) -> str:
    lines = text.splitlines()
    capture = False
    bucket: list[str] = []
    for line in lines:
        if gpp.canonical_heading_line(line) == gpp.canonical_heading_line(heading):
            capture = True
            continue
        if capture and gpp.canonical_heading_line(line).startswith("## "):
            break
        if capture:
            bucket.append(line)
    return "\n".join(bucket).strip()


def summarize_hallazgos(path: Path | None) -> str:
    if not path or not path.exists():
        return "- Sin hallazgos registrados para esta fase."
    text = path.read_text(encoding="utf-8", errors="ignore")
    section = extract_section(text, "## Hallazgos")
    if not section:
        return "- Sin hallazgos registrados para esta fase."
    if "Sin hallazgos materiales ni pendientes." in section:
        return "- Sin hallazgos materiales ni pendientes."
    lines = [line.rstrip() for line in section.splitlines() if line.strip()]
    return "\n".join(lines[:6])


def extract_suggested_effort(path: Path | None) -> str:
    if not path or not path.exists():
        return ""
    return normalize_effort(gpp.extract_metadata(gpp.read_text(path), "Esfuerzo sugerido"))


def count_receipts_for_phase(ctx: SessionContext, phase: str) -> int:
    return sum(1 for path in ctx.receipts_dir.glob(f"{phase.upper()}*.json") if path.is_file())


def suggested_claude_effort(ctx: SessionContext, phase: str) -> str:
    audit_path = audit_artifact_for_phase(ctx.paths, phase)
    suggested = extract_suggested_effort(audit_path)
    if suggested and suggested != "n/a":
        return suggested
    exception_record = ctx.paths.root / "exception_record.md"
    if exception_record.exists() and phase.endswith("REMEDIATION"):
        return "max"
    audit_text = gpp.read_text(audit_path) if audit_path else ""
    lowered = gpp.normalize_section_title(audit_text).lower()
    max_keywords = ("wiring", "canonico", "legacy", "transversal", "observable", "owner", "abstraccion")
    if any(keyword in lowered for keyword in max_keywords):
        return "max"
    if phase.endswith("REMEDIATION") and count_receipts_for_phase(ctx, phase) >= 1:
        return "max"
    if phase in {"F4", "F4_REMEDIATION", "F6", "F6_REMEDIATION"}:
        return "high"
    return "medium"


def phase_specific_reentry_notes(phase: str, commit_scope: str = "") -> list[str]:
    if phase in {"F6", "F6_REMEDIATION"}:
        notes = [
            "No dependas de memoria conversacional previa; usa solo ticket, resume packet y artefactos congelados.",
            "Actualiza `execution.md` tu mismo como motor_activo.",
        ]
        if commit_scope.strip():
            notes.append(f"Trabaja solo el tramo autorizado `{commit_scope.strip()}`.")
        return notes
    if phase == "F8":
        return [
            "No replantees F1-F5; guia validacion real sobre artefactos ya congelados.",
            "Usa chat del producto, `trace on` y terminal como evidencia viva de primer nivel.",
            "Para en el primer fallo material salvo bloqueo critico de entorno.",
        ]
    if phase in {"F3", "F5", "F7"}:
        return [
            "No uses observaciones como categoria aparte.",
            "Incluye Hallazgos, Justificacion, Escalado de remediacion y Condicion.",
        ]
    return ["No dependas de memoria conversacional previa; usa ticket y resume packet como estado operativo vigente."]


def base_prompt_file_for_phase(phase: str) -> Path:
    return PROMPTS_ROOT / PHASE_PROMPTS[phase]


def load_prompt_text(name: str) -> str:
    prompt_path = PROMPTS_ROOT / name
    if not prompt_path.exists():
        raise SystemExit(f"Missing prompt file: {prompt_path}")
    return prompt_path.read_text(encoding="utf-8").strip()


def artifact_mtime_ns(path: Path) -> int | None:
    if not path.exists():
        return None
    return path.stat().st_mtime_ns


def prompt_path(ctx: SessionContext, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ctx.target_repo.resolve())).replace("\\", "/")
    except ValueError:
        return str(path)


def build_phase_ticket_content(ctx: SessionContext, phase: str, commit_scope: str = "") -> str:
    template = (RUNTIME_TEMPLATE_ROOT / "phase_ticket.md").read_text(encoding="utf-8")
    reads = effective_reads_for_phase(ctx.paths, phase)
    if ctx.repo_capabilities.exists:
        reads = [ctx.repo_capabilities.profile_path, *reads]
    expected_motor = PHASE_ENGINES.get(phase, gpp.extract_metadata(gpp.read_text(ctx.paths.ask), "motor_activo") or "claude")
    if phase == "F8":
        writes = [ctx.paths.real_validation]
        criterion = "Completar real_validation.md con barrido real, evidencia viva y decision final."
        next_step = "WAITING_FOR_F8"
    else:
        writes = allowed_writes_for_phase(ctx.paths, phase)
        criterion = f"Completar {writes[0].name} con el contrato canonico de {phase}."
        next_step = workflow_state(ctx.paths, str(read_json(ctx.session_file).get("override_phase") or "")).get("next_step", "")
    restrictions = [
        f"Rol autorizado: {phase_role_for(phase)}.",
        "El orquestador no redacta el contenido sustantivo de esta fase.",
    ]
    if commit_scope.strip():
        restrictions.append(f"Scope autorizado para esta corrida: {commit_scope.strip()}.")
    if phase in {"F6", "F6_REMEDIATION"}:
        restrictions.append("El motor_activo debe actualizar execution.md con evidencia real de lo implementado.")
    if phase == "F8":
        restrictions.append("No tocar codigo tras el primer fallo material salvo bloqueo critico de entorno.")
    content = template
    for key, value in (
        ("Initiative ID", ctx.initiative_id),
        ("Fase autorizada", phase),
        ("Rol autorizado", phase_role_for(phase)),
        ("Motor esperado", expected_motor),
        ("Fecha", today_iso()),
    ):
        content = gpp.replace_metadata_line(content, key, value)
    replacements = {
        "## Lecturas obligatorias": "## Lecturas obligatorias\n\n" + "\n".join(f"- {prompt_path(ctx, path)}" for path in reads),
        "## Escrituras autorizadas": "## Escrituras autorizadas\n\n" + "\n".join(f"- {prompt_path(ctx, path)}" for path in writes),
        "## Restricciones operativas": "## Restricciones operativas\n\n" + "\n".join(f"- {line}" for line in restrictions),
        "## Criterio de salida": "## Criterio de salida\n\n- " + criterion,
        "## Siguiente paso permitido": "## Siguiente paso permitido\n\n- " + (next_step or "<pendiente de calcular>"),
    }
    for old, new in replacements.items():
        content = content.replace(old, new)
    return content.rstrip() + "\n"


def build_resume_packet_content(ctx: SessionContext, phase: str, commit_scope: str = "") -> str:
    template = (RUNTIME_TEMPLATE_ROOT / "resume_packet.md").read_text(encoding="utf-8")
    session_data = read_json(ctx.session_file)
    state = workflow_state(ctx.paths, str(session_data.get("override_phase") or ""))
    audit_path = audit_artifact_for_phase(ctx.paths, phase)
    latest = latest_receipt(ctx)
    last_point = latest.get("phase") or session_data.get("last_phase") or "<sin historial>"
    if commit_scope.strip():
        last_point = f"{last_point} | scope actual: {commit_scope.strip()}"
    evidence_lines = [
        f"- Rama declarada: {gpp.declared_branch(ctx.paths) or '<sin rama>'}",
        f"- Ultimo intento registrado: {session_data.get('last_attempt_phase') or '<ninguno>'}",
    ]
    if phase == "F8":
        evidence_lines.extend(
            [
                f"- Artefacto de validacion real: {prompt_path(ctx, ctx.paths.real_validation)}",
                "- Evidencia viva esperada: chat del producto, `trace on`, terminal y resultados visibles.",
            ]
        )
    routing_lines = [f"- {line}" for line in repo_capabilities_summary(ctx.repo_capabilities)]
    if ctx.repo_capabilities.exists:
        routing_lines.insert(0, f"- Perfil local: {prompt_path(ctx, ctx.repo_capabilities.profile_path)}")
    else:
        routing_lines.insert(0, "- Perfil local: NO_ENCONTRADO")
    content = template
    for key, value in (
        ("Initiative ID", ctx.initiative_id),
        ("Fase operativa", phase),
        ("Fecha", today_iso()),
        ("Orquestador", "governance_orchestrator"),
    ):
        content = gpp.replace_metadata_line(content, key, value)
    replacements = {
        "## Estado congelado y gates": "## Estado congelado y gates\n\n"
        + "\n".join(
            f"- {key}: {state.get(key, '<empty>')}"
            for key in ("ask_state", "ask_audit", "plan_state", "plan_audit", "post_audit", "next_step")
        ),
        "## Ultimo punto aceptado": f"## Ultimo punto aceptado\n\n- {last_point}",
        "## Hallazgos o bloqueos abiertos": "## Hallazgos o bloqueos abiertos\n\n" + summarize_hallazgos(audit_path),
        "## Evidencia viva relevante": "## Evidencia viva relevante\n\n" + "\n".join(evidence_lines),
        "## Capas y routing preferido": "## Capas y routing preferido\n\n" + "\n".join(routing_lines),
        "## Instrucciones de reentrada": "## Instrucciones de reentrada\n\n"
        + "\n".join(f"- {line}" for line in phase_specific_reentry_notes(phase, commit_scope)),
    }
    for old, new in replacements.items():
        content = content.replace(old, new)
    return content.rstrip() + "\n"


def write_support_artifacts(ctx: SessionContext, phase: str, commit_scope: str = "") -> tuple[Path, Path]:
    phase_ticket_path = phase_ticket_file_for(ctx, phase, commit_scope)
    resume_packet_path = resume_packet_file_for(ctx, phase, commit_scope)
    phase_ticket_path.write_text(build_phase_ticket_content(ctx, phase, commit_scope), encoding="utf-8")
    resume_packet_path.write_text(build_resume_packet_content(ctx, phase, commit_scope), encoding="utf-8")
    return phase_ticket_path, resume_packet_path


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
    exception_record = paths.root / "exception_record.md"
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
    if exception_record.exists():
        reads.append(exception_record)
    return [path for path in reads if path.exists()]


def build_prompt(ctx: SessionContext, phase: str, escalation_note: str = "", commit_scope: str = "") -> str:
    phase_ticket_path, resume_packet_path = write_support_artifacts(ctx, phase, commit_scope)
    base_prompt = load_prompt_text(PHASE_PROMPTS[phase])
    writes = "\n".join(f"- {prompt_path(ctx, path)}" for path in allowed_writes_for_phase(ctx.paths, phase))
    reads = "\n".join(
        f"- {prompt_path(ctx, path)}"
        for path in [phase_ticket_path, resume_packet_path, *effective_reads_for_phase(ctx.paths, phase)]
    )
    role = phase_role_for(phase)
    artifact = allowed_writes_for_phase(ctx.paths, phase)[0]
    exception_record = ctx.paths.root / "exception_record.md"
    exception_clause = ""
    if exception_record.exists():
        exception_clause = (
            "Hay una excepcion formal activa en esta iniciativa.\n"
            f"- Lee tambien {prompt_path(ctx, exception_record)} y respetala estrictamente.\n"
        )
    escalation_block = ""
    if escalation_note.strip():
        escalation_block = (
            "\n[ESCALADO EXCEPCIONAL]\n"
            f"{escalation_note.strip()}\n"
        )
    commit_scope_block = ""
    if commit_scope.strip():
        commit_scope_block = (
            "\n[SCOPE AUTORIZADO]\n"
            f"- Esta corrida queda limitada al tramo o commit: {commit_scope.strip()}\n"
            "- No avances otros tramos ni cierres fases adicionales.\n"
        )
    writes_block = (
        "Puedes escribir solo:\n"
        f"{writes}\n\n"
    )
    repo_write_rule = ""
    if phase in {"F6", "F6_REMEDIATION"}:
        writes_block = (
            "Puedes modificar el codigo del repo objetivo segun el plan congelado y debes actualizar obligatoriamente:\n"
            f"{writes}\n\n"
        )
        repo_write_rule = (
            "No toques archivos fuera del alcance del plan congelado ni artefactos ajenos a la fase.\n"
        )
    footer = (
        "\n\n[RESULTADO OBLIGATORIO]\n"
        f"- crear o actualizar {prompt_path(ctx, artifact)}\n"
        "- incluir metadata obligatoria\n"
        + (
            "- puedes modificar codigo del repo solo dentro del alcance del plan congelado\n"
            if phase in {"F6", "F6_REMEDIATION"}
            else "- no tocar otros archivos\n"
        )
        + "- si no puedes completar la fase, deja bloqueo con evidencia en el artefacto permitido\n"
    )
    general_write_rule = "No modifiques otros archivos.\n"
    if phase in {"F6", "F6_REMEDIATION"}:
        general_write_rule = "No modifiques archivos fuera del alcance del plan congelado.\n"
    return (
        "[ORCHESTRATOR]\n"
        f"Repo objetivo: {ctx.target_repo}\n"
        f"Initiative ID: {ctx.initiative_id}\n"
        f"Fase operativa: {phase}\n"
        f"Rol esperado: {role}\n"
        f"Motor esperado: {PHASE_ENGINES[phase]}\n\n"
        "Lee solo:\n"
        f"{reads or '- [sin lecturas adicionales]'}\n\n"
        f"{writes_block}"
        f"{general_write_rule}"
        f"{repo_write_rule}"
        f"{commit_scope_block}"
        "Confirma qué iniciativa estás usando antes de trabajar.\n\n"
        f"{exception_clause}"
        f"{base_prompt}"
        f"{escalation_block}"
        f"{footer}"
    )


def write_prompt_copy(ctx: SessionContext, phase: str, prompt: str) -> Path:
    prompt_path = ctx.prompts_dir / f"{phase.lower()}.txt"
    prompt_path.write_text(prompt, encoding="utf-8")
    return prompt_path


def run_claude(
    ctx: SessionContext,
    phase: str,
    prompt: str,
    dry_run: bool,
    model: str = "",
    effort: str = "",
) -> Path:
    output_path = output_file_for(ctx, phase, "claude")
    if dry_run:
        output_path.write_text(prompt, encoding="utf-8")
        return output_path
    settings_path = ctx.target_repo / ".claude" / "settings.local.json"
    command = ["claude", "-p", "--output-format", "text", "--permission-mode", "bypassPermissions"]
    if model:
        command.extend(["--model", model])
    if effort:
        command.extend(["--effort", effort])
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


def run_codex(ctx: SessionContext, phase: str, prompt: str, dry_run: bool, model: str = "") -> Path:
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
    ]
    if model:
        command.extend(["-m", model])
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
    output_path.write_text((result.stdout or "") + (("\n" + result.stderr) if result.stderr else ""), encoding="utf-8")
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "Codex command failed")
    return output_path


def ensure_phase_artifact(paths: gpp.InitiativePaths, phase: str, previous_mtime_ns: int | None = None) -> None:
    primary_artifact = allowed_writes_for_phase(paths, phase)[0]
    current_mtime_ns = artifact_mtime_ns(primary_artifact)
    if previous_mtime_ns is not None and current_mtime_ns == previous_mtime_ns:
        raise RuntimeError(f"Expected updated artifact in {primary_artifact}")
    if phase in {"F1", "F1_REMEDIATION"}:
        if not gpp.document_has_meaningful_content(paths.ask, gpp.ASK_HEADINGS):
            raise RuntimeError(f"Expected meaningful ask content in {paths.ask}")
        return
    if phase == "F3":
        gpp.ensure_strict_audit_artifact(paths.ask_audit)
        return
    if phase in {"F4", "F4_REMEDIATION"}:
        if not gpp.document_has_meaningful_content(paths.plan, gpp.PLAN_HEADINGS):
            raise RuntimeError(f"Expected meaningful plan content in {paths.plan}")
        return
    if phase == "F5":
        gpp.ensure_strict_audit_artifact(paths.plan_audit)
        return
    if phase in {"F6", "F6_REMEDIATION"}:
        if not gpp.document_has_meaningful_content(paths.execution, gpp.EXECUTION_HEADINGS):
            raise RuntimeError(f"Expected meaningful execution content in {paths.execution}")
        return
    if phase == "F7":
        gpp.ensure_strict_audit_artifact(paths.post_audit)
        return
    raise SystemExit(f"Unsupported phase: {phase}")


def ensure_checkpoint_artifact(path: Path, previous_mtime_ns: int | None = None) -> None:
    current_mtime_ns = artifact_mtime_ns(path)
    if previous_mtime_ns is not None and current_mtime_ns == previous_mtime_ns:
        raise RuntimeError(f"Expected updated checkpoint artifact in {path}")
    text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
    verdict = gpp.extract_metadata(text, "Veredicto").strip().strip("`").upper()
    if verdict not in {"CHECKPOINT_OK", "CHECKPOINT_CON_HALLAZGOS", "BLOQUEO_DE_EJECUCION"}:
        raise RuntimeError(f"Expected checkpoint verdict in {path}")
    normalized = gpp.normalize_section_title(text)
    for required in ("## Hallazgos", "## Contraste contra plan y execution", "## Condicion para liberar el siguiente tramo"):
        if required not in normalized:
            raise RuntimeError(f"Expected section '{required}' in {path}")


def build_checkpoint_prompt(ctx: SessionContext, commit_scope: str) -> tuple[str, Path]:
    phase_ticket_path, resume_packet_path = write_support_artifacts(ctx, "F6", commit_scope)
    checkpoint_path = checkpoint_file_for(ctx, commit_scope)
    if not checkpoint_path.exists():
        template = (RUNTIME_TEMPLATE_ROOT / "execution_checkpoint.md").read_text(encoding="utf-8")
        text = template
        for key, value in (
            ("Initiative ID", ctx.initiative_id),
            ("Commit scope", commit_scope),
            ("Auditor", gpp.extract_metadata(gpp.read_text(ctx.paths.ask), "motor_auditor") or "codex"),
            ("Fecha", today_iso()),
        ):
            text = gpp.replace_metadata_line(text, key, value)
        checkpoint_path.write_text(text, encoding="utf-8")
    reads = "\n".join(
        f"- {prompt_path(ctx, path)}"
        for path in [phase_ticket_path, resume_packet_path, ctx.paths.plan, ctx.paths.plan_audit, ctx.paths.execution]
        if path.exists()
    )
    prompt = (
        "[ORCHESTRATOR]\n"
        f"Repo objetivo: {ctx.target_repo}\n"
        f"Initiative ID: {ctx.initiative_id}\n"
        "Fase operativa: F6_CHECKPOINT\n"
        "Rol esperado: motor_auditor\n"
        "Motor esperado: codex\n\n"
        "Lee solo:\n"
        f"{reads}\n\n"
        "Puedes escribir solo:\n"
        f"- {prompt_path(ctx, checkpoint_path)}\n\n"
        "No modifiques artefactos de iniciativa ni codigo.\n"
        f"- Scope autorizado: {commit_scope}\n\n"
        f"{load_prompt_text(CHECKPOINT_PROMPT)}\n\n"
        "[RESULTADO OBLIGATORIO]\n"
        f"- crear o actualizar {prompt_path(ctx, checkpoint_path)}\n"
        "- no emitir PASS o FAIL formales\n"
        "- si no puedes completar el checkpoint, deja BLOQUEO_DE_EJECUCION con evidencia\n"
    )
    return prompt, checkpoint_path


def recover_audit_artifact(ctx: SessionContext, phase: str, output_path: Path) -> bool:
    if phase not in AUDIT_ARTIFACTS or not output_path.exists():
        return False
    text = output_path.read_text(encoding="utf-8", errors="ignore")
    matches = re.findall(r"```(?:md)?\s*\n(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
    expected_title = AUDIT_TITLES[phase]
    for candidate in reversed(matches):
        content = candidate.strip()
        if expected_title in content:
            artifact = getattr(ctx.paths, AUDIT_ARTIFACTS[phase][1])
            artifact.write_text(content + "\n", encoding="utf-8")
            return True
    return False


def run_phase(
    ctx: SessionContext,
    phase: str,
    dry_run: bool = False,
    allow_dirty_with_ask_exception: bool = False,
    claude_model: str = "",
    claude_effort: str = "",
    codex_model: str = "",
    escalation_note: str = "",
    commit_scope: str = "",
) -> dict:
    effective_claude_effort = claude_effort or (suggested_claude_effort(ctx, phase) if PHASE_ENGINES[phase] == "claude" else "")
    prompt = build_prompt(ctx, phase, escalation_note=escalation_note, commit_scope=commit_scope)
    prompt_copy = write_prompt_copy(ctx, phase, prompt)
    engine = PHASE_ENGINES[phase]
    output_path = output_file_for(ctx, phase, engine)
    primary_artifact = allowed_writes_for_phase(ctx.paths, phase)[0]
    previous_mtime_ns = artifact_mtime_ns(primary_artifact)
    started_at = dt.datetime.now(dt.timezone.utc).isoformat()
    base_receipt = {
        "phase": phase,
        "engine": engine,
        "initiative_id": ctx.initiative_id,
        "target_repo": str(ctx.target_repo),
        "prompt_file": str(prompt_copy),
        "output_file": str(output_path),
        "allowed_writes": [str(path) for path in allowed_writes_for_phase(ctx.paths, phase)],
        "commit_scope": commit_scope,
        "claude_effort": effective_claude_effort,
        "started_at": started_at,
        "timestamp": started_at,
    }
    write_json(run_state_file_for(ctx), {**base_receipt, "status": "running"})
    persist_session(ctx, {"active_phase": phase, "active_engine": engine, "last_attempt_phase": phase})
    recovered_artifact = False
    try:
        if phase in {"F6", "F6_REMEDIATION"}:
            ensure_phase_seed_artifacts(ctx, phase)
            gpp.ensure_f6_branch(ctx.paths, dry_run=dry_run)
            gpp.run_preflight(
                ctx.initiative_id,
                allow_dirty_with_ask_exception=allow_dirty_with_ask_exception,
                dry_run=dry_run,
            )
        output_path = (
            run_claude(
                ctx,
                phase,
                prompt,
                dry_run=dry_run,
                model=claude_model,
                effort=effective_claude_effort,
            )
            if engine == "claude"
            else run_codex(
                ctx,
                phase,
                prompt,
                dry_run=dry_run,
                model=codex_model,
            )
        )
        try:
            ensure_phase_artifact(ctx.paths, phase, previous_mtime_ns=previous_mtime_ns)
        except RuntimeError as exc:
            if phase in AUDIT_ARTIFACTS and recover_audit_artifact(ctx, phase, output_path):
                recovered_artifact = True
                ensure_phase_artifact(ctx.paths, phase, previous_mtime_ns=previous_mtime_ns)
            else:
                raise
        receipt = {
            **base_receipt,
            "status": "completed",
            "output_file": str(output_path),
            "snapshot": snapshot(ctx.paths),
            "finished_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "recovered_artifact": recovered_artifact,
        }
        write_json(receipt_file_for(ctx, phase), receipt)
        write_json(run_state_file_for(ctx), receipt)
        persist_session(
            ctx,
            {
                "last_phase": phase,
                "last_engine": engine,
                "last_attempt_phase": phase,
                "last_error": "",
                "active_phase": "",
                "active_engine": "",
                "override_phase": "",
            },
        )
        return receipt
    except Exception as exc:
        failed_receipt = {
            **base_receipt,
            "status": "failed",
            "error": str(exc),
            "snapshot": snapshot(ctx.paths),
            "finished_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        }
        write_json(receipt_file_for(ctx, phase), failed_receipt)
        write_json(run_state_file_for(ctx), failed_receipt)
        persist_session(
            ctx,
            {
                "last_attempt_phase": phase,
                "last_engine": engine,
                "last_error": str(exc),
                "active_phase": "",
                "active_engine": "",
            },
        )
        raise


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
    last_phase = str(data.get("last_attempt_phase") or data.get("last_phase") or "")
    if not last_phase:
        return read_json(run_state_file_for(ctx))
    path = receipt_file_for(ctx, last_phase)
    if not path.exists():
        return read_json(run_state_file_for(ctx))
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


def ensure_phase_seed_artifacts(ctx: SessionContext, phase: str) -> None:
    if phase not in {"F6", "F6_REMEDIATION", "F7"}:
        return
    if ctx.paths.post_audit.exists():
        return
    template = (gpp.TEMPLATE_ROOT / "post_audit.md").read_text(encoding="utf-8")
    text = template
    for key, value in (
        ("Initiative ID", ctx.initiative_id),
        ("Modo", "M4"),
        ("Estado", "PROPUESTO"),
        ("Fecha", today_iso()),
        ("motor_auditor", gpp.extract_metadata(gpp.read_text(ctx.paths.ask), "motor_auditor") or "codex"),
        ("Rama", gpp.declared_branch(ctx.paths)),
        ("baseline_mit", gpp.extract_metadata(gpp.read_text(ctx.paths.ask), "baseline_mit") or gpp.DEFAULT_BASELINE_MIT),
    ):
        text = gpp.replace_metadata_line(text, key, value)
    ctx.paths.post_audit.write_text(text, encoding="utf-8")


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
    for key in ("status", "phase", "engine", "prompt_file", "output_file", "timestamp", "started_at", "finished_at", "error"):
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
        raise SystemExit("Next step is WAITING_FOR_F8. Use prepare-f8 and show-bootstrap --phase F8 before ejecutar la validacion real manual.")
    phase = state.get("phase")
    if not phase:
        raise SystemExit(f"Unsupported next step: {next_step}")
    receipt = run_phase(
        ctx,
        phase,
        dry_run=args.dry_run,
        allow_dirty_with_ask_exception=args.allow_dirty_with_ask_exception,
        claude_model=args.claude_model,
        claude_effort=args.claude_effort,
        codex_model=args.codex_model,
        escalation_note=args.escalation_note,
        commit_scope=getattr(args, "commit_scope", ""),
    )
    print(json.dumps(receipt, indent=2, ensure_ascii=True))
    return 0


def run_named_phase(args: argparse.Namespace, phase: str) -> int:
    ctx = build_session_context(parse_target_repo(args.target_repo), args.initiative_id)
    gpp.configure_repo_root(str(ctx.target_repo))
    gpp.ensure_repo_supports_governance()
    require_paths(ctx)
    receipt = run_phase(
        ctx,
        phase,
        dry_run=args.dry_run,
        allow_dirty_with_ask_exception=getattr(args, "allow_dirty_with_ask_exception", False),
        claude_model=getattr(args, "claude_model", ""),
        claude_effort=getattr(args, "claude_effort", ""),
        codex_model=getattr(args, "codex_model", ""),
        escalation_note=getattr(args, "escalation_note", ""),
        commit_scope=getattr(args, "commit_scope", ""),
    )
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
            ("motor_activo", gpp.extract_metadata(gpp.read_text(ctx.paths.ask), "motor_activo") or "claude"),
            ("motor_auditor", gpp.extract_metadata(gpp.read_text(ctx.paths.ask), "motor_auditor") or "codex"),
            ("Rama", gpp.declared_branch(ctx.paths)),
            ("baseline_mit", gpp.extract_metadata(gpp.read_text(ctx.paths.ask), "baseline_mit") or gpp.DEFAULT_BASELINE_MIT),
        ):
            text = gpp.replace_metadata_line(text, key, value)
        ctx.paths.real_validation.write_text(text, encoding="utf-8")
    phase_ticket_path, resume_packet_path = write_support_artifacts(ctx, "F8")
    persist_session(ctx, {"last_phase": "F8_PREP", "override_phase": ""})
    print(f"initiative_id={ctx.initiative_id}")
    print(f"real_validation={ctx.paths.real_validation}")
    print(f"phase_ticket={phase_ticket_path}")
    print(f"resume_packet={resume_packet_path}")
    print("next_step=WAITING_FOR_F8")
    return 0


def show_bootstrap(args: argparse.Namespace) -> int:
    ctx = build_session_context(parse_target_repo(args.target_repo), args.initiative_id)
    gpp.configure_repo_root(str(ctx.target_repo))
    gpp.ensure_repo_supports_governance()
    require_paths(ctx)
    requested_phase = getattr(args, "phase", "").strip().upper()
    if not requested_phase:
        state = current_workflow_state(ctx)
        if state["next_step"] == "WAITING_FOR_F8":
            requested_phase = "F8"
        else:
            requested_phase = state.get("phase", "")
    if not requested_phase:
        raise SystemExit("Could not infer phase for bootstrap. Use --phase.")
    phase_ticket_path, resume_packet_path = write_support_artifacts(ctx, requested_phase, getattr(args, "commit_scope", ""))
    print(f"initiative_id={ctx.initiative_id}")
    print(f"phase={requested_phase}")
    print(f"phase_ticket={phase_ticket_path}")
    print(f"resume_packet={resume_packet_path}")
    print("\n[PHASE TICKET]\n")
    print(phase_ticket_path.read_text(encoding="utf-8"))
    print("\n[RESUME PACKET]\n")
    print(resume_packet_path.read_text(encoding="utf-8"))
    return 0


def run_f6_checkpoint(args: argparse.Namespace) -> int:
    ctx = build_session_context(parse_target_repo(args.target_repo), args.initiative_id)
    gpp.configure_repo_root(str(ctx.target_repo))
    gpp.ensure_repo_supports_governance()
    require_paths(ctx)
    commit_scope = getattr(args, "commit_scope", "").strip()
    if not commit_scope:
        raise SystemExit("run-f6-checkpoint requires --commit-scope")
    prompt, checkpoint_path = build_checkpoint_prompt(ctx, commit_scope)
    prompt_copy = ctx.prompts_dir / f"f6_checkpoint_{safe_slug(commit_scope)}.txt"
    prompt_copy.write_text(prompt, encoding="utf-8")
    previous_mtime_ns = artifact_mtime_ns(checkpoint_path)
    output_path = output_file_for(ctx, f"f6_checkpoint_{safe_slug(commit_scope)}", "codex")
    started_at = dt.datetime.now(dt.timezone.utc).isoformat()
    base_receipt = {
        "phase": "F6_CHECKPOINT",
        "engine": "codex",
        "initiative_id": ctx.initiative_id,
        "target_repo": str(ctx.target_repo),
        "prompt_file": str(prompt_copy),
        "output_file": str(output_path),
        "checkpoint_file": str(checkpoint_path),
        "commit_scope": commit_scope,
        "started_at": started_at,
        "timestamp": started_at,
    }
    write_json(run_state_file_for(ctx), {**base_receipt, "status": "running"})
    persist_session(ctx, {"active_phase": "F6_CHECKPOINT", "active_engine": "codex", "last_attempt_phase": "F6_CHECKPOINT"})
    if args.dry_run:
        output_path.write_text(prompt, encoding="utf-8")
    else:
        output_path = run_codex(ctx, "f6_checkpoint_" + safe_slug(commit_scope), prompt, dry_run=False, model=args.codex_model)
        ensure_checkpoint_artifact(checkpoint_path, previous_mtime_ns=previous_mtime_ns)
    receipt = {
        **base_receipt,
        "status": "completed",
        "finished_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    write_json(receipt_file_for(ctx, f"F6_CHECKPOINT_{safe_slug(commit_scope)}"), receipt)
    write_json(run_state_file_for(ctx), receipt)
    persist_session(
        ctx,
        {
            "last_phase": "F6_CHECKPOINT",
            "last_engine": "codex",
            "last_error": "",
            "active_phase": "",
            "active_engine": "",
            "last_checkpoint_scope": commit_scope,
        },
    )
    print(json.dumps(receipt, indent=2, ensure_ascii=True))
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
        "repo_governance_profile": str(ctx.repo_capabilities.profile_path),
        "repo_governance_profile_exists": ctx.repo_capabilities.exists,
        "capabilities": {
            "governance_search": ctx.repo_capabilities.governance_search,
            "symdex_code": ctx.repo_capabilities.symdex_code,
            "codebase_memory_mcp": ctx.repo_capabilities.structural_memory,
            "f8_observable": ctx.repo_capabilities.f8_observable,
            "trace_on": ctx.repo_capabilities.trace_on,
            "terminal_logs": ctx.repo_capabilities.terminal_logs,
        },
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


def prepare_weekly_review(args: argparse.Namespace) -> int:
    target_repo = parse_target_repo(args.target_repo)
    gpp.configure_repo_root(str(target_repo))
    gpp.ensure_repo_supports_governance()
    ctx = build_weekly_review_context(target_repo, args.review_date)
    summary = scaffold_weekly_review_artifacts(ctx, initial_baseline=args.initial_baseline)
    ctx.paths.briefing.write_text(
        render_weekly_briefing(ctx, summary["review_mode"], summary["compare_against"]),
        encoding="utf-8",
    )
    write_json(
        ctx.session_file,
        {
            "session_id": ctx.session_id,
            "target_repo": str(ctx.target_repo),
            "review_date": ctx.review_date,
            "review_mode": summary["review_mode"],
            "compare_against": summary["compare_against"],
            "updated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        },
    )
    print(f"review_date={ctx.review_date}")
    print(f"review_mode={summary['review_mode']}")
    print(f"briefing={ctx.paths.briefing}")
    print(f"weekly_review={ctx.paths.review}")
    print(f"weekly_delta={ctx.paths.delta}")
    print(f"findings_register={ctx.paths.findings_register}")
    print(f"candidate_initiatives={ctx.paths.candidates}")
    return 0


def run_weekly_review(args: argparse.Namespace) -> int:
    target_repo = parse_target_repo(args.target_repo)
    gpp.configure_repo_root(str(target_repo))
    gpp.ensure_repo_supports_governance()
    ctx = build_weekly_review_context(target_repo, args.review_date)
    summary = scaffold_weekly_review_artifacts(ctx, initial_baseline=args.initial_baseline)
    ctx.paths.briefing.write_text(
        render_weekly_briefing(ctx, summary["review_mode"], summary["compare_against"]),
        encoding="utf-8",
    )
    prompt = build_weekly_review_prompt(ctx, summary["review_mode"])
    prompt_copy = weekly_prompt_copy_for(ctx)
    prompt_copy.write_text(prompt, encoding="utf-8")
    previous_mtimes = weekly_artifact_mtimes(ctx)
    output_path = weekly_output_file_for(ctx, "claude")
    started_at = dt.datetime.now(dt.timezone.utc).isoformat()
    if args.dry_run:
        output_path.write_text(prompt, encoding="utf-8")
    else:
        output_path = run_claude(
            build_session_context(ctx.target_repo, args.initiative_id),
            f"weekly_review_{ctx.review_date}",
            prompt,
            dry_run=False,
            model=args.claude_model,
            effort=args.claude_effort,
        )
        ensure_weekly_artifacts_updated(ctx, previous_mtimes)
    findings_summary = findings_register_summary(ctx.paths.findings_register)
    candidates_summary = candidate_initiatives_summary(ctx.paths.candidates)
    receipt = {
        "status": "completed",
        "phase": "WEEKLY_REVIEW",
        "engine": "claude",
        "target_repo": str(ctx.target_repo),
        "review_date": ctx.review_date,
        "review_mode": summary["review_mode"],
        "prompt_file": str(prompt_copy),
        "output_file": str(output_path),
        "briefing_file": str(ctx.paths.briefing),
        "review_file": str(ctx.paths.review),
        "delta_file": str(ctx.paths.delta),
        "findings_register_file": str(ctx.paths.findings_register),
        "findings_summary": findings_summary,
        "candidate_initiatives_file": str(ctx.paths.candidates),
        "candidate_initiatives_summary": candidates_summary,
        "started_at": started_at,
        "finished_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "timestamp": started_at,
    }
    write_json(weekly_receipt_file_for(ctx), receipt)
    write_json(
        ctx.session_file,
        {
            "session_id": ctx.session_id,
            "target_repo": str(ctx.target_repo),
            "review_date": ctx.review_date,
            "review_mode": summary["review_mode"],
            "compare_against": summary["compare_against"],
            "last_phase": "WEEKLY_REVIEW",
            "findings_summary": findings_summary,
            "candidate_initiatives_summary": candidates_summary,
            "updated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        },
    )
    print(json.dumps(receipt, indent=2, ensure_ascii=True))
    return 0


def list_weekly_candidates(args: argparse.Namespace) -> int:
    target_repo = parse_target_repo(args.target_repo)
    gpp.configure_repo_root(str(target_repo))
    gpp.ensure_repo_supports_governance()
    ctx = build_weekly_review_context(target_repo, args.review_date)
    summary = candidate_initiatives_summary(ctx.paths.candidates)
    print(f"review_date={ctx.review_date}")
    print(f"candidate_total={summary['total']}")
    for candidate_id in summary["candidate_ids"]:
        print(f"candidate_id={candidate_id}")
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
        description="Orquestador canónico de gobernanza M4: coordina fase, continuidad, tickets, checkpoints y receipts dentro del repo objetivo sin sustituir la autoría de los motores."
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

    bootstrap_parser = subparsers.add_parser("show-bootstrap", help="Renderiza phase_ticket y resume_packet para pegar contexto en un chat nuevo.")
    bootstrap_parser.add_argument("--phase", default="")
    bootstrap_parser.add_argument("--commit-scope", default="")
    bootstrap_parser.set_defaults(func=show_bootstrap)

    checkpoint_parser = subparsers.add_parser("run-f6-checkpoint", help="Ejecuta un checkpoint lateral de F6 sobre un tramo o commit concreto.")
    checkpoint_parser.add_argument("--commit-scope", required=True)
    checkpoint_parser.add_argument("--dry-run", action="store_true")
    checkpoint_parser.add_argument("--codex-model", default="")
    checkpoint_parser.set_defaults(func=run_f6_checkpoint)

    doctor_parser = subparsers.add_parser("doctor", help="Diagnostica disponibilidad del orquestador y del repo objetivo.")
    doctor_parser.set_defaults(func=doctor)

    weekly_prepare_parser = subparsers.add_parser(
        "prepare-weekly-review",
        help="Prepara el arbol de artefactos de la review semanal MIT.",
    )
    weekly_prepare_parser.add_argument("--review-date", required=True)
    weekly_prepare_parser.add_argument("--initial-baseline", action="store_true")
    weekly_prepare_parser.set_defaults(func=prepare_weekly_review)

    weekly_run_parser = subparsers.add_parser(
        "run-weekly-review",
        help="Ejecuta la review semanal MIT con briefing canonico y receipt local.",
    )
    weekly_run_parser.add_argument("--review-date", required=True)
    weekly_run_parser.add_argument("--initial-baseline", action="store_true")
    weekly_run_parser.add_argument("--dry-run", action="store_true")
    weekly_run_parser.add_argument("--claude-model", default="")
    weekly_run_parser.add_argument("--claude-effort", default="")
    weekly_run_parser.set_defaults(func=run_weekly_review)

    weekly_candidates_parser = subparsers.add_parser(
        "list-weekly-candidates",
        help="Lista iniciativas candidatas detectadas por la review semanal.",
    )
    weekly_candidates_parser.add_argument("--review-date", required=True)
    weekly_candidates_parser.set_defaults(func=list_weekly_candidates)

    current_parser = subparsers.add_parser("run-current-step", help="Ejecuta el paso actual sugerido por la máquina de estados.")
    current_parser.add_argument("--dry-run", action="store_true")
    current_parser.add_argument("--allow-dirty-with-ask-exception", action="store_true")
    current_parser.add_argument("--claude-model", default="")
    current_parser.add_argument("--claude-effort", default="")
    current_parser.add_argument("--codex-model", default="")
    current_parser.add_argument("--escalation-note", default="")
    current_parser.add_argument("--commit-scope", default="")
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
        phase_parser.add_argument("--claude-model", default="")
        phase_parser.add_argument("--claude-effort", default="")
        phase_parser.add_argument("--codex-model", default="")
        phase_parser.add_argument("--escalation-note", default="")
        phase_parser.add_argument("--commit-scope", default="")
        if phase in {"F6", "F6_REMEDIATION", "F7"}:
            phase_parser.add_argument("--allow-dirty-with-ask-exception", action="store_true")
        phase_parser.set_defaults(func=lambda args, phase=phase: run_named_phase(args, phase))

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
