# Configure the Docker provider
provider "docker" {
  host = "tcp://192.168.99.101:2376"
  cert_path="/mnt/c/Users/Srikanth/.docker/machine/machines/default"
}

