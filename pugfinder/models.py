from sqlalchemy.orm import relationship

from .database import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), index=True, primary_key=True)
    username = db.Column(db.String(26), index=True, unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128))
    salt = db.Column(db.String(29))
    preferred_role = db.Column(db.String(10))

    def __init__(self, username=None, email=None,
                 password=None, salt=None, preferred_role=None, id=None):
        self.username = username
        self.email = email
        self.password = password
        self.salt = salt
        self.preferred_role = preferred_role
        self.id = id

    def __repr__(self):
        return '<User %r>' % (self.username)


class Match(db.Model):
    __tablename__ = 'matches'
    id = db.Column(db.Integer, index=True, primary_key=True)
    is_active = db.Column(db.Boolean)
    is_public = db.Column(db.Boolean)
    map = db.Column(db.String(20))

    def __init__(self, is_active=None, is_public=None, map=None):
        self.is_active = is_active
        self.is_public = is_public
        self.map = map

    def __repr__(self):
        return '<Match %r>' % self.map
