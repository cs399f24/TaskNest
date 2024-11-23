# AWS Lambda


---

#### 1. **Access AWS Lambda Console**
- Go to the AWS Management Console
- Navigate to **Lambda** under the **Compute** section.
- Click **Create function**.

---

#### 2. **Create a New Function**
1. **Choose an Authoring Method:**
   - Select **Author from scratch**.
2. **Function Name:**
   - Enter a descriptive name (e.g., `addTaskLambda`, `deleteTaskLambda`, or `getTaskLambda`).
3. **Runtime:**
   - Choose **Python 3.13** (or the latest available).
4. **Permissions:**
   - Ensure the function has an **IAM role** with permissions to access DynamoDB.

---

#### 3. **Write and Deploy Each Lambda Function**

##### **Add Task Function**
1. Paste the following code into the Lambda editor:
   ```python
   import json
   import boto3

   def lambda_handler(event, context):
       print("Event Received: ", json.dumps(event))
       
       class DynamoDB:
           def __init__(self):
               self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
               self.table = self.dynamodb.Table('task-nest-users')

           def add_task(self, user_id, task):
               response = self.table.update_item(
                   Key={'user-id': user_id},
                   UpdateExpression="SET tasks = list_append(if_not_exists(tasks, :empty_list), :new_task)",
                   ExpressionAttributeValues={':new_task': [task], ':empty_list': []},
                   ReturnValues="UPDATED_NEW"
               )
               return response

       body = json.loads(event['body'])
       db_connection = DynamoDB()
       user_id = body['user_id']
       task = {"description": body['description'], "time": body['time']}
       
       db_connection.add_task(user_id, task)
       return {'statusCode': 200, 'body': "Added"}
   ```

2. **Deploy:**
   - Click **Deploy** to save changes.

---

##### **Delete Task Function**
1. Paste the following code:
   ```python
   import json
   import boto3

   def lambda_handler(event, context):
       user_id = event.get('queryStringParameters', {}).get('user_id')
       description = event.get('queryStringParameters', {}).get('description')

       class DynamoDB:
           def __init__(self):
               self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
               self.table = self.dynamodb.Table('task-nest-users')

           def get_tasks(self, user_id):
               response = self.table.get_item(Key={'user-id': user_id})
               return response.get('Item', {}).get('tasks', [])

           def delete_task(self, user_id, description):
               tasks = self.get_tasks(user_id)
               updated_tasks = [task for task in tasks if task.get("description") != description]
               self.table.update_item(
                   Key={'user-id': user_id},
                   UpdateExpression="SET tasks = :tasks",
                   ExpressionAttributeValues={':tasks': updated_tasks}
               )

       db_connection = DynamoDB()
       db_connection.delete_task(user_id, description)
       return {'statusCode': 200, 'body': "Task deleted"}
   ```

2. **Deploy.**

---

##### **Get Task Function**
1. Paste the following code:
   ```python
   import json
   import boto3

   def lambda_handler(event, context):
       dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
       table = dynamodb.Table('task-nest-users')

       user_id = event.get('queryStringParameters', {}).get('user_id')
       response = table.get_item(Key={'user-id': user_id})
       tasks = response.get('Item', {}).get('tasks', [])
       
       return {'statusCode': 200, 'body': json.dumps(tasks)}
   ```

2. **Deploy.**

---

#### 4. **API Gateway Setup (Optional)**
- Integrate these Lambda functions with an **API Gateway** to allow HTTP requests.
  - Map **GET** (for fetching tasks), **POST** (for adding tasks), and **DELETE** (for deleting tasks) methods to the appropriate Lambda functions.

---

