#!/bin/bash

 # Change to your preferred region, bucket name, and Amplify app name
BUCKET_NAME="task-nest-test-bucket-1"
AMPLIFY_APP_NAME="task-nest-app"
REGION="us-east-1"

# Ensure the S3 bucket exists
if ! aws s3 ls "s3://$BUCKET_NAME" > /dev/null 2>&1; then
    echo "Bucket '$BUCKET_NAME' does not exist. Please create it or specify an existing bucket."
    exit 1
fi

# Run DynamoDB and Lambda setup scripts
if [ -d "scripts" ]; then
    cd scripts
    if [ -f "./create_dynamoDB.sh" ]; then
        ./create_dynamoDB.sh || { echo "Failed to execute create_dynamoDB.sh"; exit 1; }
    fi

    if [ -f "./create_lambdas.sh" ]; then
        ./create_lambdas.sh || { echo "Failed to execute create_lambdas.sh"; exit 1; }
    fi
    cd ..
else
    echo "Scripts directory not found!"
    exit 1
fi

# Create virtual environment and install dependencies
python3 -m venv .venv || { echo "Failed to create virtual environment"; exit 1; }
./.venv/bin/pip install boto3 awscli || { echo "Failed to install Python dependencies"; exit 1; }

# Run the Python script to create the API
if [ -f "./scripts/create_task_nest_api.py" ]; then
    ./.venv/bin/python ./scripts/create_task_nest_api.py || { echo "Failed to run create_task_nest_api.py"; exit 1; }
else
    echo "create_task_nest_api.py not found!"
    exit 1
fi

# Build the frontend
if [ -f "package.json" ]; then
    npm install || { echo "Failed to run npm install"; exit 1; }
    npm run build || { echo "Failed to build the project"; exit 1; }
else
    echo "package.json not found! Make sure you are in the correct directory."
    exit 1
fi

# Upload to S3 bucket
if [ -d "./build" ]; then
    aws s3 cp ./build s3://$BUCKET_NAME/ --recursive || { echo "Failed to upload files to S3"; exit 1; }
    echo "Build successfully uploaded to S3 bucket: $BUCKET_NAME"
else
    echo "Build directory not found. Ensure 'npm run build' generates a 'build' folder."
    exit 1
fi

# Initialize Amplify App
echo "Initializing Amplify app..."
if ! command -v amplify &> /dev/null; then
    echo "Amplify CLI not found. Install it using 'npm install -g @aws-amplify/cli'."
    exit 1
fi

amplify init --app "$AMPLIFY_APP_NAME" --envName prod --region "$REGION" --yes || {
    echo "Failed to initialize Amplify app.";
    exit 1;
}

# Add hosting to Amplify
echo "Adding Amplify hosting..."
amplify add hosting \
    --bucketName "$BUCKET_NAME" \
    --indexDocument "index.html" \
    --errorDocument "index.html" \
    --yes || {
    echo "Failed to add Amplify hosting.";
    exit 1;
}

# Publish the Amplify app
echo "Publishing Amplify app..."
amplify publish --yes || {
    echo "Failed to publish Amplify app.";
    exit 1;
}

echo "Amplify app created and published successfully!"
