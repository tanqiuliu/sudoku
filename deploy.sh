#!/bin/bash

echo "🎮 Deploying Sudoku Game to AWS Lambda..."

# Check if AWS CLI is configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS CLI not configured. Please run 'aws configure' first."
    exit 1
fi

# Bootstrap CDK if needed (only run once per account/region)
echo "🔧 Bootstrapping CDK..."
cdk bootstrap

# Deploy the stack
echo "🚀 Deploying CDK stack..."
cdk deploy --require-approval never

echo "✅ Deployment complete! Check the output for your API URL."