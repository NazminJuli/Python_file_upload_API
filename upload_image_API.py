import os

import numpy as np
from flask import Flask, request, flash, send_file, jsonify
import cv2

app = Flask(__name__)

app.config["IMAGE_UPLOADS"] = "E:/projects/clippingpath/"
app.secret_key = "super secret key"


@app.route('/', methods=['GET'])
def index():
    return "Hello Flask!"


@app.route('/Hello')
def hello_world():
    return app.config['IMAGE_UPLOADS']

#@app.route("/test", methods=['POST'])
#def test_method():
#    imagefile = request.files['files']
#    imagefile.save(app.config["IMAGE_UPLOADS"]+imagefile.filename)
#    return "OK", 200


@app.route("/upload-image", methods=['POST'])
def upload_image():
    if request.method == 'POST':
        # This will be executed on POST request.
        file = request.files['files']

        text_name = file.filename + '_bezier' + '.txt'
        file.save(app.config['IMAGE_UPLOADS'] + file.filename)
        flash("File uploaded: Thanks!", "success")
        image = cv2.imread(app.config['IMAGE_UPLOADS'] + file.filename)

        
        return send_file(text_name, as_attachment=True)


@app.route("/upload-multiple", methods=['POST'])
def upload_multiple():
    if request.method == 'POST':
        # This will be executed on POST request.
        files = request.files.getlist('files')
        success = False

        for each_file in files:
            text_name = each_file.filename + '_bezier' + '.txt'
            each_file.save(app.config['IMAGE_UPLOADS'] + each_file.filename)
            image = cv2.imread(app.config['IMAGE_UPLOADS'] + each_file.filename)
            success = True

        if success:
            resp = jsonify({'message': 'Files successfully uploaded'})
            resp.status_code = 201
            return resp
            # print(url_for('upload-image'))
    return "OK"
    
    
if __name__ == '__main__':
    app.run(debug=True)