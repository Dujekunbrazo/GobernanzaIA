"""
Install SymDex from its official GitHub repository and prepare optional local wiring.

Usage:
    python scripts/ops/install_symdex.py --repo-root <path>
    python scripts/ops/install_symdex.py --repo-root <path> --write-root-mcp
    python scripts/ops/install_symdex.py --repo-root <path> --write-roo-mcp
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from roo_mcp_config import upsert_root_server, upsert_roo_server


DEFAULT_SOURCE = "git+https://github.com/husnainpk/SymDex.git"
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
    "index_folder",
    "index_repo",
    "search_symbols",
    "semantic_search",
    "search_text",
    "get_symbol",
    "get_symbols",
    "get_file_outline",
    "get_file_tree",
    "get_repo_outline",
    "get_callers",
    "get_callees",
    "search_routes",
    "get_index_status",
    "get_repo_stats",
    "get_graph_diagram",
    "find_circular_deps",
    "list_repos",
    "invalidate_cache",
    "gc_stale_indexes",
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
        help="Overwrite generated files and force runtime reinstall when possible.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned actions without modifying files or installing runtime.",
    )
    return parser.parse_args()


def run_command(command: list[str], dry_run: bool) -> None:
    rendered = " ".join(command)
    if dry_run:
        print(f"DRY-RUN INSTALL: {rendered}")
        return
    subprocess.run(command, check=True)


def install_symdex(source: str, installer: str, dry_run: bool, force: bool) -> str:
    uv_path = shutil.which("uv")
    can_use_pip = sys.version_info >= (3, 11)

    if installer in ("auto", "uv") and uv_path:
        command = [uv_path, "tool", "install"]
        if force:
            command.append("--force")
        command.append(source)
        run_command(command, dry_run=dry_run)
        return "uv"

    if installer == "uv":
        raise RuntimeError("uv is required for installer=uv but was not found in PATH.")

    if installer in ("auto", "pip"):
        if not can_use_pip:
            raise RuntimeError(
                "pip fallback requires Python >= 3.11 because SymDex requires Python >= 3.11."
            )
        command = [sys.executable, "-m", "pip", "install", "--upgrade", source]
        run_command(command, dry_run=dry_run)
        return "pip"

    if installer == "pip":
        raise RuntimeError("pip installation path could not be resolved.")

    print("SKIP INSTALL: installer=none")
    return "none"


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


def ensure_symdexignore(repo_root: Path, force: bool, dry_run: bool) -> None:
    lines = ["# Paths ignored by SymDex during indexing.", *DEFAULT_IGNORE_LINES, ""]
    content = "\n".join(lines)
    write_text_file(repo_root / ".symdexignore", content, force=force, dry_run=dry_run)


def symdex_server_config(source: str) -> dict:
    return {
        "type": "stdio",
        "command": "uvx",
        "args": ["--from", source, "symdex", "serve"],
        "env": {"SYMDEX_STATE_DIR": ".symdex"},
        "alwaysAllow": list(SYMDEX_TOOLS),
    }


def ensure_root_mcp(repo_root: Path, source: str, force: bool, dry_run: bool) -> None:
    if not dry_run and shutil.which("uvx") is None:
        raise RuntimeError(
            "Root MCP wiring for SymDex requires uvx in PATH. Install uv or omit --write-root-mcp."
        )

    upsert_root_server(
        repo_root=repo_root,
        server_name="symdex_code",
        server_config=symdex_server_config(source),
        force=force,
        dry_run=dry_run,
    )


def ensure_roo_mcp(repo_root: Path, source: str, force: bool, dry_run: bool) -> None:
    if not dry_run and shutil.which("uvx") is None:
        raise RuntimeError(
            "Roo wiring for SymDex requires uvx in PATH. Install uv or omit --write-roo-mcp."
        )

    upsert_roo_server(
        repo_root=repo_root,
        server_name="symdex_code",
        server_config=symdex_server_config(source),
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
        force=args.force,
    )
    print(f"Installer used: {chosen_installer}")

    ensure_symdexignore(repo_root=repo_root, force=args.force, dry_run=args.dry_run)

    if args.write_root_mcp:
        ensure_root_mcp(
            repo_root=repo_root,
            source=args.source,
            force=args.force,
            dry_run=args.dry_run,
        )

    if args.write_roo_mcp:
        ensure_roo_mcp(
            repo_root=repo_root,
            source=args.source,
            force=args.force,
            dry_run=args.dry_run,
        )

    print("SymDex bootstrap summary")
    print("------------------------")
    print(f"Repo root: {repo_root}")
    print(f"Source: {args.source}")
    print(f"Installer: {chosen_installer}")
    print(f"Root MCP wiring: {'yes' if args.write_root_mcp else 'no'}")
    print(f"Roo MCP wiring: {'yes' if args.write_roo_mcp else 'no'}")
    print(f"Mode: {'dry-run' if args.dry_run else 'write'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
