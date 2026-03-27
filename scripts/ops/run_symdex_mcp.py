"""
Launch SymDex MCP with repo-local state bootstrapping.

This wrapper prefers an already installed `symdex` executable to avoid the
startup latency of resolving the Git source on every MCP session. If no local
binary is available, it falls back to `uvx --from <source> symdex serve`.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_SOURCE = "git+https://github.com/husnainpk/SymDex.git"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run SymDex MCP with repo-local state bootstrap."
    )
    parser.add_argument(
        "--repo-root",
        help="Repository root. Defaults to the repo that contains this script.",
    )
    parser.add_argument(
        "--source",
        default=DEFAULT_SOURCE,
        help="Fallback source used when local symdex is not available.",
    )
    parser.add_argument(
        "--state-dir",
        default=".symdex",
        help="Relative state directory for SymDex. Defaults to .symdex.",
    )
    return parser.parse_args()


def resolve_repo_root(raw_value: str | None) -> Path:
    if raw_value:
        return Path(raw_value).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def ensure_state_dir(repo_root: Path, state_dir: str) -> Path:
    state_path = (repo_root / state_dir).resolve()
    state_path.mkdir(parents=True, exist_ok=True)
    return state_path


def resolve_command(source: str) -> tuple[list[str], str]:
    symdex_path = shutil.which("symdex")
    if symdex_path:
        return [symdex_path, "serve"], "symdex"

    uvx_path = shutil.which("uvx")
    if uvx_path:
        return [uvx_path, "--from", source, "symdex", "serve"], "uvx"

    raise RuntimeError(
        "SymDex MCP requires either `symdex` in PATH or `uvx` available as fallback."
    )


def main() -> int:
    args = parse_args()
    repo_root = resolve_repo_root(args.repo_root)
    state_path = ensure_state_dir(repo_root=repo_root, state_dir=args.state_dir)

    command, backend = resolve_command(args.source)
    env = os.environ.copy()
    env["SYMDEX_STATE_DIR"] = str(state_path)

    print(
        f"[run_symdex_mcp] backend={backend} repo_root={repo_root} state_dir={state_path}",
        file=sys.stderr,
    )
    subprocess.run(command, cwd=repo_root, env=env, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
