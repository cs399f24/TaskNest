# lambda_function.py
import json
import boto3
from decimal import Decimal

class DynamoDB:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = self.dynamodb.Table('task-nest-users')

    def get_tasks(self, user_id):
        response = self.table.get_item(Key={'user-id': user_id})
        return response.get('Item', {}).get('tasks', [])

    def add_task(self, user_id, task):
        return self.table.update_item(
            Key={'user-id': user_id},
            UpdateExpression="SET tasks = list_append(if_not_exists(tasks, :empty_list), :new_task)",
            ExpressionAttributeValues={':new_task': [task], ':empty_list': []},
            ReturnValues="UPDATED_NEW"
        )

    def delete_task(self, user_id, description):
        tasks = self.get_tasks(user_id)
        updated_tasks = [task for task in tasks if task.get("description") != description]
        if len(tasks) == len(updated_tasks):
            return {"error": "Task not found."}

        return self.table.update_item(
            Key={'user-id': user_id},
            UpdateExpression="SET tasks = :tasks",
            ExpressionAttributeValues={':tasks': updated_tasks},
            ReturnValues="UPDATED_NEW"
        )

db = DynamoDB()

def lambda_handler(event, context):
    http_method = event['httpMethod']
    
    # Handle CORS preflight requests
    if http_method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,DELETE'
            },
            'body': json.dumps({'status': 'ok'})
        }

    # Common headers for all responses
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    try:
        if http_method == 'GET':
            if event['resource'] == '/test':
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({"message": "This is a response from Lambda!"})
                }
            elif event['resource'] == '/tasks':
                user_id = event['queryStringParameters'].get('user_id')
                if not user_id:
                    return {
                        'statusCode': 400,
                        'headers': headers,
                        'body': json.dumps({"error": "User ID is required"})
                    }
                tasks = db.get_tasks(user_id)
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps(tasks, default=str)
                }

        elif http_method == 'POST' and event['resource'] == '/add':
            body = json.loads(event['body'])
            task_description = body.get('description')
            task_time = body.get('time')
            user_id = body.get('user_id')

            if not all([task_description, task_time, user_id]):
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({"error": "Description, time, and user_id are required."})
                }

            db.add_task(user_id, {"description": task_description, "time": task_time})
            updated_tasks = db.get_tasks(user_id)
            return {
                'statusCode': 201,
                'headers': headers,
                'body': json.dumps(updated_tasks, default=str)
            }

        elif http_method == 'DELETE' and event['resource'] == '/delete':
            user_id = event['queryStringParameters'].get('user_id')
            description = event['queryStringParameters'].get('description')

            if not user_id or not description:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({"error": "User ID and description are required"})
                }

            response = db.delete_task(user_id, description)
            if "error" in response:
                return {
                    'statusCode': 404,
                    'headers': headers,
                    'body': json.dumps(response)
                }

            updated_tasks = db.get_tasks(user_id)
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(updated_tasks, default=str)
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({"error": str(e)})
        }