import boto3
import time

# Create an SNS client
sns_client = boto3.client('sns', region_name='us-east-1')

# Create an SNS topic
response = sns_client.create_topic(Name='TaskNoti')
topic_arn = response['TopicArn']  
print(f"Created topic with ARN: {topic_arn}")

# # Test subcribe function
# def taskSubscribe(email):
#     response = sns_client.subscribe(
#         TopicArn=topic_arn,
#         Protocol='email',  # Change to 'sms', 'http', etc.
#         Endpoint= 'youremail@example' #Change to test email
#     )

# Subscribe to the topic
def taskSubscribe(email):
    response = sns_client.subscribe(
        TopicArn=topic_arn,
        Protocol='email',  # Change to 'sms', 'http', etc.
        Endpoint=email
    )
    response = sns_client.publish(    
        TopicArn=topic_arn,
        Message="Thank you for subscribing to TaskNest's push notifications system!",
        Subject='Thank you!'
    )
    print(f"Subscription ARN: {response['SubscriptionArn']}")


# Publish a reminder message
def taskReminder():
    time.sleep(20) #send reminder X minutes after task is made
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message="It has been an hour since you've created your task!",
        Subject='Task Reminder'
    )
    print(f"Message ID: {response['MessageId']}")



