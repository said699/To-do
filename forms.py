from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length, EqualTo
from models import Users

class RegisterForm(FlaskForm):
    name = StringField('Имя: ', validators=[DataRequired(), Length(min=3, max=100, message='Имя должно быть больше 3 и меньше 100 символов')])
    psw = PasswordField('Пароль: ', validators=[DataRequired(), Length(min=3, max=300, message='Пароль должен быть больше 3 и меньше 300 символов')])
    psw2 = PasswordField('Повтор пароля: ', validators=[DataRequired(), EqualTo('psw', message='Пароли не совпадают')])
    login = StringField('Логин: ', validators=[DataRequired(), Length(min=3, max=100, message='Логин должен быть больше 3 и меньше 100 символов')])
    submit = SubmitField('Зарегестрироваться')

    def validate_login(self, field):
        if Users.query.filter_by(login=field.data).first():
            raise ValidationError("Этот логин уже занят!")
        
