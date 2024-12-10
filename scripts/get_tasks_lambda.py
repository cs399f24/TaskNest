import boto3
import json

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('task-nest-users')

    user_id = event.get('queryStringParameters', {}).get('user_id')
    if not user_id:
        try:
            body = json.loads(event.get('body', '{}'))
            user_id = body.get('user_id')
        except json.JSONDecodeError:
            pass
    
    if not user_id:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            },
            'body': json.dumps(["User ID is required"])
        }

    response = table.get_item(Key={'user-id': user_id})
    
    if 'Item' not in response:
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            },
            'body': json.dumps([])
        }

    tasks = response['Item'].get('tasks', [])
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        },
        'body': json.dumps(tasks)
    }
