import json

import httpx
import pytest

from ticket_app.analysis_models import Request
from ticket_app.analysis_provider import (
    FENCE,
    InvalidModelOutput,
    LocalAnalysisProvider,
    ProviderUnavailable,
)

REQUEST = Request(subject="Repo access", text="Read access to the docs repository please")
VALID = {
    "summary": "Read access to one repository",
    "category": "resource",
    "priority": "low",
    "next_action": "Send to the repository owner",
}


def reply(content):
    return httpx.Response(200, json={"choices": [{"message": {"content": content}}]})


def make(handler, key=""):
    return LocalAnalysisProvider(
        "http://lm.test/v1",
        "test-model",
        timeout=5,
        key=key,
        transport=httpx.MockTransport(handler),
        max_tokens=300,
    )


def test_request_payload_and_parser(policy):
    seen = {}

    def handler(request):
        seen["url"] = str(request.url)
        seen["auth"] = request.headers.get("authorization")
        seen["body"] = json.loads(request.content)
        return reply(json.dumps(VALID))

    analysis = make(handler).analyze(REQUEST, policy)
    body = seen["body"]
    assert seen["url"] == "http://lm.test/v1/chat/completions"
    assert seen["auth"] is None
    assert body["model"] == "test-model"
    assert body["temperature"] == 0
    assert body["max_tokens"] == 300
    assert body["reasoning_effort"] == "none"
    assert json.loads(body["messages"][-1]["content"]) == {
        "subject": "Repo access",
        "text": "Read access to the docs repository please",
    }
    assert "account, role, resource" in body["messages"][0]["content"]
    assert analysis.category == "resource"


def test_optional_key_is_sent_as_bearer(policy):
    seen = {}

    def handler(request):
        seen["auth"] = request.headers.get("authorization")
        return reply(json.dumps(VALID))

    make(handler, key="test-token").analyze(REQUEST, policy)
    assert seen["auth"] == "Bearer test-token"


def test_code_fence_is_accepted(policy):
    content = FENCE + "json\n" + json.dumps(VALID) + "\n" + FENCE
    assert make(lambda request: reply(content)).analyze(REQUEST, policy).priority == "low"


def test_timeout_is_unavailable(policy):
    def handler(request):
        raise httpx.ReadTimeout("too slow", request=request)

    with pytest.raises(ProviderUnavailable):
        make(handler).analyze(REQUEST, policy)


def test_connection_refused_is_unavailable(policy):
    def handler(request):
        raise httpx.ConnectError("refused", request=request)

    with pytest.raises(ProviderUnavailable):
        make(handler).analyze(REQUEST, policy)


@pytest.mark.parametrize(
    "content",
    [
        "Sure! Here is my answer.",
        json.dumps({key: value for key, value in VALID.items() if key != "next_action"}),
        json.dumps(["not", "an", "object"]),
    ],
)
def test_malformed_output_is_rejected(policy, content):
    with pytest.raises(InvalidModelOutput):
        make(lambda request: reply(content)).analyze(REQUEST, policy)
