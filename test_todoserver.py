import unittest
import json
import todoserver

todoserver.app.testing = True

def load_json(data):
    return json.loads(data.decode('utf-8'))

class TestTodo(unittest.TestCase):
    def setUp(self):
        self.app = todoserver.app.test_client()
        todoserver.store.clear()

    def test_get_empty_task_list(self):
        resp = self.app.get('/items/')
        self.assertEqual(200, resp.status_code)
        self.assertEqual([], load_json(resp.data))

    def test_add_one_task(self):
        task_summary = 'Buy milk'
        task_description = 'Lots and lots of delicious milk!'
        # check test assumption
        resp = self.app.get('/items/')
        self.assertEqual(200, resp.status_code)
        self.assertEqual([], load_json(resp.data))
        # add an item
        resp = self.app.post(
            '/items/',
            content_type='application/json',
            data = json.dumps({
                'summary': task_summary,
                'description': task_description,
        }))
        self.assertEqual(200, resp.status_code)
        returned = load_json(resp.data)
        self.assertEqual(dict, type(returned))
        self.assertIn('id', returned)
        task_id = returned['id']
        # fetch this one task
        resp = self.app.get('/items/{:d}/'.format(task_id))
        self.assertEqual(200, resp.status_code)
        returned = load_json(resp.data)
        self.assertEqual(dict, type(returned))
        self.assertEqual(task_id, returned['id'])
        self.assertEqual(task_summary, returned['summary'])
        self.assertEqual(task_description, returned['description'])
        # fetch all tasks
        resp = self.app.get('/items/')
        self.assertEqual(200, resp.status_code)
        returned = load_json(resp.data)
        self.assertEqual(1, len(returned))
        self.assertEqual(task_id, returned[0]['id'])
