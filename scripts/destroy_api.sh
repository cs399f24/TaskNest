API_IDS=$(aws apigateway get-rest-apis --query "items[?name=='task_nest_rest_api_1'].id" --output text)
echo $API_IDS
if [ "$API_IDS" != "None" ]; then
    for API_ID in $API_IDS; do
        aws apigateway delete-rest-api --rest-api-id "$API_ID"
        echo "API with ID $API_ID deleted"
    done
else
    echo "No APIs named 'task_nest_rest_api_1' found"
fi
