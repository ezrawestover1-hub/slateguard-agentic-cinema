from unittest import TestCase

from app.mcp.runner import _result_text, _server_environment


class _TextBlock:
    def __init__(self, text: str) -> None:
        self.text = text


class McpRunnerTests(TestCase):
    def test_reader_child_gets_only_reader_identity_and_no_write_permission(self) -> None:
        parent = {
            "PATH": "/usr/bin",
            "CLICKHOUSE_HOST": "example.clickhouse.cloud",
            "CLICKHOUSE_PORT": "8443",
            "CLICKHOUSE_DATABASE": "slateguard",
            "CLICKHOUSE_SECURE": "true",
            "CLICKHOUSE_VERIFY": "true",
            "CLICKHOUSE_READER_USER": "reader",
            "CLICKHOUSE_READER_PASSWORD": "reader-secret",
            "CLICKHOUSE_WRITER_USER": "writer",
            "CLICKHOUSE_WRITER_PASSWORD": "writer-secret",
        }
        environment = _server_environment(parent, "reader")
        self.assertEqual(environment["CLICKHOUSE_USER"], "reader")
        self.assertEqual(environment["CLICKHOUSE_ALLOW_WRITE_ACCESS"], "false")
        self.assertNotIn("CLICKHOUSE_WRITER_PASSWORD", environment)

    def test_mcp_text_blocks_are_joined(self) -> None:
        self.assertEqual(_result_text([_TextBlock('{"columns":'), _TextBlock('[]}')]), '{"columns":[]}')
