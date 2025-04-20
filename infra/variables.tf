variable "aws_region" {
  description = "AWS region"
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name prefix"
  default     = "tech5"
}

variable "environment" {
  description = "Environment name"
  default     = "dev"
}
variable "sqs_queue_name" {
  default = "tech5-video-queue"
}

variable "sns_topic_name" {
  default = "tech5-video-topic"
}

variable "s3_bucket_name" {
  default = "tech5-videos"
}

variable "dynamodb_table_name" {
  default = "tech5-dev-video-status"
}
