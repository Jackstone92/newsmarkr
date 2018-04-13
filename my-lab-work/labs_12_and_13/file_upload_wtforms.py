from flask import Flask
from flask import render_template, session, request
from flask import redirect, url_for, flash
from flask import send_from_directory
import os
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
from wtforms import validators

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = 'static/uploads'

class UploadForm(FlaskForm):
    file = FileField('image', validators=[
        FileRequired(),
        FileAllowed(['jpg','png'], 'Images only!')])
    submit = SubmitField('submit', [validators.DataRequired()])

app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/')
def index():
    files = [os.path.join(UPLOAD_FOLDER,f) for f in os.listdir(UPLOAD_FOLDER)]
    return render_template('upload_index.html', files=files)


@app.route('/upload', methods = ['GET','POST'])
def upload_image():
    form = UploadForm()
    if form.validate_on_submit():
        upload = form.file.data
        filename = secure_filename(upload.filename)
        upload.save(os.path.join(UPLOAD_FOLDER,filename))
        flash('File "{}" successfully uploaded'.format(filename))
        return redirect(url_for('index'))
    return render_template('file_upload_wtforms.html',form=form)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)
