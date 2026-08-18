from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from fastapi.testclient import TestClient

from app.main import create_app
from app.settings import Settings


class ApplicationFoundationTests(TestCase):
    def test_health_response_is_safe(self) -> None:
        app = create_app(Settings("test", Path("/missing"), False))
        response = TestClient(app).get("/healthz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_missing_frontend_is_explicit_without_exposing_configuration(self) -> None:
        app = create_app(Settings("test", Path("/missing"), False))
        response = TestClient(app).get("/")
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()["state"], "frontend_pending")
        self.assertNotIn("CLICKHOUSE", response.text)

    def test_static_index_is_served_when_present(self) -> None:
        with TemporaryDirectory() as directory:
            index = Path(directory) / "index.html"
            index.write_text("<main>SlateGuard</main>", encoding="utf-8")
            app = create_app(Settings("test", Path(directory), True))
            response = TestClient(app).get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("SlateGuard", response.text)
