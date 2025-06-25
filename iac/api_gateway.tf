# API Gateway for Telegram Webhooks (REST API)

# Create REST API Gateway
resource "aws_api_gateway_rest_api" "weaponsLeft_api" {
  name        = "weaponsLeft-telegram-webhook"
  description = "REST API Gateway for weaponsLeft Telegram bot webhooks"
}

# Create REST API Gateway resource policy
resource "aws_api_gateway_rest_api_policy" "weaponsLeft_api_policy" {
  rest_api_id = aws_api_gateway_rest_api.weaponsLeft_api.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = "*"
        Action = "execute-api:Invoke"
        Resource = "arn:aws:execute-api:${data.aws_region.current.region}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.weaponsLeft_api.id}/*/*"
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

# Create REST API Gateway webhook resource
resource "aws_api_gateway_resource" "webhook" {
  rest_api_id = aws_api_gateway_rest_api.weaponsLeft_api.id
  parent_id   = aws_api_gateway_rest_api.weaponsLeft_api.root_resource_id
  path_part   = "webhook"
}

# Create REST API Gateway method
resource "aws_api_gateway_method" "webhook_post" {
  rest_api_id   = aws_api_gateway_rest_api.weaponsLeft_api.id
  resource_id   = aws_api_gateway_resource.webhook.id
  http_method   = "POST"
  authorization = "NONE"
}

# Create REST API Gateway integration
resource "aws_api_gateway_integration" "webhook_lambda" {
  rest_api_id = aws_api_gateway_rest_api.weaponsLeft_api.id
  resource_id = aws_api_gateway_resource.webhook.id
  http_method = aws_api_gateway_method.webhook_post.http_method

  integration_http_method = "POST"
  type                   = "AWS_PROXY"
  uri                    = aws_lambda_function.weaponsLeft.invoke_arn
}

# Create REST API Gateway deployment
resource "aws_api_gateway_deployment" "prod" {
  depends_on = [
    aws_api_gateway_integration.webhook_lambda
  ]

  rest_api_id = aws_api_gateway_rest_api.weaponsLeft_api.id

  lifecycle {
    create_before_destroy = true
  }
}

# Create REST API Gateway stage
resource "aws_api_gateway_stage" "prod" {
  deployment_id = aws_api_gateway_deployment.prod.id
  rest_api_id   = aws_api_gateway_rest_api.weaponsLeft_api.id
  stage_name    = "prod"
}

# Lambda permission for REST API Gateway
resource "aws_lambda_permission" "allow_rest_api_gateway" {
  statement_id  = "AllowExecutionFromRESTAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.weaponsLeft.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.weaponsLeft_api.execution_arn}/*/*"
}

# CloudWatch log group for API Gateway logs
resource "aws_cloudwatch_log_group" "api_gw_logs" {
  name              = "/aws/apigateway/weaponsLeft-rest"
  retention_in_days = 1
}

# IAM role for API Gateway CloudWatch logging
resource "aws_iam_role" "apigw_cloudwatch_role" {
  name = "RESTAPIGatewayCloudWatchRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "apigateway.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "apigw_cloudwatch_policy" {
  name = "RESTAPIGatewayCloudWatchPolicy"
  role = aws_iam_role.apigw_cloudwatch_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:DescribeLogGroups",
        "logs:DescribeLogStreams",
        "logs:PutLogEvents",
        "logs:GetLogEvents",
        "logs:FilterLogEvents"
      ]
      Resource = "*"
    }]
  })
}
