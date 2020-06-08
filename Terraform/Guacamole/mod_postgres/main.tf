variable "name" {
  default = "postgres"
}

provider "postgresql" {
   
  host            = "192.168.99.102"
  username        = "guacamole_user"
  password        = "potato"
  sslmode         = "disable"
  connect_timeout = 15
}

resource "postgresql_database" "guacamole_db" {
  provider = "postgresql"
  name     = "guacamole_db"
}


