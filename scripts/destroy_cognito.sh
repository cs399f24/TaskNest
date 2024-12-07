#!/bin/bash

USER_POOL_NAME="task-nest-user-pool"
USER_POOL_CLIENT_NAME="task-nest-client"

echo "Retrieving user pool ID for '$USER_POOL_NAME'..."
USER_POOL_ID=$(aws cognito-idp list-user-pools --max-results 60 \
    --query "UserPools[?Name=='$USER_POOL_NAME'].Id | [0]" --output text)

if [ "$USER_POOL_ID" == "None" ]; then
    echo "User pool '$USER_POOL_NAME' not found."
    exit 1
fi
echo "User pool ID: $USER_POOL_ID"

echo "Retrieving client ID for '$USER_POOL_CLIENT_NAME'..."
CLIENT_ID=$(aws cognito-idp list-user-pool-clients --user-pool-id "$USER_POOL_ID" \
    --query "UserPoolClients[?ClientName=='$USER_POOL_CLIENT_NAME'].ClientId | [0]" --output text)

if [ "$CLIENT_ID" == "None" ]; then
    echo "Client '$USER_POOL_CLIENT_NAME' not found in user pool '$USER_POOL_NAME'."
else
    echo "Client ID: $CLIENT_ID"
    echo "Deleting User Pool Client '$USER_POOL_CLIENT_NAME'..."
    aws cognito-idp delete-user-pool-client --user-pool-id "$USER_POOL_ID" --client-id "$CLIENT_ID"
    echo "User Pool Client deleted."
fi

echo "Deleting User Pool '$USER_POOL_NAME'..."
aws cognito-idp delete-user-pool --user-pool-id "$USER_POOL_ID"
echo "User Pool deleted."

echo "All operations completed successfully."
