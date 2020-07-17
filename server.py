import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from pugfinder import app, socketio
from pugfinder.database import db

migrate = Migrate(app, db)
manager = Manager(app)

server = os.environ['MYSQL_SERVER']
username = os.environ['MYSQL_USERNAME']
password = os.environ['MYSQL_PASSWORD']
database = os.environ['MYSQL_DB']
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{username}:{password}@{server}/{database}'

db.init_app(app)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    socketio.run(app)

if __name__ == "__main__":
    manager.run()
