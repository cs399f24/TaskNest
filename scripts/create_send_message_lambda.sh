if aws lambda get-function --function-name send_message > /dev/null 2>&1; then
    echo "Function already exists"
    exit 1
fi

ROLE=$(aws iam get-role --role-name labRole --query "Role.Arn" --output text)
if [ -z "$ROLE" ]; then
    echo "IAM role not found. Please create it with the correct permissions."
    exit 1
fi

zip objects/send_message_lambda.zip send_message_lambda.py > /dev/null 2>&1

aws lambda create-function --function-name send_message \
    --runtime python3.9 \
    --role "$ROLE" \
    --zip-file fileb://objects/send_message_lambda.zip \
    --handler send_message_lambda.lambda_handler \
    > /dev/null 2>&1

echo "Waiting for get_tasks function to be active..."
aws lambda wait function-active --function-name get_tasks
aws lambda publish-version --function-name get_tasks > /dev/null 2>&1
rm -rf objects/send_message_lambda.zip
echo "Created send_message lambda function"
