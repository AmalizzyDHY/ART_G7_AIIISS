terraform {
  required_version = ">= 1.13.0"

  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "4.0.0"
    }
  }
}

provider "docker" {
  host = var.docker_host
}
