from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired


class CompanyForm(FlaskForm):
    name = StringField("Название компании", validators=[DataRequired()])
    about = TextAreaField("О компании", validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired()])
    phone_number = StringField("Телефон", validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    type_app = SelectField('Тип организации', coerce=int)
    submit = SubmitField('Регистрация')
