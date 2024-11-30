if aws lambda get-function --function-name delete > /dev/null 2>&1; then
    echo "Function already exists"
    exit 1
fi  