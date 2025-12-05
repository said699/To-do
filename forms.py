from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class RegisterForm(FlaskForm):
    name = StringField('Имя: ', validators=[DataRequired(), Length(min=3, max=100, message='Имя должно быть больше 3 и меньше 100 символов')])
    psw = PasswordField('Пароль: ', validators=[DataRequired()])
    psw2 = PasswordField('Павтор пароля: ', validators=[DataRequired(), EqualTo('psw', message='Пароли не совпадают')])
    login = StringField('Логин: ', validators=[DataRequired(), Length(min=3, max=100, message='Логин должен быть больше 3 и меньше 100 символов')])
    submit = SubmitField('Зарегестрироваться')

