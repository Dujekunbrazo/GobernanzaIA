"""
Shared helpers to upsert MCP server definitions without clobbering siblings.
"""

from __future__ import annotations

import json
from pathlib import Path


def upsert_mcp_server(
    *,
    repo_root: Path,
    config_relative_path: str,
    server_name: str,
    server_config: dict,
    force: bool,
    dry_run: bool,
) -> None:
    config_path = repo_root / config_relative_path
    payload = {"mcpServers": {}}

    if config_path.exists():
        payload = json.loads(config_path.read_text(encoding="utf-8"))
        if "mcpServers" not in payload or not isinstance(payload["mcpServers"], dict):
            payload["mcpServers"] = {}

    existing = payload["mcpServers"].get(server_name)
    if existing is not None and not force:
        print(f"SKIP (exists): {config_path} -> {server_name}")
        return

    payload["mcpServers"][server_name] = server_config
    content = json.dumps(payload, indent=2) + "\n"

    if dry_run:
        action = "OVERWRITE" if existing is not None else "WRITE"
        print(f"DRY-RUN {action}: {config_path} -> {server_name}")
        return

    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(content, encoding="utf-8")
    print(f"WROTE: {config_path} -> {server_name}")


def upsert_roo_server(
    *,
    repo_root: Path,
    server_name: str,
    server_config: dict,
    force: bool,
    dry_run: bool,
) -> None:
    upsert_mcp_server(
        repo_root=repo_root,
        config_relative_path=".roo/mcp.json",
        server_name=server_name,
        server_config=server_config,
        force=force,
        dry_run=dry_run,
    )


def upsert_root_server(
    *,
    repo_root: Path,
    server_name: str,
    server_config: dict,
    force: bool,
    dry_run: bool,
) -> None:
    upsert_mcp_server(
        repo_root=repo_root,
        config_relative_path=".mcp.json",
        server_name=server_name,
        server_config=server_config,
        force=force,
        dry_run=dry_run,
    )
