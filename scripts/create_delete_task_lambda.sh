if aws lambda get-function --function-name delete_task > /dev/null 2>&1; then
    echo "Function already exists"
    exit 1
fi

ROLE=$(aws iam get-role --role-name labRole --query "Role.Arn" --output text)
if [ -z "$ROLE" ]; then
    echo "IAM role not found. Please create it with the correct permissions."
    exit 1
fi

zip objects/delete_task_lambda.zip delete_task_lambda.py > /dev/null 2>&1

aws lambda create-function --function-name delete_task \
    --runtime python3.9 \
    --role "$ROLE" \
    --zip-file fileb://objects/delete_task_lambda.zip \
    --handler delete_task_lambda.lambda_handler \
    > /dev/null 2>&1

echo "Waiting for delete_task function to be active..."
aws lambda wait function-active --function-name delete_task
aws lambda publish-version --function-name delete_task > /dev/null 2>&1
rm -rf objects/delete_task_lambda.zip
echo "Created delete_task lambda function"
