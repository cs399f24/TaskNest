from flask import Flask, jsonify, request
from flask_cors import CORS
import boto3

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Allows cross-origin requests from your React frontend

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Tasknest-Users')

def get_user_tasks(user_id):
    """Retrieve tasks for a specific user from DynamoDB."""
    response = table.get_item(Key={'user_id': user_id})
    return response.get('Item', {}).get('tasks', [])

def add_task_to_db(user_id, task):
    """Add a task for a specific user to DynamoDB."""
    response = table.update_item(
        Key={'user_id': user_id},
        UpdateExpression="SET tasks = list_append(if_not_exists(tasks, :empty_list), :new_task)",
        ExpressionAttributeValues={':new_task': [task], ':empty_list': []},
        ReturnValues="UPDATED_NEW"
    )
    return response

@app.route('/test', methods=['GET'])
def test_task():
    return jsonify({"message": "This is a response from Flask!"})

@app.route('/tasks/<string:user_id>', methods=['GET'])
def get_tasks(user_id):
    """Retrieve all tasks for a specific user."""
    tasks = get_user_tasks(user_id)
    return jsonify(tasks), 200

@app.route('/add', methods=['POST', 'OPTIONS'])
def add_task():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200  # Handle preflight request

    data = request.get_json()
    user_id = data.get('user_id')
    task_description = data.get('description')
    task_time = data.get('time')
    
    if not user_id or not task_description or not task_time:
        return jsonify({"error": "User ID, description, and time are required."}), 400
    
    # Structure the task object and add it to the database
    task = {"description": task_description, "time": task_time}
    add_task_to_db(user_id, task)
    return jsonify({"message": "Task added successfully"}), 201

@app.route('/delete/<string:user_id>/<string:description>', methods=['DELETE'])
def delete_task(user_id, description):
    """Delete a specific task by description for a user."""
    tasks = get_user_tasks(user_id)
    # Filter out the task with the given description
    updated_tasks = [task for task in tasks if task.get("description") != description]
    
    # Update the tasks list in DynamoDB
    response = table.update_item(
        Key={'user_id': user_id},
        UpdateExpression="SET tasks = :updated_tasks",
        ExpressionAttributeValues={':updated_tasks': updated_tasks},
        ReturnValues="UPDATED_NEW"
    )
    
    if tasks == updated_tasks:
        return jsonify({"error": "Task not found."}), 404
    return jsonify({"message": "Task deleted successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)  # Exposes Flask server publicly on port 5300
