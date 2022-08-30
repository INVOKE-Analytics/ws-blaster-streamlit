resource "aws_api_gateway_rest_api" "api_gateway" {
  name        = local.prefix
  description = "API Gateway that proxies all requests to the FastAPI Lambda function"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
  tags = local.common_tags
}
