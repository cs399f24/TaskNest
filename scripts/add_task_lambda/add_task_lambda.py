import json
import boto3
import time
from botocore.exceptions import ClientError
import jwt

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
sns_client = boto3.client('sns', region_name='us-east-1')

def create_or_get_topic(topic_name):
    try:
        response = sns_client.create_topic(Name=topic_name)
        return response['TopicArn']
    except ClientError as e:
        print(f"Error creating or retrieving SNS topic: {e}")
        return None

def subscribe_email_to_topic(email, topic_arn):
    try:
        response = sns_client.list_subscriptions_by_topic(TopicArn=topic_arn)
        existing_emails = [sub['Endpoint'] for sub in response.get('Subscriptions', []) if sub['Protocol'] == 'email']

        if email not in existing_emails:
            sns_client.subscribe(TopicArn=topic_arn, Protocol='email', Endpoint=email)
            sns_client.publish(
                TopicArn=topic_arn,
                Message="Welcome to your personalized TaskNest notification system!",
                Subject="Welcome to TaskNest"
            )
    except ClientError as e:
        print(f"Error subscribing email to SNS topic: {e}")

def send_task_notification(task_description, topic_arn):
    try:
        sns_client.publish(
            TopicArn=topic_arn,
            Message=f"Task Added: {task_description}",
            Subject="New Task Added"
        )
    except ClientError as e:
        print(f"Error sending task notification: {e}")

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

def decode_id_token(id_token):
    try:
        decoded = jwt.decode(id_token, options={"verify_signature": False})
        return decoded.get('email')
    except Exception as e:
        print(f"Error decoding idToken: {e}")
        return None

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
        topic_name = f"task-notification-{user_id}"
        topic_arn = create_or_get_topic(topic_name)

        if topic_arn:
            subscribe_email_to_topic(email, topic_arn)

            send_task_notification(task_description, topic_arn)
        else:
            return respond_with_error("Failed to create or retrieve SNS topic.")
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
