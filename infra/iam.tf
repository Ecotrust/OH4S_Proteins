resource "aws_iam_role" "oh4s_ec2" {
  name = "${var.project_name}-ec2-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy" "oh4s_s3_read" {
  role = aws_iam_role.oh4s_ec2.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject"]
        Resource = "arn:aws:s3:::oh4s-db-dump/*"
      },
      {
        Effect   = "Allow"
        Action   = ["s3:ListBucket"]
        Resource = "arn:aws:s3:::oh4s-db-dump"
      }
    ]
  })
}

resource "aws_iam_instance_profile" "oh4s" {
  name = "oh4s-ec2-profile"
  role = aws_iam_role.oh4s_ec2.name
}