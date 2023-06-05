from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class LkForm(FlaskForm):
    second_name = StringField("Фамилия", validators=[DataRequired()])
    first_name = StringField("Имя", validators=[DataRequired()])
    phone_number = StringField("Телефон", validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
