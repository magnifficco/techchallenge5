output "access_key_id" {
  value       = aws_iam_access_key.tech5_video_access_key.id
  description = "Access Key ID para o bot"
}

output "secret_access_key" {
  value       = aws_iam_access_key.tech5_video_access_key.secret
  sensitive   = true
  description = "Secret Key para o bot (NÃO compartilhe)"
}

output "user_pool_id" {
  value = aws_cognito_user_pool.user_pool.id
}

output "user_pool_client_id" {
  value = aws_cognito_user_pool_client.user_pool_client.id
}

output "s3_bucket_name" {
  value = aws_s3_bucket.video_bucket.bucket
}

output "sqs_queue_url" {
  value = aws_sqs_queue.video_queue.id
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.video_status.name
}

output "sns_topic_arn" {
  value = aws_sns_topic.video_topic.arn
}
