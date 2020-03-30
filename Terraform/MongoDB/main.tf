

 variable "mongo_container_name" {
 type         = "string"
 description  = "name of the container"
}

# Get MongoDB image
resource "docker_image" "mongo"{
 name         = "mongo:latest"
 keep_locally = true
}

# Start a MongoDB container
resource "docker_container" "mongodb" {
 name         = "${var.mongo_container_name}"
 image        = "${docker_image.mongo.latest}"
 ports {
  internal    = 27107
  external    = 27107
	}
}

