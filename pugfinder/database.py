import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

server = os.environ['MYSQL_SERVER']
username = os.environ['MYSQL_USERNAME']
password = os.environ['MYSQL_PASSWORD']
db = os.environ['MYSQL_DB']

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{username}:{password}@{server}/{db}'

db = SQLAlchemy(app)
