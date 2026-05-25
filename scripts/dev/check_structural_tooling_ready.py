from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Best-effort preflight for structural governance tooling."
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root to inspect. Defaults to the current directory.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=10,
        help="Timeout used for the lightweight binary probe.",
    )
    return parser.parse_args()


def load_root_mcp(repo_root: Path) -> tuple[dict | None, str | None]:
    config_path = repo_root / ".mcp.json"
    if not config_path.exists():
        return None, f"Missing MCP config: {config_path}"
    try:
        payload = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, f"Invalid JSON in {config_path}: {exc}"
    return payload, None


def resolve_binary(command: str) -> str | None:
    candidate = Path(command)
    if candidate.is_absolute() and candidate.exists():
        return str(candidate)
    return shutil.which(command)


def probe_binary(command: str, timeout_seconds: int) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            [command, "--help"],
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
    except FileNotFoundError:
        return False, f"Binary not found: {command}"
    except subprocess.TimeoutExpired:
        return False, f"Timed out probing binary: {command}"
    except OSError as exc:
        return False, f"Could not execute {command}: {exc}"

    if result.returncode not in (0, 1):
        message = result.stderr.strip() or result.stdout.strip() or f"exit={result.returncode}"
        return False, f"Unexpected binary probe result for {command}: {message}"
    return True, "ok"


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    if not repo_root.exists():
        print(f"BLOCKED: missing repo root: {repo_root}")
        return 1

    payload, payload_error = load_root_mcp(repo_root)
    if payload_error:
        print(f"BLOCKED: {payload_error}")
        return 1

    servers = payload.get("mcpServers", {})
    server = servers.get("codebase-memory-mcp")
    if not isinstance(server, dict):
        print("BLOCKED: .mcp.json does not declare codebase-memory-mcp")
        return 1

    command = str(server.get("command", "")).strip()
    if not command:
        print("BLOCKED: codebase-memory-mcp has no command in .mcp.json")
        return 1

    resolved = resolve_binary(command)
    binary_ok, binary_message = probe_binary(resolved or command, timeout_seconds=args.timeout_seconds)

    overall = "READY_FOR_SESSION_PREFLIGHT" if binary_ok else "BLOCKED"
    print("Structural tooling readiness")
    print("---------------------------")
    print(f"Repo root: {repo_root}")
    print(f"MCP config: {repo_root / '.mcp.json'}")
    print(f"Server declared: yes")
    print(f"Configured command: {command}")
    print(f"Resolved binary: {resolved or 'NOT_RESOLVED'}")
    print(f"Binary probe: {'ok' if binary_ok else binary_message}")
    print("Project resolution: pendiente en sesión con list_projects")
    print("Schema preflight: pendiente en sesión con get_graph_schema si habrá Cypher")
    print(f"Overall: {overall}")
    return 0 if binary_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
