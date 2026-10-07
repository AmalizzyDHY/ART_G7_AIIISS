import re

from ticket_app.analysis_models import Analysis, Request
from ticket_app.analysis_provider import AnalysisProvider, InvalidModelOutput

# A routing proposal must never claim that something already happened.
ACTION_CLAIM = re.compile(
    r"\b(access (is )?granted|(has|have) been (granted|created|approved|added|provisioned|changed)"
    r"|i (have )?(granted|created|added|approved))\b",
    re.IGNORECASE,
)


class AnalysisService:
    def __init__(self, provider: AnalysisProvider, policy: dict):
        self.provider, self.policy = provider, policy

    def analyze(self, request: Request) -> Analysis:
        result = self.provider.analyze(request, self.policy)
        if result.category not in self.policy["categories"]:
            raise InvalidModelOutput("Category outside the scenario contract")
        if ACTION_CLAIM.search(result.summary) or ACTION_CLAIM.search(result.next_action):
            raise InvalidModelOutput("Output claims that an action was performed")
        return result
