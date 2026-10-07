# AI usage — Group 07

The course allows coding assistants when their use is declared and the kept code can be explained.

| Tool | Used for | Kept / changed | How it was verified |
| --- | --- | --- | --- |
| Claude (Claude Code, model Opus 5.5) | Step-by-step procedure for the project; code for the provider, service guard, UI, tests, Dockerfile, Jenkinsfile and Terraform files, adapted from that procedure | Kept, after reading each file. Fixed afterwards: `src.ticket_app` imports, UTF-16 `group.txt`, ruff findings | `python -m pytest` (36 tests, green with LM Studio stopped), `ruff check`, manual API calls |
| Claude (Claude Code, model Opus 5.5) | Diagnosis of the live 503 errors: Qwen3.5 thinking mode consumed the token budget; added `reasoning_effort: "none"` to the LM Studio payload | Kept, with a test assertion on the payload | Direct `curl` to LM Studio with and without the parameter, then the before/after runs in `docs/model-evaluation.md` |
| Claude (Claude Code, model Opus 5.5) | First drafts of README, ADR 0001, ADR 0002, CONTRIBUTIONS.md and this file | Reviewed and to be completed by both students (PR links, Jenkins and Terraform evidence) | Peer review in pull requests |

Rules we follow:

- No secret, `.env`, token or full request text is ever pasted into an assistant.
- Each student can explain every line of the code listed under their name in `CONTRIBUTIONS.md`.
- Tests never assert the exact wording of a live model answer.
