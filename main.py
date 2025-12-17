from flask import Flask, render_template, flash, redirect, url_for, request
import os, datetime
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm, LoginForm
from models import Users, Todo
from flask_login import login_required, current_user, LoginManager, UserMixin, login_user, logout_user
from flask_bcrypt import Bcrypt 
from extensios import db

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['MAX_CONTENT_LENGTH'] = 5*1024*1024

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_INFO')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)
login_manager.login_view = 'login'
db.init_app(app)
bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта!', 'success')
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    
    return render_template('profile.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(login=form.login.data).first()
        if user and bcrypt.check_password_hash(user.psw, form.psw.data):
            login_user(user, remember=form.remember.data)
            return redirect(request.args.get('next') or url_for('profile'))
        flash('Неверный логин или пароль!', 'error')
    
    else:
        print(form.errors)
    return render_template('login.html', form=form)

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            hash_pass = bcrypt.generate_password_hash(form.psw.data).decode('utf-8')
            user = Users(login=form.login.data, name=form.name.data, psw=hash_pass)
            db.session.add(user)
            db.session.flush()
            db.session.commit()
            flash('Вы успешно зарегестрировались!', 'success')
            print(user.psw)
            return redirect(url_for('login'))

        except Exception as e:
            db.session.rollback()
            flash("Не правильно заполненные поля", "error")
            print('Ошибка при добавлении в БД ', str(e))

    return render_template('register.html', form=form)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('not_found.html')


if __name__ == '__main__':
    app.run(debug=True)