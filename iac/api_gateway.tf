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

resource "aws_api_gateway_stage" "prod" {
  stage_name    = "prod"
  rest_api_id   = aws_api_gateway_rest_api.weaponsLeft_api.id
  deployment_id = aws_api_gateway_deployment.weaponsLeft_deployment.id
}


# Lambda permission for API Gateway
resource "aws_lambda_permission" "allow_api_gateway" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.weaponsLeft.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.weaponsLeft_api.execution_arn}/*/*"
}
