import boto3
import json
import sys

client = boto3.client('apigateway', region_name='us-east-1')

response = client.get_rest_apis()
apis = response.get('items', [])

for api in apis:
    if api.get('name') == 'task_nest_rest_api_1':
        print('API already exists')
        sys.exit(0)

response = client.create_rest_api(
    name='task_nest_rest_api_1',
    description='API to manage tasks.',
    endpointConfiguration={
        'types': [
            'REGIONAL',
        ]
    }
)
api_id = response["id"]

resources = client.get_resources(restApiId=api_id)
root_id = [resource for resource in resources["items"] if resource["path"] == "/"][0]["id"]

cognito_client = boto3.client('cognito-idp', region_name='us-east-1')
api_gateway_client = boto3.client('apigateway', region_name='us-east-1')
sts_client = boto3.client('sts')

account_id = sts_client.get_caller_identity()['Account']
region = 'us-east-1'

response = cognito_client.list_user_pools(MaxResults=10)
user_pools = response.get('UserPools', [])

if not user_pools:
    raise Exception("No user pools found in this account.")

user_pool_id = next(pool['Id'] for pool in user_pools if pool['Name'] == 'task-nest-user-pool')

if user_pool_id is None:
    user_pool = cognito_client.create_user_pool(
        PoolName='task-nest-user-pool',
        Policies={
            'PasswordPolicy': {
                'MinimumLength': 8,
                'RequireUppercase': True,
                'RequireLowercase': True,
                'RequireNumbers': True,
                'RequireSymbols': True
            }
        }
    )
    user_pool_id = user_pool['UserPool']['Id']
    print(f"User pool created with ID: {user_pool_id}")

cognito_user_pool_arn = f"arn:aws:cognito-idp:{region}:{account_id}:userpool/{user_pool_id}"

authorizer = api_gateway_client.create_authorizer(
    restApiId=api_id,
    name='task_nest_authorizer',
    type='COGNITO_USER_POOLS',
    providerARNs=[cognito_user_pool_arn],
    identitySource='method.request.header.Authorization'
)

authorizer_id = authorizer['id']
print(f"Authorizer created with ID: {authorizer_id}")

# Create the /tasks resource
tasks = client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='tasks'
)
tasks_resource_id = tasks["id"]

tasks_method = client.put_method(
    restApiId=api_id,
    resourceId=tasks_resource_id,
    httpMethod='GET',
    authorizationType='COGNITO_USER_POOLS',
    authorizerId=authorizer_id,
    requestParameters={
        'method.request.querystring.user_id': True
    }
)

tasks_response = client.put_method_response(
    restApiId=api_id,
    resourceId=tasks_resource_id,
    httpMethod='GET',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': True,
        'method.response.header.Access-Control-Allow-Origin': True,
        'method.response.header.Access-Control-Allow-Methods': True
    },
    responseModels={
        'application/json': 'Empty'
    }
)

lambda_client = boto3.client('lambda', region_name='us-east-1')
lambda_arn = lambda_client.get_function(FunctionName='get_tasks')['Configuration']['FunctionArn']
uri = f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'

if lambda_arn is None:
    raise Exception("No Lambda function found, make sure lambda function get_tasks exists")

iam_client = boto3.client('iam')
lab_role = iam_client.get_role(RoleName='LabRole')['Role']['Arn']

tasks_integration = client.put_integration(
    restApiId=api_id,
    resourceId=tasks_resource_id,
    httpMethod='GET',
    credentials=lab_role,
    integrationHttpMethod='POST',
    uri=uri,
    type='AWS',
    requestTemplates={
        "application/json": '{ "queryStringParameters": { "user_id": "$input.params(\'user_id\')" } }'
    }
)

tasks_integration_response = client.put_integration_response(
    restApiId=api_id,
    resourceId=tasks_resource_id,
    httpMethod='GET',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': '\'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token\'',
        'method.response.header.Access-Control-Allow-Methods': '\'GET,OPTIONS\'',
        'method.response.header.Access-Control-Allow-Origin': '\'*\'' 
    }
)

# Now /tasks preflight
tasks_method = client.put_method(
    restApiId=api_id,
    resourceId=tasks_resource_id,
    httpMethod='OPTIONS',
    authorizationType='NONE'
)

tasks_response = client.put_method_response(
    restApiId=api_id,
    resourceId=tasks_resource_id,
    httpMethod='OPTIONS',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': True,
        'method.response.header.Access-Control-Allow-Origin': True,
        'method.response.header.Access-Control-Allow-Methods': True
    },
    responseModels={
        'application/json': 'Empty'
    }
)

tasks_integration = client.put_integration(
    restApiId=api_id,
    resourceId=tasks_resource_id,
    httpMethod='OPTIONS',
    type='MOCK',
    requestTemplates={
        'application/json': '{"statusCode": 200}'
    }
)

tasks_integration_response = client.put_integration_response(
    restApiId=api_id,
    resourceId=tasks_resource_id,
    httpMethod='OPTIONS',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': '\'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token\'',
        'method.response.header.Access-Control-Allow-Methods': '\'GET,OPTIONS\'',
        'method.response.header.Access-Control-Allow-Origin': '\'*\'' 
    }
)

# Create the /add resource
add_resource = client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='add'
)
add_resource_id = add_resource["id"]

add_method = client.put_method(
    restApiId=api_id,
    resourceId=add_resource_id,
    httpMethod='POST',
    authorizationType='COGNITO_USER_POOLS',
    authorizerId=authorizer_id
)

add_response = client.put_method_response(
    restApiId=api_id,
    resourceId=add_resource_id,
    httpMethod='POST',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': True,
        'method.response.header.Access-Control-Allow-Origin': True,
        'method.response.header.Access-Control-Allow-Methods': True
    },
    responseModels={
        'application/json': 'Empty'
    }
)

lambda_arn = lambda_client.get_function(FunctionName='add_task')['Configuration']['FunctionArn']
uri = f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'

if lambda_arn is None:
    raise Exception("No Lambda function found, make sure lambda function add_task exists")

add_integration = client.put_integration(
    restApiId=api_id,
    resourceId=add_resource_id,
    httpMethod='POST',
    credentials=lab_role,
    integrationHttpMethod='POST',
    type='AWS',
    uri=uri,
    requestTemplates={
        "application/json": '{ "body": $input.json("$") }'
    }
)

add_integration_response = client.put_integration_response(
    restApiId=api_id,
    resourceId=add_resource_id,
    httpMethod='POST',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': '\'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token\'',
        'method.response.header.Access-Control-Allow-Methods': '\'POST,OPTIONS\'',
        'method.response.header.Access-Control-Allow-Origin': '\'*\'' 
    }
)

# Now /add preflight
add_method = client.put_method(
    restApiId=api_id,
    resourceId=add_resource_id,
    httpMethod='OPTIONS',
    authorizationType='NONE'
)

add_response = client.put_method_response(
    restApiId=api_id,
    resourceId=add_resource_id,
    httpMethod='OPTIONS',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': True,
        'method.response.header.Access-Control-Allow-Origin': True,
        'method.response.header.Access-Control-Allow-Methods': True
    },
    responseModels={
        'application/json': 'Empty'
    }
)

add_integration = client.put_integration(
    restApiId=api_id,
    resourceId=add_resource_id,
    httpMethod='OPTIONS',
    type='MOCK',
    requestTemplates={
        'application/json': '{"statusCode": 200}'
    }
)

add_integration_response = client.put_integration_response(
    restApiId=api_id,
    resourceId=add_resource_id,
    httpMethod='OPTIONS',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': '\'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token\'',
        'method.response.header.Access-Control-Allow-Methods': '\'POST,OPTIONS\'',
        'method.response.header.Access-Control-Allow-Origin': '\'*\'' 
    }
)

# Create the /delete resource
delete_resource = client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='delete'
)
delete_resource_id = delete_resource["id"]

# Define the DELETE method for /delete
delete_method = client.put_method(
    restApiId=api_id,
    resourceId=delete_resource_id,
    httpMethod='POST',
    authorizationType='COGNITO_USER_POOLS',
    authorizerId=authorizer_id,
    requestParameters={
        'method.request.querystring.description': True,
        'method.request.querystring.user_id': True
    }
)

# Method response for DELETE
delete_response = client.put_method_response(
    restApiId=api_id,
    resourceId=delete_resource_id,
    httpMethod='POST',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': True,
        'method.response.header.Access-Control-Allow-Origin': True,
        'method.response.header.Access-Control-Allow-Methods': True
    },
    responseModels={
        'application/json': 'Empty'
    }
)

# Get the Lambda function ARN for delete_task function
lambda_arn = lambda_client.get_function(FunctionName='delete_task')['Configuration']['FunctionArn']
uri = f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'

if lambda_arn is None:
    raise Exception("No Lambda function found, make sure the lambda function delete_task exists")

# Create the integration for DELETE method
delete_integration = client.put_integration(
    restApiId=api_id,
    resourceId=delete_resource_id,
    httpMethod='POST',
    credentials=lab_role,  # IAM role that grants API Gateway permission to invoke Lambda
    integrationHttpMethod='POST',
    type='AWS',
    uri=uri,
    requestTemplates={
        "application/json": '{ "queryStringParameters": { "user_id": "$input.params(\'user_id\')", "description": "$input.params(\'description\')" } }'
    }
)

# Integration response for DELETE method
delete_integration_response = client.put_integration_response(
    restApiId=api_id,
    resourceId=delete_resource_id,
    httpMethod='POST',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': '\'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token\'',
        'method.response.header.Access-Control-Allow-Methods': '\'POST,OPTIONS\'',
        'method.response.header.Access-Control-Allow-Origin': '\'*\'' 
    }
)

# Now, configure CORS (OPTIONS) preflight for /delete
delete_method_options = client.put_method(
    restApiId=api_id,
    resourceId=delete_resource_id,
    httpMethod='OPTIONS',
    authorizationType='NONE'
)

delete_response_options = client.put_method_response(
    restApiId=api_id,
    resourceId=delete_resource_id,
    httpMethod='OPTIONS',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': True,
        'method.response.header.Access-Control-Allow-Origin': True,
        'method.response.header.Access-Control-Allow-Methods': True
    },
    responseModels={
        'application/json': 'Empty'
    }
)

delete_integration_options = client.put_integration(
    restApiId=api_id,
    resourceId=delete_resource_id,
    httpMethod='OPTIONS',
    type='MOCK',
    requestTemplates={
        'application/json': '{"statusCode": 200}'
    }
)

delete_integration_response_options = client.put_integration_response(
    restApiId=api_id,
    resourceId=delete_resource_id,
    httpMethod='OPTIONS',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': '\'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token\'',
        'method.response.header.Access-Control-Allow-Methods': '\'POST,OPTIONS\'',
        'method.response.header.Access-Control-Allow-Origin': '\'*\'' 
    }
)

# Deploy the API
deployment = client.create_deployment(
    restApiId=api_id,
    stageName='prod'
)

print(f'API created successfully: {api_id}, deployment: prod')
with open("../.env", "a") as file:
    file.write(f"API_ID={api_id}\n")
