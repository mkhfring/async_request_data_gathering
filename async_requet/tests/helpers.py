from uuid import uuid4

import requests

from flask import Flask, jsonify, abort
from threading import Thread



tasks = [
    {
        'id': 1,
        'item': 'Apple'
    },
    {
        'id': 2,
        'item': 'Banana'
    }
]


class MockServer(Thread):
    def __init__(self, port=5000):
        super().__init__()
        self.port = port
        self.url = "http://localhost:%s" % self.port
        self.app = Flask(__name__)

        self.app.add_url_rule("/shutdown", view_func=self._shutdown_server)
        self.app.add_url_rule(
            '/todo/api/v1.0/tasks/<int:task_id>',
            view_func=self.get_task,
        )

    def _shutdown_server(self):
        from flask import request
        if not 'werkzeug.server.shutdown' in request.environ:
            raise RuntimeError('Not running the development server')
        request.environ['werkzeug.server.shutdown']()
        return 'Server shutting down...'

    def shutdown_server(self):
        requests.get("http://localhost:%s/shutdown" % self.port)
        self.join()

    def get_task(self, task_id):
        task = [task for task in tasks if task['id'] == task_id]
        if len(task) == 0:
            abort(404)
        return jsonify(task[0])

    def run(self):
        self.app.run()