#!/bin/bash

TABLE_NAME="task-nest-users"
REGION="us-east-1"

echo "Checking if DynamoDB table '$TABLE_NAME' exists..."
TABLE_STATUS=$(aws dynamodb describe-table --table-name "$TABLE_NAME" --region "$REGION" \
    --query "Table.TableStatus" --output text 2>/dev/null)

if [ "$TABLE_STATUS" == "None" ]; then
    echo "Table '$TABLE_NAME' does not exist. Nothing to delete."
    exit 0
fi

echo "Deleting table '$TABLE_NAME'..."
aws dynamodb delete-table --table-name "$TABLE_NAME" --region "$REGION"

echo "Waiting for the table '$TABLE_NAME' to be deleted..."
aws dynamodb wait table-not-exists --table-name "$TABLE_NAME" --region "$REGION"

echo "Table '$TABLE_NAME' successfully deleted."
