from flask import Flask, jsonify, request
from flask_cors import CORS
from dynamodb import DynamoDB

app = Flask(__name__)
CORS(app, supports_credentials=True)

dynamodb = DynamoDB()

@app.route('/test', methods=['GET'])
def test_task():
    return jsonify({"message": "This is a response from Flask!"})

@app.route('/tasks/<string:user_id>', methods=['GET'])
def get_tasks(user_id):
    user_id = 'DEV_USER'  # For now, we'll use a hardcoded user ID
    tasks = dynamodb.get_tasks(user_id)
    return jsonify(tasks), 200

@app.route('/add', methods=['POST', 'OPTIONS'])
def add_task():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    data = request.get_json()
    user_id = 'DEV_USER'  # For now, we'll use a hardcoded user ID
    task_description = data.get('description')
    task_time = data.get('time')
    
    if not user_id or not task_description or not task_time:
        return jsonify({"error": "User ID, description, and time are required."}), 400
    
    task = {"description": task_description, "time": task_time}
    dynamodb.add_task(user_id, task)
    return jsonify({"message": "Task added successfully"}), 201

@app.route('/delete/<string:user_id>/<string:description>', methods=['DELETE'])
def delete_task(user_id, description):
    user_id = 'DEV_USER'  # For now, we'll use a hardcoded user ID
    response = dynamodb.delete_task(user_id, description)
    if "error" in response:
        return jsonify(response), 404
    return jsonify({"message": "Task deleted successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5300)  # Exposes Flask server publicly on port 5300
