import abc
import argparse
import json
import re
import psycopg2
from flask import (
    Flask,
    request,
    make_response,
    )

app = Flask(__name__)

class TaskStore(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add(self, summary, description):
        pass
    
    @abc.abstractmethod
    def get_task(self, task_id):
        pass

    @abc.abstractmethod
    def delete_task(self, task_id):
        pass

    @abc.abstractmethod
    def update_task(self, task_id, summary, description):
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

    def get_task(self, task_id):
        return self.tasks[task_id]

    def delete_task(self, task_id):
        try:
            del self.tasks[task_id]
            return True
        except KeyError:
            return False
 
    def update_task(self, task_id, summary, description):
        task = self.tasks[task_id]
        task['summary'] = summary
        task['description'] = description

    def all_tasks(self):
        return iter(self.tasks.values())

    def clear(self):
        self._last_id = 0
        self.tasks = {}

class DbTaskStore(TaskStore):
    def __init__(self):
        self.dsn = 'dbname=todoserver user=www-data'

    def add(self, summary, description):
        insert_stmt = 'INSERT INTO tasks (summary, description) VALUES (%s, %s) RETURNING id'
        with psycopg2.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(insert_stmt, (summary, description))
                task_id = cur.fetchone()[0]
        return task_id

    def get_task(self, task_id: int):
        cols = (
            'id',
            'summary',
            'description',
            )
        select_stmt = 'select ' + ','.join(cols) + ' from tasks WHERE id = %s'
        with psycopg2.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(select_stmt, (task_id,))
                row = cur.fetchone()
                if row is None:
                    return None
                return dict(zip(cols, row))

    def update_task(self, task_id, summary, description):
        fields = [
            summary,
            description,
        ]
        clauses = [
            'summary = %s',
            'description = %s',
        ]
        statement = 'UPDATE tasks SET ' + ', '.join(clauses) + ' WHERE id = %s'
        fields.append(task_id)
        with psycopg2.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(statement, fields)
                count = _update_count(cur.statusmessage)
                assert count in {0, 1}, count
                return count == 1
        
    def delete_task(self, task_id):
        with psycopg2.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
                count = _delete_count(cur.statusmessage)
                assert count in {0, 1}, count
                return count == 1

    def all_tasks(self):
        cols = (
            'id',
            'summary',
            'description',
            )
        select_stmt = 'select ' + ','.join(cols) + ' from tasks'
        with psycopg2.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(select_stmt)
                for row in cur:
                    yield dict(zip(cols, row))

    def clear(self):
        pass

def _delete_count(statusmessage):
    match = re.match(r'DELETE (\d+)$', statusmessage)
    assert match is not None, statusmessage
    return int(match.group(1))

def _update_count(statusmessage):
    match = re.match(r'UPDATE (\d+)$', statusmessage)
    assert match is not None, statusmessage
    return int(match.group(1))

DEFAULT_STORE = 'db'
store_types = {
    'memory': MemoryTaskStore,
    'db': DbTaskStore,
}
assert DEFAULT_STORE in store_types
store = store_types[DEFAULT_STORE]()

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=5000, type=int)
    parser.add_argument('--host', default='127.0.0.1', type=str)
    parser.add_argument('--store', default=DEFAULT_STORE, choices=store_types.keys(),
                        help='storage backend')
    parser.add_argument('--debug', action='store_true', default=False)
    return parser.parse_args()


def init_store(store_type_name):
    global store
    store_type = store_types[store_type_name]
    store = store_type()
        
@app.route('/tasks/', methods=['GET'])
def get_tasks():
    return json.dumps([
    {'id': task['id'], 'summary': task['summary']}
        for task in store.all_tasks()])

@app.route('/tasks/<int:task_id>/', methods=['GET'])
def describe_task(task_id):
    task = store.get_task(task_id)
    if task is None:
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
    did_exist = store.delete_task(task_id)
    if did_exist:
        return ''
    return make_response('', 404)

@app.route('/tasks/<int:task_id>/', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    did_update = store.update_task(task_id, data['summary'], data['description'])
    if did_update:
        return ''
    return make_response('', 404)

if __name__ == '__main__':
    args = get_args()
    if args.store != 'memory':
        init_store(args.store)
    if args.debug:
        app.debug = True
    app.run(host=args.host, port=args.port)
