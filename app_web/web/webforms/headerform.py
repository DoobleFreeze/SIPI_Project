from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired
from markupsafe import Markup


class HeaderForm(FlaskForm):
    type_app = SelectField('Тип организации', coerce=int)
    search = StringField('Поиск', validators=[DataRequired()])
    submit = SubmitField(Markup('search'))
