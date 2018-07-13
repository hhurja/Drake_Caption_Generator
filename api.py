import os
import base64
import json
from flask import Flask, request, redirect, url_for, Response
from werkzeug.utils import secure_filename
from emotion import get_key_emotions
from object_recognition import get_tags
from caption_chooser import Lookup
from flask import jsonify

UPLOAD_FOLDER = './images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

csv = 'MakeItDrake.csv'
lookup = Lookup(csv)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        # if 'file' not in request.files:
        #     print 'No file part'
        #     print "no file in request.files"
        #     return redirect(request.url)
        # file = request.files['file']
        # # if user does not select file, browser also
        # # submit a empty part without filename
        # if file.filename == '':
        #     print 'No selected file'
        #     return redirect(request.url)
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        image = request.get_json()['string']
        # image = request.files['image']
        image_64_decode = base64.b64decode(image)
        filename = 'images/temp.jpeg'

        # image_string = base64.b64decode(image.read())
        image_result = open(filename, 'wb') # create a writable image and write the decoding result 
        image_result.write(image_64_decode)
        # filename = 'images/temp.jpeg'
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # return redirect(url_for('uploaded_file',
        #                         filename=filename))
        # print type(file), filename
        print get_tags(filename, .75)
        # print(str(get_key_emotions(filename, 3, .15)))
        # return str(get_key_emotions(filename, 3, .5))
        tags = get_tags(filename, .9)
        emotion = str(get_key_emotions(filename, 3, .5))
        print emotion, tags
        print '-----------'
        # data = 
        # response = app.response_class(
        #     response=json.dumps(data),
        #     status=200,
        #     mimetype='application/json'
        # )
        print type(jsonify(
            caption=str(lookup.get_captions(emotion, tags))
            ))
        return jsonify(
            caption=str(lookup.get_captions(emotion, tags))
            )
        resp = Response(str(lookup.get_captions(emotion, tags)))
        resp.headers['caption'] =  str(lookup.get_captions(emotion, tags))
        return resp
        # return str(lookup.get_captions(emotion, tags))
        # return {"caption", str(lookup.get_captions(emotion, tags))}
            # return 'success'
    # return 'fail'

@app.route('/test', methods=['POST'])
def test():
    print "Timmy hit me"
    print
    # print type(request.get_json()['string'])
    print '-----'

    image = request.get_json()['string']
    # image = request.files['image']
    image_64_decode = base64.b64decode(image)

    # image_string = base64.b64decode(image.read())
    image_result = open('test/temp.jpeg', 'wb') # create a writable image and write the decoding result 
    image_result.write(image_64_decode)






if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)