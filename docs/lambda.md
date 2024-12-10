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
import datetime
import jwt
from botocore.exceptions import ClientError
import time

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
sns_client = boto3.client('sns', region_name='us-east-1')

TOPIC_NAME = "task-notification"

def lambda_handler(event, context):
    start_time = time.time()

    if 'body' not in event or not event['body']:
        return respond_with_error("Request body is missing")

    body = parse_event_body(event)

    if body is None:
        return respond_with_error("Invalid JSON format")

    task_description = body.get('description')
    task_time = body.get('time')
    user_id = body.get("user_id")
    id_token = body.get("idToken")

    if not all([task_description, task_time, user_id, id_token]):
        return respond_with_error("Description, time, user_id, and idToken are required.")

    task = {"description": task_description, "time": task_time}

    task_list = add_task_to_dynamodb(user_id, task)

    email = decode_id_token(id_token)

    if email:
        try:
            topic_arn = get_topic_arn_by_name(TOPIC_NAME)
            if topic_arn and not is_already_subscribed(email, topic_arn):
                subscribe_to_sns_topic(email, topic_arn)
            send_task_notification(task_description, topic_arn)
        except ClientError as e:
            return respond_with_error(f"Error subscribing email to SNS topic: {str(e)}")
    else:
        return respond_with_error("Invalid or missing email in idToken.")

    print(f"Total execution time: {time.time() - start_time:.2f} seconds")

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps(task_list, default=str)
    }

def add_task_to_dynamodb(user_id, task):
    table = dynamodb.Table('task-nest-users')
    try:
        response = table.update_item(
            Key={'user-id': user_id},
            UpdateExpression="SET tasks = list_append(if_not_exists(tasks, :empty_list), :new_task)",
            ExpressionAttributeValues={':new_task': [task], ':empty_list': []},
            ReturnValues="UPDATED_NEW"
        )
        return response['Attributes'].get('tasks', [])
    except ClientError as e:
        print(f"Error adding task: {e}")
        return []

def parse_event_body(event):
    if isinstance(event['body'], str):
        try:
            return json.loads(event['body'])
        except json.JSONDecodeError:
            return None
    return event['body']

def respond_with_error(message):
    return {
        'statusCode': 400,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps([message])
    }

def get_topic_arn_by_name(topic_name):
    response = sns_client.list_topics()
    topics = response.get('Topics', [])

    for topic in topics:
        if topic_name in topic['TopicArn']:
            return topic['TopicArn']
    return None

def is_already_subscribed(email, topic_arn):
    response = sns_client.list_subscriptions_by_topic(TopicArn=topic_arn)
    for subscription in response.get('Subscriptions', []):
        if subscription['Endpoint'] == email and subscription['Protocol'] == 'email':
            return True
    return False

def subscribe_to_sns_topic(email, topic_arn):
    sns_client.subscribe(
        TopicArn=topic_arn,
        Protocol='email',
        Endpoint=email
    )
    send_welcome_message(topic_arn)

def send_welcome_message(topic_arn):
    sns_client.publish(
        TopicArn=topic_arn,
        Message="Thank you for subscribing to TaskNest's push notifications system!",
        Subject='Welcome to TaskNest'
    )

def send_task_notification(task_description, topic_arn):
    sns_client.publish(
        TopicArn=topic_arn,
        Message=f"Task Added: {task_description}",
        Subject="New Task Added"
    )
    print(f"Task notification sent: {task_description}")

def decode_id_token(id_token):
    try:
        decoded = jwt.decode(id_token, options={"verify_signature": False})
        return decoded.get('email')
    except Exception as e:
        print(f"Error decoding idToken: {e}")
        return None
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
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
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
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                'Access-Control-Allow-Methods': 'OPTIONS,DELETE',
            }
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps({"message": "Task deleted successfully"}),
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Allow-Methods': 'OPTIONS,DELETE',
        }
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
```

2. **Deploy**

