import json
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"

SUPPLIED = json.loads((FIXTURES / "g07.json").read_text())
EXTRA = json.loads((FIXTURES / "g07_extra.json").read_text())


def test_six_supplied_examples_two_per_category():
    assert len(SUPPLIED) == 6
    for category in ("account", "role", "resource"):
        assert sum(case["expected_category"] == category for case in SUPPLIED) == 2


@pytest.mark.parametrize("case", SUPPLIED + EXTRA, ids=lambda case: case["subject"])
def test_mock_routes_each_example(make_client, case):
    response = make_client().post(
        "/api/analyze", json={"subject": case["subject"], "text": case["text"]}
    )
    assert response.status_code == 200
    record = response.json()
    assert record["requires_review"] is True
    assert record["analysis"]["category"] == case["expected_category"]
    assert record["analysis"]["priority"] == case["expected_priority"]
    assert "password" not in json.dumps(record["analysis"]).lower()


def test_successful_result_is_saved(make_client):
    client = make_client()
    client.post("/api/analyze", json={"subject": "Role request", "text": "I need the reporting role."})
    history = client.get("/api/history").json()
    assert len(history) == 1
    assert history[0]["analysis"]["category"] == "role"
    assert history[0]["requires_review"] is True
