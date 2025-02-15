from flask import request
from app import app

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return 'Hello, World!'
    elif request.method == 'POST':
        return 'Hello, World! (POST-запрос)'
    else:
        return 'Неизвестный метод запроса'