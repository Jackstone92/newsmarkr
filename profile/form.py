from flask_wtf import FlaskForm
from wtforms import validators, StringField, TextAreaField
from flask_wtf.file import FileField, FileAllowed

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
