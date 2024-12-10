# Creation and destruction of lambda functions
- files that create the three lambda functions: `create_add_task_lambda.sh`, `create_get_tasks_lambda.sh`, and `create_delete_task_lambda.sh`.
- batch file for creating lambda functions: `create_lambdas.sh`.
- files that destroy lambda functions: `destroy_add_task_lambda.sh`, `destroy_get_tasks_lambda.sh`, and `destroy_delete_task_lambda.sh`.
- batch file for the destruction of lambda files: `destroy_lambdas`.
## Creation
```bash
if aws lambda get-function --function-name add_task > /dev/null 2>&1; then
    echo "Function already exists"
    exit 1
fi
```
- Checking if the lambda function already exists.
```bash
ROLE=$(aws iam get-role --role-name labRole --query "Role.Arn" --output text)
if [ -z "$ROLE" ]; then
    echo "IAM role not found. Please create it with the correct permissions."
    exit 1
fi
```
- Looking for the role `labRole` if it exists store the arn in a variable named `ROLE`.
```bash
cd add_task_lambda
pip install pyjwt==2.10.1 -t . > /dev/null 2>&1

zip -r ../add_task_lambda.zip . > /dev/null 2>&1
```
- Changing working directory to the add_task_lambda folder (this is unique to the lambda function `add_task`)
- Installing `pyjwt` into the current directory.
    - The `-t` flag says to install into the following directory.
- Next zipping the folder which includes the lambda function along with its dependencies.
```bash
aws lambda create-function --function-name add_task \
    --runtime python3.9 \
    --role "$ROLE" \
    --zip-file fileb://../add_task_lambda.zip \
    --handler add_task_lambda.lambda_handler \
    > /dev/null 2>&1
```
- Description: Creates the Lambda function.
- Command: aws lambda create-function
- Flags:
`--function-name`: Specifies the name of the Lambda function.
`--runtime`: Specifies the runtime environment (Python 3.9 in this case).
`--role`: Specifies the ARN of the IAM role.
`--zip-file`: Points to the packaged code.
`--handler`: Specifies the handler function's entry point.
```bash
aws lambda wait function-active --function-name add_task
```
- Waiting for function to be active.
    - `--function-name` is specifying the function name. go figure
```bash
aws lambda publish-version --function-name add_task > /dev/null 2>&1

rm -rf ../add_task_lambda.zip
```
- Now we publish the function to AWS and cleanup the object.
## Destruction

```bash
if [ -z "$FUNCTION_EXISTS" ]; then
    echo "Lambda function '$FUNCTION_NAME' does not exist. Nothing to delete."
    exit 0
fi
```
- First we check if the function exists.
```bash
aws lambda delete-function --function-name "$FUNCTION_NAME" --region "$REGION"
```
- Then we delete the function.
```bash
if [ $? -eq 0 ]; then
    echo "Lambda function '$FUNCTION_NAME' successfully deleted."
else
    echo "Failed to delete Lambda function '$FUNCTION_NAME'. Please check for errors."
    exit 1
fi
```
- Notifying the user.