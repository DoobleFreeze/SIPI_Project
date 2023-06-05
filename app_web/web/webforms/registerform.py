from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    second_name = StringField("Фамилия", validators=[DataRequired()])
    first_name = StringField("Имя", validators=[DataRequired()])
    phone_number = StringField("Телефон", validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Регистрация')
