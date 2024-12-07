#!/bin/bash
# WARNING: DESTROYS... EVERYTHING (It's in the name...)

read -p "Are you sure you want to DESTROY... EVERYTHING? This action cannot be undone. (yes/no): " CONFIRM
if [ "$CONFIRM" != "yes" ]; then
    echo "Table deletion aborted."
    exit 0
fi

if [ ! -d "scripts" ]; then
    echo "Please run this script from the root directory of the project."
    exit 1
else
    cd scripts
fi

./clean_s3_bucket.sh > /dev/null 2>&1
echo "DESTROYED... S3 BUCKET CONTENTS"
./destroy_dynamodb.sh > /dev/null 2>&1
echo "DESTROYED... DYNAMODB TABLE"
./destroy_api.sh > /dev/null 2>&1
echo "DESTROYED... API GATEWAY"
./destroy_cognito.sh > /dev/null 2>&1
echo "DESTROYED... COGNITO USER POOL"
./destroy_lambdas.sh > /dev/null 2>&1
echo "DESTROYED... LAMBDAS"

echo "DESTROYED... EVERYTHING"