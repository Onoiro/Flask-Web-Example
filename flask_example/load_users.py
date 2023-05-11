import json

def load_users():
    filename = 'users.json'
    with open(filename) as f:
        users = (json.loads(f.read()))
    return users

users = load_users()
print(users)


# filename = '/home/abo/hexlet-flask-example/flask_example/flask_example/users.json'
# with open(filename) as f:
#     users = json.loads(f.read())