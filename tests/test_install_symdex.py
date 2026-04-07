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


if __name__ == "__main__":
    unittest.main()
