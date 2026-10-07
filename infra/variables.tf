variable "group_id" {
  type    = string
  default = "g07"
}

variable "image_name" {
  type        = string
  description = "Image tag produced by the green Jenkins run, for example copilot-g07:12"
}

variable "docker_host" {
  type        = string
  default     = "unix:///var/run/docker.sock"
  description = "Docker endpoint from docker context inspect (Windows: npipe:////./pipe/docker_engine)"
}

variable "api_port" {
  type    = number
  default = 8007
}

variable "ui_port" {
  type    = number
  default = 8507
}

variable "llm_provider" {
  type    = string
  default = "mock"

  validation {
    condition     = contains(["mock", "local"], var.llm_provider)
    error_message = "llm_provider must be mock or local."
  }
}

variable "llm_base_url" {
  type    = string
  default = "http://host.docker.internal:1234/v1"
}

variable "llm_model" {
  type    = string
  default = ""
}

variable "llm_timeout" {
  type    = number
  default = 60
}

variable "llm_max_tokens" {
  type    = number
  default = 300
}
