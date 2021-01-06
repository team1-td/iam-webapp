from flask import Flask, render_template, request, jsonify, url_for, flash, redirect
import os
from image import Image
from flask_dropzone import Dropzone
​
​
app = Flask(__name__)
app.secret_key = "team1_webapp"
​
app_root = os.path.dirname(os.path.abspath(__file__))
​
app.config.update(
    UPLOADED_PATH=os.path.join(app_root, 'user_images'),
    DROPZONE_MAX_FILE_SIZE=1024,
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILES=10,
    DROPZONE_UPLOAD_ON_CLICK=True
)
​
dropzone = Dropzone(app)
​
​
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
​
​
users = [User('sara', 'sara123'), User('marco', 'marco123'), User('stefan', 'stefan123'),
         User('lorenzo', 'lorenzo123'), User('alessio', 'alessio123'),
         User('diana', 'diana123'), User('nicolo', 'nicolo123'), User('nur', 'nur123')]
​
​
@app.route('/')
def index():
    return render_template('index.html')
​
​
@app.route('/home', methods=['POST'])
def home():
    username = request.form['username']
    password = request.form['password']
    for user in users:
        if user.username == username:
            if user.password == password:
                return render_template('upload.html', message=f'{username}')
            else:
                flash('Wrong password!')
                return render_template('index.html')
    else:
        flash('The username is not valid!')
        return redirect(url_for('index'))
​
​
@app.route('/logout', methods=['POST'])
def logout():
    flash('You have successfully logged out!')
    return redirect(url_for('index'))
​
​
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    user_images_path = os.path.join(app_root, 'user_images')
​
    if not os.path.isdir(user_images_path):
        os.mkdir(user_images_path)
​
    all_results = []
​
    result = {}
​
    for key, f in request.files.items():
        if key.startswith('file'):
            f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
​
        my_image_path = os.path.join(app.config['UPLOADED_PATH'], f.filename)
        image_name = f.filename
​
        image = Image(my_image_path)
        if image.is_image_format_valid():
            # image processing
            image.classify_image()
            result["image_name"] = image_name
            result["image_ia"] = image.classification
        else:
            # invalid format
            result["image_name"] = image_name
            result["image_ia"] = 'INVALID FORMAT'
​
        all_results.append(result)
        result = {}
​
    my_json = {}
    my_json["response"] = all_results
​
    # RESPONSE
    content, status_code = jsonify(my_json), 200
    headers = {'Access-Control-Allow-Origin': '*'}
    return content, status_code, headers
​
​
if __name__ == '__main__':
    app.run(debug=True)