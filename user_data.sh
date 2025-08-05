#!/bin/bash
yum update -y
yum install -y docker
systemctl enable docker
systemctl start docker

# Set your AWS region and account number
aws_region="us-east-1"
aws_account_number="${AWS_ACCOUNT_NUMBER}"
image_name="$aws_account_number.dkr.ecr.$aws_region.amazonaws.com/ingredients-api"

aws ecr get-login-password --region "$aws_region" | docker login --username AWS --password-stdin "$aws_account_number".dkr.ecr."$aws_region".amazonaws.com

docker run -dit --rm -w /ingredients-api -p 8000:8000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e ALLERGY_INSIGHTS_KEY=$ALLERGY_INSIGHTS_KEY> \
  $image_name