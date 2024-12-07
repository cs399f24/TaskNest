#!/bin/bash

# Edit the bucket name
BUCKET_NAME="task-nest-test-bucket-1"

if ! aws s3api head-bucket --bucket "$BUCKET_NAME" 2>/dev/null; then
    echo "Bucket '$BUCKET_NAME' does not exist."
    exit 1
fi

aws s3 rm "s3://$BUCKET_NAME" --recursive
if [ $? -ne 0 ]; then
    echo "Failed to delete objects from bucket '$BUCKET_NAME'."
    exit 1
fi

echo "All objects successfully deleted from bucket '$BUCKET_NAME'."
