
# DynamoDB

<ol>
    <li>**Open DynamoDB** </li>
    - Search for DynamoDB using the search bar next to services
    <li> **Create a table** </li>
    - From the DynamoDB welcome page, select "Create table" <br>
        - Enter the table name: "TaskNest-users" <br>
        - Enter your Partition key: "user_id" <br>
    - Choose the Read/Write Capacity Mode (this can be edited later <br>
        - Select Provisioned <br>
    - Use Default settings <br>
    - Select "Create table" to finish <br>
    <li>**Setting up DynamoDB within your code**</li>
    - Install Boto3
    
    pip install boto3
</ol>
<ol>
    -Access DynamoDB
    
    import boto3 
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('YourTableName')
</ol>