from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired


class LkPasForm(FlaskForm):
    password_now = PasswordField('Текущий пароль', validators=[DataRequired()])
    password = PasswordField('Новый пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите новый пароль', validators=[DataRequired()])
    submit = SubmitField('Изменить')
