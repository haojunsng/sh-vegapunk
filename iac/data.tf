# Get current account ID
data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

# Data source to get S3 object ETag for strong_right
data "aws_s3_object" "strong_right_zip" {
  bucket = aws_s3_bucket.data_robot_bucket.bucket
  key    = "lambda/strong-right/lambda_function.zip"
}

# Data source to get S3 object ETag for weapons_left
data "aws_s3_object" "weapons_left_zip" {
  bucket = aws_s3_bucket.data_robot_bucket.bucket
  key    = "lambda/weapons-left/lambda_function.zip"
}
