resource "docker_image" "app" {
  name         = var.image_name
  keep_locally = true # destroy must not delete the CI image
}

resource "docker_network" "net" {
  name = "${var.group_id}-net"
}

resource "docker_volume" "data" {
  name = "${var.group_id}-data"
}

resource "docker_container" "api" {
  name    = "${var.group_id}-api"
  image   = docker_image.app.image_id
  restart = "unless-stopped"
  command = ["python", "-m", "uvicorn", "ticket_app.api:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]

  env = [
    "LLM_PROVIDER=${var.llm_provider}",
    "SCENARIO_ID=${var.group_id}",
    "LLM_BASE_URL=${var.llm_base_url}",
    "LLM_MODEL=${var.llm_model}",
    "LLM_TIMEOUT=${var.llm_timeout}",
    "LLM_MAX_TOKENS=${var.llm_max_tokens}",
    "DB_PATH=/data/analyses.db",
  ]

  ports {
    internal = 8000
    external = var.api_port
    ip       = "127.0.0.1"
  }

  networks_advanced {
    name    = docker_network.net.name
    aliases = ["api"]
  }

  volumes {
    volume_name    = docker_volume.data.name
    container_path = "/data"
  }

  # Lets the container reach LM Studio on the host, including on Linux.
  host {
    host = "host.docker.internal"
    ip   = "host-gateway"
  }
}

resource "docker_container" "ui" {
  name    = "${var.group_id}-ui"
  image   = docker_image.app.image_id
  restart = "unless-stopped"
  command = ["python", "-m", "streamlit", "run", "ui/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
  env     = ["API_URL=http://api:8000"]

  ports {
    internal = 8501
    external = var.ui_port
    ip       = "127.0.0.1"
  }

  networks_advanced {
    name = docker_network.net.name
  }

  depends_on = [docker_container.api]
}
