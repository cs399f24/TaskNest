import boto3, json
import sys

client = boto3.client('apigateway', region_name='us-east-1')

response = client.get_rest_apis()
apis = response.get('items', [])
        
for api in apis:
    if api.get('name') == 'task_nest_rest_api':
        print('API already exits')
        sys.exit(0)


response = client.create_rest_api(
    name='task_nest_rest_api',
    description='API to tally votes.',
    endpointConfiguration={
        'types': [
            'REGIONAL',
        ]
    }
)
api_id = response["id"]

resources = client.get_resources(restApiId=api_id)
root_id = [resource for resource in resources["items"] if resource["path"] == "/"][0]["id"]

import boto3

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
    pass # Create the user pool

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
    authorizerId=authorizer_id
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

tasks_integration_response = client.put_integration_response(
    restApiId=api_id,
    resourceId=tasks_resource_id,
    httpMethod='GET',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': '\'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token\'',
        'method.response.header.Access-Control-Allow-Methods': '\'GET\'.\'OPTIONS\'',
        'method.response.header.Access-Control-Allow-Origin': '\'*\''
    }
)

lambda_client = boto3.client('lambda', region_name='us-east-1')
lambda_arn=lambda_client.get_function(FunctionName='get_tasks')['Configuration']['FunctionArn']
uri=f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'

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
    type='AWS_PROXY',
    uri=uri,
    requestTemplates={
        "application/json": '{ "queryStringParameters": { "user_id": "$input.params(\'user_id\')" } }'
    }
)

# Now /tasks preflight
tasks_method = client.put_method(
    restApiId=api_id,
    resourceId=tasks_resource_id,
    httpMethod='OPTIONS',
    authorization='NONE'
    Type='NONE'
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
        'method.response.header.Access-Control-Allow-Methods': '\'GET\',\'OPTIONS\'',
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

add_integration_response = client.put_integration_response(
    restApiId=api_id,
    resourceId=add_resource_id,
    httpMethod='POST',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': '\'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token\'',
        'method.response.header.Access-Control-Allow-Methods': '\'POST\'.\'OPTIONS\'',
        'method.response.header.Access-Control-Allow-Origin': '\'*\''
    }
)

lambda_arn=lambda_client.get_function(FunctionName='add_task')['Configuration']['FunctionArn']
uri=f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'

if lambda_arn is None:
    raise Exception("No Lambda function found, make sure lambda function add_task exists")

add_integration = client.put_integration(
    restApiId=api_id,
    resourceId=add_resource_id,
    httpMethod='POST',
    credentials=lab_role,
    integrationHttpMethod='POST',
    type='AWS_PROXY',
    uri=uri,
    requestTemplates={
        "application/json": '{ "body": $input.json("$") }'
    }
)

# Now /add preflight

add_method = client.put_method(
    restApiId=api_id,
    resourceId=add_resource_id,
    httpMethod='OPTIONS',
    authorization='NONE',
    Type='NONE'
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
        'method.response.header.Access-Control-Allow-Methods': '\'POST\',\'OPTIONS\'',
        'method.response.header.Access-Control-Allow-Origin': '\'*\''
    }
)

# Create the /delete resource

#vote_integration_response = client.put_integration_response(
#    restApiId=api_id,
#    resourceId=vote_resource_id,
##    httpMethod='POST',
#    statusCode='200',
#    responseParameters={
#        'method.response.header.Access-Control-Allow-Headers': '\'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token\'',
#        'method.response.header.Access-Control-Allow-Methods': '\'POST\'.\'OPTIONS\'',
#        'method.response.header.Access-Control-Allow-Origin': '\'*\''
#    },
#    responseTemplates={
#        "application/json": json.dumps({
#            "yes": 20,
#            "no": 10               
#        })
#    }
#)


vote_method = client.put_method(
    restApiId=api_id,
    resourceId=vote_resource_id,
    httpMethod='OPTIONS',
    authorizationType='NONE'
)

vote_response = client.put_method_response(
    restApiId=api_id,
    resourceId=vote_resource_id,
    httpMethod='OPTIONS',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': False,
        'method.response.header.Access-Control-Allow-Origin': False,
        'method.response.header.Access-Control-Allow-Methods': False
    },
    responseModels={
        'application/json': 'Empty'
    }
)


vote_integration = client.put_integration(
    restApiId=api_id,
    resourceId=vote_resource_id,
    httpMethod='OPTIONS',
    type='MOCK',
    requestTemplates={
        'application/json': '{"statusCode": 200}'
    }
)


vote_integration_response = client.put_integration_response(
    restApiId=api_id,
    resourceId=vote_resource_id,
    httpMethod='OPTIONS',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': '\'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token\'',
        'method.response.header.Access-Control-Allow-Methods': '\'POST\',\'OPTIONS\'',
        'method.response.header.Access-Control-Allow-Origin': '\'*\''
    }
)



print ("DONE")