from flask_wtf import FlaskForm
from wtforms import validators, StringField, TextAreaField

# class AcceptFriendsForm(FlaskForm):
#
#

class AddFriendsForm(FlaskForm):
    username = StringField('', validators=[validators.Required()])
