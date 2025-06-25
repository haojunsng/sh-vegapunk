# API Gateway for Telegram Webhooks (HTTP API)

# Create HTTP API Gateway
resource "aws_apigatewayv2_api" "weaponsLeft_api" {
  name          = "weaponsLeft-telegram-webhook"
  protocol_type = "HTTP"
  description   = "HTTP API Gateway for weaponsLeft Telegram bot webhooks"
}

# Create HTTP API Gateway stage
resource "aws_apigatewayv2_stage" "prod" {
  api_id = aws_apigatewayv2_api.weaponsLeft_api.id
  name   = "prod"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gw_logs.arn
    format = jsonencode({
      requestId      = "$context.requestId"
      ip             = "$context.identity.sourceIp"
      requestTime    = "$context.requestTime"
      httpMethod     = "$context.httpMethod"
      routeKey       = "$context.routeKey"
      status         = "$context.status"
      protocol       = "$context.protocol"
      responseLength = "$context.responseLength"
      integrationLatency = "$context.integrationLatency"
      responseLatency    = "$context.responseLatency"
    })
  }

  default_route_settings {
    throttling_burst_limit = 100
    throttling_rate_limit  = 50
  }

  tags = {
    App = "weaponsLeft"
  }
}

# Create HTTP API Gateway integration
resource "aws_apigatewayv2_integration" "webhook_lambda" {
  api_id           = aws_apigatewayv2_api.weaponsLeft_api.id
  integration_type = "AWS_PROXY"

  connection_type      = "INTERNET"
  description         = "Lambda integration for weaponsLeft webhook"
  integration_method  = "POST"
  integration_uri     = aws_lambda_function.weaponsLeft.invoke_arn
  payload_format_version = "2.0"
}

# Create HTTP API Gateway route
resource "aws_apigatewayv2_route" "webhook_post" {
  api_id    = aws_apigatewayv2_api.weaponsLeft_api.id
  route_key = "POST /webhook"
  target    = "integrations/${aws_apigatewayv2_integration.webhook_lambda.id}"
}

# Lambda permission for HTTP API Gateway
resource "aws_lambda_permission" "allow_http_api_gateway" {
  statement_id  = "AllowExecutionFromHTTPAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.weaponsLeft.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.weaponsLeft_api.execution_arn}/*/*"
}

# CloudWatch log group for API Gateway logs
resource "aws_cloudwatch_log_group" "api_gw_logs" {
  name              = "/aws/apigateway/weaponsLeft-http"
  retention_in_days = 1
}

# IAM role for API Gateway CloudWatch logging (if needed for HTTP API)
resource "aws_iam_role" "apigw_cloudwatch_role" {
  name = "HTTPAPIGatewayCloudWatchRole"

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
  name = "HTTPAPIGatewayCloudWatchPolicy"
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

resource "aws_apigatewayv2_api_policy" "weaponsLeft_api_policy" {
  api_id = aws_apigatewayv2_api.weaponsLeft_api.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = "*",
        Action = "execute-api:Invoke",
        Resource = "arn:aws:execute-api:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:${aws_apigatewayv2_api.weaponsLeft_api.id}/*/*",
        Condition = {
          IpAddress = {
            "aws:SourceIp" = [
              "173.245.48.0/20",
              "103.21.244.0/22",
              "103.22.200.0/22",
              "103.31.4.0/22",
              "141.101.64.0/18",
              "108.162.192.0/18",
              "190.93.240.0/20",
              "188.114.96.0/20",
              "197.234.240.0/22",
              "198.41.128.0/17",
              "162.158.0.0/15",
              "104.16.0.0/13",
              "104.24.0.0/14",
              "172.64.0.0/13",
              "131.0.72.0/22"
            ]
          }
        }
      }
    ]
  })
}
