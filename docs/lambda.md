# AWS Lambda

## 1. Access AWS Lambda Console
- Go to the AWS Management Console
- Navigate to **Lambda** under the **Compute** section
- Click **Create function**

## 2. Create a New Function
1. **Choose an Authoring Method:**
   - Select **Author from scratch**
2. **Function Name:**
   - Enter a descriptive name (e.g., `addTaskLambda`, `deleteTaskLambda`, or `getTaskLambda`)
3. **Runtime:**
   - Choose **Python 3.13** (or the latest available)
4. **Permissions:**
   - Ensure the function has an **IAM role** with permissions to access DynamoDB

## 3. Write and Deploy Each Lambda Function

### Add Task Function
1. Paste the following code into the Lambda editor:
```python
import json
import boto3

def lambda_handler(event, context):
    print("Event Received: ", json.dumps(event))

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
            'body': json.dumps(["Request body is missing"])
        }

    if isinstance(event['body'], str):
        try:
            body = json.loads(event['body'])
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'body': json.dumps(["Invalid JSON format"])
            }
    else:
        body = event['body']

    db_connection = DynamoDB()

    user_id = body['user_id']
    task_description = body['description']
    task_time = body['time']
    
    if not all([task_description, task_time, user_id]):
        return {
            'statusCode': 400,
            'body': json.dumps(["Description, time, and user-id are required."])
        }

    task = {"description": task_description, "time": task_time}
    
    db_connection.add_task(user_id, task)

    return {
        'statusCode': 200,
        'body': "Added"
    }
```

2. **Deploy:**
   - Click **Deploy** to save changes

### Delete Task Function
1. Paste the following code:
```python
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
            print(tasks)
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
            'body': json.dumps({"error": "User ID and description are required"})
        }

    response = db_connection.delete_task(user_id, description)
    
    if "error" in response:
        return {
            'statusCode': 404,
            'body': json.dumps(response)
        }
    
    return {
        'statusCode': 200,
        'body': "Task deleted"
    }
```

2. **Deploy**

### Get Task Function
1. Paste the following code:
```python
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
                'Access-Control-Allow-Headers': 'Content-Type',
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
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps([])
        }
    
    tasks = response['Item'].get('tasks', [])
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        },
        'body': json.dumps(tasks)
    }
```

2. **Deploy**

