resource "aws_s3_bucket" "sh_datrun_landing_bucket" {
  bucket        = "sh-datrun-landing"
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "privatise_bucket" {
  bucket = aws_s3_bucket.sh_datrun_landing_bucket.id

  block_public_acls   = true
  block_public_policy = true
  ignore_public_acls  = true
}

resource "aws_s3_bucket" "sh_datrun_lambda_bucket" {
  bucket        = "sh-datrun-lambda"
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "privatise_lambda_bucket" {
  bucket = aws_s3_bucket.sh_datrun_lambda_bucket.id

  block_public_acls   = true
  block_public_policy = true
  ignore_public_acls  = true
}
