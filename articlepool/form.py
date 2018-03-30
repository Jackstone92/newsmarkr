from flask_wtf import FlaskForm
from wtforms import validators, StringField, TextAreaField

class LiveCommentForm(FlaskForm):
    comment = TextAreaField('', validators=[validators.Required()])
