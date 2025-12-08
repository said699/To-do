from extensios import db
import datetime as dt

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    date_for_doing = db.Column(db.DateTime, nullable=False)
    date_of_added = db.Column(db.DateTime, default=dt.datetime.now(dt.UTC))

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    psw = db.Column(db.String(300), nullable=False)
    login = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)