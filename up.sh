#!/bin/bash

BUCKET_NAME="task-nest-test-bucket-1"

if ! aws s3 ls "s3://$BUCKET_NAME" > /dev/null 2>&1; then
    echo "Bucket '$BUCKET_NAME' does not exist. Please create it or specify an existing bucket."
    exit 1
fi

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
