from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Regexp, Length, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),
                                             Email(),
                                             Length(1, 64)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(),
                                                   Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                        'Имя пользователя должно содержать только латиницу, '
                                                        'цифры, точки или подчёркивания')])
    email = StringField('Email', validators=[DataRequired(),
                                             Email(),
                                             Length(1, 64)])
    password = PasswordField('Пароль', validators=[DataRequired(),
                                                 EqualTo('password2', message='Пароли должны совпадать.')])
    password2 = PasswordField('Подтвердите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрировать')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Пользователь с таким именем уже зарегистрирован.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Указанный email уже используется.')
