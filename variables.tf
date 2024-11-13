variable "region" {
  default = "us-east-2"  # Región donde se encuentra el AMI y grupo de seguridad
}

variable "instance_type" {
  default = "t2.micro"
}

variable "ami_id" {
  default = "ami-0a790393a4e66699a"  # ID del AMI existente que deseas utilizar
}

variable "security_group_id" {
  default = "sg-05ec517d83b925979"  # ID del grupo de seguridad existente
}

variable "key_name" {
  default = "GC"  # Nombre de la clave SSH ya cargada en AWS
}
