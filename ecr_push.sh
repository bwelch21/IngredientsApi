#!/bin/bash

# Set your AWS region and account number
aws_region="us-east-1"
aws_account_number="***REMOVED***"

# Log in to ECR
aws ecr get-login-password --region "$aws_region" | docker login --username AWS --password-stdin "$aws_account_number".dkr.ecr."$aws_region".amazonaws.com

# Build the Docker image
docker build --platform linux/amd64 --build-arg OPENAI_API_KEY="$OPENAI_API_KEY" -t "$aws_account_number".dkr.ecr."$aws_region".amazonaws.com/ingredients-api:latest .

# Push the Docker image to ECR
docker push "$aws_account_number".dkr.ecr."$aws_region".amazonaws.com/ingredients-api:latest