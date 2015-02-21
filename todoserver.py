import json
from flask import Flask
app = Flask(__name__)

class TaskStore:
    def __init__(self):
        self.last_id = 0
        self.tasks = {}

    def add(self, summary, description):
        task_id = self.last_id
        self.last_id += 1
        task = {
            'id': task_id,
            'summary': summary,
            'description': description,
            }
        self.tasks[task_id] = task
        return task

    def all_tasks(self):
        return list(self.tasks.values())

    def clear(self):
        self.last_id = 0
        self.tasks = {}
        
store = TaskStore()

@app.route('/items/', methods=['GET'])
def get_tasks():
    return json.dumps(store.all_tasks())

@app.route('/items/<task_id>/')
def describe_task(task_id, methods=['GET']):
    return 'GET /items/{}/'.format(task_id)

@app.route('/items/', methods=['POST'])
def add_task():
    return 'POST /items/'

@app.route('/items/<task_id>/', methods=['DELETE'])
def task_done(task_id):
    return 'DELETE /items/{}/'.format(task_id)

@app.route('/items/<task_id>/', methods=['PUT'])
def update_task(task_id):
    return 'PUT /items/{}/'.format(task_id)


if __name__ == '__main__':
    app.run(debug=True)
