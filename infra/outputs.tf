output "ec2_public_ip" {
  description = "Elastic IP of the EC2 instance — use this for DNS and GitHub secrets"
  value       = aws_eip.oh4s.public_ip
}

output "wagtail_media_bucket_name" {
  description = "S3 bucket that stores versioned Wagtail media archives used by local dev and EC2 bootstrap"
  value       = aws_s3_bucket.wagtail_media.bucket
}