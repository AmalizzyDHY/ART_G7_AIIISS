# ADR 0001 — Analysis provider boundary

Status: accepted · Group 07 · 2026-10-07

## Context

Access Request Triage must classify a request into `account`, `role` or `resource` with a local
model served by LM Studio, but the CI agent (`ai-lab`) has no GPU, no LM Studio and no token. The
tests must therefore run without any model, and the code that talks to LM Studio must still be
tested (payload, parser, timeout, malformed output). The model output is untrusted: it can be
invalid JSON, contain an extra field, use an unknown category or claim that access was granted.

## Decision

All inference goes through one interface, `AnalysisProvider.analyze(request, policy) -> Analysis`,
defined in `src/ticket_app/analysis_provider.py`. It has two implementations:

- `MockAnalysisProvider`: deterministic keyword routing driven by `scenarios/g07.json`
  (`keywords`, `high_priority_words`). Used by CI, tests and the Docker smoke test.
- `LocalAnalysisProvider`: calls the OpenAI-compatible `/chat/completions` endpoint of LM Studio
  with a finite timeout (`LLM_TIMEOUT`), an output token limit (`LLM_MAX_TOKENS`) and
  `temperature: 0`. Network errors, timeouts and HTTP error statuses become `ProviderUnavailable`
  (HTTP 503); unparsable or invalid output becomes `InvalidModelOutput` (HTTP 502).

`api.py` picks the implementation from `LLM_PROVIDER` once, in `create_app`. `AnalysisService`
only sees the interface and adds the scenario rules (allowed category, no claimed action). The
Streamlit UI only calls the HTTP API and never imports a provider. The request text is sent to the
model as a JSON string, so it stays data and is never concatenated into the instructions.

## Alternatives considered

- **HTTP call directly inside `AnalysisService`**: fewer files, but the service could no longer be
  tested without a server, and the scenario rules would be mixed with transport error handling.
- **Calling a real LLM in CI**: closest to production, but CI would depend on a laptop or a paid
  token, be slow and non-deterministic, and could not assert exact categories.
- **UI calling LM Studio directly**: would bypass validation and storage, so an invalid answer
  could be shown as a result.

## Consequences

- The whole suite (36 tests) runs in about two seconds with LM Studio stopped; `conftest.py`
  forces `LLM_PROVIDER=mock` so a local `.env` cannot leak into tests.
- The adapter is still covered through `httpx.MockTransport` (payload, bearer key, code fence,
  timeout, refused connection, malformed output).
- Mock quality says nothing about model quality: live behaviour is measured separately in
  `docs/model-evaluation.md`.
- Adding a hosted provider later only requires a new class with the same `analyze` method.
