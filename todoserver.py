import abc
import argparse
import json
from flask import (
    Flask,
    request,
    make_response,
    )

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=5000, type=int)
    parser.add_argument('--host', default='127.0.0.1', type=str)
    parser.add_argument('--store', default=':memory:', choices=[':memory:'],
                        help='storage backend')
    return parser.parse_args()

app = Flask(__name__)

class TaskStore(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add(self, summary, description):
        pass
    
    @abc.abstractmethod
    def all_tasks(self):
        pass

class MemoryTaskStore(TaskStore):
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

store = None

def init_store(store_type_name):
    global store
    store_types = {
        ':memory:' : MemoryTaskStore,
        }
    store_type = store_types[store_type_name]
    store = store_type()
        
@app.route('/tasks/', methods=['GET'])
def get_tasks():
    return json.dumps([
    {'id': task['id'], 'summary': task['summary']}
        for task in store.all_tasks()])

@app.route('/tasks/<int:task_id>/', methods=['GET'])
def describe_task(task_id):
    try:
        task = store.tasks[task_id]
    except KeyError:
            return make_response('', 404)
    return json.dumps(task)

@app.route('/tasks/', methods=['POST'])
def add_task():
    data = request.get_json()
    task_id = store.add(data['summary'], data['description'])
    return make_response(json.dumps({'id': task_id}), 201)

@app.route('/tasks/ALL/', methods=['DELETE'])
def wipe_tasks():
    store.clear()
    return ''
    
@app.route('/tasks/<int:task_id>/', methods=['DELETE'])
def task_done(task_id):
    if task_id in store.tasks:
        del store.tasks[task_id]
        return ''
    return make_response('', 404)

@app.route('/tasks/<int:task_id>/', methods=['PUT'])
def update_task(task_id):
    try:
        task = store.tasks[task_id]
    except KeyError:
        return make_response('', 404)
    data = request.get_json()
    for field in {'summary', 'description'}:
        task[field] = data[field]
    return ''

if __name__ == '__main__':
    args = get_args()
    init_store(args.store)
    app.run(host=args.host, port=args.port)
