import json
import boto3

def lambda_handler(event, context):

    user_id = event.get('queryStringParameters', {}).get('user_id')
    description = event.get('queryStringParameters', {}).get('description')

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

        def delete_task(self, user_id, description):
            """Delete a specific task by description for a user."""
            tasks = self.get_tasks(user_id)
            updated_tasks = [task for task in tasks if task.get("description") != description]
            if len(tasks) == len(updated_tasks):
                return {"error": "Task not found."}

            response = self.table.update_item(
                Key={'user-id': user_id},
                UpdateExpression="SET tasks = :tasks",
                ExpressionAttributeValues={':tasks': updated_tasks},
                ReturnValues="UPDATED_NEW"
            )
            return response

    db_connection = DynamoDB()

    if not user_id or not description:
        return {
            'statusCode': 400,
            'body': json.dumps({"error": "User ID and description are required"}),
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,DELETE',
            }
        }

    response = db_connection.delete_task(user_id, description)
    
    if "error" in response:
        return {
            'statusCode': 404,
            'body': json.dumps(response),
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,DELETE',
            }
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps({"message": "Task deleted successfully"}),
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,DELETE',
        }
    }
