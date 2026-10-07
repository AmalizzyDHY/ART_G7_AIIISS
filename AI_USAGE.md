# AI usage — Group 07

The course allows coding assistants when their use is declared and the kept code can be explained.

| Tool | Used for | Kept / changed | How it was verified |
| --- | --- | --- | --- |
| Claude (Claude Code, model Opus 5.5) | Step-by-step procedure for the project; code for the provider, service guard, UI, tests, Dockerfile, Jenkinsfile and Terraform files, adapted from that procedure | Kept, after reading each file. Fixed afterwards: `src.ticket_app` imports, UTF-16 `group.txt`, ruff findings | `python -m pytest` (36 tests, green with LM Studio stopped), `ruff check`, manual API calls |
| Claude (Claude Code, model Opus 5.5) | Diagnosis of the live 503 errors: Qwen3.5 thinking mode consumed the token budget; added `reasoning_effort: "none"` to the LM Studio payload | Kept, with a test assertion on the payload | Direct `curl` to LM Studio with and without the parameter, then the before/after runs in `docs/model-evaluation.md` |
| Claude (Claude Code, model Opus 5.5) | Diagnosis of the Docker Desktop crash: Docker VM logs showed `python3.12` and `dockerd` killed by SIGBUS and `mkfs` failing because `C:` had 1 GB free; then removal of the corrupted base image and rebuild with `--no-cache --pull` | Kept; the disk space was freed by the student | Smoke test, `whoami`, `/data` write test (`evidence/docker-checks.txt`) |
| Claude (Claude Code, model Opus 5.5) | Running the Terraform cycle (mock then local mode) and recording the outputs as evidence; Linux rehearsal of the Jenkins stages in `python:3.12-slim` and `hashicorp/terraform:1.13.3` containers | Kept as evidence; no Terraform file was changed | Second plan "No changes" with exit code 0, destroy leaving no `g07` resource, screenshots taken by the student |
| Claude (Claude Code, model Opus 5.5) | Checking the LM Studio setup (network listening, model loaded with 4096 context, access from a container); translation of commit messages into French before the first push | Kept | Real request from a container (`evidence/deploy-local-checks.txt`); file content unchanged by the message rewrite |
| Claude (Claude Code, model Opus 5.5) | First drafts of README, ADR 0001, ADR 0002, CONTRIBUTIONS.md and this file | Reviewed and to be completed by both students (PR links, Jenkins and Terraform evidence) | Peer review in pull requests |

Rules we follow:

- No secret, `.env`, token or full request text is ever pasted into an assistant.
- Each student can explain every line of the code listed under their name in `CONTRIBUTIONS.md`.
- Tests never assert the exact wording of a live model answer.
