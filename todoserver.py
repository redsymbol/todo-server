from flask import Flask
app = Flask(__name__)

@app.route('/items/', methods=['GET'])
def get_tasks():
    return 'GET /items'

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
