import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "security-scanner.py"
SPEC = importlib.util.spec_from_file_location("security_scanner", MODULE_PATH)
SECURITY_SCANNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SECURITY_SCANNER)


class McpScanFailureTest(unittest.TestCase):
    def test_all_failed_scans_use_basic_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            config_path = Path(directory) / "mcp.json"
            config_path.write_text('{"mcpServers": {}}', encoding="utf-8")
            failed = subprocess.CompletedProcess([], 2, "", "unsupported option")

            with patch.object(SECURITY_SCANNER.subprocess, "run", return_value=failed):
                result = SECURITY_SCANNER.SecurityScanner()._run_mcp_scan(directory)

        self.assertEqual(result["status"], "warning")
        self.assertEqual(result["score"], 70)
        self.assertIn("failed for all 1 configuration file(s)", result["details"])
        self.assertIn(str(config_path), result["scan_results"])

    def test_partial_scan_failure_cannot_report_full_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            first_config = Path(directory) / "mcp.json"
            second_config = Path(directory) / "mcp_config.json"
            first_config.write_text('{"mcpServers": {}}', encoding="utf-8")
            second_config.write_text('{"mcpServers": {}}', encoding="utf-8")
            succeeded = subprocess.CompletedProcess(
                [], 0, json.dumps({"results": []}), ""
            )
            failed = subprocess.CompletedProcess([], 2, "", "scan failed")

            with patch.object(
                SECURITY_SCANNER.subprocess,
                "run",
                side_effect=[succeeded, failed],
            ):
                result = SECURITY_SCANNER.SecurityScanner()._run_mcp_scan(directory)

        self.assertEqual(result["status"], "warning")
        self.assertEqual(result["score"], 75)
        self.assertEqual(result["issues_found"], 0)
        self.assertIn("1 configuration scan(s) failed", result["details"])


if __name__ == "__main__":
    unittest.main()
