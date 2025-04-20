# Cognito User Pool
resource "aws_cognito_user_pool" "user_pool" {
  name = "${var.project_name}-${var.environment}-user-pool"
}

resource "aws_cognito_user_pool_client" "user_pool_client" {
  name         = "${var.project_name}-${var.environment}-user-pool-client"
  user_pool_id = aws_cognito_user_pool.user_pool.id
}

# S3 Bucket
resource "aws_s3_bucket" "video_bucket" {
  bucket = "${var.project_name}-${var.environment}-videos"
}

# SQS Queue
resource "aws_sqs_queue" "video_queue" {
  name = "${var.project_name}-${var.environment}-video-queue"
}

# DynamoDB Table
resource "aws_dynamodb_table" "video_status" {
  name         = "${var.project_name}-${var.environment}-video-status"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "video_id"

  attribute {
    name = "video_id"
    type = "S"
  }

  global_secondary_index {
    name               = "user_id-index"
    hash_key           = "user_id"
    projection_type    = "ALL"
  }

  attribute {
    name = "user_id"
    type = "S"
  }
}

# SNS Topic
resource "aws_sns_topic" "video_topic" {
  name = "${var.project_name}-${var.environment}-video-topic"
}

# IAM User
resource "aws_iam_user" "tech5_video_bot" {
  name = "tech5-video-bot"
}

resource "aws_iam_user_policy" "tech5_video_policy" {
  name = "tech5-video-policy"
  user = aws_iam_user.tech5_video_bot.name

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid    = "AllowDynamoDB"
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:Query",
          "dynamodb:UpdateItem"
        ]
        Resource = aws_dynamodb_table.video_status.arn
      },
      {
        Sid    = "AllowSQS"
        Effect = "Allow"
        Action = [
          "sqs:SendMessage",
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes"
        ]
        Resource = aws_sqs_queue.video_queue.arn
      },
      {
        Sid    = "AllowSNS"
        Effect = "Allow"
        Action = "sns:Publish"
        Resource = aws_sns_topic.video_topic.arn
      },
      {
        Sid    = "AllowS3"
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = "${aws_s3_bucket.video_bucket.arn}/*"
      }
    ]
  })
}

resource "aws_iam_access_key" "tech5_video_access_key" {
  user = aws_iam_user.tech5_video_bot.name
}

data "aws_caller_identity" "current" {}
