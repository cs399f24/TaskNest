from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

# Configure CORS with All settings

CORS(app, resources={r"/*": {"origins": "*"}})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

tasks = []

@app.route('/tasks', methods=['GET'])
def get_tasks():
    response = jsonify(tasks)
    return response, 200

@app.route('/add', methods=['POST'])
def add_task():
    data = request.get_json()
    task_description = data.get('description')
    
    if task_description:
        tasks.append(task_description)
        response = jsonify(tasks)
        return response, 201
    else:
        return jsonify({"error": "Invalid input"}), 400

@app.route('/delete/<int:index>', methods=['DELETE'])
def delete_task(index):
    if 0 <= index < len(tasks):
        tasks.pop(index)
        response = jsonify(tasks)
        return response, 200
    else:
        return jsonify({"error": "Task not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)