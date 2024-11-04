from flask import Flask, jsonify, request
from flask_cors import CORS
import boto3

class DynamoDB:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = self.dynamodb.Table('task-nest-users')

    def get_tasks(self, user_id):
        """Retrieve tasks for a specific user from DynamoDB."""
        response = self.table.get_item(Key={'user-id': user_id})
        if 'Item' not in response:
            return []
        
        tasks = response['Item'].get('tasks', [])
        print(tasks)
        return tasks

    def add_task(self, user_id, task):
        """Add a task for a specific user to DynamoDB."""
        response = self.table.update_item(
            Key={'user_id': user_id},
            UpdateExpression="SET tasks = list_append(if_not_exists(tasks, :empty_list), :new_task)",
            ExpressionAttributeValues={':new_task': [task], ':empty_list': []},
            ReturnValues="UPDATED_NEW"
        )
        return response

    def delete_task(self, user_id, description):
        """Delete a specific task by description for a user."""
        tasks = self.get_tasks(user_id)
        updated_tasks = [task for task in tasks if task.get("description") != description]
        if len(tasks) == len(updated_tasks):
            return {"error": "Task not found."}

        response = self.table.update_item(
            Key={'user_id': user_id},
            UpdateExpression="SET tasks = :tasks",
            ExpressionAttributeValues={':tasks': updated_tasks},
            ReturnValues="UPDATED_NEW"
        )
        return response


app = Flask(__name__)
CORS(app, supports_credentials=True)

# Task storage: {user_id: {description: {"time": time}}}
tasks = {}
db_connection = DynamoDB()

@app.route('/test', methods=['GET'])
def test_task():
    return jsonify({"message": "This is a response from Flask!"})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Retrieve tasks for a specific user."""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    user_tasks = db_connection.get_tasks('DEV_USER')
    return jsonify(user_tasks), 200

@app.route('/add', methods=['POST', 'OPTIONS'])
def add_task():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    data = request.get_json()
    task_description = data.get('description')
    task_time = data.get('time')
    user_id = data.get('user_id')
    
    if not all([task_description, task_time, user_id]):
        return jsonify({"error": "Description, time, and user_id are required."}), 400

    if user_id not in tasks:
        tasks[user_id] = {}
    tasks[user_id][task_description] = {"time": task_time}
    
    return jsonify(tasks[user_id]), 201

@app.route('/delete/<string:description>', methods=['DELETE'])
def delete_task(description):
    """Delete a task by description."""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    if user_id in tasks and description in tasks[user_id]:
        del tasks[user_id][description]
        return jsonify(tasks[user_id]), 200
    else:
        return jsonify({"error": "Task not found."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
