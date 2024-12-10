#!/bin/bash

TOPIC_NAME="task-notification"
REGION="us-east-1"

TOPIC_ARN=$(aws sns list-topics --region "$REGION" --query "Topics[?contains(TopicArn, '$TOPIC_NAME')].TopicArn" --output text)

if [ "$TOPIC_ARN" != "None" ]; then
  echo "Found SNS Topic: $TOPIC_ARN"
  
  aws sns delete-topic --topic-arn "$TOPIC_ARN" --region "$REGION"
  
  if [ $? -eq 0 ]; then
    echo "SNS Topic '$TOPIC_ARN' deleted successfully."
  else
    echo "Failed to delete SNS Topic."
  fi
else
  echo "SNS Topic '$TOPIC_NAME' not found."
fi
