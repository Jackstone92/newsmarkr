from flask_wtf import FlaskForm
from wtforms import validators, RadioField, SelectField, SelectMultipleField, StringField, TextAreaField
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField, FileAllowed

# for list comprehension
from profile.models import POLITICAL_SPECTRUM, POLITICAL_PARTIES, FAVOURITE_NEWS_WEBSITES

class AddFriendsForm(FlaskForm):
    username = StringField('', validators=[validators.Required()])


class EditProfilePicture(FlaskForm):
    profile_picture = StringField('Image URL', validators=[
        validators.URL(False, 'Please make sure you enter a valid URL...')
    ])
    profile_picture_upload = FileField('Image Upload', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])

class EditCoverPhoto(FlaskForm):
    cover_photo = StringField('Image URL', validators=[
        validators.URL(False, 'Please make sure you enter a valid URL...')
    ])
    cover_photo_upload = FileField('Image Upload', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])

class EditAbout(FlaskForm):
    birthday = DateField('Birthday', validators=[validators.Required()])
    political_spectrum = SelectField('Where you are on the political spectrum', choices=[
        (key, POLITICAL_SPECTRUM[key]) for key in POLITICAL_SPECTRUM
    ], validators=[validators.Required()])

    political_party = SelectField('Political party that you support', choices=[
        (key, POLITICAL_PARTIES[key]) for key in POLITICAL_PARTIES
    ], validators=[validators.Required()])

    favourite_news_websites = SelectMultipleField('Favourite news websites (for multiple choices, hold "cmd" or "ctrl" key)', choices=[
        (key, FAVOURITE_NEWS_WEBSITES[key]) for key in FAVOURITE_NEWS_WEBSITES
    ], validators=[validators.Required()])

    allow_location_detection = RadioField('Allow NewsmarkR to display local news for you?', choices=[('yes', 'Yes (recommended)'), ('no', 'No')], default='yes', validators=[validators.DataRequired()])
