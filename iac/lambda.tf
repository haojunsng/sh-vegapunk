# strongRight bot
# Lambda role
resource "aws_iam_role" "strongRight_lambda_role" {
  name = "strongRight-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

# Lambda policy
resource "aws_iam_role_policy" "strongRight_lambda_policy" {
  name = "strongRight-logs-policy"
  role = aws_iam_role.strongRight_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "logs:CreateLogGroup"
        Resource = "arn:aws:logs:ap-southeast-1:${data.aws_caller_identity.current.account_id}:*"
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = [
          "arn:aws:logs:ap-southeast-1:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/strongRight:*",
          "arn:aws:logs:ap-southeast-1:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/weaponsLeft:*"
        ]
      }
    ]
  })
}

# Lambda function
resource "aws_lambda_function" "tsrc_poll_bot" {
  function_name = "strongRight"

  s3_bucket = aws_s3_bucket.data_robot_bucket.bucket
  s3_key    = "lambda/strong-right/lambda_function.zip"

  handler = "strong_right_bot.lambda_handler"
  runtime = "python3.13"

  role = aws_iam_role.strongRight_lambda_role.arn

  source_code_hash = data.aws_s3_object.strong_right_zip.etag

  environment {
    variables = {
      BOT_TOKEN       = var.bot_token
      CHAT_ID        = var.chat_id
      THREAD_ID = var.thread_id
    }
  }
}

# EventBridge rule (schedule)
resource "aws_cloudwatch_event_rule" "weekly_schedule" {
  name                = "2000hrs-sunday-weekly"
  description         = "Every Sunday at 2000hrs"
  schedule_expression = "cron(0 6 ? * SUN *)"  # Sunday 2 PM SGT
}

# Permission for EventBridge to invoke Lambda
resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.tsrc_poll_bot.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.weekly_schedule.arn
}

# EventBridge target (link rule to Lambda)
resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.weekly_schedule.name
  target_id = "tsrc-poll-lambda"
  arn       = aws_lambda_function.tsrc_poll_bot.arn
}

# weaponsLeft bot
resource "aws_lambda_function" "weaponsLeft" {
  function_name = "weaponsLeft"
  role          = aws_iam_role.strongRight_lambda_role.arn
  handler       = "weapons_left_bot.lambda_handler"
  runtime       = "python3.13"
  timeout       = 30

  s3_bucket = aws_s3_bucket.data_robot_bucket.bucket
  s3_key    = "lambda/weapons-left/lambda_function.zip"

  source_code_hash = data.aws_s3_object.weapons_left_zip.etag

  environment {
    variables = {
      WEAPONS_LEFT_BOT_TOKEN = var.weapons_left_bot_token
    }
  }
}
