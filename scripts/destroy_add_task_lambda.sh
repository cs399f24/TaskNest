#!/bin/bash

FUNCTION_NAME="add_task"
REGION="us-east-1"

echo "Checking if Lambda function '$FUNCTION_NAME' exists..."
FUNCTION_EXISTS=$(aws lambda get-function --function-name "$FUNCTION_NAME" --region "$REGION" 2>/dev/null)

if [ -z "$FUNCTION_EXISTS" ]; then
    echo "Lambda function '$FUNCTION_NAME' does not exist. Nothing to delete."
    exit 0
fi

echo "Deleting Lambda function '$FUNCTION_NAME'..."
aws lambda delete-function --function-name "$FUNCTION_NAME" --region "$REGION"

if [ $? -eq 0 ]; then
    echo "Lambda function '$FUNCTION_NAME' successfully deleted."
else
    echo "Failed to delete Lambda function '$FUNCTION_NAME'. Please check for errors."
    exit 1
fi
