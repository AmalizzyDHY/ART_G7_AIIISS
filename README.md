# ART_G7_AIIISS
# Access Request Triage

Group 07 — [Student name 1] and [Student name 2]

## Objective and user stories
[Describe the user, problem and measurable benefit. Write three stories and acceptance checks.]
Assigned scope: Route an access request without granting permissions or exposing credentials.
Allowed categories: account, role, resource.

## Architecture
[Explain UI, API, analysis service, provider adapter, LM Studio and SQLite.]
[Include a diagram and explain which host runs each process.]
[Record two ADRs in docs/adr: provider boundary and local deployment ownership.]

## Prerequisites
[List the exact Python, Docker, Terraform and Jenkins versions used.]
[Name the Jenkins job and prepared agent label. Do not include credentials.]

## Installation
```bash
python -m venv .venv
# Activate .venv for your operating system.
python -m pip install -r requirements-dev.txt
python -m pip install --no-deps -e .
# Copy .env.example to .env and fill local settings.
```
On PowerShell: `.venv\Scripts\Activate.ps1`; on macOS/Linux: `source .venv/bin/activate`.

## LM Studio configuration
[Document exact model ID, server address and timeout. Record parameter settings.]
Get the ID from `http://localhost:1234/v1/models` using your actual port.
Use `LLM_PROVIDER=local` and `SCENARIO_ID=g07` in .env, then restart the API.
[Explain auth if enabled. Never print or commit a token.]
[Describe host-to-container connectivity. A remote CI agent does not share your laptop's localhost.]

## Running the application
```bash
python -m uvicorn ticket_app.api:create_app --factory --host 127.0.0.1 --port 8000
# In a second terminal:
python -m streamlit run ui/app.py
```
Open localhost:8501 and localhost:8000/docs. Set mock mode before the first run.
[Describe the request and four model-output fields, plus requires_review.]

## Tests and local model evaluation
```bash
python -m pytest --junitxml=reports/pytest.xml
```
[List tests for fixtures, validation, timeout and malformed output.]
[Show a six-case live model evaluation. Record model output, observed labels and latency.]
[Explain any mismatch. Do not expect exact wording from a live model.]

## Git workflow
[List both contributors, branches, reviewed pull requests and meaningful commits.]
[Link the failing-test commit, red Jenkins run, fix commit and green run.]
[Summarize AI coding assistance in AI_USAGE.md and verify submitted code.]

## Jenkins pipeline
[Provide the job URL, SCM branch, Script Path Jenkinsfile, ai-lab agent and trigger.]
[Explain checkout, dependencies, pytest/JUnit, IaC validation, image build and smoke test.]
[Explain why image creation must stop after a failed test.]
[Record the generated image tag and whether CI and Terraform use the same daemon.]

## Docker
```bash
docker build -t copilot-g07:manual .
python scripts/container_smoke.py copilot-g07:manual
```
[Document .dockerignore, unprivileged runtime user and startup command.]
[Explain how API and UI use the same image with different commands.]

## Terraform
[Create infra/terraform.tfvars from the example, with group_id="g07".]
[Use the image tag from the green Jenkins run, not an unrelated manual build.]
```bash
terraform -chdir=infra init
terraform -chdir=infra fmt -check
terraform -chdir=infra validate
terraform -chdir=infra plan -out=deployment.tfplan
terraform -chdir=infra apply deployment.tfplan
terraform -chdir=infra output
terraform -chdir=infra destroy
```
Expected local ports: API 8007, UI 8507. Stop the baseline UI before deployment.
[Explain local Docker image, network, data volume and two containers.]
[Show a second plan with no changes and explain that destroy removes the teaching DB.]
[Document the Docker endpoint for Windows, macOS or Linux.]
State, plans, .env and tokens stay out of Git. Commit .terraform.lock.hcl.

## Reproduction evidence
[Provide a clean-clone run, report paths, CI evidence and Terraform plan/output.]
[Have the other student reproduce the run using only this README.]

## Troubleshooting
| Symptom | Diagnosis | Resolution |
| --- | --- | --- |
| [Example] | [Concrete check] | [Verified fix] |

## Limitations and improvements
[Describe observed model mistakes, localhost boundaries and deployment limits.]
[Name one prioritized improvement and the evidence that supports it.]
