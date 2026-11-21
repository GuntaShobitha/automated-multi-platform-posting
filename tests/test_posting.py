from fastapi.testclient import TestClient
from app.main import app
from app.services import posting_service
from app.platforms.base import Outcome

client = TestClient(app)

def test_health():
    assert client.get("/").json()["status"] == "online"

def test_too_long():
    assert client.post("/posting", json={"message": "x" * 201}).status_code == 422

def test_no_url():
    assert client.post("/posting", json={"message": "Hello there"}).status_code == 422

def test_two_urls():
    r = client.post("/posting", json={"message": "https://one.com https://two.com"})
    assert r.status_code == 422

def test_bad_url():
    assert client.post("/posting", json={"message": "Go https://"}).status_code == 422

def test_platform_failure_isolated(monkeypatch):
    class Good:
        name = "Good"
        async def publish(self, message):
            return Outcome("Good", "success", "https://example.com/post/1", True, "2026-11-21", "12:00:00")
        def fail(self, error):
            return Outcome(self.name, "failed", error=error)
    class Bad(Good):
        name = "Bad"
        async def publish(self, message):
            raise RuntimeError("test failure")
    monkeypatch.setattr(posting_service, "get_platforms", lambda: [Good(), Bad()])
    r = client.post("/posting", json={"message": "Hello https://example.com"})
    assert r.status_code == 200
    assert [x["status"] for x in r.json()["results"]] == ["success", "failed"]
