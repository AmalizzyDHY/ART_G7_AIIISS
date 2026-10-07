# ADR 0002 — Deployment ownership

Status: accepted · Group 07 · 2026-10-07

## Context

The application runs as two processes (FastAPI on 8000, Streamlit on 8501) from one image, needs a
writable SQLite file and must reach LM Studio on the host. Several groups share the same Docker
daemon on the lab machine, so our resources must be clearly named and removable without touching
anyone else's. The deployed image must be the exact one that passed Jenkins.

## Decision

Terraform (provider `kreuzwerker/docker` 4.0.0, files in `infra/`) is the only owner of the
group's runtime resources:

| Resource | Name | Notes |
| --- | --- | --- |
| `docker_image.app` | `copilot-g07:<green build>` | `keep_locally = true` |
| `docker_network.net` | `g07-net` | UI reaches the API through the alias `api` |
| `docker_volume.data` | `g07-data` | mounted on `/data` for SQLite |
| `docker_container.api` | `g07-api` | published on `127.0.0.1:8007` |
| `docker_container.ui` | `g07-ui` | published on `127.0.0.1:8507`, `API_URL=http://api:8000` |

Jenkins builds and smoke-tests the image and tags it `copilot-g07:<BUILD_NUMBER>`; Terraform
only references that tag through `image_name`. The API container gets a `host.docker.internal`
entry pointing to `host-gateway`, so it reaches LM Studio on the host on Windows, macOS and Linux.

## Alternatives considered

- **Docker Compose**: simpler to write, but it would own the same containers as Terraform, so
  `terraform plan` would no longer describe reality and `destroy` could leave orphans.
- **Manual `docker run`**: not reproducible, no plan, no proof of a no-change state.
- **Terraform building the image**: would deploy an image that CI never tested.

## Consequences

- A second `terraform plan -detailed-exitcode` must return 0 (no changes); this is our drift check.
- `terraform destroy` removes the network, the containers **and the `g07-data` volume**, so the
  demonstration database is lost. This is acceptable because it only holds teaching data.
- `keep_locally = true` keeps the CI image after `destroy`, so the same tag can be redeployed.
- If the Jenkins agent does not share the laptop's Docker daemon, the green image has to be moved
  with `docker save` / `docker load` before `apply`, and this handoff must be recorded.
- Nobody should run Compose or `docker run` on the names `g07-*` while Terraform manages them.
