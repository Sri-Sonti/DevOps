# Configure the Docker provider
provider "docker" {
  host = "tcp://<hostIP>:2376"
  cert_path="/mnt/c/Users/sri/.docker/machine/machines/default"
}

