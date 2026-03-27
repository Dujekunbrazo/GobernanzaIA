from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

CANONICAL_REPO_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = CANONICAL_REPO_ROOT
INITIATIVES_ROOT = REPO_ROOT / "dev" / "records" / "initiatives"
TEMPLATE_ROOT = REPO_ROOT / "dev" / "templates" / "initiative"
DEFAULT_BASELINE_MIT = "MIT Concept-Sync"
DEFAULT_MAX_AUDITS = 3
M4_ARTIFACTS = (
    "ask.md",
    "ask_audit.md",
    "plan.md",
    "plan_audit.md",
    "execution.md",
    "post_audit.md",
    "closeout.md",
    "lessons_learned.md",
)
OPTIONAL_ARTIFACTS = ("handoff.md", "real_validation.md")
ASK_HEADINGS = (
    "## Objetivo y contexto",
    "## Evidencia tecnica",
    "## Supuestos",
    "## Preguntas bloqueantes / no bloqueantes",
    "## Opciones y trade-offs",
    "## Recomendacion Ask",
    "## Criterios de aceptacion para el motor_activo",
)
PLAN_HEADINGS = (
    "## Objetivo",
    "## Alcance",
    "## No-alcance",
    "## Impacto tecnico",
    "## Riesgos (Top 3)",
    "## Plan por commits",
    "## Rollback",
    "## Definition of Done",
)
EXECUTION_HEADINGS = (
    "## Referencia al plan congelado",
    "## Commits ejecutados",
    "## Validaciones",
    "## Riesgos detectados",
)


@dataclass(frozen=True)
class InitiativePaths:
    initiative_id: str
    root: Path
    ask: Path
    ask_audit: Path
    handoff: Path
    plan: Path
    plan_audit: Path
    execution: Path
    post_audit: Path
    closeout: Path
    lessons: Path
    real_validation: Path


def configure_repo_root(target_repo: str) -> None:
    global REPO_ROOT, INITIATIVES_ROOT, TEMPLATE_ROOT
    resolved = Path(target_repo).expanduser().resolve() if target_repo else CANONICAL_REPO_ROOT
    REPO_ROOT = resolved
    INITIATIVES_ROOT = REPO_ROOT / "dev" / "records" / "initiatives"
    TEMPLATE_ROOT = REPO_ROOT / "dev" / "templates" / "initiative"


def get_effective_repo_root(args: argparse.Namespace) -> Path:
    if getattr(args, "target_repo", ""):
        return Path(args.target_repo).expanduser().resolve()
    env_value = os.environ.get("GOVERNANCE_TARGET_REPO", "").strip()
    if env_value:
        return Path(env_value).expanduser().resolve()
    return CANONICAL_REPO_ROOT


def ensure_repo_supports_governance() -> None:
    missing: list[str] = []
    if not (REPO_ROOT / "AGENTS.md").exists():
        missing.append("AGENTS.md")
    if not TEMPLATE_ROOT.exists():
        missing.append("dev/templates/initiative")
    if not (REPO_ROOT / "scripts" / "dev" / "initiative_preflight.py").exists():
        missing.append("scripts/dev/initiative_preflight.py")
    if missing:
        raise SystemExit(
            f"Target repo does not look governance-ready: {REPO_ROOT} | missing: {', '.join(missing)}"
        )


def today_iso() -> str:
    return dt.date.today().isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def replace_metadata_line(text: str, key: str, value: str) -> str:
    pattern = re.compile(rf"^- {re.escape(key)}:.*$", re.MULTILINE)
    line = f"- {key}: {value}"
    if pattern.search(text):
        return pattern.sub(line, text, count=1)
    if text.startswith("# "):
        parts = text.splitlines()
        return "\n".join([parts[0], "", line, *parts[1:]]) + ("\n" if text.endswith("\n") else "")
    return f"{line}\n{text}"


def extract_metadata(text: str, key: str) -> str:
    match = re.search(rf"^- {re.escape(key)}:\s*(.*)$", text, re.MULTILINE)
    if not match:
        return ""
    return match.group(1).strip()


def normalize_section_title(heading: str) -> str:
    translation = str.maketrans(
        {
            "á": "a",
            "é": "e",
            "í": "i",
            "ó": "o",
            "ú": "u",
            "Á": "A",
            "É": "E",
            "Í": "I",
            "Ó": "O",
            "Ú": "U",
        }
    )
    return heading.translate(translation)


def section_has_content(text: str, heading: str) -> bool:
    heading = normalize_section_title(heading)
    normalized_text = normalize_section_title(text)
    lines = normalized_text.splitlines()
    capture = False
    bucket: list[str] = []
    for line in lines:
        if line.strip() == heading.strip():
            capture = True
            bucket = []
            continue
        if capture and line.startswith("## "):
            break
        if capture:
            bucket.append(line)
    for line in bucket:
        stripped = line.strip()
        if stripped and not stripped.startswith("1.") and stripped not in {"-", "1."}:
            return True
    return False


def document_has_meaningful_content(path: Path, headings: tuple[str, ...]) -> bool:
    text = read_text(path)
    return any(section_has_content(text, heading) for heading in headings)


def get_verdict(path: Path) -> str:
    verdict = extract_metadata(read_text(path), "Veredicto")
    return verdict.upper()


def get_state(path: Path) -> str:
    state = extract_metadata(read_text(path), "Estado")
    return state.upper()


def set_state(path: Path, state: str) -> None:
    text = read_text(path)
    write_text(path, replace_metadata_line(text, "Estado", state))


def set_metadata(path: Path, key: str, value: str) -> None:
    text = read_text(path)
    write_text(path, replace_metadata_line(text, key, value))


def get_git_branch() -> str:
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
        check=False,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def planned_branch_name(initiative_id: str) -> str:
    return f"initiative/{initiative_id.replace('_', '-')}"


def git_run(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def get_paths(initiative_id: str) -> InitiativePaths:
    root = INITIATIVES_ROOT / initiative_id
    return InitiativePaths(
        initiative_id=initiative_id,
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


def initiative_exists(paths: InitiativePaths) -> bool:
    return paths.root.exists()


def populate_template(
    template_name: str,
    initiative_id: str,
    mode: str,
    motor_activo: str,
    motor_auditor: str,
    branch: str,
    baseline_mit: str,
) -> str:
    text = read_text(TEMPLATE_ROOT / template_name)
    fields = {
        "Initiative ID": initiative_id,
        "Modo": mode,
        "Fecha": today_iso(),
        "motor_activo": motor_activo,
        "motor_auditor": motor_auditor,
        "Rama": branch,
        "baseline_mit": baseline_mit,
    }
    for key, value in fields.items():
        if value:
            text = replace_metadata_line(text, key, value)
    if template_name == "ask.md":
        text = replace_metadata_line(text, "Estado", "PROPUESTO")
    if template_name == "plan.md":
        text = replace_metadata_line(text, "Estado", "PROPUESTO")
        text = replace_metadata_line(text, "Etiqueta", "PENDIENTE DE AUDITORIA DEL MOTOR_AUDITOR")
    return text


def init_artifacts(args: argparse.Namespace) -> int:
    paths = get_paths(args.initiative_id)
    if initiative_exists(paths) and not args.force:
        raise SystemExit(f"Initiative already exists: {paths.root}")
    paths.root.mkdir(parents=True, exist_ok=True)
    branch = args.branch or planned_branch_name(args.initiative_id)
    for name in M4_ARTIFACTS:
        target = paths.root / name
        text = populate_template(
            name,
            initiative_id=args.initiative_id,
            mode="M4",
            motor_activo=args.motor_activo,
            motor_auditor=args.motor_auditor,
            branch=branch,
            baseline_mit=args.baseline_mit,
        )
        if args.summary and name == "ask.md":
            text = text.replace("## Objetivo y contexto\n", f"## Objetivo y contexto\n\n{args.summary}\n\n", 1)
        write_text(target, text)
    for name in OPTIONAL_ARTIFACTS:
        should_create = name == "handoff.md" and args.with_handoff
        should_create = should_create or (name == "real_validation.md" and args.with_real_validation)
        if should_create:
            target = paths.root / name
            text = populate_template(
                name,
                initiative_id=args.initiative_id,
                mode="M4",
                motor_activo=args.motor_activo,
                motor_auditor=args.motor_auditor,
                branch=branch,
                baseline_mit=args.baseline_mit,
            )
            write_text(target, text)
    print(f"Created initiative scaffold: {paths.root}")
    print("Next steps:")
    print(f"- Edit {paths.ask} or {paths.handoff} before the first automated pass")
    print(f"- Run: python scripts/dev/governance_ping_pong.py advance --initiative-id {args.initiative_id}")
    return 0


def approve_f2(args: argparse.Namespace) -> int:
    paths = get_paths(args.initiative_id)
    if not initiative_exists(paths):
        raise SystemExit(f"Missing initiative folder: {paths.root}")
    if not document_has_meaningful_content(paths.ask, ASK_HEADINGS):
        raise SystemExit("ask.md does not contain enough content for F2 validation")
    set_state(paths.ask, "VALIDADO")
    for path in (paths.ask, paths.plan, paths.execution, paths.closeout, paths.lessons):
        set_metadata(path, "motor_auditor", args.motor_auditor)
    print(f"F2 approved for {args.initiative_id}. motor_auditor={args.motor_auditor}")
    print(f"Run: python scripts/dev/governance_ping_pong.py advance --initiative-id {args.initiative_id}")
    return 0


def status(args: argparse.Namespace) -> int:
    paths = get_paths(args.initiative_id)
    if not initiative_exists(paths):
        raise SystemExit(f"Missing initiative folder: {paths.root}")
    ask_state = get_state(paths.ask)
    plan_state = get_state(paths.plan)
    ask_verdict = get_verdict(paths.ask_audit)
    plan_verdict = get_verdict(paths.plan_audit)
    post_verdict = get_verdict(paths.post_audit)
    print(f"initiative_id={args.initiative_id}")
    print(f"ask_state={ask_state or '<empty>'}")
    print(f"ask_audit={ask_verdict or '<empty>'}")
    print(f"plan_state={plan_state or '<empty>'}")
    print(f"plan_audit={plan_verdict or '<empty>'}")
    print(f"post_audit={post_verdict or '<empty>'}")
    print(f"next_step={recommend_next_step(paths)}")
    return 0


def recommend_next_step(paths: InitiativePaths) -> str:
    ask_state = get_state(paths.ask)
    plan_state = get_state(paths.plan)
    post_verdict = get_verdict(paths.post_audit)
    if post_verdict == "PASS":
        return "WAITING_FOR_F8"
    if plan_state == "CONGELADO":
        return "RUN_F6_F7"
    if get_verdict(paths.plan_audit) == "FAIL":
        return "RUN_F4_F5_REMEDIATION"
    if document_has_meaningful_content(paths.plan, PLAN_HEADINGS):
        return "RUN_F5"
    if ask_state == "CONGELADO":
        return "RUN_F4"
    if get_verdict(paths.ask_audit) == "FAIL":
        return "RUN_F1_F3_REMEDIATION"
    if ask_state == "VALIDADO":
        return "RUN_F3"
    if document_has_meaningful_content(paths.ask, ASK_HEADINGS):
        return "WAITING_FOR_F2"
    return "RUN_F1"


def declared_branch(paths: InitiativePaths) -> str:
    for candidate in (paths.plan, paths.ask):
        branch = extract_metadata(read_text(candidate), "Rama")
        if branch:
            return branch
    return planned_branch_name(paths.initiative_id)


def run_preflight(initiative_id: str, allow_dirty_with_ask_exception: bool, dry_run: bool) -> None:
    command = [
        sys.executable,
        str(REPO_ROOT / "scripts" / "dev" / "initiative_preflight.py"),
        "--initiative-id",
        initiative_id,
        "--mode",
        "M4",
    ]
    if allow_dirty_with_ask_exception:
        command.append("--allow-dirty-with-ask-exception")
    if dry_run:
        print(f"[dry-run] {' '.join(command)}")
        return
    result = subprocess.run(
        command,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stdout.strip() or result.stderr.strip() or "initiative_preflight failed")


def ensure_f6_branch(paths: InitiativePaths, dry_run: bool) -> None:
    target_branch = declared_branch(paths)
    current_branch = get_git_branch()
    if current_branch == target_branch:
        return
    if dry_run:
        action = "checkout" if git_run("branch", "--list", target_branch) else "checkout -b"
        print(f"[dry-run][git] git {action} {target_branch}")
        return
    branch_exists = bool(git_run("branch", "--list", target_branch))
    if branch_exists:
        git_run("checkout", target_branch)
    else:
        git_run("checkout", "-b", target_branch)


def run_claude(prompt: str, dry_run: bool) -> None:
    if dry_run:
        print("[dry-run][claude]")
        print(prompt)
        return
    settings_path = REPO_ROOT / ".claude" / "settings.local.json"
    command = ["claude", "-p", "--output-format", "text", "--permission-mode", "bypassPermissions"]
    if settings_path.exists():
        command.extend(["--settings", str(settings_path)])
    command.append(prompt)
    result = subprocess.run(
        command,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "Claude command failed")


def run_codex(prompt: str, dry_run: bool) -> None:
    if dry_run:
        print("[dry-run][codex]")
        print(prompt)
        return
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as handle:
        output_path = Path(handle.name)
    command = [
        "codex",
        "-a",
        "never",
        "-s",
        "workspace-write",
        "exec",
        "-C",
        str(REPO_ROOT),
        "-o",
        str(output_path),
        prompt,
    ]
    result = subprocess.run(
        command,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "Codex command failed")


def ensure_file_updated(path: Path, key: str) -> None:
    if not path.exists():
        raise RuntimeError(f"Expected file was not created: {path}")
    actual = extract_metadata(read_text(path), key)
    if not actual:
        raise RuntimeError(f"Expected {key} in {path}, found <empty>")


def build_f1_prompt(paths: InitiativePaths) -> str:
    handoff_clause = (
        f"- Lee {paths.handoff} como fuente primaria de apertura si existe.\n"
        if paths.handoff.exists()
        else "- Si no existe handoff.md, usa el contexto presente en ask.md como seed minimo.\n"
    )
    return (
        f"Trabaja en M4 como motor_activo.\n"
        f"Iniciativa: {paths.initiative_id}\n"
        "Sigue estrictamente AGENTS.md, dev/workflow.md y dev/prompts/ask_discovery.md.\n"
        f"{handoff_clause}"
        f"- Actualiza solo {paths.ask}.\n"
        "- Completa todas las secciones obligatorias del Ask.\n"
        "- Mantiene 'Estado: PROPUESTO'.\n"
        "- No implementes codigo.\n"
        "- No crees otros artefactos.\n"
        "- Si falta contexto obligatorio, deja evidencia de BLOQUEADO dentro del ask.\n"
    )


def build_f3_prompt(paths: InitiativePaths) -> str:
    return (
        f"Trabaja en M4 como motor_auditor.\n"
        f"Iniciativa: {paths.initiative_id}\n"
        "Sigue AGENTS.md, dev/workflow.md y dev/guarantees/ask_gate.md.\n"
        f"Audita {paths.ask} y escribe el resultado en {paths.ask_audit}.\n"
        "- El veredicto debe ser PASS o FAIL.\n"
        "- No edites ask.md ni otros archivos.\n"
        "- Clasifica solo problemas materiales como hallazgos.\n"
    )


def build_f1_revision_prompt(paths: InitiativePaths) -> str:
    return (
        f"Trabaja en M4 como motor_activo.\n"
        f"Iniciativa: {paths.initiative_id}\n"
        "Sigue AGENTS.md, dev/workflow.md y dev/prompts/ask_discovery.md.\n"
        f"Lee {paths.ask_audit} y corrige {paths.ask} para resolver todos los hallazgos materiales.\n"
        "- No cambies el alcance material ya validado sin dejar el ask en BLOQUEADO con evidencia.\n"
        "- Mantiene el ask listo para nueva auditoria F3.\n"
        "- Conserva 'Estado: VALIDADO' salvo que debas bloquear por cambio material.\n"
    )


def build_f4_prompt(paths: InitiativePaths) -> str:
    handoff_clause = f"- Lee {paths.handoff} antes de proponer el plan.\n" if paths.handoff.exists() else ""
    return (
        f"Trabaja en M4 como motor_activo.\n"
        f"Iniciativa: {paths.initiative_id}\n"
        "Sigue AGENTS.md, dev/workflow.md y dev/prompts/plan_create.md.\n"
        f"- Lee {paths.ask} y {paths.ask_audit}.\n"
        f"{handoff_clause}"
        f"- Actualiza solo {paths.plan}.\n"
        "- Genera un plan ejecutable y auditable.\n"
        "- Mantiene 'Estado: PROPUESTO'.\n"
        "- No implementes codigo en esta fase.\n"
    )


def build_f4_revision_prompt(paths: InitiativePaths) -> str:
    return (
        f"Trabaja en M4 como motor_activo.\n"
        f"Iniciativa: {paths.initiative_id}\n"
        "Sigue AGENTS.md, dev/workflow.md y dev/prompts/plan_create.md.\n"
        f"Lee {paths.plan_audit} y corrige {paths.plan} para resolver todos los hallazgos materiales.\n"
        "- No introduzcas alcance nuevo.\n"
        "- Mantiene 'Estado: PROPUESTO'.\n"
    )


def build_f5_prompt(paths: InitiativePaths) -> str:
    return (
        f"Trabaja en M4 como motor_auditor.\n"
        f"Iniciativa: {paths.initiative_id}\n"
        "Sigue AGENTS.md, dev/workflow.md y dev/prompts/plan_audit.md.\n"
        f"Audita {paths.plan} y escribe el resultado en {paths.plan_audit}.\n"
        "- El veredicto debe ser PASS o FAIL.\n"
        "- No edites plan.md ni implementes nada.\n"
    )


def build_f6_prompt(paths: InitiativePaths) -> str:
    return (
        f"Trabaja en M4 como motor_activo.\n"
        f"Iniciativa: {paths.initiative_id}\n"
        "Sigue AGENTS.md, dev/workflow.md y dev/prompts/implementation_execute.md.\n"
        f"- Lee {paths.plan} y {paths.plan_audit}.\n"
        f"- Implementa los cambios de codigo necesarios en el repo y actualiza {paths.execution}.\n"
        "- No cierres la iniciativa.\n"
        "- Mantente dentro del plan congelado.\n"
    )


def build_f6_revision_prompt(paths: InitiativePaths) -> str:
    return (
        f"Trabaja en M4 como motor_activo.\n"
        f"Iniciativa: {paths.initiative_id}\n"
        "Sigue AGENTS.md, dev/workflow.md y dev/prompts/implementation_execute.md.\n"
        f"Lee {paths.post_audit} y corrige la implementacion y {paths.execution} para resolver los hallazgos materiales.\n"
        "- No cambies el alcance del plan congelado.\n"
        "- Registra validaciones y riesgos en execution.md.\n"
    )


def build_f7_prompt(paths: InitiativePaths) -> str:
    return (
        f"Trabaja en M4 como motor_auditor.\n"
        f"Iniciativa: {paths.initiative_id}\n"
        "Sigue AGENTS.md, dev/workflow.md y dev/prompts/post_audit.md.\n"
        f"Audita la implementacion contra {paths.plan} y {paths.execution}.\n"
        f"Escribe el resultado en {paths.post_audit}.\n"
        "- El veredicto debe ser PASS o FAIL.\n"
        "- No edites codigo ni execution.md.\n"
    )


def run_f1_if_needed(paths: InitiativePaths, dry_run: bool) -> bool:
    if document_has_meaningful_content(paths.ask, ASK_HEADINGS):
        return False
    run_claude(build_f1_prompt(paths), dry_run=dry_run)
    return True


def loop_f1_f3(paths: InitiativePaths, max_audits: int, dry_run: bool) -> str:
    failures = 1 if get_verdict(paths.ask_audit) == "FAIL" else 0
    while True:
        run_codex(build_f3_prompt(paths), dry_run=dry_run)
        if not dry_run:
            ensure_file_updated(paths.ask_audit, "Veredicto")
        verdict = "PASS" if dry_run else get_verdict(paths.ask_audit)
        if verdict == "PASS":
            if not dry_run:
                set_state(paths.ask, "CONGELADO")
            return "PASS"
        failures += 1
        if failures >= max_audits:
            return "USER_BLOCK"
        run_claude(build_f1_revision_prompt(paths), dry_run=dry_run)


def loop_f4_f5(paths: InitiativePaths, max_audits: int, dry_run: bool) -> str:
    failures = 1 if get_verdict(paths.plan_audit) == "FAIL" else 0
    if not document_has_meaningful_content(paths.plan, PLAN_HEADINGS):
        run_claude(build_f4_prompt(paths), dry_run=dry_run)
    while True:
        run_codex(build_f5_prompt(paths), dry_run=dry_run)
        if not dry_run:
            ensure_file_updated(paths.plan_audit, "Veredicto")
        verdict = "PASS" if dry_run else get_verdict(paths.plan_audit)
        if verdict == "PASS":
            if not dry_run:
                set_state(paths.plan, "CONGELADO")
            return "PASS"
        failures += 1
        if failures >= max_audits:
            return "USER_BLOCK"
        run_claude(build_f4_revision_prompt(paths), dry_run=dry_run)


def loop_f6_f7(paths: InitiativePaths, max_audits: int, allow_dirty_with_ask_exception: bool, dry_run: bool) -> str:
    failures = 1 if get_verdict(paths.post_audit) == "FAIL" else 0
    ensure_f6_branch(paths, dry_run=dry_run)
    run_preflight(paths.initiative_id, allow_dirty_with_ask_exception=allow_dirty_with_ask_exception, dry_run=dry_run)
    if get_verdict(paths.post_audit) == "FAIL":
        run_claude(build_f6_revision_prompt(paths), dry_run=dry_run)
    elif not document_has_meaningful_content(paths.execution, EXECUTION_HEADINGS):
        run_claude(build_f6_prompt(paths), dry_run=dry_run)
    while True:
        run_codex(build_f7_prompt(paths), dry_run=dry_run)
        if not dry_run:
            ensure_file_updated(paths.post_audit, "Veredicto")
        verdict = "PASS" if dry_run else get_verdict(paths.post_audit)
        if verdict == "PASS":
            return "WAITING_FOR_F8"
        failures += 1
        if failures >= max_audits:
            return "USER_BLOCK"
        run_claude(build_f6_revision_prompt(paths), dry_run=dry_run)


def advance(args: argparse.Namespace) -> int:
    paths = get_paths(args.initiative_id)
    if not initiative_exists(paths):
        raise SystemExit(f"Missing initiative folder: {paths.root}")
    run_f1_if_needed(paths, dry_run=args.dry_run)
    if get_state(paths.ask) == "PROPUESTO":
        print("WAITING_FOR_F2")
        return 0
    if get_state(paths.ask) == "VALIDADO":
        result = loop_f1_f3(paths, max_audits=args.max_audits, dry_run=args.dry_run)
        if result == "USER_BLOCK":
            print("BLOCKED_AFTER_F3")
            return 2
    if get_state(paths.ask) == "CONGELADO":
        result = loop_f4_f5(paths, max_audits=args.max_audits, dry_run=args.dry_run)
        if result == "USER_BLOCK":
            print("BLOCKED_AFTER_F5")
            return 2
    if get_state(paths.plan) == "CONGELADO":
        result = loop_f6_f7(
            paths,
            max_audits=args.max_audits,
            allow_dirty_with_ask_exception=args.allow_dirty_with_ask_exception,
            dry_run=args.dry_run,
        )
        if result == "USER_BLOCK":
            print("BLOCKED_AFTER_F7")
            return 2
        print("WAITING_FOR_F8")
        return 0
    print(recommend_next_step(paths))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Automatiza el ping-pong M4 entre Claude y Codex hasta el siguiente checkpoint humano."
    )
    parser.add_argument(
        "--target-repo",
        default="",
        help="Repo destino donde se ejecuta la iniciativa. Si se omite, usa el repo canonico o GOVERNANCE_TARGET_REPO.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Crear artefactos M4 y dejar lista la iniciativa")
    init_parser.add_argument("--initiative-id", required=True)
    init_parser.add_argument("--motor-activo", default="claude")
    init_parser.add_argument("--motor-auditor", default="codex")
    init_parser.add_argument("--baseline-mit", default=DEFAULT_BASELINE_MIT)
    init_parser.add_argument("--branch", default="")
    init_parser.add_argument("--summary", default="")
    init_parser.add_argument("--with-handoff", action="store_true")
    init_parser.add_argument("--with-real-validation", action="store_true")
    init_parser.add_argument("--force", action="store_true")
    init_parser.set_defaults(func=init_artifacts)

    approve_parser = subparsers.add_parser("approve-f2", help="Checkpoint manual F2: valida Ask y confirma auditor")
    approve_parser.add_argument("--initiative-id", required=True)
    approve_parser.add_argument("--motor-auditor", default="codex")
    approve_parser.set_defaults(func=approve_f2)

    status_parser = subparsers.add_parser("status", help="Mostrar estado resumido y siguiente paso")
    status_parser.add_argument("--initiative-id", required=True)
    status_parser.set_defaults(func=status)

    advance_parser = subparsers.add_parser("advance", help="Avanzar automaticamente hasta el siguiente checkpoint")
    advance_parser.add_argument("--initiative-id", required=True)
    advance_parser.add_argument("--max-audits", type=int, default=DEFAULT_MAX_AUDITS)
    advance_parser.add_argument("--allow-dirty-with-ask-exception", action="store_true")
    advance_parser.add_argument("--dry-run", action="store_true")
    advance_parser.set_defaults(func=advance)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])
    configure_repo_root(str(get_effective_repo_root(args)))
    ensure_repo_supports_governance()
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
