API_ID=$(aws apigateway get-rest-apis --query "items[?name=='task_nest_api'].id" --output text)
if [ -n "$API_ID" ]; then
    aws apigateway delete-rest-api --rest-api-id  $API_ID;
    echo "DONE"
else
    echo "API does not exist"
fi