import unittest
import json
import todoserver

todoserver.app.testing = True

def load_json(data):
    return json.loads(data.decode('utf-8'))

class TestTodo(unittest.TestCase):
    def setUp(self):
        self.app = todoserver.app.test_client()
        todoserver.init_store(':memory:')

    def test_get_empty_task_list(self):
        resp = self.app.get('/tasks/')
        self.assertEqual(200, resp.status_code)
        self.assertEqual([], load_json(resp.data))

    def test_add_one_task_then_delete(self):
        task_summary = 'Buy milk'
        task_description = 'Lots and lots of delicious milk'
        # check test assumption
        resp = self.app.get('/tasks/')
        self.assertEqual(200, resp.status_code)
        self.assertEqual([], load_json(resp.data))
        # add an item
        resp = self.app.post(
            '/tasks/',
            content_type='application/json',
            data = json.dumps({
                'summary': task_summary,
                'description': task_description,
        }))
        self.assertEqual(201, resp.status_code)
        returned = load_json(resp.data)
        self.assertEqual(dict, type(returned))
        self.assertIn('id', returned)
        task_id = returned['id']
        # fetch this one task
        resp = self.app.get('/tasks/{:d}/'.format(task_id))
        self.assertEqual(200, resp.status_code)
        returned = load_json(resp.data)
        self.assertEqual(dict, type(returned))
        self.assertEqual(task_id, returned['id'])
        self.assertEqual(task_summary, returned['summary'])
        self.assertEqual(task_description, returned['description'])
        # fetch all tasks
        resp = self.app.get('/tasks/')
        self.assertEqual(200, resp.status_code)
        returned = load_json(resp.data)
        self.assertEqual(1, len(returned))
        self.assertEqual(task_id, returned[0]['id'])
        # delete this task
        resp = self.app.delete('/tasks/{:d}/'.format(task_id))
        self.assertEqual(200, resp.status_code)
        #  now it shouldn't exist - by direct lookup...
        resp = self.app.get('/tasks/{:d}/'.format(task_id))
        self.assertEqual(404, resp.status_code)
        #  or in all items...
        resp = self.app.get('/tasks/')
        self.assertEqual(200, resp.status_code)
        returned = load_json(resp.data)
        self.assertEqual(0, len(returned))
        #  or if we try to delete a second time.
        resp = self.app.delete('/tasks/{:d}/'.format(task_id))
        self.assertEqual(404, resp.status_code)
        
    def test_update_task(self):
        task_summary = 'Buy milk'
        task_description = 'Lots and lots of delicious milk'
        task_summary2 = task_summary + '!!'
        task_description2 = task_description + '!!'
        # add an item
        resp = self.app.post(
            '/tasks/',
            content_type='application/json',
            data = json.dumps({
                'summary': task_summary,
                'description': task_description,
        }))
        self.assertEqual(201, resp.status_code)
        returned = load_json(resp.data)
        task_id = returned['id']

        # now update it
        resp = self.app.put(
            '/tasks/{:d}/'.format(task_id),
            content_type='application/json',
            data = json.dumps({
                'summary': task_summary2,
                'description': task_description2,
        }))
        self.assertEqual(200, resp.status_code)

        # refetch and check
        resp = self.app.get('/tasks/{:d}/'.format(task_id))
        self.assertEqual(200, resp.status_code)
        returned = load_json(resp.data)
        self.assertEqual(task_summary2, returned['summary'])
        self.assertEqual(task_description2, returned['description'])

    def test_update_task_not_found_returns_error(self):
        task_id = 0
        resp = self.app.put(
            '/tasks/{:d}/'.format(task_id),
            content_type='application/json',
            data = json.dumps({
                'summary': 'foo',
                'description': 'bar',
        }))
        self.assertEqual(404, resp.status_code)

    def test_wipe(self):
        # check test assumption
        resp = self.app.get('/tasks/')
        self.assertEqual(200, resp.status_code)
        self.assertEqual([], load_json(resp.data))
        # add items
        resp = self.app.post(
            '/tasks/',
            content_type='application/json',
            data = json.dumps({
                'summary': 'summary 1',
                'description': '',
        }))
        resp = self.app.post(
            '/tasks/',
            content_type='application/json',
            data = json.dumps({
                'summary': 'summary 2',
                'description': '',
        }))
        resp = self.app.get('/tasks/')
        self.assertEqual(200, resp.status_code)
        returned = load_json(resp.data)
        self.assertEqual(2, len(returned))


        # wipe all
        resp = self.app.delete('/tasks/ALL/')
        self.assertEqual(200, resp.status_code)

        resp = self.app.get('/tasks/')
        self.assertEqual(200, resp.status_code)
        returned = load_json(resp.data)
        self.assertEqual(0, len(returned))
