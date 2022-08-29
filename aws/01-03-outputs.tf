output "ecr_repository_url" {
  description = "The URL of the ecr reposiory"
  value       = aws_ecr_repository.ecr_repo.repository_url
}

output "ecr_repository_arm" {
  description = "The ARN of the ecr reposiory"
  value       = aws_ecr_repository.ecr_repo.arn
}
