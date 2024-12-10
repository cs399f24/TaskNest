#!/bin/bash

BUCKET_NAME="task-nest-test-bucket-1"
APP_NAME="task-nest-app"
REGION="us-east-1"
BRANCH_NAME="main"

if [ -f ".env" ]; then
    rm -rf .env
fi

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

    if [ -f "./create_sns_topic.sh" ]; then
        ./create_sns_topic.sh || { echo "Failed to execute create_sns_topic.sh"; exit 1; }
    fi
else
    echo "Scripts directory not found!"
    exit 1
fi

./create_venv.sh || { echo "Failed to create virtual environment"; exit 1; }

if [ -f "./create_task_nest_api.py" ]; then
    ./.venv/bin/python ./create_task_nest_api.py || { echo "Failed to run create_task_nest_api.py"; exit 1; }
else
    echo "create_task_nest_api.py not found!"
    exit 1
fi

cd ..

if [ -f "package.json" ]; then
    npm install > /dev/null 2>&1 || { echo "Failed to run npm install"; exit 1; }
    npm run build > /dev/null 2>&1 || { echo "Failed to build the project"; exit 1; }
else
    echo "package.json not found! Make sure you are in the correct directory."
    exit 1
fi

if [ -d "./build" ]; then
    aws s3 cp ./build s3://$BUCKET_NAME/ --recursive > /dev/null 2>&1 || { echo "Failed to upload files to S3"; exit 1; }
    echo "Build successfully uploaded to S3 bucket: $BUCKET_NAME"
else
    echo "Build directory not found. Ensure 'npm run build' generates a 'build' folder."
    exit 1
fi

echo "Now you must create a amplify app by clicking create new app in amplify console,
select deploy without git provider, select the s3 bucket created for the app and name 
the branch name what ever you would like."
echo "DONE"
