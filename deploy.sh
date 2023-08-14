#!/bin/bash

# AWS Variables
ECR_REGION="eu-west-1"
ECR_ACCOUNT_ID="502761249685"
ECR_REPO_NAME="piccadilly_status"
LAMBDA_FUNCTION_NAME="arn:aws:lambda:eu-west-1:502761249685:function:ecr-picc_status"

# Authenticate Docker with Amazon ECR registry
aws ecr get-login-password --region "$ECR_REGION" | docker login --username AWS --password-stdin "$ECR_ACCOUNT_ID".dkr.ecr."$ECR_REGION".amazonaws.com

# Build the Docker image
docker build -f app.Dockerfile -t "$ECR_ACCOUNT_ID".dkr.ecr."$ECR_REGION".amazonaws.com/"$ECR_REPO_NAME":latest --build-arg PLATFORM=lambda .

# Tag the Docker image
docker tag "$ECR_ACCOUNT_ID".dkr.ecr."$ECR_REGION".amazonaws.com/"$ECR_REPO_NAME":latest "$ECR_ACCOUNT_ID".dkr.ecr."$ECR_REGION".amazonaws.com/"$ECR_REPO_NAME":latest

# Push the Docker image to ECR
docker push "$ECR_ACCOUNT_ID".dkr.ecr."$ECR_REGION".amazonaws.com/"$ECR_REPO_NAME":latest

# Update the Lambda function with the new image
aws lambda update-function-code --function-name "$LAMBDA_FUNCTION_NAME" --image-uri "$ECR_ACCOUNT_ID".dkr.ecr."$ECR_REGION".amazonaws.com/"$ECR_REPO_NAME":latest

echo "Deployment completed successfully."
