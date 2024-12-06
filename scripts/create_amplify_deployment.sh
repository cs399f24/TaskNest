#!/bin/bash

AMPLIFY_APP_NAME="TaskNestApp"
S3_BUCKET_NAME="task-nest-test-bucket-1"
REGION="us-east-1"

AMPLIFY_APP_ID=$(aws amplify create-app \
  --name "$AMPLIFY_APP_NAME" \
  --region "$REGION" \
  --output json \
  | jq -r '.app.appId')

if [ -z "$AMPLIFY_APP_ID" ]; then
  echo "Failed to create Amplify app."
  exit 1
fi
echo "Amplify app created successfully with ID: $AMPLIFY_APP_ID"

HOSTING_RESOURCE=$(aws amplify create-backend-environment \
  --app-id "$AMPLIFY_APP_ID" \
  --environment-name "dev" \
  --region "$REGION" \
  --output json \
  | jq -r '.backendEnvironment')

if [ -z "$HOSTING_RESOURCE" ]; then
  echo "Failed to configure the hosting resource."
  exit 1
fi
echo "Hosting resource configured successfully."

aws amplify update-app \
  --app-id "$AMPLIFY_APP_ID" \
  --region "$REGION" \
  --custom-rules '[{"source": "/<*>", "target": "/index.html", "status": "200"}]' \
  --output json

echo "S3 bucket configured for Amplify hosting."

echo "Amplify app setup complete!"
echo "Amplify App ID: $AMPLIFY_APP_ID"
