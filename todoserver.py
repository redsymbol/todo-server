import json
from flask import (
    Flask,
    request,
    )
app = Flask(__name__)
class TaskStore:
    def __init__(self):
        self.clear()

    def new_id(self):
        id = self._last_id
        self._last_id += 1
        return id

    def add(self, summary, description):
        task_id = self.new_id()
        task = {
            'id': task_id,
            'summary': summary,
            'description': description,
            }
        self.tasks[task_id] = task
        return task_id

    def all_tasks(self):
        return list(self.tasks.values())

    def clear(self):
        self._last_id = 0
        self.tasks = {}
        
store = TaskStore()

@app.route('/items/', methods=['GET'])
def get_tasks():
    return json.dumps([
    {'id': task['id'], 'summary': task['summary']}
        for task in store.all_tasks()])

@app.route('/items/<task_id>/', methods=['GET'])
def describe_task(task_id):
    task_id = int(task_id)
    return json.dumps(store.tasks[task_id])

@app.route('/items/', methods=['POST'])
def add_task():
    data = request.get_json()
    task_id = store.add(data['summary'], data['description'])
    return json.dumps({'id': task_id})

@app.route('/items/<task_id>/', methods=['DELETE'])
def task_done(task_id):
    return 'DELETE /items/{}/'.format(task_id)

@app.route('/items/<task_id>/', methods=['PUT'])
def update_task(task_id):
    return 'PUT /items/{}/'.format(task_id)


if __name__ == '__main__':
    app.run()
