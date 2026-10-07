import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from ticket_app.analysis_provider import MockAnalysisProvider
from ticket_app.api import create_app


@pytest.fixture(autouse=True)
def force_mock_mode(monkeypatch):
    # A local .env must never make the deterministic suite call a model.
    monkeypatch.setenv("LLM_PROVIDER", "mock")


@pytest.fixture
def policy():
    return json.loads(Path("scenarios/g07.json").read_text())


@pytest.fixture
def make_client(policy, tmp_path):
    def _make(provider=None):
        app = create_app(
            provider=provider or MockAnalysisProvider(),
            policy=policy,
            db_path=str(tmp_path / "test.db"),
        )
        return TestClient(app)

    return _make
