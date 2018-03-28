from flask_wtf import FlaskForm
from wtforms import validators, StringField, TextAreaField

class PostForm(FlaskForm):
    url = StringField('', validators=[
        validators.Required(),
        validators.URL(False, 'Please make sure you enter a valid URL...')
    ])
    post = TextAreaField('', validators=[validators.Required()])

class CommentForm(FlaskForm):
    comment = TextAreaField('', validators=[validators.Required()])
