import unittest
import json
import todoserver

def load_json(data):
    return json.loads(data.decode('utf-8'))

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = todoserver.app.test_client()
        todoserver.store.clear()

class TestTodo(FlaskTestCase):
    def test_get_tasks(self):
        resp = self.app.get('/items/')
        self.assertEqual(200, resp.status_code)
        self.assertEqual([], load_json(resp.data))
        
    def test_describe_task(self):
        resp = self.app.get('/items/42/')
        self.assertEqual(200, resp.status_code)
        self.assertEqual(b'GET /items/42/', resp.data)

    def test_add_task(self):
        resp = self.app.post('/items/')
        self.assertEqual(200, resp.status_code)
        self.assertEqual(b'POST /items/', resp.data)

    def test_task_done(self):
        resp = self.app.delete('/items/42/')
        self.assertEqual(200, resp.status_code)
        self.assertEqual(b'DELETE /items/42/', resp.data)

    def test_update_task(self):
        resp = self.app.put('/items/42/')
        self.assertEqual(200, resp.status_code)
        self.assertEqual(b'PUT /items/42/', resp.data)


