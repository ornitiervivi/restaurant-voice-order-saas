"""Health endpoint tests."""

import pytest

fastapi = pytest.importorskip("fastapi")
TestClient = pytest.importorskip("fastapi.testclient").TestClient

from src.main import create_app


def test_health_returns_ok_response() -> None:
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "Restaurant Voice Order API",
        "version": "0.1.0",
    }
