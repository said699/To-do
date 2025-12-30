# Импорты
from flask import Flask, render_template, flash, redirect, url_for, request, session, current_app
import os, datetime
from forms import RegisterForm, LoginForm, AddTaskForm
from models import Users, Todo
from flask_login import login_required, current_user, LoginManager, UserMixin, login_user, logout_user
from flask_bcrypt import Bcrypt 
from extensios import db
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from flask_admin.theme import Bootstrap4Theme
from admin import AdminModelView, TodoAdminIndexView
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError

# Конфигурации приложения
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['MAX_CONTENT_LENGTH'] = 5*1024*1024

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_INFO')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Создание авторизации
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Подключение к БД
db.init_app(app)
# Подключении к bcrypt для шифрования паролей
bcrypt = Bcrypt(app)
# Миграции
migrate = Migrate(app, db)

# Создание админки
admin = Admin(app, index_view=TodoAdminIndexView(), name='todolist-admin', theme=Bootstrap4Theme(swatch='cerulean'), url='/secret-admin-panel')
print('Admin init')
admin.add_view(AdminModelView(Users, db.session, name='Пользователи', endpoint='users'))
admin.add_view(AdminModelView(Todo, db.session, name='Todo', endpoint='todo'))

# Получение пользователя по Id, Flask-Login сам вызывает эту функцию, когда ему нужно
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Users, int(user_id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта!', 'success')
    return redirect(url_for('login'))

# Страница профиля
@app.route('/profile')
@login_required
def profile():
    tasks = Todo.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', tasks=tasks)

# Страница добавления задач
@app.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    form = AddTaskForm()
    if form.validate_on_submit():
        try:
            task = Todo(text = form.text.data, date_for_doing = form.date_for_doing.data, date_of_added=datetime.datetime.utcnow(), user_id=current_user.id, user=current_user)
            db.session.add(task)
            db.session.commit()
            flash('Задача добавлена успешно!', 'success')
            return redirect(url_for('profile    '))

        except SQLAlchemyError as e:
            db.session.rollback()
            flash("Ошибка при добавлении задачи", "error")
            print('Ошибка при добавлении задачи в БД ', str(e))
    
    return render_template('add_task.html', form=form)

# Страница авторизации
@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(login=form.login.data).first()
        if user and bcrypt.check_password_hash(user.psw, form.psw.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            if user.is_admin:
                return redirect(url_for('admin.index'))
            
            elif user.is_admin and next_page:
                return redirect(next_page)

            
            return redirect(request.args.get('next') or url_for('profile'))
        flash('Неверный логин или пароль!', 'error')
    
    else:
        print(form.errors)
    return render_template('login.html', form=form)

# Страница регестрации
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
            return redirect(url_for('login'))

        except Exception as e:
            db.session.rollback()
            flash("Не правильно заполненные поля", "error")
            print('Ошибка при добавлении в БД ', str(e))

    return render_template('register.html', form=form)

# Страница 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('not_found.html')

# Запуск приложения
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)