from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class CompanyAppointmentForm(FlaskForm):
    org_data = StringField('Дата записи', validators=[DataRequired()])
    org_time = StringField('Время записи', validators=[DataRequired()])
    org_comment = TextAreaField("Комментарий", validators=[DataRequired()])
    submit = SubmitField('Подтвердить')
