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
      "STAGE"            = "${each.key}",
      "SQS_URL"          = "${local.prefix}-sqs-${each.key}"
      "LOCAL_MOUNT_PATH" = "/mnt/files"

    }
  }
}

resource "aws_lambda_function" "worker_lambda" {
  for_each      = toset(local.environments)
  function_name = "${local.prefix}-worker-${each.key}"
  role          = data.aws_iam_role.lambda_role.arn
  image_uri     = "${data.aws_ecr_repository.ecr_repo.repository_url}@${data.aws_ecr_image.lambda_image.id}"
  package_type  = "Image"

  vpc_config {
    # Every subnet should be able to reach an EFS mount target in the same Availability Zone. Cross-AZ mounts are not permitted.
    subnet_ids         = data.aws_subnets.subnets.ids
    security_group_ids = ["sg-0f858f501b1216043"]
  }

  file_system_config {
    # EFS file system access point ARN
    arn = aws_efs_access_point.access_point_for_lambda.arn

    # Local mount path inside the lambda function. Must start with '/mnt/'.
    local_mount_path = "/mnt/files"
  }

  depends_on = [aws_efs_mount_target.alpha]

  image_config {
    command = ["app.lambda_function.consumer_handler"]
  }
}
