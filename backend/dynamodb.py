import boto3

# This class is responsible for interacting with DynamoDB.
# Line 8, `task-nest-users` is the name of the DynamoDB table.
class DynamoDB:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = self.dynamodb.Table('task-nest-dynamodb')

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