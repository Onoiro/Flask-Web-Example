from flask import Flask, request, make_response, render_template, \
                  redirect, url_for, flash, get_flashed_messages
#from data import UserRepository
import os
import json

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.secret_key = "secret_key"

# users = [{'first_name': 'mike', 'tel': '89036259090'},
#          {'first_name': 'mishel', 'tel': '89036665555'},
#          {'first_name': 'adel', 'tel': '89036201111'},
#          {'first_name': 'keks', 'tel': '89152224444'},
#          {'first_name': 'kamila', 'tel': '8902553333'}
#     ]


@app.route('/')
def hello_world():
    return 'Hello Hexlet!'


# @app.route('/json/')
# def json():
#     return {'json': 42} # Возвращает тип application/json


@app.errorhandler(404)
def not_found(error):
    return 'Oops!', 404


@app.route('/foo')
def foo():
    response = make_response('foo')
    # Устанавливаем заголовок
    response.headers['X-Parachutes'] = 'parachutes are cool'
    # Меняем тип ответа
    response.mimetype = 'text/plain'
    # Задаем статус
    response.status_code = 418
    # Устанавливаем cookie
    response.set_cookie('foo', 'bar')
    return response


@app.route('/users/<id>')
def get_user(id):
    return render_template('users/show.html', name=id)


def load_users():
    #filename = 'users.json'
    with open('flask_example/templates/users/users.json') as f:
        users = json.loads(f.read())
    return users


@app.route('/users/')
def search_user():
    term = request.args.get('term', '', type=str)
    messages = get_flashed_messages(with_categories=True)
    users = load_users()
    filtered_users = []
    for user in users:
        pattern = user['first_name']
        if term == pattern[:len(term)]:    
            filtered_users.append(user)
    return render_template(
        'index.html',
        messages=messages,
        users=filtered_users,
        search=term
    )


@app.post('/users/')
def users_post():
    users = load_users()
    user = request.form.to_dict()
    user['id'] = str((int(users[-1]['id']) + 1))
    users.append(user)
    flash('User was added successfully', 'Message')
    with open('flask_example/templates/users/users.json', 'w') as f:
        f.write(json.dumps(users)) 
    return redirect(
        url_for('search_user'),
        code=302
    )


@app.route('/users/new_user')
def users_new():
    user = {'id': '', 
            'name': '',
            'tel': ''
    }
    return render_template(
        '/users/new_user.html',
        user=user
    )
