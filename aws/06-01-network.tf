data "aws_subnets" "subnets" {
  filter {
    name   = "vpc-id"
    values = ["vpc-8a0e6aed"]
  }
}

