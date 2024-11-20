import json
import boto3
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
            print(tasks)
            return tasks

        def add_task(self, user_id, task):
            """Add a task for a specific user to DynamoDB."""
            response = self.table.update_item(
                Key={'user-id': user_id},
                UpdateExpression="SET tasks = list_append(if_not_exists(tasks, :empty_list), :new_task)",
                ExpressionAttributeValues={':new_task': [task], ':empty_list': []},
                ReturnValues="UPDATED_NEW"
            )
            return response

    body = json.loads(event['body'])
    db_connection = DynamoDB()

    if 'user_id' not in body or 'time' not in body or 'description' not in body:
        return {
            'statusCode': 400,
            'body': json.dumps({"error": "Missing Parameters is required"})
        }

    user_id = body.get('user_id')
    task_description = body.get('description')
    task_time = body.get('time')
    
    if not all([task_description, task_time, user_id]):
        return {
            'statusCode': 400,
            'body': json.dumps({"error": "Description, time, and user_id are required."})
        }

    db_connection.add_task(user_id, {"description": task_description, "time": task_time})
    updated_tasks = db_connection.get_tasks(user_id)

    return {
        'statusCode': 201,
        'body': json.dumps(updated_tasks)
    }