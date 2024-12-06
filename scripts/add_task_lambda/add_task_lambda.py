import json
import boto3
import datetime
import jwt
from botocore.exceptions import ClientError
import time

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
sns_client = boto3.client('sns', region_name='us-east-1')

TOPIC_ARN = 'arn:aws:sns:us-east-1:507920085099:TaskNoti'

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
            subscribe_to_sns_topic(email)
            # Send message immediately after subscribing
            send_task_notification(task_description)
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

def subscribe_to_sns_topic(email):
    sns_client.subscribe(
        TopicArn=TOPIC_ARN,
        Protocol='email',
        Endpoint=email
    )
    send_welcome_message()

def send_welcome_message():
    sns_client.publish(
        TopicArn=TOPIC_ARN,
        Message="Thank you for subscribing to TaskNest's push notifications system!",
        Subject='Welcome to TaskNest'
    )

def send_task_notification(task_description):
    sns_client.publish(
        TopicArn=TOPIC_ARN,
        Message=f"Task Reminder: {task_description}",
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
