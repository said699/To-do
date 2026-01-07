# Импорты
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateTimeLocalField, TextAreaField
from wtforms.validators import ValidationError, InputRequired, DataRequired, Length, EqualTo
from models import Users
from datetime import datetime as dt
from datetime import timezone as tz

# Форма для страницы регистрации
class RegisterForm(FlaskForm):
    name = StringField('Имя: ', validators=[DataRequired(), Length(min=3, max=100, message='Имя должно быть больше 3 и меньше 100 символов')])
    psw = PasswordField('Пароль: ', validators=[DataRequired(), Length(min=3, max=300, message='Пароль должен быть больше 3 и меньше 300 символов')])
    psw2 = PasswordField('Повтор пароля: ', validators=[DataRequired(), EqualTo('psw', message='Пароли не совпадают')])
    login = StringField('Логин: ', validators=[DataRequired(), Length(min=3, max=100, message='Логин должен быть больше 3 и меньше 100 символов')])
    submit = SubmitField('Зарегестрироваться')

    # Проверка на уникальность login
    def validate_login(self, login):
        existing_user_login = Users.query.filter_by(login=login.data).first()
        
        if existing_user_login:
            raise ValidationError("Этот логин уже занят!")
        
# Форма для страницы авторизации
class LoginForm(FlaskForm):
    psw = PasswordField('Пароль: ', validators=[DataRequired()])
    login = StringField('Логин: ', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

# Форма для страницы добавления задач
class AddTaskForm(FlaskForm):
    text = StringField('Текст задачи: ', validators=[DataRequired(), Length(min=3, max=300, message='Текст задачи должен быть больше 3 и меньше 300 символов')])
    date_for_doing = DateTimeLocalField('Дата или срок выполнееия: ', format='%Y-%m-%dT%H:%M', validators=[InputRequired()])
    additional_information = TextAreaField('Дополнительная информация', validators=[DataRequired(), Length(min=3, max=1000, message='Дополнительная информация о задаче должна быть больше 3 и меньше 1000 символов')])
    submit = SubmitField('Добавить задачу')

    def validate_date_for_doing(self, field):
        user_local_dt = field.data
        user_utc_dt = user_local_dt.replace(tzinfo=tz.utc)
        now_utc = dt.now(tz.utc)

        if user_utc_dt < now_utc:
            raise ValidationError('Пожалуйста, выберите дату и время в будущем')


class DeleteAllTasksForm(FlaskForm):
    submit = SubmitField('Удалить все задачи')
