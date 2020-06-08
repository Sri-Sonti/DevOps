variable "name" {
  default = "postgres"
}

provider "postgresql" {
   
  host            = "19.16.9.12"
  username        = "guacamole_user"
  password        = "potato"
  sslmode         = "disable"
  connect_timeout = 15
}

resource "postgresql_database" "guacamole_db" {
  provider = "postgresql"
  name     = "guacamole_db"
}


