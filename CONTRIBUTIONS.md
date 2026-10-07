# Contributions — Group 07

Update this file after every merged pull request. Each student must be able to explain the code
listed under their name during the defence.

## Lisa (branch `Lisa`)

Code written:

- Import of the common starter, `group.txt`, `scenarios/g07.json`, fixtures and `.env.example`.
- `analysis_provider.py` (mock and LM Studio adapter, `reasoning_effort` fix), token limit in `api.py`.
- `analysis_service.py` guard, `Record.requires_review: Literal[True]`, Streamlit UI.
- Tests in `tests/` (conftest, scenario, validation, local adapter, API failures).
- `Dockerfile`, `.dockerignore`, `Jenkinsfile`, `infra/*.tf`.
- Import fixes (`src.ticket_app` → `ticket_app`) and ASCII `group.txt`.
- Live evaluation (`scripts/evaluate_live.py`, `docs/model-evaluation.md`), ADR 0001 and 0002, README.
- Terraform provider lock file (`infra/.terraform.lock.hcl`) for Windows, Linux and macOS.
- `demo/ci-failure` branch with the deliberate failing commit for the Jenkins demonstration.

Verification and evidence:

- Docker image checks and smoke test (`evidence/docker-checks.txt`).
- Full Terraform cycle in mock mode and in local mode with LM Studio: plan, apply, second plan
  with no changes, destroy (`evidence/tf-*.txt`, `evidence/deploy-local-checks.txt`).
- Screenshots of the deployed UI: validated account request, controlled 503 with LM Studio
  stopped (`evidence/ui-account-result.png`, `evidence/ui-lmstudio-stopped.png`).
- Linux rehearsal of the Jenkins Install, Test and Terraform validate stages.
- Diagnosis of the Docker Desktop crash (full `C:` disk) and of the Qwen3.5 thinking timeouts.

Main commits: see the table in the README, section "Git workflow".

Pull requests written: `Lisa` → `main` (link to be added), `demo/ci-failure` → `main` (link to be added).

Pull requests reviewed: to be listed with links.

Defence topic: provider boundary (ADR 0001), the live model evaluation and the Terraform
deployment in local mode.

## Rollin (branch `Rollin`)

Code written: to be completed by Rollin.

Pull requests written: to be completed.

Pull requests reviewed: to be completed.

Defence topic: to be completed (suggested: Jenkins pipeline and failure/fix demonstration, ADR 0002).

## Reviews

| PR | Author | Reviewer | Concrete comment | Merge type |
| --- | --- | --- | --- | --- |
| to be added | | | | merge commit |
