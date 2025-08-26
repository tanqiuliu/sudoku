# Sudoku Game AWS Lambda Deployment

This deploys the Sudoku game to AWS Lambda with API Gateway for web access.

## Prerequisites

1. **AWS CLI configured**:
   ```bash
   aws configure
   ```

2. **Node.js and AWS CDK CLI installed**:
   ```bash
   npm install -g aws-cdk
   ```

## Deployment

1. **Run the deployment script**:
   ```bash
   ./deploy.sh
   ```

2. **Or deploy manually**:
   ```bash
   # Bootstrap CDK (first time only)
   cdk bootstrap
   
   # Deploy the stack
   cdk deploy
   ```

## Architecture

- **AWS Lambda**: Runs the Flask app using Mangum adapter
- **API Gateway**: Provides HTTP endpoints
- **In-memory storage**: Game state (resets on Lambda cold starts)

## Usage

After deployment, you'll get an API Gateway URL like:
```
https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/prod/
```

Visit this URL to play Sudoku!

## Features

- ✅ Web-based Sudoku game
- ✅ Three difficulty levels
- ✅ Real-time validation
- ✅ Hint system
- ✅ Serverless deployment

## Cleanup

To remove all AWS resources:
```bash
cdk destroy
```