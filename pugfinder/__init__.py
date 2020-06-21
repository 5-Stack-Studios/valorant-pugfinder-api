import os
import bcrypt

from flask import Flask, request
from flask_socketio import SocketIO, emit

from pugfinder.database import init_db
from pugfinder.models import User


# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

# if test_config is None:
#     # load the instance config, if it exists, when not testing
#     app.config.from_pyfile('config.py', silent=True)
# else:
#     # load the test config if passed in
#     app.config.from_mapping(test_config)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

init_db()

# a simple page that says hello
@app.route('/api')
def hello():
    return 'Hello, World!'

@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        data = request.get_json()
        required_params = set("username", "email", "password")
        if set(data.keys()) == required_params:
            # Add password security measures
            raw_pass = data["password"]
            salt = bcrypt.gensalt()
            hashed_pass = bcrypt.hashpw(raw_pass, salt).decode('utf-8')

            user = User(username=data['username'],
                        password=hashed_pass,
                        salt=salt.decode('utf-8'),
                        email=data['email'])

        # TODO: Construct JWT and send back
    elif request.method == 'GET':
        # TODO: Return list of users
        pass



# Temporary measure; should eventually be replaced with
# a value from the config
socketio = SocketIO(app, cors_allowed_origins="*")

cnt = 0

@socketio.on('lobby.create')
def create_lobby(data):
    global cnt
    cnt += 1
    emit('lobby.create.success', {
        'error': False,
        'payload': {
            'id': cnt,
            'owner': data['owner'],
            'map': data['map'],
            'team1': [],
            'team2': [],
            'queue': {
                
            }
        }
    }, broadcast=True)

@socketio.on('message')
def mesg(message):
    print(message)

@socketio.on('connect')
def on_connect():
    print('connected')