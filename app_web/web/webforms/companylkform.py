from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, SubmitField, FileField, TextAreaField, MultipleFileField
from wtforms.validators import DataRequired


class CompanyLkForm(FlaskForm):
    name = StringField("Название", validators=[DataRequired()])
    about = TextAreaField("Описание", validators=[DataRequired()])
    phone_number = StringField("Телефон", validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired()])
    address = StringField("Адрес", validators=[DataRequired()])
    avatars = MultipleFileField('Обложка (5 изб.)')
    submit = SubmitField('Сохранить')
