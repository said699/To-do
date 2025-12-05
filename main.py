from flask import Flask, render_template, flash
import os, datetime
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['MAX_CONTENT_LENGTH'] = 5*1024*1024

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_INFO')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

print("DEBUG:", os.environ.get("DATABASE_INFO"))

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    date_for_doing = db.Column(db.DateTime, nullable=False)
    date_of_added = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    psw = db.Column(db.String(300), nullable=False)
    login = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            hash_pass = generate_password_hash(form.psw.data)
            user = Users(login=form.login.data, name=form.name.data, psw=hash_pass)
            db.session.add(user)
            db.session.flush()
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            flash("Не правильно заполненные поля", "error")
            print('Ошибка при добавлении в БД ', str(e))

    return render_template('register.html', form=form)

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('not_found.html'), 404


if __name__ == '__main__':
    app.run(debug=True)