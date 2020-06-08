
variable "name" {
  default = "Guacamole"
}

# Configure the Docker provider
provider "docker" {
  host = "tcp://192.168.99.102:2376"
  cert_path="/mnt/c/Users/Sri/.docker/machine/machines/default"
}


# Get Guacd image
resource "docker_image" "guacd"{
 name         = "guacamole/guacd"
 keep_locally = true
}    

# Start a Guacd container
resource "docker_container" "guacd" {
 name         = "some-guacd"
 image        = "${docker_image.guacd.latest}"
 ports {
  internal    = 4822
  external    = 4822
  ip	      = "0.0.0.0"
	}
}



# Get postgres image
resource "docker_image" "postgres"{
 name         = "postgres:latest"
 keep_locally = true
}

# Start a postgres container
resource "docker_container" "postgres" {
 name         = "some-postgres"
 image        = "${docker_image.postgres.latest}"
 ports {
  internal    = 5432
  external    = 5432
  ip        = "0.0.0.0"
  }
}



# Get Guacamole image
resource "docker_image" "guacamole"{
 name         = "guacamole/guacamole"
 keep_locally = true
}

# Start a Guacd container
resource "docker_container" "guacamole" {
 name         = "some-guacamole"
 image        = "${docker_image.guacamole.latest}"
 links = ["some-guacd:guacd" , "some-postgres:postgres"]
 
 ports {
  internal    = 8090
  external    = 8090
  ip	      = "0.0.0.0"
	}
}

