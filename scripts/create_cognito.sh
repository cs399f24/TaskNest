#!/bin/bash

USER_POOL_NAME="task-nest-user-pool"
USER_POOL_CLIENT_NAME="task-nest-client"
REGION="us-east-1"

echo "Checking for existing user pool '$USER_POOL_NAME'..."
USER_POOL_ID=$(aws cognito-idp list-user-pools --max-results 60 --region "$REGION" \
    --query "UserPools[?Name=='$USER_POOL_NAME'].Id | [0]" --output text)

if [ "$USER_POOL_ID" == "None" ]; then
    echo "User pool '$USER_POOL_NAME' not found. Creating a new user pool..."
    USER_POOL_ID=$(aws cognito-idp create-user-pool \
        --pool-name "$USER_POOL_NAME" \
        --policies '{"PasswordPolicy": {"MinimumLength": 8, "RequireUppercase": true, "RequireLowercase": true, "RequireNumbers": true, "RequireSymbols": true}}' \
        --auto-verified-attributes '["email"]' \
        --mfa-configuration "OFF" \
        --region "$REGION" \
        --query "UserPool.Id" --output text)
    echo "User pool created with ID: $USER_POOL_ID"
else
    echo "User pool '$USER_POOL_NAME' found with ID: $USER_POOL_ID"
fi

echo "Checking for existing user pool client '$USER_POOL_CLIENT_NAME'..."
CLIENT_ID=$(aws cognito-idp list-user-pool-clients --user-pool-id "$USER_POOL_ID" --region "$REGION" \
    --query "UserPoolClients[?ClientName=='$USER_POOL_CLIENT_NAME'].ClientId | [0]" --output text)

if [ "$CLIENT_ID" == "None" ]; then
    echo "User pool client '$USER_POOL_CLIENT_NAME' not found. Creating a new client..."
    CLIENT_ID=$(aws cognito-idp create-user-pool-client \
        --user-pool-id "$USER_POOL_ID" \
        --client-name "$USER_POOL_CLIENT_NAME" \
        --generate-secret false \
        --explicit-auth-flows '["ALLOW_USER_PASSWORD_AUTH", "ALLOW_REFRESH_TOKEN_AUTH", "ALLOW_USER_SRP_AUTH"]' \
        --read-attributes '["email"]' \
        --refresh-token-validity 30 \
        --region "$REGION" \
        --query "UserPoolClient.ClientId" --output text)
    echo "User pool client created with ID: $CLIENT_ID"
else
    echo "User pool client '$USER_POOL_CLIENT_NAME' found with ID: $CLIENT_ID"
fi

echo "Cognito User Pool and Client setup completed successfully."
