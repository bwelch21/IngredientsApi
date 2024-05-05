#!/bin/bash

# Set your AWS region and account number
aws_region="us-east-1"
aws_account_number="***REMOVED***"
image_name="$aws_account_number.dkr.ecr.$aws_region.amazonaws.com/ingredients-api"


aws ecr get-login-password --region "$aws_region" | docker login --username AWS --password-stdin "$aws_account_number".dkr.ecr."$aws_region".amazonaws.com

docker pull $image_name:latest

docker run -dit --rm -w /ingredients-api -p 8000:8000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  ***REMOVED***.dkr.ecr.us-east-1.amazonaws.com/ingredients-api