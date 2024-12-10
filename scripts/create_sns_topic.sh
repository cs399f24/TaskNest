#!/bin/bash

TOPIC_NAME="task-notification"
REGION="us-east-1"

echo "Creating SNS Topic: $TOPIC_NAME in region: $REGION"
aws sns create-topic --name "$TOPIC_NAME" --region "$REGION" > /dev/null 2>&1

if [ $? -eq 0 ]; then
  echo "SNS Topic '$TOPIC_NAME' created successfully."
else
  echo "Failed to create SNS Topic."
fi
