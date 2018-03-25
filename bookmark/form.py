from flask_wtf import FlaskForm
from wtforms import validators, StringField, TextAreaField
from bookmark.models import Category

class ScrapeForm(FlaskForm):
    url = StringField('', validators=[
        validators.Required(),
        validators.URL(False, 'Please make sure you enter a valid URL...')
    ])
