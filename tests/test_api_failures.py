import httpx
import pytest

from ticket_app.analysis_models import Analysis
from ticket_app.analysis_provider import InvalidModelOutput, LocalAnalysisProvider, ProviderUnavailable

REQ = {"subject": "Role change", "text": "Please add me to the reporting role."}
GOOD = {
    "summary": "Role change for reporting",
    "category": "role",
    "priority": "medium",
    "next_action": "Send to the role owner for review",
}


class Failing:
    def __init__(self, exc):
        self.exc = exc

    def analyze(self, request, policy):
        raise self.exc


class Static:
    def __init__(self, data):
        self.data = data

    def analyze(self, request, policy):
        return Analysis(**self.data)


@pytest.mark.parametrize(
    "exc,status",
    [(ProviderUnavailable("down"), 503), (InvalidModelOutput("bad output"), 502)],
)
def test_inference_failure_is_controlled_and_not_saved(make_client, exc, status):
    client = make_client(Failing(exc))
    assert client.post("/api/analyze", json=REQ).status_code == status
    assert client.get("/api/history").json() == []


@pytest.mark.parametrize(
    "override",
    [{"category": "network"}, {"next_action": "Access has been granted to the user."}],
)
def test_contract_violation_is_rejected_and_not_saved(make_client, override):
    client = make_client(Static({**GOOD, **override}))
    assert client.post("/api/analyze", json=REQ).status_code == 502
    assert client.get("/api/history").json() == []


def test_model_timeout_returns_503_and_saves_nothing(make_client):
    def handler(request):
        raise httpx.ReadTimeout("too slow", request=request)

    provider = LocalAnalysisProvider(
        "http://lm.test/v1", "test-model", timeout=1, transport=httpx.MockTransport(handler)
    )
    client = make_client(provider)
    assert client.post("/api/analyze", json=REQ).status_code == 503
    assert client.get("/api/history").json() == []
