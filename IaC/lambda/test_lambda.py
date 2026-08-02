import os
import json
import boto3
import pytest
from moto import mock_aws
from resumefunc import lambda_handler

# 1. Supply dummy AWS credentials so boto3 does not call live AWS
@pytest.fixture
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

# 2. Mock AWS calls for this test
@mock_aws
def test_lambda_handler(aws_credentials):
    # ARRANGE: Create fake DynamoDB table matching 'MyCRCresumeViewCount'
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table = dynamodb.create_table(
        TableName="MyCRCresumeViewCount",
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
    )
    
    # Seed fake database with item id='0' and views=0
    table.put_item(Item={"id": "0", "views": 0})

    # ACT: Run lambda_handler from resumefunc.py
    response = lambda_handler({}, None)
    body = json.loads(response["body"])

    # ASSERT: Check for status code 200 and updated view count of 1
    assert response["statusCode"] == 200
    assert body["views"] == 1