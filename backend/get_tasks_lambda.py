import boto3
import requests as request
import json
def lambda_function(event, context):

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('task-nest-users')

    body = json.loads(event['body'])

    if 'user_id' not in body:
        return {
            'statusCode': 400,
            'body': json.dumps({"error": "User ID is required"})
        }

    user_id = body.get('user_id')

    response = table.get_item(Key={'user-id': user_id})
    if 'Item' not in response:
        return {
            'statusCode': 200,
            'body': json.dumps([])
        }
    
    tasks = response['Item'].get('tasks', [])
    return {
        'statusCode': 200,
        'body': json.dumps(tasks)
    }