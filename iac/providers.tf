terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.70.0"
    }
  }
  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "ap-southeast-1"
}
