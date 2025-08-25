#!/usr/bin/env python3
import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    Duration,
)
from constructs import Construct

class SudokuStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda function
        sudoku_lambda = _lambda.Function(
            self, "SudokuLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            code=_lambda.Code.from_asset(".", 
                exclude=[
                    ".git", 
                    ".gitignore", 
                    "*.md", 
                    "__pycache__", 
                    "*.pyc",
                    "test_*",
                    "web_gui.py",
                    "sudoku_gui.py",
                    "cdk.out",
                    ".venv"
                ]
            ),
            handler="lambda_app.handler",
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