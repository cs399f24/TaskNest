import json
import boto3
import datetime

sns_client = boto3.client('sns')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('task-nest-users')

def lambda_handler(event, context):
    """
    Lambda function to handle task reminders by sending a notification via SNS.
    """
    try:
        # Parse the event to get task details
        task_description = event.get('task_description')
        task_time = event.get('task_time')  # ISO 8601 formatted string

        if not task_description or not task_time:
            return {
                'statusCode': 400,
                'body': json.dumps('Missing task description or task time')
            }

        try:
            task_datetime = datetime.datetime.fromisoformat(task_time)
        except ValueError as e:
            return {
                'statusCode': 400,
                'body': json.dumps(f"Invalid task time format: {e}")
            }

        user_id = event.get('user_id')

        if not user_id:
            return {
                'statusCode': 400,
                'body': json.dumps('User ID is missing')
            }

        response = table.get_item(Key={'user-id': user_id})
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps(f"User with ID {user_id} not found")
            }

        user_data = response['Item']
        email = user_data.get('email')

        if not email:
            return {
                'statusCode': 404,
                'body': json.dumps(f"Email not found for user {user_id}")
            }

        topic_name = 'TaskReminderTopic'
        topic_response = sns_client.create_topic(Name=topic_name)
        topic_arn = topic_response['TopicArn']

        subscriptions = sns_client.list_subscriptions_by_topic(TopicArn=topic_arn)
        is_subscribed = any(sub['Endpoint'] == email for sub in subscriptions['Subscriptions'])

        if not is_subscribed:
            sns_client.subscribe(
                TopicArn=topic_arn,
                Protocol='email',
                Endpoint=email
            )
            print(f"Subscribed {email} to the topic")

        reminder_message = f"Reminder: Your task '{task_description}' is scheduled for {task_datetime}."
        subject = "Task Reminder"

        sns_client.publish(
            TopicArn=topic_arn,
            Message=reminder_message,
            Subject=subject
        )

        return {
            'statusCode': 200,
            'body': json.dumps(f"Task reminder sent to {email}")
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error sending task reminder: {str(e)}")
        }
