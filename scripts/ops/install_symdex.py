"""
Install SymDex from its official GitHub repository and prepare optional local wiring.

Usage:
    python scripts/ops/install_symdex.py --repo-root <path>
    python scripts/ops/install_symdex.py --repo-root <path> --write-root-mcp
    python scripts/ops/install_symdex.py --repo-root <path> --write-roo-mcp
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from roo_mcp_config import upsert_root_server, upsert_roo_server


DEFAULT_SOURCE = "git+https://github.com/husnainpk/SymDex.git"
DEFAULT_PACKAGE = "symdex"
LOCAL_PACKAGE = "symdex[local]"
VOYAGE_PACKAGE = "symdex[voyage]"
DEFAULT_IGNORE_LINES = (
    ".git/",
    ".venv/",
    "__pycache__/",
    ".pytest_cache/",
    "node_modules/",
    "dist/",
    "build/",
    "coverage/",
    "logs/",
    "reports/",
    "sessions/",
    "state/",
    "content/",
    "dev/records/",
    "legacy/",
)
SYMDEX_TOOLS = (
    "search_symbols",
    "semantic_search",
    "search_text",
    "get_symbol",
    "get_symbols",
    "get_file_outline",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install SymDex from GitHub and prepare repo-local wiring."
    )
    parser.add_argument(
        "--repo-root",
        required=True,
        help="Target repository root where local wiring should be prepared.",
    )
    parser.add_argument(
        "--source",
        default=DEFAULT_SOURCE,
        help="SymDex package source. Defaults to the official GitHub repo.",
    )
    parser.add_argument(
        "--installer",
        choices=("auto", "uv", "pip", "none"),
        default="auto",
        help="Runtime installer strategy. Defaults to auto.",
    )
    parser.add_argument(
        "--write-root-mcp",
        action="store_true",
        help="Generate .mcp.json wired to SymDex over uvx.",
    )
    parser.add_argument(
        "--write-roo-mcp",
        action="store_true",
        help="Generate .roo/mcp.json wired to SymDex over uvx.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite generated files and MCP wiring if they already exist.",
    )
    parser.add_argument(
        "--force-runtime-install",
        action="store_true",
        help="Force runtime reinstall of SymDex when using the installer backend.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned actions without modifying files or installing runtime.",
    )
    parser.add_argument(
        "--semantic-backend",
        choices=("none", "local", "voyage"),
        default="local",
        help="Semantic backend strategy for SymDex. Defaults to local.",
    )
    return parser.parse_args()


def run_command(command: list[str], dry_run: bool, cwd: Path | None = None) -> None:
    rendered = " ".join(command)
    if dry_run:
        suffix = f" (cwd={cwd})" if cwd else ""
        print(f"DRY-RUN INSTALL: {rendered}{suffix}")
        return
    subprocess.run(command, check=True, cwd=cwd)


def install_symdex(
    source: str,
    installer: str,
    dry_run: bool,
    force_runtime_install: bool,
    semantic_backend: str,
) -> str:
    uv_path = shutil.which("uv")
    can_use_pip = sys.version_info >= (3, 11)
    existing_symdex = shutil.which("symdex")

    if existing_symdex and not force_runtime_install and semantic_backend == "none":
        print(f"SKIP INSTALL: symdex already available at {existing_symdex}")
        return "existing"

    install_target = resolve_install_target(source=source, semantic_backend=semantic_backend)

    if installer in ("auto", "uv") and uv_path:
        command = [uv_path, "tool", "install"]
        if force_runtime_install or semantic_backend != "none":
            command.append("--force")
        command.append(install_target)
        run_command(command, dry_run=dry_run)
        return "uv"

    if installer == "uv":
        raise RuntimeError("uv is required for installer=uv but was not found in PATH.")

    if installer in ("auto", "pip"):
        if not can_use_pip:
            raise RuntimeError(
                "pip fallback requires Python >= 3.11 because SymDex requires Python >= 3.11."
            )
        command = [sys.executable, "-m", "pip", "install", "--upgrade", install_target]
        run_command(command, dry_run=dry_run)
        return "pip"

    if installer == "pip":
        raise RuntimeError("pip installation path could not be resolved.")

    print("SKIP INSTALL: installer=none")
    return "none"


def resolve_install_target(source: str, semantic_backend: str) -> str:
    if semantic_backend == "none":
        return source
    if semantic_backend == "local":
        return LOCAL_PACKAGE
    if semantic_backend == "voyage":
        return VOYAGE_PACKAGE
    raise RuntimeError(f"Unsupported SymDex semantic backend: {semantic_backend}")


def write_text_file(path: Path, content: str, force: bool, dry_run: bool) -> None:
    if path.exists() and not force:
        print(f"SKIP (exists): {path}")
        return

    if dry_run:
        action = "OVERWRITE" if path.exists() else "WRITE"
        print(f"DRY-RUN {action}: {path}")
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"WROTE: {path}")


def ensure_state_dir(repo_root: Path, dry_run: bool) -> None:
    state_dir = repo_root / ".symdex"
    if dry_run:
        print(f"DRY-RUN MKDIR: {state_dir}")
        return
    state_dir.mkdir(parents=True, exist_ok=True)
    print(f"READY: {state_dir}")


def ensure_symdexignore(repo_root: Path, force: bool, dry_run: bool) -> None:
    lines = ["# Paths ignored by SymDex during indexing.", *DEFAULT_IGNORE_LINES, ""]
    content = "\n".join(lines)
    write_text_file(repo_root / ".symdexignore", content, force=force, dry_run=dry_run)


def resolve_node_command() -> str:
    node_path = shutil.which("node")
    if node_path is None:
        raise RuntimeError("SymDex MCP wiring requires node in PATH.")
    return str(Path(node_path).resolve())


def resolve_server_path(repo_root: Path) -> str:
    return str((repo_root / "scripts" / "ops" / "context_mcp" / "symdex_code_server.mjs").resolve())


def install_context_mcp_dependencies(repo_root: Path, dry_run: bool, force: bool) -> str:
    package_dir = repo_root / "scripts" / "ops" / "context_mcp"
    npm_path = shutil.which("npm")
    if npm_path is None:
        raise RuntimeError("SymDex MCP wiring requires npm to install context_mcp dependencies.")

    command = [npm_path, "ci" if (package_dir / "package-lock.json").exists() else "install"]
    if force and command[1] == "install":
        command.append("--force")
    run_command(command, dry_run=dry_run, cwd=package_dir)
    return "npm"


def resolve_symdex_binary() -> str | None:
    symdex_path = shutil.which("symdex")
    if symdex_path is None:
        return None
    return str(Path(symdex_path).resolve())


def resolve_uvx_binary() -> str | None:
    uvx_path = shutil.which("uvx")
    if uvx_path is None:
        return None
    return str(Path(uvx_path).resolve())


def symdex_server_config(repo_root: Path, source: str, semantic_backend: str) -> dict:
    args = [
        resolve_server_path(repo_root),
        "--symdex-source",
        source,
        "--semantic-backend",
        semantic_backend,
    ]
    symdex_binary = resolve_symdex_binary()
    uvx_binary = resolve_uvx_binary()
    if symdex_binary:
        args.extend(["--symdex-bin", symdex_binary])
    if uvx_binary:
        args.extend(["--uvx-bin", uvx_binary])
    return {
        "type": "stdio",
        "command": resolve_node_command(),
        "args": args,
        "alwaysAllow": list(SYMDEX_TOOLS),
    }


def warmup_symdex(source: str, dry_run: bool) -> None:
    symdex_path = shutil.which("symdex")
    if symdex_path:
        command = [symdex_path, "--version"]
    else:
        uvx_path = shutil.which("uvx")
        if uvx_path is None:
            print("WARN: SymDex warmup skipped because neither symdex nor uvx is available.")
            return
        command = [uvx_path, "--from", source, "symdex", "--version"]

    rendered = " ".join(command)
    if dry_run:
        print(f"DRY-RUN WARMUP: {rendered}")
        return

    try:
        subprocess.run(command, check=True, timeout=30)
        print(f"WARMED UP: {rendered}")
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        print(f"WARN: SymDex warmup failed ({rendered}): {exc}")


def run_symdex_cli(
    *,
    source: str,
    semantic_backend: str,
    args: list[str],
) -> subprocess.CompletedProcess[str]:
    symdex_path = shutil.which("symdex")
    if symdex_path:
        command = [symdex_path, *args]
    else:
        uvx_path = shutil.which("uvx")
        if uvx_path is None:
            raise RuntimeError(
                "SymDex validation requires either `symdex` or `uvx` available in PATH."
            )
        command = [uvx_path, "--from", resolve_install_target(source, semantic_backend), "symdex", *args]
    return subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )


def validate_semantic_backend(
    *,
    repo_root: Path,
    source: str,
    semantic_backend: str,
    dry_run: bool,
) -> str:
    if semantic_backend == "none":
        return "SKIPPED_NONE"

    state_dir = repo_root / ".symdex"
    repo_name = resolve_repo_name_for_validation(
        repo_root=repo_root,
        source=source,
        semantic_backend=semantic_backend,
        state_dir=state_dir,
    )
    probe_args = [
        "semantic",
        "routing logic",
        "--repo",
        repo_name,
        "--limit",
        "1",
        "--json",
        "--state-dir",
        str(state_dir),
    ]

    if dry_run:
        print(f"DRY-RUN VALIDATE: semantic backend={semantic_backend} probe={' '.join(probe_args)}")
        return "DRY_RUN"

    initial = run_symdex_cli(
        source=source,
        semantic_backend=semantic_backend,
        args=probe_args,
    )
    stderr_text = f"{initial.stdout}\n{initial.stderr}".lower()
    if initial.returncode == 0:
        print("VALIDATED: SymDex semantic backend probe passed")
        return "VALIDATED"

    needs_index = (
        "no semantic embeddings" in stderr_text
        or "repo not indexed" in stderr_text
        or "no indexed repos" in stderr_text
    )
    if needs_index:
        index_result = run_symdex_cli(
            source=source,
            semantic_backend=semantic_backend,
            args=["index", str(repo_root), "--state-dir", str(state_dir)],
        )
        if index_result.returncode != 0:
            print(
                "WARN: SymDex semantic validation failed during index: "
                f"{index_result.stderr.strip() or index_result.stdout.strip()}"
            )
            return "FAILED"
        retried = run_symdex_cli(
            source=source,
            semantic_backend=semantic_backend,
            args=probe_args,
        )
        if retried.returncode == 0:
            print("VALIDATED: SymDex semantic backend probe passed after local index")
            return "VALIDATED"
        print(
            "WARN: SymDex semantic validation probe still failed after index: "
            f"{retried.stderr.strip() or retried.stdout.strip()}"
        )
        return "FAILED"

    print(
        "WARN: SymDex semantic validation failed: "
        f"{initial.stderr.strip() or initial.stdout.strip()}"
    )
    return "FAILED"


def resolve_repo_name_for_validation(
    *,
    repo_root: Path,
    source: str,
    semantic_backend: str,
    state_dir: Path,
) -> str:
    repos_result = run_symdex_cli(
        source=source,
        semantic_backend=semantic_backend,
        args=["repos", "--json", "--state-dir", str(state_dir)],
    )
    if repos_result.returncode == 0:
        selected = select_repo_name_from_registry(repos_result.stdout, repo_root)
        if selected:
            return selected

    index_result = run_symdex_cli(
        source=source,
        semantic_backend=semantic_backend,
        args=["index", str(repo_root), "--state-dir", str(state_dir)],
    )
    if index_result.returncode != 0:
        raise RuntimeError(
            "SymDex validation could not index the repo: "
            f"{index_result.stderr.strip() or index_result.stdout.strip()}"
        )

    repos_result = run_symdex_cli(
        source=source,
        semantic_backend=semantic_backend,
        args=["repos", "--json", "--state-dir", str(state_dir)],
    )
    if repos_result.returncode != 0:
        raise RuntimeError(
            "SymDex validation could not list indexed repos: "
            f"{repos_result.stderr.strip() or repos_result.stdout.strip()}"
        )
    selected = select_repo_name_from_registry(repos_result.stdout, repo_root)
    if not selected:
        raise RuntimeError(f"SymDex validation could not resolve repo name for {repo_root}")
    return selected


def select_repo_name_from_registry(payload: str, repo_root: Path) -> str | None:
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        return None

    expected_root = str(repo_root.resolve()).replace("/", "\\").lower()
    candidates: list[tuple[datetime, str]] = []
    for entry in data.get("repos", []):
        root_path = str(entry.get("root_path", "")).replace("/", "\\").lower()
        if root_path != expected_root:
            continue
        raw_last_indexed = str(entry.get("last_indexed", "")).strip()
        try:
            parsed = datetime.fromisoformat(raw_last_indexed.replace(" ", "T"))
        except ValueError:
            parsed = datetime.min
        candidates.append((parsed, str(entry.get("name", ""))))

    if not candidates:
        return None

    candidates.sort(reverse=True)
    return candidates[0][1]


def ensure_root_mcp(
    repo_root: Path, source: str, semantic_backend: str, force: bool, dry_run: bool
) -> None:
    if not dry_run and shutil.which("node") is None:
        raise RuntimeError("Root MCP wiring for SymDex requires node in PATH.")

    upsert_root_server(
        repo_root=repo_root,
        server_name="symdex_code",
        server_config=symdex_server_config(repo_root, source, semantic_backend),
        force=force,
        dry_run=dry_run,
    )


def ensure_roo_mcp(
    repo_root: Path, source: str, semantic_backend: str, force: bool, dry_run: bool
) -> None:
    if not dry_run and shutil.which("node") is None:
        raise RuntimeError("Roo wiring for SymDex requires node in PATH.")

    upsert_roo_server(
        repo_root=repo_root,
        server_name="symdex_code",
        server_config=symdex_server_config(repo_root, source, semantic_backend),
        force=force,
        dry_run=dry_run,
    )


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()

    if not repo_root.exists():
        raise FileNotFoundError(f"Missing repo root: {repo_root}")

    chosen_installer = install_symdex(
        source=args.source,
        installer=args.installer,
        dry_run=args.dry_run,
        force_runtime_install=args.force_runtime_install,
        semantic_backend=args.semantic_backend,
    )
    print(f"Installer used: {chosen_installer}")

    ensure_state_dir(repo_root=repo_root, dry_run=args.dry_run)
    ensure_symdexignore(repo_root=repo_root, force=args.force, dry_run=args.dry_run)
    warmup_symdex(source=args.source, dry_run=args.dry_run)
    chosen_context_installer = install_context_mcp_dependencies(
        repo_root=repo_root,
        dry_run=args.dry_run,
        force=args.force,
    )
    semantic_validation = validate_semantic_backend(
        repo_root=repo_root,
        source=args.source,
        semantic_backend=args.semantic_backend,
        dry_run=args.dry_run,
    )

    if args.write_root_mcp:
        ensure_root_mcp(
            repo_root=repo_root,
            source=args.source,
            semantic_backend=args.semantic_backend,
            force=args.force,
            dry_run=args.dry_run,
        )

    if args.write_roo_mcp:
        ensure_roo_mcp(
            repo_root=repo_root,
            source=args.source,
            semantic_backend=args.semantic_backend,
            force=args.force,
            dry_run=args.dry_run,
        )

    print("SymDex bootstrap summary")
    print("------------------------")
    print(f"Repo root: {repo_root}")
    print(f"Source: {args.source}")
    print(f"Installer: {chosen_installer}")
    print(f"Semantic backend: {args.semantic_backend}")
    print(f"Semantic validation: {semantic_validation}")
    print(f"Context MCP installer: {chosen_context_installer}")
    print(f"Root MCP wiring: {'yes' if args.write_root_mcp else 'no'}")
    print(f"Roo MCP wiring: {'yes' if args.write_roo_mcp else 'no'}")
    print(f"Mode: {'dry-run' if args.dry_run else 'write'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
