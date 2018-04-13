from flask import Flask
from flask import render_template, session, request
from flask import redirect, url_for, flash
from flask import send_from_directory
import os
#from vs_url_for import vs_url_for
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# defining which file types are allowed to be uploaded
def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/index')
@app.route('/')
def index():
    files = [os.path.join(UPLOAD_FOLDER, f) for f in os.listdir(UPLOAD_FOLDER)]
    return render_template('upload_index.html', files=files)


@app.route('/upload', methods = ['GET','POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('no file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('no selected file')
            return redirect(request.url)

        if not allowed_files(file.filename):
            flash('file type not allowed')
            return redirect(request.url)

        if file and allowed_files(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            flash('file "{}" successfully uploaded'.format(filename))
            return redirect(url_for('index'))

    return render_template('file_upload.html')


@app.route('/download/<filename>')
def download_file(filename):
    print(filename)
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
