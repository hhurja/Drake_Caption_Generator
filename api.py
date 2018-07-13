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

@app.route('/', methods=['POST'])
def get_caption():

    image = request.get_json()['string']
    image_64_decode = base64.b64decode(image)
    filename = 'images/temp.jpeg'

    image_result = open(filename, 'wb') 
    image_result.write(image_64_decode)

    print get_tags(filename, .75)

    tags = get_tags(filename, .9)
    emotion = str(get_key_emotions(filename, 3, .5))
    print emotion, tags
    print '-----------'

    return jsonify(
        caption=str(lookup.get_captions(emotion, tags))
    )


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