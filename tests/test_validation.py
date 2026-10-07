import pytest
from pydantic import ValidationError

from ticket_app.analysis_models import Analysis

OK_TEXT = "Please create an account for a new hire."
VALID = {
    "summary": "A valid summary text",
    "category": "role",
    "priority": "low",
    "next_action": "Send to the role queue",
}


@pytest.mark.parametrize(
    "subject,text",
    [("ab", OK_TEXT), ("a" * 101, OK_TEXT), ("Valid subject", "too short"), ("Valid subject", "a" * 4001)],
)
def test_invalid_input_rejected(make_client, subject, text):
    response = make_client().post("/api/analyze", json={"subject": subject, "text": text})
    assert response.status_code == 422


@pytest.mark.parametrize("subject,text", [("abc", "a" * 10), ("a" * 100, "a" * 4000)])
def test_boundaries_accepted(make_client, subject, text):
    response = make_client().post("/api/analyze", json={"subject": subject, "text": text})
    assert response.status_code == 200


@pytest.mark.parametrize(
    "field,value",
    [("summary", "short"), ("summary", "x" * 241), ("next_action", "too short"), ("priority", "urgent")],
)
def test_invalid_output_rejected(field, value):
    with pytest.raises(ValidationError):
        Analysis.model_validate({**VALID, field: value})


def test_extra_output_field_rejected():
    with pytest.raises(ValidationError):
        Analysis.model_validate({**VALID, "action_taken": "granted"})
