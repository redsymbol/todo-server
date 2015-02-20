from flask import Flask
app = Flask(__name__)

@app.route('/items')
def get_tasks():
    return 'GET /items'

if __name__ == '__main__':
    app.run(debug=True)
