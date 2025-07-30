variable "aws_region" {
  default = "eu-west-2"
}

variable "ami_id" {
  description = "Ubuntu 22.04 AMI ID"
  default     = "ami-0fc5d935ebf8bc3bc" # London region
}

variable "public_key" {
  description = "SSH public key content"
  type        = string
}
