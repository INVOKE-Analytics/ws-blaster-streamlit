terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  # Configuration options
  region  = var.aws_region
  profile = "INVOKE"
}

# These are a set of local values that can be declared together
locals {
  prefix       = var.app_prefix
  docker_image = var.docker_image
  common_tags = {
    creator  = var.creator
    app_name = var.app_name
  }
}
