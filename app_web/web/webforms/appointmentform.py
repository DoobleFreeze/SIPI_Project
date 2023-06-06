from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired


class AppointmentForm(FlaskForm):
    user_comment = TextAreaField("Комментарий", validators=[DataRequired()])
    submit = SubmitField('Записаться')
