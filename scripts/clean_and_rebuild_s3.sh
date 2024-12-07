#!/bin/bash
BUCKET_NAME="task-nest-test-bucket-1"

./clean_s3_bucket.sh > /dev/null 2>&1

if [ ! -d "scripts" ]; then
    cd .. || { echo "Failed to change directory"; exit 1; }
fi

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