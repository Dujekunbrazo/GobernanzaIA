"""
Install governance retrieval MCP support and optional MCP wiring.

Usage:
    python scripts/ops/install_governance_mcp.py --repo-root <path>
    python scripts/ops/install_governance_mcp.py --repo-root <path> --write-root-mcp
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

from roo_mcp_config import upsert_root_server


TOOLS = ("governance_search", "governance_scope")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install governance retrieval MCP support for a target repository."
    )
    parser.add_argument(
        "--repo-root",
        required=True,
        help="Target repository root where local wiring should be prepared.",
    )
    parser.add_argument(
        "--installer",
        choices=("auto", "npm", "none"),
        default="auto",
        help="Dependency installer strategy for scripts/ops/context_mcp.",
    )
    parser.add_argument(
        "--write-root-mcp",
        action="store_true",
        help="Generate or merge .mcp.json with governance retrieval server wiring.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite generated files and force dependency reinstall when possible.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned actions without modifying files or installing dependencies.",
    )
    return parser.parse_args()


def run_command(command: list[str], cwd: Path, dry_run: bool) -> None:
    rendered = " ".join(command)
    if dry_run:
        print(f"DRY-RUN INSTALL: {rendered} (cwd={cwd})")
        return
    subprocess.run(command, cwd=cwd, check=True)


def install_dependencies(repo_root: Path, installer: str, dry_run: bool, force: bool) -> str:
    package_dir = repo_root / "scripts" / "ops" / "context_mcp"
    npm_path = shutil.which("npm")

    if installer in ("auto", "npm") and npm_path:
        command = [npm_path, "ci" if (package_dir / "package-lock.json").exists() else "install"]
        if force and command[1] == "install":
            command.append("--force")
        run_command(command, cwd=package_dir, dry_run=dry_run)
        return "npm"

    if installer == "npm":
        raise RuntimeError("npm is required for installer=npm but was not found in PATH.")

    print("SKIP INSTALL: installer=none")
    return "none"


def governance_server_config() -> dict:
    return {
        "type": "stdio",
        "command": "node",
        "args": ["scripts/ops/context_mcp/governance_retrieval_server.mjs"],
        "alwaysAllow": list(TOOLS),
    }


def ensure_root_mcp(repo_root: Path, force: bool, dry_run: bool) -> None:
    if not dry_run and shutil.which("node") is None:
        raise RuntimeError(
            "Root MCP wiring for governance_search requires node in PATH. Install Node or omit --write-root-mcp."
        )

    upsert_root_server(
        repo_root=repo_root,
        server_name="governance_retrieval",
        server_config=governance_server_config(),
        force=force,
        dry_run=dry_run,
    )


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    if not repo_root.exists():
        raise FileNotFoundError(f"Missing repo root: {repo_root}")

    chosen_installer = install_dependencies(
        repo_root=repo_root,
        installer=args.installer,
        dry_run=args.dry_run,
        force=args.force,
    )
    print(f"Installer used: {chosen_installer}")

    if args.write_root_mcp:
        ensure_root_mcp(repo_root=repo_root, force=args.force, dry_run=args.dry_run)

    print("Governance MCP bootstrap summary")
    print("-------------------------------")
    print(f"Repo root: {repo_root}")
    print(f"Installer: {chosen_installer}")
    print(f"Root MCP wiring: {'yes' if args.write_root_mcp else 'no'}")
    print(f"Mode: {'dry-run' if args.dry_run else 'write'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
