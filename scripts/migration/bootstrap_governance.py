"""
Bootstrap governance files into a target repository.

Usage:
    python scripts/migration/bootstrap_governance.py --target <path>
    python scripts/migration/bootstrap_governance.py --target <path> --with-ia codex --with-ia claude --preferred-working-ia codex --preferred-auditor-ia claude
    python scripts/migration/bootstrap_governance.py --target <path> --with-ia codex --with-ia claude --preferred-working-ia codex --preferred-auditor-ia claude --include-pack symdex
    python scripts/migration/bootstrap_governance.py --target <path> --with-ia codex --with-ia claude --preferred-working-ia codex --preferred-auditor-ia claude --include-pack governance_search
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PACKS = ("core",)
DEFAULT_SYMDEX_SOURCE = "git+https://github.com/husnainpk/SymDex.git"

# Catalogo conocido de IAs. Extensible: anadir una entrada por motor que
# quiera soportarse por defecto. El argparse acepta cualquier string;
# si la IA elegida no esta en el catalogo, se emite un WARNING pero la
# instalacion continua (el consumidor debera crear su adapter a mano).
IA_CATALOG: dict[str, dict[str, str | bool]] = {
    "claude":   {"vendor": "Anthropic",     "has_adapter_in_kit": True},
    "codex":    {"vendor": "OpenAI",        "has_adapter_in_kit": True},
    "gpt":      {"vendor": "OpenAI",        "has_adapter_in_kit": False},
    "gemini":   {"vendor": "Google",        "has_adapter_in_kit": False},
    "kimi":     {"vendor": "Moonshot",      "has_adapter_in_kit": False},
    "grok":     {"vendor": "xAI",           "has_adapter_in_kit": False},
    "deepseek": {"vendor": "DeepSeek",      "has_adapter_in_kit": False},
    "qwen":     {"vendor": "Alibaba",       "has_adapter_in_kit": False},
    "mistral":  {"vendor": "Mistral",       "has_adapter_in_kit": False},
    "llama":    {"vendor": "Meta",          "has_adapter_in_kit": False},
}

# Cada IA elegida puede tener un pack opcional con artefactos especificos
# (ej. `claude` copia CLAUDE.md raiz). Los packs vacios estan declarados
# para que sea trivial anadirles contenido en futuras iteraciones.
IA_PACKS = {name: name for name in IA_CATALOG}

MANIFEST_PATH = Path("dev/governance_baseline.json")
REPO_PROFILE_TEMPLATE_PATH = Path("dev/templates/governance/repo_governance_profile.md")
REPO_PROFILE_DESTINATION = Path("dev/repo_governance_profile.md")
ADAPTER_TEMPLATE_PATH = Path("dev/templates/governance/adapter_template.md")
ADAPTERS_DIR = Path("dev/ai/adapters")
PRESERVE_IF_EXISTS = {
    Path(".gitignore"),
    Path("AGENTS.md"),
    Path("CLAUDE.md"),
    Path("README.md"),
    Path("dev/logs/decisions.md"),
    Path("dev/repo_governance_profile.md"),
}
REMOVE_ON_FORCE_IF_EXISTS = {
    Path("doc/governance_prompts/01_m4_f1_ask.md"),
    Path("doc/governance_prompts/07b_validacion_real_guiada.md"),
    Path("doc/governance_prompts/08_f8_cierre.md"),
    Path("doc/governance_prompts/08_f8_f9_cierre y lecciones.md"),
    Path("doc/governance_prompts/09_f9_cierre.md"),
    Path("doc/governance_prompts/09_f9_f10_cierre y lecciones.md"),
    Path("doc/governance_prompts/09_f9_lecciones.md"),
    Path("doc/governance_prompts/10_f10_lecciones.md"),
    Path("doc/governance_prompts/97 handoff codex audit.md"),
    # F4-F10 legacy prompts purgados en v0.2.0 (esquema viejo, antes de F1-F7):
    Path("doc/governance_prompts/04_f4_plan.md"),
    Path("doc/governance_prompts/05_f5_auditoria_plan.md"),
    Path("doc/governance_prompts/06_f6_implementacion.md"),
    Path("doc/governance_prompts/07_f7_post_auditoria.md"),
    Path("doc/governance_prompts/09_f9_f10_cierre_y_lecciones.md"),
    Path("doc/governance_prompts/15_f4_remediacion_plan.md"),
    Path("doc/governance_prompts/97 idea codex.md"),
    Path("doc/governance_prompts/98 idea codex to claude plan.md"),
    Path("doc/governance_prompts/99 prompt plan a codex.md"),
}


@dataclass(frozen=True)
class PackSpec:
    description: str
    files: tuple[Path, ...] = ()
    globs: tuple[tuple[Path, str, bool], ...] = ()
    post_copy_actions: tuple[str, ...] = ()


PACKS: dict[str, PackSpec] = {
    "core": PackSpec(
        description=(
            "Baseline canónico reusable: AGENTS, dev, records scaffolding,"
            " scripts de enforcement y documentación reusable."
        ),
        files=(
            Path(".gitignore"),
            Path("AGENTS.md"),
            Path("dev/workflow.md"),
            Path("dev/governance_guide.md"),
            Path("dev/ai/README.md"),
            Path("dev/checklists/state0.md"),
            Path("dev/logs/decisions.md"),
            Path("dev/records/README.md"),
            Path("dev/records/bitacora/README.md"),
            Path("dev/records/bitacora/.gitkeep"),
            Path("dev/records/initiatives/.gitkeep"),
            Path("dev/records/reviews/README.md"),
            Path("dev/records/reviews/weekly/.gitkeep"),
            Path("dev/skills/REGISTRY.md"),
            Path("dev/skills/SKILL_CONTRACT.md"),
            Path("dev/templates/orchestrator/execution_checkpoint.md"),
            Path("doc/architecture/ai_engineering_dossier.md"),
            Path("doc/architecture/context_retrieval_architecture.md"),
            Path("doc/governance_ping_pong_guide.md"),
            Path("doc/governance_prompts/README.md"),
            Path("scripts/README.md"),
            Path("scripts/ops/bitacora_append.py"),
            Path("scripts/ops/roo_mcp_config.py"),  # kept: shared MCP config helper
            Path("scripts/ops/context_mcp/refresh_governance_index.mjs"),
            Path("scripts/dev/README.md"),
            Path("scripts/dev/check_bitacora_compliance.py"),
            Path("scripts/dev/check_capability_closure.py"),
            Path("scripts/dev/check_clock_canon.py"),
            Path("scripts/dev/check_exception_record.py"),
            Path("scripts/dev/check_naming_compliance.py"),
            Path("scripts/dev/check_state0.py"),
            Path("scripts/dev/check_structural_tooling_ready.py"),
            Path("scripts/dev/governance_ping_pong.py"),
            Path("scripts/dev/governance_ping_pong_launcher.bat"),
            Path("scripts/dev/initiative_preflight.py"),
            Path("scripts/dev/memory_precheck.py"),
            Path("scripts/dev/refresh_codebase_memory_index.ps1"),
            Path("scripts/dev/refresh_governance_retrieval_index.ps1"),
            Path("scripts/dev/refresh_symdex_index.ps1"),
            Path("scripts/migration/bootstrap_governance.py"),
            Path("scripts/migration/sync_governance_consumers.py"),
        ),
        globs=(
            (Path("dev/guarantees"), "*.md", False),
            (Path("dev/policies"), "*.md", False),
            (Path("dev/prompts"), "*.md", False),
            (Path("dev/ai/adapters"), "*.md", False),
            (Path("dev/skills"), "*.md", True),  # recursivo: SKILL.md anidados por capability
            (Path("dev/templates/initiative"), "*.md", False),
            (Path("dev/templates/governance"), "*.md", False),
            (Path("doc/governance_prompts"), "*.md", False),
        ),
    ),
    "claude": PackSpec(
        description=(
            "Superficie opcional de Claude. Incluye solo artefactos reusables,"
            " no settings locales."
        ),
        files=(Path("CLAUDE.md"),),
    ),
    "codex": PackSpec(
        description=(
            "Perfil opcional de Codex para instalacion multi-IA. La capa"
            " normativa de Codex ya viaja dentro de core mediante"
            " dev/ai/adapters/codex.md."
        ),
    ),
    "gpt": PackSpec(
        description=(
            "Perfil opcional de GPT (OpenAI). Pack vacio extensible:"
            " usar dev/templates/governance/adapter_template.md para crear"
            " dev/ai/adapters/gpt.md si no existe todavia."
        ),
    ),
    "gemini": PackSpec(
        description=(
            "Perfil opcional de Gemini (Google). Pack vacio extensible:"
            " usar dev/templates/governance/adapter_template.md para crear"
            " dev/ai/adapters/gemini.md si no existe todavia."
        ),
    ),
    "kimi": PackSpec(
        description=(
            "Perfil opcional de Kimi (Moonshot). Pack vacio extensible:"
            " usar dev/templates/governance/adapter_template.md para crear"
            " dev/ai/adapters/kimi.md si no existe todavia."
        ),
    ),
    "grok": PackSpec(
        description=(
            "Perfil opcional de Grok (xAI). Pack vacio extensible:"
            " usar dev/templates/governance/adapter_template.md para crear"
            " dev/ai/adapters/grok.md si no existe todavia."
        ),
    ),
    "deepseek": PackSpec(
        description=(
            "Perfil opcional de DeepSeek. Pack vacio extensible:"
            " usar dev/templates/governance/adapter_template.md para crear"
            " dev/ai/adapters/deepseek.md si no existe todavia."
        ),
    ),
    "qwen": PackSpec(
        description=(
            "Perfil opcional de Qwen (Alibaba). Pack vacio extensible:"
            " usar dev/templates/governance/adapter_template.md para crear"
            " dev/ai/adapters/qwen.md si no existe todavia."
        ),
    ),
    "mistral": PackSpec(
        description=(
            "Perfil opcional de Mistral. Pack vacio extensible:"
            " usar dev/templates/governance/adapter_template.md para crear"
            " dev/ai/adapters/mistral.md si no existe todavia."
        ),
    ),
    "llama": PackSpec(
        description=(
            "Perfil opcional de Llama (Meta). Pack vacio extensible:"
            " usar dev/templates/governance/adapter_template.md para crear"
            " dev/ai/adapters/llama.md si no existe todavia."
        ),
    ),
    "symdex": PackSpec(
        description=(
            "Instala SymDex desde su GitHub oficial y prepara .symdexignore "
            "mas wiring MCP opcional sobre el adaptador canónico local."
        ),
        files=(
            Path("scripts/ops/install_symdex.py"),
            Path("scripts/ops/context_mcp/symdex_code_server.mjs"),
            Path("scripts/ops/context_mcp/package.json"),
            Path("scripts/ops/context_mcp/package-lock.json"),
        ),
        post_copy_actions=("install_symdex",),
    ),
    "governance_search": PackSpec(
        description=(
            "Instala el MCP local de governance_search y prepara wiring MCP."
        ),
        files=(
            Path("scripts/ops/install_governance_mcp.py"),
            Path("scripts/ops/context_mcp/governance_retrieval_server.mjs"),
            Path("scripts/ops/context_mcp/shared.mjs"),
            Path("scripts/ops/context_mcp/package.json"),
            Path("scripts/ops/context_mcp/package-lock.json"),
            Path("scripts/ops/context_mcp/README.md"),
            Path("scripts/ops/context_mcp/smoke_governance_mcp.mjs"),
        ),
        post_copy_actions=("install_governance_mcp",),
    ),
    "codebase_memory": PackSpec(
        description=(
            "Prepara codebase-memory-mcp como capacidad estructural opcional y "
            "wiring MCP local controlado."
        ),
        files=(Path("scripts/ops/install_codebase_memory_mcp.py"),),
        post_copy_actions=("install_codebase_memory_mcp",),
    ),
}


def iter_globbed_files(rel_dir: Path, pattern: str, recursive: bool) -> list[Path]:
    abs_dir = REPO_ROOT / rel_dir
    iterator = abs_dir.rglob(pattern) if recursive else abs_dir.glob(pattern)
    return sorted(path for path in iterator if path.is_file())


def collect_sources(pack_names: list[str]) -> list[Path]:
    sources: list[Path] = []
    seen: set[Path] = set()

    for pack_name in pack_names:
        spec = PACKS[pack_name]
        for rel in spec.files:
            abs_path = REPO_ROOT / rel
            if abs_path not in seen:
                sources.append(abs_path)
                seen.add(abs_path)
        for rel_dir, pattern, recursive in spec.globs:
            for abs_path in iter_globbed_files(rel_dir, pattern, recursive):
                if abs_path not in seen:
                    sources.append(abs_path)
                    seen.add(abs_path)

    missing = [src for src in sources if not src.exists()]
    if missing:
        lines = ["Missing source files in governance pack:"]
        lines.extend(f"- {path}" for path in missing)
        raise FileNotFoundError("\n".join(lines))

    return sources


def copy_sources(sources: list[Path], target_root: Path, force: bool, dry_run: bool) -> tuple[int, int]:
    copied = 0
    skipped = 0

    for src in sources:
        rel = src.relative_to(REPO_ROOT)
        dst = target_root / rel

        if rel in PRESERVE_IF_EXISTS and dst.exists():
            skipped += 1
            print(f"SKIP (preserve local): {rel}")
            continue

        if dst.exists() and not force:
            skipped += 1
            print(f"SKIP (exists): {rel}")
            continue

        if dry_run:
            action = "OVERWRITE" if dst.exists() else "COPY"
            print(f"{action}: {rel}")
            copied += 1
            continue

        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied += 1
        print(f"COPIED: {rel}")

    return copied, skipped


def prune_obsolete_files(target_root: Path, force: bool, dry_run: bool) -> int:
    if not force:
        return 0

    removed = 0
    for rel in sorted(REMOVE_ON_FORCE_IF_EXISTS):
        dst = target_root / rel
        if not dst.exists():
            continue
        if dry_run:
            print(f"REMOVE: {rel}")
            removed += 1
            continue
        dst.unlink()
        removed += 1
        print(f"REMOVED: {rel}")

    return removed


def ensure_repo_governance_profile(target_root: Path, dry_run: bool) -> str:
    destination = target_root / REPO_PROFILE_DESTINATION
    if destination.exists():
        print(f"SKIP (preserve local): {REPO_PROFILE_DESTINATION}")
        return "preserved"

    source = REPO_ROOT / REPO_PROFILE_TEMPLATE_PATH
    if dry_run:
        print(f"WRITE: {REPO_PROFILE_DESTINATION} (from {REPO_PROFILE_TEMPLATE_PATH})")
        return "planned"

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    print(f"COPIED: {REPO_PROFILE_DESTINATION}")
    return "written"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy governance baseline into another repository."
    )
    parser.add_argument(
        "--list-packs",
        action="store_true",
        help="List available packs and exit.",
    )
    parser.add_argument(
        "--target",
        help="Target repository path where governance files will be copied.",
    )
    parser.add_argument(
        "--include-pack",
        action="append",
        choices=sorted(PACKS),
        default=[],
        help=(
            "Optional pack to copy in addition to the default core baseline. "
            "Repeat the flag to include multiple packs."
        ),
    )
    parser.add_argument(
        "--with-ia",
        action="append",
        default=[],
        help=(
            "IA to include in the installation profile. Repeat the flag to"
            " include multiple IAs. Minimum two distinct IAs are required."
            " Accepts any string; if the IA is not in IA_CATALOG a warning is"
            " emitted but the install continues. Known IAs: "
            + ", ".join(sorted(IA_CATALOG))
            + "."
        ),
    )
    parser.add_argument(
        "--preferred-working-ia",
        help=(
            "Preferred IA for active work in the installation profile."
            " Must be one of the --with-ia values."
        ),
    )
    parser.add_argument(
        "--preferred-auditor-ia",
        help=(
            "Preferred IA for audit in the installation profile."
            " Must be one of the --with-ia values and distinct from"
            " --preferred-working-ia."
        ),
    )
    parser.add_argument(
        "--generate-adapter-template-for",
        action="append",
        default=[],
        dest="generate_adapter_template_for",
        help=(
            "IA name for which to generate an initial adapter from"
            " dev/templates/governance/adapter_template.md at"
            " dev/ai/adapters/<ia>.md if the file does not already exist."
            " Repeat the flag to generate adapters for multiple IAs."
        ),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite files that already exist in target.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be copied without writing files.",
    )
    parser.add_argument(
        "--skip-claude-root",
        action="store_true",
        help=(
            "Deprecated compatibility flag. If present, removes CLAUDE.md from "
            "the selected packs."
        ),
    )
    parser.add_argument(
        "--symdex-source",
        default=DEFAULT_SYMDEX_SOURCE,
        help="Source used by the optional symdex pack. Defaults to the official GitHub repo.",
    )
    parser.add_argument(
        "--symdex-installer",
        choices=("auto", "uv", "pip", "none"),
        default="auto",
        help="Installer strategy used by the optional symdex pack.",
    )
    parser.add_argument(
        "--symdex-semantic-backend",
        choices=("none", "local", "voyage"),
        default="local",
        help="Semantic backend strategy used by the optional symdex pack.",
    )
    parser.add_argument(
        "--governance-mcp-installer",
        choices=("auto", "npm", "none"),
        default="auto",
        help="Installer strategy used by the optional governance_search pack.",
    )
    parser.add_argument(
        "--codebase-memory-installer",
        choices=("auto", "setup", "none"),
        default="auto",
        help="Installer strategy used by the optional codebase_memory pack.",
    )
    parser.add_argument(
        "--codebase-memory-command",
        default="codebase-memory-mcp",
        help="Command or path used by the optional codebase_memory pack for MCP wiring.",
    )
    args = parser.parse_args()

    if args.list_packs:
        return args

    if not args.target:
        parser.error("--target is required unless --list-packs is used")

    resolve_ia_profile(parser, args)

    return args


def print_available_packs() -> None:
    print("Available governance packs")
    print("--------------------------")
    for pack_name in sorted(PACKS):
        default_suffix = " (default)" if pack_name in DEFAULT_PACKS else ""
        print(f"- {pack_name}{default_suffix}: {PACKS[pack_name].description}")


def dedupe(values: list[str]) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value not in seen:
            ordered.append(value)
            seen.add(value)
    return ordered


def parse_ia_csv(raw_value: str) -> list[str]:
    raw_items = [item.strip().lower() for item in raw_value.split(",")]
    values = [item for item in raw_items if item]
    # Sin restriccion contra catalogo cerrado: cualquier IA es valida.
    # Las IAs fuera del catalogo emiten WARN en warn_unknown_ias().
    return dedupe(values)


def warn_unknown_ias(ias: list[str]) -> None:
    unknown = [ia for ia in ias if ia not in IA_CATALOG]
    if not unknown:
        return
    known = ", ".join(sorted(IA_CATALOG))
    for ia in unknown:
        print(
            f"WARN: IA '{ia}' no esta en IA_CATALOG. Se aceptara pero deberas"
            f" crear dev/ai/adapters/{ia}.md manualmente (puedes usar"
            f" --generate-adapter-template-for {ia} para sembrarlo desde la"
            f" plantilla). IAs conocidas: {known}."
        )


def prompt_text(message: str) -> str:
    return input(message).strip()


def prompt_ias(current_values: list[str]) -> list[str]:
    known = ", ".join(sorted(IA_CATALOG))
    prompt = (
        "IAs para este repo (minimo 2, separadas por comas; cualquier nombre"
        " es valido). Catalogo conocido: "
        + known
    )
    if current_values:
        prompt += f" [{', '.join(current_values)}]"
    prompt += ": "

    while True:
        raw_value = prompt_text(prompt)
        if not raw_value and current_values:
            return current_values
        try:
            values = parse_ia_csv(raw_value)
        except ValueError as exc:
            print(exc)
            continue
        if len(values) < 2:
            print("Se requieren al menos dos IAs distintas para el perfil de instalacion.")
            continue
        return values


def prompt_choice(message: str, allowed: list[str], current_value: str | None) -> str:
    prompt = f"{message} ({', '.join(allowed)})"
    if current_value:
        prompt += f" [{current_value}]"
    prompt += ": "

    while True:
        raw_value = prompt_text(prompt).lower()
        if not raw_value and current_value:
            return current_value
        if raw_value in allowed:
            return raw_value
        print(f"Valor invalido. Opciones validas: {', '.join(allowed)}.")


def resolve_ia_profile(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    installed_ias = dedupe(args.with_ia)
    interactive = sys.stdin.isatty() and sys.stdout.isatty()

    if not installed_ias:
        if interactive:
            installed_ias = prompt_ias(current_values=installed_ias)
        else:
            parser.error(
                "the installation profile requires at least two --with-ia values"
            )

    if len(installed_ias) < 2:
        if interactive:
            installed_ias = prompt_ias(current_values=installed_ias)
        else:
            parser.error("the installation profile requires at least two IAs")

    working_ia = args.preferred_working_ia
    auditor_ia = args.preferred_auditor_ia

    if working_ia and working_ia not in installed_ias:
        parser.error("--preferred-working-ia must be present in --with-ia")
    if auditor_ia and auditor_ia not in installed_ias:
        parser.error("--preferred-auditor-ia must be present in --with-ia")

    if not working_ia:
        if interactive:
            working_ia = prompt_choice(
                "IA preferida para trabajo",
                installed_ias,
                current_value=None,
            )
        else:
            parser.error("--preferred-working-ia is required in non-interactive mode")

    remaining_auditors = [ia for ia in installed_ias if ia != working_ia]
    if not remaining_auditors:
        parser.error("the auditor IA must be different from the working IA")

    if auditor_ia == working_ia:
        parser.error("the auditor IA must be different from the working IA")

    if not auditor_ia:
        if interactive:
            auditor_ia = prompt_choice(
                "IA preferida para auditoria",
                remaining_auditors,
                current_value=None,
            )
        else:
            parser.error("--preferred-auditor-ia is required in non-interactive mode")

    if auditor_ia not in installed_ias:
        parser.error("--preferred-auditor-ia must be present in --with-ia")
    if auditor_ia == working_ia:
        parser.error("the auditor IA must be different from the working IA")

    args.with_ia = installed_ias
    args.preferred_working_ia = working_ia
    args.preferred_auditor_ia = auditor_ia

    warn_unknown_ias(installed_ias)


def resolve_selected_packs(args: argparse.Namespace) -> list[str]:
    selected = list(DEFAULT_PACKS)
    for ia_name in args.with_ia:
        pack_name = IA_PACKS.get(ia_name)
        # IAs fuera del catalogo no tienen pack en el kit; el adapter se
        # genera con --generate-adapter-template-for o se crea a mano.
        if pack_name and pack_name not in selected:
            selected.append(pack_name)
    for pack_name in args.include_pack:
        if pack_name not in selected:
            selected.append(pack_name)

    if args.skip_claude_root and "claude" in selected:
        selected.remove("claude")

    return selected


def ensure_adapter_templates(
    target_root: Path,
    ia_names: list[str],
    dry_run: bool,
) -> list[str]:
    """Para cada IA en `ia_names`, copia adapter_template.md a
    dev/ai/adapters/<ia>.md si ese adapter aun no existe en el destino.
    Devuelve la lista de adapters efectivamente generados."""
    source = REPO_ROOT / ADAPTER_TEMPLATE_PATH
    if not source.exists():
        print(f"WARN: plantilla {ADAPTER_TEMPLATE_PATH} no existe, omito generacion de adapters")
        return []
    generated: list[str] = []
    for ia in ia_names:
        ia_clean = ia.strip().lower()
        if not ia_clean:
            continue
        dst = target_root / ADAPTERS_DIR / f"{ia_clean}.md"
        if dst.exists():
            print(f"SKIP adapter (exists): dev/ai/adapters/{ia_clean}.md")
            continue
        if dry_run:
            print(f"WRITE adapter: dev/ai/adapters/{ia_clean}.md (from {ADAPTER_TEMPLATE_PATH})")
            generated.append(ia_clean)
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dst)
        print(f"COPIED adapter: dev/ai/adapters/{ia_clean}.md")
        generated.append(ia_clean)
    return generated


def git_value(*args: str) -> str | None:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )
    if result.returncode != 0:
        return None
    value = result.stdout.strip()
    return value or None


def run_post_copy_actions(
    selected_packs: list[str],
    target_root: Path,
    force: bool,
    dry_run: bool,
    symdex_source: str,
    symdex_installer: str,
    symdex_semantic_backend: str,
    governance_mcp_installer: str,
    codebase_memory_installer: str,
    codebase_memory_command: str,
) -> None:
    action_names = {
        action_name
        for pack_name in selected_packs
        for action_name in PACKS[pack_name].post_copy_actions
    }

    if "install_symdex" in action_names:
        command = [
            sys.executable,
            str(target_root / "scripts" / "ops" / "install_symdex.py"),
            "--repo-root",
            str(target_root),
            "--source",
            symdex_source,
            "--installer",
            symdex_installer,
            "--semantic-backend",
            symdex_semantic_backend,
            "--write-root-mcp",
        ]
        if force:
            command.append("--force")
        if dry_run:
            command.append("--dry-run")
            print(f"POST-COPY ACTION: {' '.join(command)}")
        else:
            subprocess.run(command, check=True)

    if "install_governance_mcp" not in action_names:
        pass
    else:
        command = [
            sys.executable,
            str(target_root / "scripts" / "ops" / "install_governance_mcp.py"),
            "--repo-root",
            str(target_root),
            "--installer",
            governance_mcp_installer,
            "--write-root-mcp",
        ]
        if force:
            command.append("--force")
        if dry_run:
            command.append("--dry-run")
            print(f"POST-COPY ACTION: {' '.join(command)}")
        else:
            subprocess.run(command, check=True)

    if "install_codebase_memory_mcp" not in action_names:
        return

    command = [
        sys.executable,
        str(target_root / "scripts" / "ops" / "install_codebase_memory_mcp.py"),
        "--repo-root",
        str(target_root),
        "--installer",
        codebase_memory_installer,
        "--binary-command",
        codebase_memory_command,
        "--write-root-mcp",
    ]
    if force:
        command.append("--force")
    if dry_run:
        command.append("--dry-run")
        print(f"POST-COPY ACTION: {' '.join(command)}")
        return

    subprocess.run(command, check=True)


def write_manifest(
    *,
    target_root: Path,
    selected_packs: list[str],
    installed_ias: list[str],
    preferred_working_ia: str,
    preferred_auditor_ia: str,
    copied: int,
    dry_run: bool,
    symdex_source: str,
    symdex_semantic_backend: str,
    codebase_memory_command: str,
) -> None:
    payload = {
        "baseline": "GobernanzaIA",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_repo_path": str(REPO_ROOT),
        "source_git_commit": git_value("rev-parse", "HEAD"),
        "source_git_branch": git_value("branch", "--show-current"),
        "source_git_remote": git_value("remote", "get-url", "origin"),
        "packs": selected_packs,
        "installation_profile": {
            "installed_ias": installed_ias,
            "preferred_working_ia": preferred_working_ia,
            "preferred_auditor_ia": preferred_auditor_ia,
            "governance_note": (
                "Installation preferences only. Governance runtime still requires"
                " explicit motor_activo and motor_auditor designation by the user."
            ),
        },
        "file_count": copied,
        "symdex_source": symdex_source if "symdex" in selected_packs else None,
        "symdex_semantic_backend": (
            symdex_semantic_backend if "symdex" in selected_packs else None
        ),
        "codebase_memory_command": codebase_memory_command if "codebase_memory" in selected_packs else None,
    }
    manifest_path = target_root / MANIFEST_PATH
    if dry_run:
        print(f"WRITE MANIFEST: {manifest_path}")
        return
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"WROTE: {MANIFEST_PATH}")


def main() -> int:
    args = parse_args()

    if args.list_packs:
        print_available_packs()
        return 0

    selected_packs = resolve_selected_packs(args)
    target_root = Path(args.target).expanduser().resolve()

    if not args.dry_run:
        target_root.mkdir(parents=True, exist_ok=True)

    sources = collect_sources(pack_names=selected_packs)
    copied, skipped = copy_sources(
        sources=sources,
        target_root=target_root,
        force=args.force,
        dry_run=args.dry_run,
    )
    removed = prune_obsolete_files(
        target_root=target_root,
        force=args.force,
        dry_run=args.dry_run,
    )
    ensure_repo_governance_profile(
        target_root=target_root,
        dry_run=args.dry_run,
    )
    generated_adapters = ensure_adapter_templates(
        target_root=target_root,
        ia_names=args.generate_adapter_template_for,
        dry_run=args.dry_run,
    )
    run_post_copy_actions(
        selected_packs=selected_packs,
        target_root=target_root,
        force=args.force,
        dry_run=args.dry_run,
        symdex_source=args.symdex_source,
        symdex_installer=args.symdex_installer,
        symdex_semantic_backend=args.symdex_semantic_backend,
        governance_mcp_installer=args.governance_mcp_installer,
        codebase_memory_installer=args.codebase_memory_installer,
        codebase_memory_command=args.codebase_memory_command,
    )
    write_manifest(
        target_root=target_root,
        selected_packs=selected_packs,
        installed_ias=args.with_ia,
        preferred_working_ia=args.preferred_working_ia,
        preferred_auditor_ia=args.preferred_auditor_ia,
        copied=copied,
        dry_run=args.dry_run,
        symdex_source=args.symdex_source,
        symdex_semantic_backend=args.symdex_semantic_backend,
        codebase_memory_command=args.codebase_memory_command,
    )

    print("\nGovernance bootstrap summary")
    print("----------------------------")
    print(f"Target: {target_root}")
    print(f"IAs: {', '.join(args.with_ia)}")
    print(f"Preferred work IA: {args.preferred_working_ia}")
    print(f"Preferred audit IA: {args.preferred_auditor_ia}")
    print(f"Packs: {', '.join(selected_packs)}")
    print(f"Copied: {copied}")
    print(f"Skipped: {skipped}")
    print(f"Removed obsolete: {removed}")
    if generated_adapters:
        print(f"Generated adapters: {', '.join(generated_adapters)}")
    print(f"Mode: {'dry-run' if args.dry_run else 'write'}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
