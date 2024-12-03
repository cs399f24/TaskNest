import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    print("Event Received: ", json.dumps(event))

    # Get the token from the 'Authorization' header
    token = None
    if 'headers' in event and 'Authorization' in event['headers']:
        token = event['headers']['Authorization']
    if not token:
        return {
            'statusCode': 401,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(["Authorization token is missing"])
        }

    if token.startswith("Bearer "):
        token = token[7:]

    cognito_client = boto3.client('cognito-idp')

    try:
        response = cognito_client.get_user(
            AccessToken=token
        )
        print(f"User validated: {json.dumps(response)}")
        user_id = response['Username']
    except ClientError as e:
        return {
            'statusCode': 403,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps([f"Token validation failed: {str(e)}"])
        }

    class DynamoDB:
        def __init__(self):
            self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
            self.table = self.dynamodb.Table('task-nest-users')

        def get_tasks(self, user_id):
            """Retrieve tasks for a specific user from DynamoDB."""
            response = self.table.get_item(Key={'user-id': user_id})
            if 'Item' not in response:
                return []
            tasks = response['Item'].get('tasks', [])
            return tasks

        def add_task(self, user_id, task):
            """Add a task for a specific user to DynamoDB."""
            response = self.table.update_item(
                Key={'user-id': user_id},
                UpdateExpression="SET tasks = list_append(if_not_exists(tasks, :empty_list), :new_task)",
                ExpressionAttributeValues={':new_task': [task], ':empty_list': []},
                ReturnValues="UPDATED_NEW"
            )
            print(f"DynamoDB update response: {json.dumps(response)}")
            return response

    if 'body' not in event or not event['body']:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(["Request body is missing"])  # Ensure the body is a JSON string
        }

    if isinstance(event['body'], str):
        try:
            body = json.loads(event['body'])
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps(["Invalid JSON format"])  # Ensure the body is a JSON string
            }
    else:
        body = event['body']

    db_connection = DynamoDB()

    task_description = body['description']
    task_time = body['time']
    
    if not all([task_description, task_time]):
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(["Description and time are required."])  # Ensure the body is a JSON string
        }

    task = {"description": task_description, "time": task_time}
    
    db_connection.add_task(user_id, task)

    task_list = db_connection.get_tasks(user_id)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS, GET',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps(task_list, default=str)
    }
