from urllib import request
import boto3
import time
import datetime
from dynamodb import DynamoDB
import jwt  # Add to handle decoding JWTs

# Connect to DynamoDB
db_connection = DynamoDB()

# Parse incoming data
data = request.get_json()
task_description = data.get('description')
task_time = data.get('time')  # This should be in a standard datetime format like "2024-11-25T10:00:00"
id_token = data.get('idToken')  # Retrieve the idToken for extracting email
user_id = data.get('user_id')

# Decode the idToken to extract the user's email
def decode_id_token(id_token):
    """Decode the idToken to extract the user's email."""
    try:
        decoded = jwt.decode(id_token, options={"verify_signature": False})
        return decoded.get('email')
    except Exception as e:
        print(f"Error decoding idToken: {e}")
        return None

# Extract email from idToken
email = decode_id_token(id_token)

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
    """Subscribe an email to the SNS topic."""
    try:
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
    except Exception as e:
        print(f"Error subscribing email: {e}")

# Publish a reminder message
def taskReminder():
    """Send a task reminder email."""
    now = datetime.datetime.now()
    reminder_time = task_datetime + datetime.timedelta(minutes=1)
    delay_seconds = (reminder_time - now).total_seconds()

    # Ensure we don't delay for a negative time
    if delay_seconds > 0:
        print(f"Waiting for {delay_seconds} seconds before sending the reminder.")
        time.sleep(delay_seconds)  # Wait until the reminder time
    else:
        print("The task reminder time has already passed; sending immediately.")

    # Send the reminder message
    try:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=f"Reminder: It's been 1 hour since your task '{task_description}' was created!",
            Subject='Task Reminder'
        )
        print(f"Message ID: {response['MessageId']}")
    except Exception as e:
        print(f"Error sending reminder: {e}")

# Subscribe the user if email exists
if email:
    taskSubscribe(email)
else:
    print("Email not found in idToken.")
