from urllib import request
import boto3
import time
import datetime
from dynamodb import DynamoDB

# Connect to DynamoDB
db_connection = DynamoDB()

data = request.get_json()
task_description = data.get('description')
task_time = data.get('time')  # This should be in a standard datetime format like "2024-11-25T10:00:00"
user_id = data.get('user_id')

# Parse task_time into a datetime object
task_datetime = datetime.datetime.fromisoformat(task_time)  # Assuming task_time is ISO 8601 formatted

# Create an SNS client
sns_client = boto3.client('sns', region_name='us-east-1')

# Create an SNS topic
response = sns_client.create_topic(Name='TaskNoti')
topic_arn = response['TopicArn']  
print(f"Created topic with ARN: {topic_arn}")

# Subscribe to the topic
def taskSubscribe(email):
    response = sns_client.subscribe(
        TopicArn=topic_arn,
        Protocol='email',  # Change to 'sms', 'http', or whatever form of notification you'd like to use
        Endpoint=email
    )
    sns_client.publish(    
        TopicArn=topic_arn,
        Message="Thank you for subscribing to TaskNest's push notifications system!",
        Subject='Thank you!'
    )
    print(f"Subscription ARN: {response['SubscriptionArn']}")


# Publish a reminder message
def taskReminder():
    # Calculate the delay until 1 hour after the task_time
    now = datetime.datetime.now()
    reminder_time = task_datetime + datetime.timedelta(hours=1)
    delay_seconds = (reminder_time - now).total_seconds()

    # Ensure we don't delay for a negative time
    if delay_seconds > 0:
        print(f"Waiting for {delay_seconds} seconds before sending the reminder.")
        time.sleep(delay_seconds)  # Wait until the reminder time
    else:
        print("The task reminder time has already passed; sending immediately.")

    # Send the reminder message
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=f"Reminder: It's been 1 hour since your task '{task_description}' was created!",
        Subject='Task Reminder'
    )
    print(f"Message ID: {response['MessageId']}")
