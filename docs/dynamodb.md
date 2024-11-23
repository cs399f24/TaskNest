# DynamoDB Setup

1. **Open DynamoDB**
   - Search for DynamoDB using the search bar next to services.

2. **Create a table**
   - From the DynamoDB welcome page, select "Create table".
   - Enter the table name: `TaskNest-users`.
   - Enter your Partition key: `user_id`.
   - Choose the Read/Write Capacity Mode (this can be edited later).
   - Select **Provisioned**.
   - Use **Default settings**.
   - Select "Create table" to finish.

3. **Setting up DynamoDB within your code**
   - Install Boto3:
     ```bash
     pip install boto3
     ```

   - Access DynamoDB:
     ```python
     import boto3
     
     dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
     table = dynamodb.Table('YourTableName')
     ```

