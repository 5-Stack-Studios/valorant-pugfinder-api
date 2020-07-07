from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from pugfinder.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, index=True, primary_key=True)
    username = Column(String(26), index=True, unique=True)
    email = Column(String(120), unique=True)
    hashed_pass = Column(String(128))
    # TODO: add salt
    preferred_role = Column(String(10))
    curr_match_id = Column(Integer, ForeignKey('matches.id'))

    def __init__(self, username=None, email=None,
                 hashed_pass=None, preferred_role=None):
        self.username = username
        self.email = email
        self.hashed_pass = hashed_pass
        self.preferred_role = preferred_role

    def __repr__(self):
        return '<User %r>' % (self.username)


class Match(Base):
    __tablename__ = 'matches'
    id = Column(Integer, index=True, primary_key=True)
    is_active = Column(Boolean)
    is_public = Column(Boolean)
    map = Column(String(20))
    players = relationship('User', backref='player')

    def __init__(self, is_active=None, is_public=None, map=None):
        self.is_active = is_active
        self.is_public = is_public
        self.map = map

    def __repr__(self):
        return '<Match %r>' % self.map
