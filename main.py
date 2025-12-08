from flask import Flask, render_template, flash, redirect, url_for
import os, datetime
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm
from werkzeug.security import generate_password_hash
from models import Users, Todo
from extensios import db

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['MAX_CONTENT_LENGTH'] = 5*1024*1024

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_INFO')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

print("DEBUG:", os.environ.get("DATABASE_INFO"))
db.init_app(app)


@app.route('/profile')
def profile():
    return render_template('profile.html')

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
            flash('Вы успешно зарегестрировались!', 'success')
            return redirect(url_for('profile'))

        except Exception as e:
            db.session.rollback()
            flash("Не правильно заполненные поля", "error")
            print('Ошибка при добавлении в БД ', str(e))

    return render_template('register.html', form=form)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('not_found.html'), 404


if __name__ == '__main__':
    app.run(debug=True)