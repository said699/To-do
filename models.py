from extensios import db
import datetime as dt
from flask_login import UserMixin

class Todo(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    date_for_doing = db.Column(db.DateTime, nullable=False)
    date_of_added = db.Column(db.DateTime, default=dt.datetime.now(dt.UTC))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('Users', back_populates='tasks')

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    psw = db.Column(db.String(300), nullable=False)
    login = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)    
    is_admin = db.Column(db.Boolean, default=False)
    tasks = db.relationship('Todo', lazy=True, back_populates='user')