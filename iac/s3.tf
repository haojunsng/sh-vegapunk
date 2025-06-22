resource "aws_s3_bucket" "data_robot_bucket" {
  bucket        = "data-robot-franky"
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "privatise_bucket" {
  bucket = aws_s3_bucket.data_robot_bucket.id

  block_public_acls   = true
  block_public_policy = true
  ignore_public_acls  = true
}
