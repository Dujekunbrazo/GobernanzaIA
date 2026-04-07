from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest import mock


OPS_DIR = Path(__file__).resolve().parents[1] / "scripts" / "ops"
if str(OPS_DIR) not in sys.path:
    sys.path.insert(0, str(OPS_DIR))

import install_symdex as symdex  # noqa: E402


class InstallSymDexTests(unittest.TestCase):
    def test_resolve_install_target_respects_semantic_backend(self) -> None:
        self.assertEqual(
            symdex.resolve_install_target(symdex.DEFAULT_SOURCE, "none"),
            symdex.DEFAULT_SOURCE,
        )
        self.assertEqual(
            symdex.resolve_install_target(symdex.DEFAULT_SOURCE, "local"),
            symdex.LOCAL_PACKAGE,
        )
        self.assertEqual(
            symdex.resolve_install_target(symdex.DEFAULT_SOURCE, "voyage"),
            symdex.VOYAGE_PACKAGE,
        )

    def test_symdex_server_config_includes_semantic_backend(self) -> None:
        repo_root = Path("C:/repos/Kiminion")
        with (
            mock.patch.object(symdex, "resolve_node_command", return_value="C:/node.exe"),
            mock.patch.object(
                symdex,
                "resolve_server_path",
                return_value="C:/repos/Kiminion/scripts/ops/context_mcp/symdex_code_server.mjs",
            ),
            mock.patch.object(symdex, "resolve_symdex_binary", return_value="C:/symdex.exe"),
            mock.patch.object(symdex, "resolve_uvx_binary", return_value="C:/uvx.exe"),
        ):
            config = symdex.symdex_server_config(
                repo_root=repo_root,
                source=symdex.DEFAULT_SOURCE,
                semantic_backend="local",
            )

        self.assertEqual(config["command"], "C:/node.exe")
        self.assertIn("--semantic-backend", config["args"])
        self.assertIn("local", config["args"])
        self.assertIn("--symdex-bin", config["args"])
        self.assertIn("--uvx-bin", config["args"])
        self.assertIn("semantic_search", config["alwaysAllow"])

    def test_select_repo_name_from_registry_prefers_latest_match_for_repo_root(self) -> None:
        payload = """
        {
          "repos": [
            {
              "name": "other-repo",
              "root_path": "C:/repos/Other",
              "last_indexed": "2026-04-07 12:00:00"
            },
            {
              "name": "kiminion-old",
              "root_path": "C:/repos/Kiminion",
              "last_indexed": "2026-04-07 09:00:00"
            },
            {
              "name": "kiminion-new",
              "root_path": "C:/repos/Kiminion",
              "last_indexed": "2026-04-07 13:00:00"
            }
          ]
        }
        """

        selected = symdex.select_repo_name_from_registry(payload, Path("C:/repos/Kiminion"))

        self.assertEqual(selected, "kiminion-new")

    def test_validate_semantic_backend_uses_resolved_repo_name_for_probe(self) -> None:
        repo_root = Path("C:/repos/Kiminion")

        with (
            mock.patch.object(
                symdex,
                "resolve_repo_name_for_validation",
                return_value="kiminion-current-index",
            ),
            mock.patch.object(
                symdex,
                "run_symdex_cli",
                return_value=mock.Mock(returncode=0, stdout='{"symbols":[]}', stderr=""),
            ) as run_symdex_cli,
        ):
            result = symdex.validate_semantic_backend(
                repo_root=repo_root,
                source=symdex.DEFAULT_SOURCE,
                semantic_backend="local",
                dry_run=False,
            )

        self.assertEqual(result, "VALIDATED")
        run_symdex_cli.assert_called_once()
        self.assertEqual(
            run_symdex_cli.call_args.kwargs["args"],
            [
                "semantic",
                "routing logic",
                "--repo",
                "kiminion-current-index",
                "--limit",
                "1",
                "--json",
                "--state-dir",
                str(repo_root / ".symdex"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
