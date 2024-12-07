#!/bin/bash

# Edit to your specifications
BUCKET_NAME="sliztastico"
REGION="us-east-1"
INDEX_FILE_PATH="index.html"

if aws s3api head-bucket --bucket "$BUCKET_NAME" 2>/dev/null; then
    echo "Bucket '$BUCKET_NAME' already exists."
else
    aws s3api create-bucket --bucket "$BUCKET_NAME" --region "$REGION"
    if [ $? -ne 0 ]; then
        echo "Failed to create bucket '$BUCKET_NAME'. Exiting."
        exit 1
    fi
    echo "Bucket '$BUCKET_NAME' created."
fi

echo "Static website setup complete."
echo "Access your site at: http://$BUCKET_NAME.s3-website-$REGION.amazonaws.com"
