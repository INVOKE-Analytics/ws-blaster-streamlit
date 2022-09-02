# data "aws_iam_policy_document" "lambda_assume_policy" {
#   statement {
#     effect = "Allow"
#     actions = [
#       "sts:AssumeRole",
#     ]
#     principals {
#       type        = "Service"
#       identifiers = ["lambda.amazonaws.com"]
#     }
#   }
# }

# resource "aws_iam_role" "lambda_role" {
#   name               = "WhatsAppBlasterLambdaRole"
#   assume_role_policy = data.aws_iam_policy_document.lambda_assume_policy.json
# }

# resource "aws_iam_role_policy_attachment" "lambda_sqs_role_policy" {
#   role       = aws_iam_role.lambda_role.name
#   policy_arn = "arn:aws:iam::aws:policy/AmazonSQSFullAccess"
# }

# resource "aws_iam_role_policy_attachment" "lambda_logs_policy" {
#   role       = aws_iam_role.lambda_role.name
#   policy_arn = "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"
# }

data "aws_iam_role" "lambda_role" {
  name = "WhatsAppBlasterLambdaRole"
}

data "aws_ecr_image" "lambda_image" {
  repository_name = "whatsapp-blaster"
  image_tag       = "latest"
}

data "aws_ecr_repository" "ecr_repo" {
  name = "whatsapp-blaster"
}

resource "aws_lambda_function_event_invoke_config" "lambda" {
  for_each      = toset(local.environments)
  function_name = aws_lambda_function.api_lambda[each.key].function_name
  destination_config {
    on_success {
      destination = module.sqs[each.key].sqs_queue_arn
    }
    on_failure {
      destination = module.sqs[each.key].sqs_queue_arn
    }
  }
}

resource "aws_lambda_event_source_mapping" "event_source_mapping" {
  for_each         = toset(local.environments)
  event_source_arn = module.sqs[each.key].sqs_queue_arn
  function_name    = aws_lambda_function.worker_lambda[each.key].arn
}

resource "aws_lambda_permission" "api_lambda_permission" {
  for_each      = toset(local.environments)
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.api_lambda[each.key].function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.api_gateway.execution_arn}/*/*"
}

resource "aws_lambda_function" "api_lambda" {
  for_each      = toset(local.environments)
  function_name = "${local.prefix}-api-${each.key}"
  role          = data.aws_iam_role.lambda_role.arn
  image_uri     = "${data.aws_ecr_repository.ecr_repo.repository_url}@${data.aws_ecr_image.lambda_image.id}"
  package_type  = "Image"
  environment {
    variables = {
      "STAGE"   = "${each.key}",
      "SQS_URL" = "${local.prefix}-sqs-${each.key}"

    }
  }
}

resource "aws_lambda_function" "worker_lambda" {
  for_each      = toset(local.environments)
  function_name = "${local.prefix}-worker-${each.key}"
  role          = data.aws_iam_role.lambda_role.arn
  image_uri     = "${data.aws_ecr_repository.ecr_repo.repository_url}@${data.aws_ecr_image.lambda_image.id}"
  package_type  = "Image"

  image_config {
    command = ["app.lambda_function.consumer_handler"]
  }
}
