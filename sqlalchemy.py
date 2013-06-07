"""The application's model objects"""
from mymissedopportunities.model.meta import Session, Base

import sqlalchemy 
from sqlalchemy import types
from sqlalchemy.orm import relation, backref

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)

class User(Base):
    __tablename__ = "users"
    
    id = sqlalchemy.Column(types.Integer, primary_key=True)
    username = sqlalchemy.Column(types.Unicode(), unique=True, nullable=False)
    password = sqlalchemy.Column(types.Unicode())
    email = sqlalchemy.Column(types.Unicode())
    date_joined = sqlalchemy.Column(types.DateTime())
    last_login = sqlalchemy.Column(types.DateTime())
    

class Post(Base):
    __tablename__ = "posts"
    __mapper_args__ = dict(order_by="date desc")

    id = sqlalchemy.Column(types.Integer, primary_key=True)
    category = sqlalchemy.Column(types.Unicode())
    content = sqlalchemy.Column(types.UnicodeText())
    date = sqlalchemy.Column(types.DateTime())
    
    likes = sqlalchemy.Column(types.Integer)
    dislikes = sqlalchemy.Column(types.Integer)
    
    user_id = sqlalchemy.Column(types.Integer, sqlalchemy.ForeignKey('users.id'))
    user = relation(User, backref="posts")
   
class Comment(Base):
    __tablename__ = "comments"
    
    id = sqlalchemy.Column(types.Integer, primary_key=True)
    content = sqlalchemy.Column(types.UnicodeText())
    date = sqlalchemy.Column(types.DateTime())
    
    
    likes = sqlalchemy.Column(types.Integer)
    dislikes = sqlalchemy.Column(types.Integer)
    
    post_id = sqlalchemy.Column(types.Integer, sqlalchemy.ForeignKey('posts.id'))
    post = relation(Post, backref="comments")
    
    user_id = sqlalchemy.Column(types.Integer, sqlalchemy.ForeignKey('users.id'))
    user = relation(User, backref="comments")
    
    
   
class Feedback(Base):
    __tablename__ = "feedback"
    
    id = sqlalchemy.Column(types.Integer, primary_key=True)
    name = sqlalchemy.Column(types.Unicode(), unique=True, nullable=False)
    email = sqlalchemy.Column(types.Unicode())
    
    
    