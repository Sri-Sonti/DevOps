
module "docker" {
  source = "mod_docker"
  name   = "Guacamole"
}

module "postgres" {
  source = "mod_postgres"
  name   = "postgres"
}