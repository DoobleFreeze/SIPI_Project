from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired
from markupsafe import Markup


class ReviewForm(FlaskForm):
    stars = SelectField('Оценка', coerce=int)
    comment = TextAreaField('Отзыв', validators=[DataRequired()])
    submit = SubmitField("Опубликовать")
