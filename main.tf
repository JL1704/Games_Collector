# Definir el proveedor de AWS
provider "aws" {
  region = var.region
}

# Configuración de una clave SSH para acceder a la instancia
# Usaremos el key_name ya existente, así que no crearemos un aws_key_pair
resource "aws_instance" "app_server" {
  ami                    = var.ami_id  # Reutilizar el ID del AMI existente
  instance_type          = var.instance_type
  key_name               = var.key_name  # Reutilizar el nombre de la clave SSH
  vpc_security_group_ids = [var.security_group_id]  # Reutilizar el grupo de seguridad existente

  # Etiqueta para identificar la instancia
  tags = {
    Name = "GamesCollector-Server"
  }
}
