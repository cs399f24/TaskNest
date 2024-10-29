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
    """Retrieve all tasks."""
    return jsonify(tasks), 200

@app.route('/add', methods=['POST', 'OPTIONS'])
def add_task():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200  # Handle preflight request

    data = request.get_json()
    task_description = data.get('description')
    task_time = data.get('time')
    
    if not task_description or not task_time:
        return jsonify({"error": "Both description and time are required."}), 400
    
    tasks[task_description] = task_time
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
    app.run(host='0.0.0.0', port=5300)  # Exposes Flask server publicly on port 5300
