from flask import Flask, render_template, request, jsonify, url_for, flash, redirect
import os
from image import Image
from flask_dropzone import Dropzone


app = Flask(__name__)
app.secret_key = "team1_webapp"

app_root = os.path.dirname(os.path.abspath(__file__))

app.config.update(
    UPLOADED_PATH=os.path.join(app_root, 'user_images'),
    DROPZONE_MAX_FILE_SIZE=1024,
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILES=10,
    DROPZONE_UPLOAD_ON_CLICK=True
)

dropzone = Dropzone(app)


class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password


users = [User('sara@gmail.com', 'sara123'), User('marco@gmail.com', 'marco123'), User('stefan@gmail.com', 'stefan123'),
         User('lorenzo@gmail.com', 'lorenzo123'), User('alessio@gmail.com', 'alessio123'),
         User('diana@gmail.com', 'diana123'), User('nicolo@gmail.com', 'nicolo123'), User('nur@gmail.com', 'nur123')]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home', methods=['POST'])
def home():
    email = request.form['email']
    password = request.form['password']
    for user in users:
        if user.email == email:
            if user.password == password:
                return render_template('upload.html', message=f'{email}')
            else:
                flash('Wrong password!')
                return render_template('index.html')
    else:
        flash('The email is not valid!')
        return redirect(url_for('index'))


@app.route('/logout', methods=['POST'])
def logout():
    flash('You have successfully logged out!')
    return redirect(url_for('index'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    user_images_path = os.path.join(app_root, 'user_images')

    if not os.path.isdir(user_images_path):
        os.mkdir(user_images_path)

    result = {
        fileName: "",
        resultIA: ""
    }

    for key, f in request.files.items():
        if key.startswith('file'):
            f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))

        my_image_path = os.path.join(app.config['UPLOADED_PATH'], f.filename)
        result.fileName = f.filename

        image = Image(my_image_path)
        if image.is_image_format_valid():
            # image processing
            image.classify_image()
            result.resultIA = image.classification
        else:
            # invalid format
            result.fileName = 'INVALID FORMAT'

    # RESPONSE
    content, status_code = jsonify(result), 200
    headers = {'Access-Control-Allow-Origin': '*'}
    return content, status_code, headers

if __name__ == '__main__':
    app.run(debug=True)
