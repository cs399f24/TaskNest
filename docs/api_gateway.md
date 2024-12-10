# Api Gateway
## What is does:
Check if API exists:

- The script first checks if an API with the name task_nest_rest_api_1 already exists. If it does, the script exits. Otherwise, it proceeds to create the API.

Create API Gateway:

- The script creates a new REST API called task_nest_rest_api_1 with a REGIONAL endpoint configuration.
- It retrieves the root resource ID to later create sub-resources like /tasks, /add, and /delete.

Cognito Setup:

- The script checks if the Cognito User Pool task-nest-user-pool exists. If it doesn't, it creates it with specific password policies and email verification.
- It creates a user pool client task-nest-client if it doesn't already exist.
- It constructs the ARN for the Cognito User Pool and creates a Cognito Authorizer for API Gateway to handle authentication.

### API Gateway Resources and Methods:

- Tasks Resource (/tasks):
    - It creates a resource /tasks in the API.
    - Configures a GET method with Cognito User Pool authentication, which requires a user_id query string parameter.
    - Configures a method response with CORS headers.
    - Integrates the Lambda function get_tasks.

- Add Resource (/add):
    - It creates a resource /add in the API.
    - Configures a POST method with Cognito User Pool authentication.
    - Configures a method response with CORS headers.
    - Integrates the Lambda function add_task.

- Delete Resource (/delete):
    - It creates a resource /delete in the API.
    - Configures a POST method with Cognito User Pool authentication, requiring both user_id and description query parameters.
    - Configures a method response with CORS headers.
    - Integrates the Lambda function delete_task.

- CORS Preflight:
    - For each of the resources (/tasks, /add, /delete), the script sets up an OPTIONS method to handle preflight CORS requests.
    - The OPTIONS method is configured with a mock integration and CORS headers.

- Deploy API:
    - The script creates a deployment of the API under the prod stage.
    - Once the deployment is complete, it prints the API ID and deployment stage.

- Write Environment Variables:
    - The script writes the API Gateway ID, Cognito User Pool ID, and Client ID into the .env file to be used in the frontend.