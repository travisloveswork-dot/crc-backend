import json
import boto3

def lambda_handler(event, context):
    # Initializing boto3 inside the handler allows testing tools to mock AWS correctly
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('MyCRCresumeViewCount')

    response = table.update_item(
        Key={
            'id': '0'
        },
        UpdateExpression='ADD #v :inc',
        ExpressionAttributeNames={
            '#v': 'views'
        },
        ExpressionAttributeValues={
            ':inc': 1
        },
        ReturnValues='UPDATED_NEW'
    )

    views = int(response['Attributes']['views'])

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
        },
        'body': json.dumps({'views': views})
    }