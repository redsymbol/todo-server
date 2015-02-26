import unittest
import requests
import todo
todo.API_BASE = 'http://127.0.0.1:5000'

class TestTodo(unittest.TestCase):
    def setUp(self):
        resp = requests.delete(todo.API_BASE + '/tasks/ALL/')
        self.assertEqual(200, resp.status_code)
        
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
