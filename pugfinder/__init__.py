import os
import random
import bcrypt
import uuid
import jwt

from flask import Flask, request, abort, jsonify
from flask_socketio import SocketIO, emit

from pugfinder.models import User
from pugfinder.database import db

AGENTS = [ "breach",
  "brimstone",
  "cypher",
  "jett",
  "omen",
  "phoenix",
  "raze",
  "reyna",
  "sage",
  "sova",
  "viper"
]

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

def create_session_token(user):
    return jwt.encode(
                {
                    "user": {
                    "id": str(user.id),
                    "name": user.username}
                }, app.config.get("SECRET_KEY"))

# a simple page that says hello
@app.route('/api')
def hello():
    return 'Hello, World!'

@app.route('/api/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        data = request.get_json()
        required_params = {"username", "email", "password"}
        if set(data.keys()) == required_params:
            # Add password security measures
            raw_pass = data["password"].encode()
            salt = bcrypt.gensalt()
            hashed_pass = bcrypt.hashpw(raw_pass, salt).decode('utf-8')
            user = User(username=data['username'],
                        password=hashed_pass,
                        salt=salt.decode('utf-8'),
                        email=data['email'],
                        id = str(uuid.uuid4()))

            db.session.add(user)
            db.session.commit()

            token = jwt.encode(
                {
                    "user": {
                    "id": str(user.id),
                    "name": user.username}
                }, app.config.get("SECRET_KEY"))

            return jsonify({'token': token.decode()})
    elif request.method == 'GET':
        # TODO: Return list of users
        pass

@app.route('/api/login', methods=["POST"])
def login():
    data = request.get_json()
    required_params = {"email", "password"}
    if set(data.keys()) == required_params:
        user = User.query.filter_by(email=data["email"]).first()
        if user and bcrypt.checkpw(data["password"].encode(), user.password.encode()):
            # Authenticated
            return jsonify({
                'token': create_session_token(user).decode('utf-8')
            })
        else:
            # Access denied
            abort(401)
    abort(400)



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
            'team1': [{'name': 'pattyjogal', 'selectedRole': random.choice(AGENTS)} for i in range(5)],
            'team2': [{'name': 'pattyjogal', 'selectedRole': random.choice(AGENTS)} for i in range(5)],
            'queue': {agent: [] for agent in AGENTS}
        }
    }, broadcast=True)

@socketio.on('message')
def mesg(message):
    print(message)

@socketio.on('connect')
def on_connect():
    print('connected')