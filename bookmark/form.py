from flask_wtf import FlaskForm
from wtforms import validators, StringField, TextAreaField
from flask_wtf.file import FileField, FileAllowed

from bookmark.models import Category

class SearchForm(FlaskForm):
    search = StringField('', validators=[validators.Required()])


class ScrapeForm(FlaskForm):
    url = StringField('', validators=[
        validators.Required(),
        validators.URL(False, 'Please make sure you enter a valid URL...')
    ])

class EditForm(FlaskForm):
    name = StringField('Name', validators=[validators.Required()])
    image = StringField('Image URL', validators=[
        validators.URL(False, 'Please make sure you enter a valid URL...')
    ])
    image_upload = FileField('Image Upload', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    category = StringField('Category', validators=[validators.Required()])
