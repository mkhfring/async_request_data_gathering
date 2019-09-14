import pytest
from flask import Flask, jsonify, abort, request

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'item': 1
    },
    {
        'id': 2,
        'item': 2
    }
]


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


@pytest.fixture(scope='session')
def start_server():
    yield app.run(debug=True)
    shutdown_server()



if __name__ == '__main__':
    app.run(debug=True)
