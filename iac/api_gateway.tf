# API Gateway for Telegram Webhooks

# Create API Gateway REST API
resource "aws_api_gateway_rest_api" "weaponsLeft_api" {
  name        = "weaponsLeft-telegram-webhook"
  description = "API Gateway for weaponsLeft Telegram bot webhooks"
}

# Create the webhook resource and tie it to the weaponsLeft bot
resource "aws_api_gateway_resource" "webhook" {
  rest_api_id = aws_api_gateway_rest_api.weaponsLeft_api.id
  parent_id   = aws_api_gateway_rest_api.weaponsLeft_api.root_resource_id
  path_part   = "webhook"
}

# Allow POST requests to the webhook resource
resource "aws_api_gateway_method" "webhook_post" {
  rest_api_id   = aws_api_gateway_rest_api.weaponsLeft_api.id
  resource_id   = aws_api_gateway_resource.webhook.id
  http_method   = "POST"
  authorization = "NONE"
}

# Connect the webhook resource to the weaponsLeft bot
resource "aws_api_gateway_integration" "webhook_lambda" {
  rest_api_id             = aws_api_gateway_rest_api.weaponsLeft_api.id
  resource_id             = aws_api_gateway_resource.webhook.id
  http_method             = aws_api_gateway_method.webhook_post.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.weaponsLeft.invoke_arn
}

# Deploy the API Gateway
resource "aws_api_gateway_deployment" "weaponsLeft_deployment" {
  depends_on = [
    aws_api_gateway_integration.webhook_lambda,
  ]

  rest_api_id = aws_api_gateway_rest_api.weaponsLeft_api.id
}

# Lambda permission for API Gateway
resource "aws_lambda_permission" "allow_api_gateway" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.weaponsLeft.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.weaponsLeft_api.execution_arn}/*/POST/webhook"
}

resource "aws_cloudwatch_log_group" "api_gw_logs" {
  name              = "/aws/apigateway/weaponsLeft"
  retention_in_days = 7
}

resource "aws_iam_role" "apigw_cloudwatch_role" {
  name = "APIGatewayCloudWatchRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "apigateway.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "apigw_cloudwatch_policy" {
  name = "APIGatewayCloudWatchPolicy"
  role = aws_iam_role.apigw_cloudwatch_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Action = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:DescribeLogGroups",
        "logs:DescribeLogStreams",
        "logs:PutLogEvents",
        "logs:GetLogEvents",
        "logs:FilterLogEvents"
      ],
      Resource = "*"
    }]
  })
}

resource "aws_api_gateway_stage" "prod" {
  stage_name    = "prod"
  rest_api_id   = aws_api_gateway_rest_api.weaponsLeft_api.id
  deployment_id = aws_api_gateway_deployment.weaponsLeft_deployment.id

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gw_logs.arn
    format          = "$context.requestId $context.integrationStatus $context.status"
  }

  xray_tracing_enabled = true
  tags = {
    App = "weaponsLeft"
  }
}
