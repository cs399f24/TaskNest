import boto3
import datetime
import time
import jwt  # For decoding JWTs

# DynamoDB helper class
class DynamoDB:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = self.dynamodb.Table('task-nest-users')

    def get_tasks(self, user_id):
        """Retrieve tasks for a specific user from DynamoDB."""
        response = self.table.get_item(Key={'user-id': user_id})
        if 'Item' not in response:
            return []
        
        return response['Item'].get('tasks', [])

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

# Decode the idToken to extract the user's email
def decode_id_token(id_token):
    """Decode the idToken to extract the user's email."""
    try:
        decoded = jwt.decode(id_token, options={"verify_signature": False})
        return decoded.get('email')
    except Exception as e:
        print(f"Error decoding idToken: {e}")
        return None

# Subscribe to an SNS topic
def task_subscribe(email, topic_arn, sns_client):
    """Subscribe an email to the SNS topic."""
    try:
        response = sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol='email',
            Endpoint=email
        )
        sns_client.publish(
            TopicArn=topic_arn,
            Message="Thank you for subscribing to TaskNest's push notifications system!",
            Subject='Thank you!'
        )
        print(f"Subscription ARN: {response['SubscriptionArn']}")
    except Exception as e:
        print(f"Error subscribing email: {e}")

# Publish a reminder message
def task_reminder(task_datetime, task_description, topic_arn, sns_client):
    """Send a task reminder email."""
    now = datetime.datetime.now()
    reminder_time = task_datetime + datetime.timedelta(minutes=1)
    delay_seconds = (reminder_time - now).total_seconds()

    # Ensure we don't delay for a negative time
    if delay_seconds > 0:
        print(f"Waiting for {delay_seconds} seconds before sending the reminder.")
        time.sleep(delay_seconds)  # Wait until the reminder time

    try:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=f"Reminder: It's been 1 hour since your task '{task_description}' was created!",
            Subject='Task Reminder'
        )
        print(f"Message ID: {response['MessageId']}")
    except Exception as e:
        print(f"Error sending reminder: {e}")

# Lambda handler
def lambda_handler(event, context):
    # Parse incoming data
    data = event
    task_description = data.get('description')
    task_time = data.get('time')  # ISO 8601 format: "YYYY-MM-DDTHH:MM:SS"
    id_token = data.get('idToken')  # Retrieve the idToken for extracting email
    user_id = data.get('user_id')

    # Initialize resources
    db_connection = DynamoDB()
    sns_client = boto3.client('sns', region_name='us-east-1')

    # Decode the idToken to extract email
    email = decode_id_token(id_token)

    # Validate task time
    try:
        task_datetime = datetime.datetime.fromisoformat(task_time)
    except ValueError as e:
        print(f"Invalid task time format: {e}")
        return {"error": "Invalid task time format."}

    # Create an SNS topic
    topic_response = sns_client.create_topic(Name='TaskNoti')
    topic_arn = topic_response['TopicArn']
    print(f"Created topic with ARN: {topic_arn}")

    # Subscribe the user if email exists
    if email:
        task_subscribe(email, topic_arn, sns_client)
    else:
        print("Email not found in idToken.")
        return {"error": "Invalid or missing email in idToken."}

    # Add the task to DynamoDB
    task = {
        "description": task_description,
        "time": task_time,
    }
    db_connection.add_task(user_id, task)

    # Set up the task reminder
    task_reminder(task_datetime, task_description, topic_arn, sns_client)

    return {"statusCode": 200, "body": "Task created and reminder set successfully."}
