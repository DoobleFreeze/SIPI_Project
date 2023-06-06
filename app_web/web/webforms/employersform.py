from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class EmployersForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    submit = SubmitField('Пригласить')
