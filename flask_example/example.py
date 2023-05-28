from flask import Flask, request, make_response, render_template, \
                  redirect, url_for, flash, get_flashed_messages, session
import os
import json

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.secret_key = "secret_key"


@app.route('/')
def hello_world():
    return 'Hello Hexlet!'


@app.errorhandler(404)
def not_found(error):
    return 'Oops!', 404


@app.route('/users/<int:id>')
def get_user(id):
    users = load_users()
    for user in users:
        if user['id'] == str(id):
            return render_template('/users/show.html', user=user)
    return 'Page not found', 404
    

def load_users():
    try:
        users = json.loads(request.cookies.get('users', json.dumps([])))
    except:
        with open('flask_example/templates/users/users.json') as f:
            users = json.loads(f.read())
    return users


def validate(user):
    errors = []
    if len(user['first_name']) < 4:
        errors.append('Nickname must be greater than 4 characters')
        return errors


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
    errors = validate(user)
    if errors:
        return render_template(
            'users/new_user.html',
            user=user,
            errors=errors
        ), 422
    if users:
        user['id'] = str((int(users[-1]['id']) + 1))
    else:
        user['id'] = str(0)
    users.append(user)
    encoded_users = json.dumps(users)
    response = make_response(redirect(url_for('search_user')))
    response.set_cookie('users', encoded_users)
    return response


@app.route('/users/new_user')
def users_new():
    user = {'id': '', 
            'name': '',
            'tel': ''
    }
    errors = []
    return render_template(
        '/users/new_user.html',
        user=user,
        errors=errors
    )


@app.route('/users/<id>/edit')
def edit_user(id):
    users = load_users()
    for user in users:
        if user['id'] == str(id):
            user=user
    errors = []
    return render_template(
        'users/edit.html',
        user=user,
        errors=errors
    )

@app.route('/users/<id>/patch', methods=['POST'])
def patch_user(id):
    users = load_users()
    for user in users:
        if user['id'] == str(id):
            user = user
    data = request.form.to_dict()
    errors = validate(data)
    if errors:
        return render_template(
            'users/edit.html',
            user=user,
            errors=errors
        ), 422
    user['first_name'] = data['first_name']
    user['tel'] = data['tel']
    flash('User was updated successfully', 'success')
    encoded_users = json.dumps(users)
    response = make_response(redirect(url_for('search_user')))
    response.set_cookie('users', encoded_users)
    return response


@app.route('/users/<id>/delete', methods=['POST'])
def delete_user(id):
    users = load_users()
    for user in users:
        if user['id'] == str(id):
            users.remove(user)
    flash('User was removed successfully', 'success')
    encoded_users = json.dumps(users)
    response = make_response(redirect(url_for('search_user')))
    response.set_cookie('users', encoded_users)
    return response


@app.route('/login', methods = ['POST', 'GET'])
def user_login():
    message = ''
    session_status = 0
    users = load_users()
    tel = request.args.get('tel', '', type=str)
    session['users'] = []
    for user in users:
        print(f"{user['tel']} {tel}")
        if str(tel) == user['tel']:
            session['users'].append(user)
            session_status = 1
            flash(f"{user['first_name']} is successfully logged in")
            return redirect(url_for('search_user'))
    return render_template(
            'users/login.html',
            users=users,
            message=message,
            tel=tel
            )
