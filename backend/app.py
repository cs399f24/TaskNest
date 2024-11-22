from flask import Flask, jsonify, request
from flask_cors import CORS
from dynamodb import DynamoDB

app = Flask(__name__)
CORS(app, supports_credentials=True)

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

    user_tasks = db_connection.get_tasks(user_id)
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

    db_connection.add_task(user_id, {"description": task_description, "time": task_time})
    updated_tasks = db_connection.get_tasks(user_id)

    return jsonify(updated_tasks), 201

@app.route('/delete', methods=['DELETE', 'OPTIONS'])
def delete_task():
    """Delete a task by description."""
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    user_id = request.args.get('user_id')
    description = request.args.get('description')
    if not user_id or not description:
        return jsonify({"error": "User ID and description are required"}), 400

    response = db_connection.delete_task(user_id, description)
    
    if "error" in response:
        return jsonify(response), 404
    
    updated_tasks = db_connection.get_tasks(user_id)
    return jsonify(updated_tasks), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
