"""
Install codebase-memory-mcp and prepare optional local MCP wiring.

Usage:
    python scripts/ops/install_codebase_memory_mcp.py --repo-root <path>
    python scripts/ops/install_codebase_memory_mcp.py --repo-root <path> --write-root-mcp
    python scripts/ops/install_codebase_memory_mcp.py --repo-root <path> --write-roo-mcp
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from roo_mcp_config import upsert_root_server, upsert_roo_server
else:
    from .roo_mcp_config import upsert_root_server, upsert_roo_server


DEFAULT_COMMAND = "codebase-memory-mcp"
TOOLS = (
    "index_repository",
    "list_projects",
    "delete_project",
    "index_status",
    "search_graph",
    "trace_path",
    "detect_changes",
    "query_graph",
    "get_graph_schema",
    "get_code_snippet",
    "get_architecture",
    "search_code",
    "manage_adr",
    "ingest_traces",
)
WINDOWS_SETUP = 'irm https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/scripts/setup-windows.ps1 | iex'
POSIX_SETUP = "curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/scripts/setup.sh | bash"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install codebase-memory-mcp and prepare repo-local MCP wiring."
    )
    parser.add_argument(
        "--repo-root",
        required=True,
        help="Target repository root where local wiring should be prepared.",
    )
    parser.add_argument(
        "--installer",
        choices=("auto", "setup", "none"),
        default="auto",
        help="Installer strategy. 'setup' uses the official setup script from the upstream project.",
    )
    parser.add_argument(
        "--binary-command",
        default=DEFAULT_COMMAND,
        help="Command or absolute path used in MCP wiring. Defaults to codebase-memory-mcp.",
    )
    parser.add_argument(
        "--write-root-mcp",
        action="store_true",
        help="Generate or merge .mcp.json with codebase-memory-mcp wiring.",
    )
    parser.add_argument(
        "--write-roo-mcp",
        action="store_true",
        help="Generate or merge .roo/mcp.json with codebase-memory-mcp wiring.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite generated MCP wiring if it already exists.",
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


def install_codebase_memory(installer: str, dry_run: bool) -> str:
    existing = shutil.which(DEFAULT_COMMAND)
    if existing:
        print(f"SKIP INSTALL: codebase-memory-mcp already available at {existing}")
        return "existing"

    if installer == "none":
        print("SKIP INSTALL: installer=none")
        return "none"

    if installer in {"auto", "setup"}:
        if sys.platform.startswith("win"):
            command = ["powershell", "-ExecutionPolicy", "ByPass", "-c", WINDOWS_SETUP]
        else:
            command = ["bash", "-lc", POSIX_SETUP]
        run_command(command, dry_run=dry_run)
        return "setup"

    raise RuntimeError(f"Unsupported installer strategy: {installer}")


def resolve_binary_command(binary_command: str) -> str:
    candidate = Path(binary_command)
    if candidate.is_absolute() and candidate.exists():
        return str(candidate)

    resolved = shutil.which(binary_command)
    if resolved:
        return resolved

    if sys.platform.startswith("win"):
        windows_candidate = (
            Path.home()
            / "AppData"
            / "Local"
            / "codebase-memory-mcp"
            / "codebase-memory-mcp.exe"
        )
        if windows_candidate.exists():
            return str(windows_candidate)

    return binary_command


def codebase_memory_server_config(binary_command: str) -> dict:
    return {
        "type": "stdio",
        "command": binary_command,
        "args": [],
        "alwaysAllow": list(TOOLS),
    }


def ensure_root_mcp(repo_root: Path, binary_command: str, force: bool, dry_run: bool) -> None:
    upsert_root_server(
        repo_root=repo_root,
        server_name="codebase-memory-mcp",
        server_config=codebase_memory_server_config(binary_command),
        force=force,
        dry_run=dry_run,
    )


def ensure_roo_mcp(repo_root: Path, binary_command: str, force: bool, dry_run: bool) -> None:
    upsert_roo_server(
        repo_root=repo_root,
        server_name="codebase-memory-mcp",
        server_config=codebase_memory_server_config(binary_command),
        force=force,
        dry_run=dry_run,
    )


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    if not repo_root.exists():
        raise FileNotFoundError(f"Missing repo root: {repo_root}")

    chosen_installer = install_codebase_memory(installer=args.installer, dry_run=args.dry_run)
    print(f"Installer used: {chosen_installer}")
    resolved_binary_command = resolve_binary_command(args.binary_command)

    if args.write_root_mcp:
        ensure_root_mcp(
            repo_root=repo_root,
            binary_command=resolved_binary_command,
            force=args.force,
            dry_run=args.dry_run,
        )

    if args.write_roo_mcp:
        ensure_roo_mcp(
            repo_root=repo_root,
            binary_command=resolved_binary_command,
            force=args.force,
            dry_run=args.dry_run,
        )

    print("codebase-memory-mcp bootstrap summary")
    print("-------------------------------------")
    print(f"Repo root: {repo_root}")
    print(f"Installer: {chosen_installer}")
    print(f"Binary command: {resolved_binary_command}")
    print(f"Root MCP wiring: {'yes' if args.write_root_mcp else 'no'}")
    print(f"Roo MCP wiring: {'yes' if args.write_roo_mcp else 'no'}")
    print(f"Mode: {'dry-run' if args.dry_run else 'write'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
