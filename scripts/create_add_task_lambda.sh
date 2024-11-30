if aws lambda get-function --function-name add_task > /dev/null 2>&1; then
    echo "Function already exists"
    exit 1
fi
ROLE=$(aws iam get-role --role-name labRole --query "Role.Arn" --output text)
if [ -z "$ROLE" ]; then
    echo "IAM role not found. Please create it with the correct permissions."
    exit 1
fi

zip objects/add_task_lambda.zip add_task_lambda.py > /dev/null 2>&1

aws lambda create-function --function-name add_task \
    --runtime python3.9 \
    --role "$ROLE" \
    --zip-file fileb://objects/add_task_lambda.zip \
    --handler add_task_lambda.lambda_handler \
    > /dev/null 2>&1

echo "Waiting for add_task function to be active..."
aws lambda wait function-active --function-name add_task
aws lambda publish-version --function-name add_task > /dev/null 2>&1
echo "Created add_task lambda function"
