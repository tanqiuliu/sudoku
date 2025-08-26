#!/usr/bin/env python3
import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    Duration,
    BundlingOptions,
)
from constructs import Construct

class SudokuStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda function with dependency bundling
        sudoku_lambda = _lambda.Function(
            self, "SudokuLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            code=_lambda.Code.from_asset("../../",
                bundling=BundlingOptions(
                    image=_lambda.Runtime.PYTHON_3_11.bundling_image,
                    command=[
                        "bash", "-c",
                        "pip install flask mangum a2wsgi --target /asset-output && "
                        "cp -r src /asset-output/"
                    ],
                ),
                exclude=[
                    ".git", 
                    ".gitignore", 
                    "*.md", 
                    "__pycache__", 
                    "*.pyc",
                    "test_*",
                    "src/desktop",
                    "src/cli", 
                    "build",
                    "docs",
                    "deploy/cdk/cdk.out",
                    ".venv",
                    ".claude"
                ]
            ),
            handler="src.web.lambda_app.handler",
            timeout=Duration.seconds(30),
            memory_size=512,
            environment={
                'SECRET_KEY': 'sudoku_lambda_secret_key_456'
            }
        )

        # API Gateway
        api = apigateway.LambdaRestApi(
            self, "SudokuApi",
            handler=sudoku_lambda,
            proxy=True,
            description="Sudoku Game API"
        )

        # Output the API endpoint
        cdk.CfnOutput(
            self, "ApiUrl",
            value=api.url,
            description="Sudoku Game API URL"
        )

app = cdk.App()
SudokuStack(app, "SudokuStack", env=cdk.Environment(
    account=app.node.try_get_context("account"),
    region=app.node.try_get_context("region") or "us-east-1"
))

app.synth()