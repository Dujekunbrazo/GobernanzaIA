from __future__ import annotations

import unittest

from scripts.ops import install_codebase_memory_mcp as icm


class InstallCodebaseMemoryMcpTests(unittest.TestCase):
    def test_server_config_uses_expected_command_and_tools(self) -> None:
        config = icm.codebase_memory_server_config("codebase-memory-mcp")
        self.assertEqual(config["command"], "codebase-memory-mcp")
        self.assertEqual(config["args"], [])
        self.assertIn("get_architecture", config["alwaysAllow"])
        self.assertIn("detect_changes", config["alwaysAllow"])
        self.assertIn("ingest_traces", config["alwaysAllow"])


if __name__ == "__main__":
    unittest.main()
