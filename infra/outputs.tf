output "api_url" {
  value = "http://127.0.0.1:${var.api_port}"
}

output "ui_url" {
  value = "http://127.0.0.1:${var.ui_port}"
}

output "image" {
  value = docker_image.app.name
}

output "containers" {
  value = [docker_container.api.name, docker_container.ui.name]
}
