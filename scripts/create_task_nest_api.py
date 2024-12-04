import boto3
import sys

# Creating connections to the various services
client = boto3.client('apigateway', region_name='us-east-1')
lambda_client = boto3.client('lambda', region_name='us-east-1')
iam_client = boto3.client('iam')

response = client.get_rest_apis()
apis = response.get('items', [])

# Only continues if API doesn't exist
for api in apis:
    if api.get('name') == 'task_nest_api':
        print('API already exists')
        sys.exit(0)

response = client.create_rest_api(
    name='task_nest_api',
    description='API to manage tasks',
    endpointConfiguration={'types': ['REGIONAL']}
)
api_id = response["id"]

resources = client.get_resources(restApiId=api_id)
root_id = [resource for resource in resources["items"] if resource["path"] == "/"][0]["id"]

lab_role = iam_client.get_role(RoleName='LabRole')['Role']['Arn']

def create_method(client, api_id, resource_id, method, lambda_function_name, is_mock=False):
    """
    Create a method for a resource in an API Gateway.
    Created this because script was getting very lengthy and since its python,
    we can just use a function to reduce the boilerplate code.
    """
    client.put_method(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod=method,
        authorizationType='NONE'
    )

    client.put_method_response(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod=method,
        statusCode='200',
        responseParameters={
            'method.response.header.Access-Control-Allow-Headers': True,
            'method.response.header.Access-Control-Allow-Origin': True,
            'method.response.header.Access-Control-Allow-Methods': True
        },
        responseModels={'application/json': 'Empty'}
    )

    if is_mock:
        client.put_integration(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod=method,
            type='MOCK',
            requestTemplates={'application/json': '{"statusCode": 200}'}
        )
    else:
        lambda_arn = lambda_client.get_function(FunctionName=lambda_function_name)['Configuration']['FunctionArn']
        uri = f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'

        client.put_integration(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod=method,
            credentials=lab_role,
            integrationHttpMethod='POST',
            type='AWS_PROXY',
            uri=uri
        )

# /tasks
tasks = client.create_resource(restApiId=api_id, parentId=root_id, pathPart='tasks')
create_method(client, api_id, tasks["id"], 'GET', 'get_tasks')
create_method(client, api_id, tasks["id"], 'OPTIONS', 'get_tasks', is_mock=True)

# /add
add_resource = client.create_resource(restApiId=api_id, parentId=root_id, pathPart='add')
create_method(client, api_id, add_resource["id"], 'POST', 'add_task')
create_method(client, api_id, add_resource["id"], 'OPTIONS', 'add_task', is_mock=True)

# /delete
delete_resource = client.create_resource(restApiId=api_id, parentId=root_id, pathPart='delete')
create_method(client, api_id, delete_resource["id"], 'DELETE', 'delete_task')
create_method(client, api_id, delete_resource["id"], 'OPTIONS', 'delete_task', is_mock=True)

print("DONE")
