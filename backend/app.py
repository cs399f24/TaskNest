from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Allows cross-origin requests from your React frontend

# Task storage: description mapped to time
tasks = {}

@app.route('/test', methods=['GET'])
def test_task():
    return jsonify({"message": "This is a response from Flask!"})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Retrieve tasks for a specific user."""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    # Fetch tasks for the specific user from DynamoDB or your storage mechanism
    user_tasks = {desc: time for desc, time in tasks.items() if tasks[desc].get('user_id') == user_id}
    
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
    
    # Store the task with the user_id as part of the task's attributes
    tasks[task_description] = {"time": task_time, "user_id": user_id}
    return jsonify(tasks), 201

@app.route('/delete/<string:description>', methods=['DELETE'])
def delete_task(description):
    """Delete a task by description."""
    if description in tasks:
        del tasks[description]
        return jsonify(tasks), 200
    else:
        return jsonify({"error": "Task not found."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
