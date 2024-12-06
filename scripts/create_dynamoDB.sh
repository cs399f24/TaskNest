#!/bin/bash

TABLE_NAME="task-nest-users"
PARTITION_KEY="user-id"
ATTRIBUTE_TYPE="S"
PROVISIONED_READ_UNITS=5
PROVISIONED_WRITE_UNITS=5

echo "Checking if table '$TABLE_NAME' exists..."
EXISTING_TABLES=$(aws dynamodb list-tables --query "TableNames" --output text)

if echo "$EXISTING_TABLES" | grep -qw "$TABLE_NAME"; then
    echo "Table '$TABLE_NAME' already exists. No action taken."
else
    echo "Table '$TABLE_NAME' does not exist. Creating the table..."

    aws dynamodb create-table \
        --table-name "$TABLE_NAME" \
        --attribute-definitions AttributeName="$PARTITION_KEY",AttributeType="$ATTRIBUTE_TYPE" \
        --key-schema AttributeName="$PARTITION_KEY",KeyType=HASH \
        --provisioned-throughput ReadCapacityUnits="$PROVISIONED_READ_UNITS",WriteCapacityUnits="$PROVISIONED_WRITE_UNITS"

    if [ $? -eq 0 ]; then
        echo "DynamoDB table '$TABLE_NAME' created successfully."
    else
        echo "Failed to create DynamoDB table '$TABLE_NAME'."
    fi
fi
