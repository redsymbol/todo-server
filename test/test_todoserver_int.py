import unittest
import requests
import subprocess
import logging
import time

import todo
import todoserver

TEST_HOST = '127.0.0.1'
TEST_PORT = 5003
todo.API_BASE = 'http://{}:{}'.format(TEST_HOST, TEST_PORT)

logging.basicConfig(
    filename='test/log/inttest.log',
    level=logging.INFO,
    filemode='w',
)

class TestTodo(unittest.TestCase):
    def setUp(self):
        self._stdout_log = open('test/log/inttest-stdout.log', 'w')
        self._stderr_log = open('test/log/inttest-stderr.log', 'w')
        # start test server
        self.server = subprocess.Popen([
            'python',
            'todoserver.py',
            '--debug',
            '--port',
            str(TEST_PORT),
            '--host',
            TEST_HOST,
            '--store',
            'memory',
            ],
            stdout=self._stdout_log,
            stderr=self._stderr_log,
        )
        logging.info('Starting test todoserver: %d', self.server.pid)
        
        # wait for server to be up and accepting connections
        max_tries = 6
        tries = 0
        while True:
            try:
                resp = requests.get(todo.API_BASE + '/tasks/')
                break
            except requests.exceptions.ConnectionError:
                if tries >= max_tries:
                    self.terminate_test_server()
                    raise
                time.sleep(.1)
                tries += 1
        self.assertEqual(200, resp.status_code)

    def tearDown(self):
        self.terminate_test_server()
        
    def terminate_test_server(self):
        logging.info('Terminating test todoserver: %d', self.server.pid)
        self.server.terminate()
        self.server.wait(1)
        
    def test_get_empty_task_list(self):
        resp = todo.get_tasks()
        self.assertEqual(200, resp.status_code)
        self.assertEqual([], resp.json())

    def test_add_one_task_then_delete(self):
        task_summary = 'Buy milk'
        task_description = 'Lots and lots of delicious milk'
        # check test assumption
        resp = todo.get_tasks()
        self.assertEqual(200, resp.status_code)
        self.assertEqual([], resp.json())
        # add an item
        resp = todo.add_task(task_summary, task_description)
        self.assertEqual(201, resp.status_code)
        returned = resp.json()
        self.assertEqual(dict, type(returned))
        self.assertIn('id', returned)
        task_id = returned['id']
        # fetch this one task
        resp = todo.describe_task(task_id)
        self.assertEqual(200, resp.status_code)
        returned = resp.json()
        self.assertEqual(dict, type(returned))
        self.assertEqual(task_id, returned['id'])
        self.assertEqual(task_summary, returned['summary'])
        self.assertEqual(task_description, returned['description'])
        # fetch all tasks
        resp = todo.get_tasks()
        self.assertEqual(200, resp.status_code)
        returned = resp.json()
        self.assertEqual(1, len(returned))
        self.assertEqual(task_id, returned[0]['id'])
        # delete this task
        resp = todo.task_done(task_id)
        self.assertEqual(200, resp.status_code)
        #  now it shouldn't exist - by direct lookup...
        resp = todo.describe_task(task_id)
        self.assertEqual(404, resp.status_code)
        #  or in all items...
        resp = todo.get_tasks()
        self.assertEqual(200, resp.status_code)
        returned = resp.json()
        self.assertEqual(0, len(returned))
        #  or if we try to delete a second time.
        resp = todo.task_done(task_id)
        self.assertEqual(404, resp.status_code)
        
    def test_update_task(self):
        task_summary = 'Buy milk'
        task_description = 'Lots and lots of delicious milk'
        task_summary2 = task_summary + '!!'
        task_description2 = task_description + '!!'
        # add an item
        resp = todo.add_task(task_summary, task_description)
        self.assertEqual(201, resp.status_code)
        task_id = resp.json()['id']

        # now update it
        resp = todo.update_task(task_id, task_summary2, task_description2)
        self.assertEqual(200, resp.status_code)

        # refetch and check
        resp = todo.describe_task(task_id)
        self.assertEqual(200, resp.status_code)
        returned = resp.json()
        self.assertEqual(task_summary2, returned['summary'])
        self.assertEqual(task_description2, returned['description'])

    def test_update_task_not_found_returns_error(self):
        resp = todo.update_task(42, 'foo', 'bar')
        self.assertEqual(404, resp.status_code)
