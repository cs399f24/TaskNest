from flask import Flask, jsonify, request
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def create_app(tasks):

    app = Flask(__name__)
    CORS(app)

    @app.route('/tasks', methods=['GET'])
    def tasks():
        return jsonify(tasks.get_tasks())

    @app.route('/add', methods=['POST'])
    def vote():
        data = json.loads(request.data)

        if 'tasks' not in data:
            return 'Invalid body', 400

        the_task = data['task']

        if not tasks.is_valid_vote(the_task):
            return 'Invalid vote', 400

        tasks.register_task(the_task)

        return jsonify(tasks.get_tasks())

    return app