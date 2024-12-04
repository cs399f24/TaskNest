import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    
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
            'body': json.dumps(["Request body is missing"])
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
                'body': json.dumps(["Invalid JSON format"])
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
            'body': json.dumps(["Description and time are required."])
        }

    task = {"description": task_description, "time": task_time}
    
    user_id = body.get("user_id")

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
