import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from emotion import get_key_emotions
from object_recognition import get_tags

UPLOAD_FOLDER = './images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print 'No file part'
            print "no file in request.files"
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print 'No selected file'
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
            # print type(file), filename
            print get_tags(filename, .9)
            print(str(get_key_emotions(filename, 3, .15)))
            return str(get_key_emotions(filename, 3, .15))
            # return 'success'
    return 'fail'

app.route('/emotion', methods=['GET'])
def hit_azure():
	pass


if __name__ == '__main__':
	app.run(debug=True)