from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired


class LkForm(FlaskForm):
    second_name = StringField("Фамилия", validators=[DataRequired()])
    first_name = StringField("Имя", validators=[DataRequired()])
    phone_number = StringField("Телефон", validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired()])
    avatar = FileField('Аватар', validators=[FileRequired()])
    submit = SubmitField('Сохранить')
