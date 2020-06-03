from sqlalchemy import Column, String, Integer
from pugfinder.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, index=True, primary_key=True)
    username = Column(String(26), index=True, unique=True)
    email = Column(String(120), unique=True)
    hashed_pass = Column(String(128))
    preferred_role = Column(String(10))

    def __init__(self, username=None, email=None, hashed_pass=None, preferred_role=None):
        self.username = username
        self.email = email
        self.hashed_pass = hashed_pass
        self.preferred_role = preferred_role

    def __repr__(self):
        return '<User %r>' % (self.username)
