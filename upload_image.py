import os

import numpy as np
from flask import Flask, request, flash, send_file, jsonify
import cv2

app = Flask(__name__)

app.config["IMAGE_UPLOADS"] = "E:/projects/clippingpath/"
app.secret_key = "super secret key"


def find_bezier_points(text_name, image):

    height, width, s = image.shape
    height = int(height / 2)
    width = int(width / 2)
    image = cv2.resize(image, (height, height))
    h = height
    w = width
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    grayscale = cv2.cvtColor(grayscale, cv2.COLOR_RGB2GRAY)

    blur = cv2.blur(grayscale, (5, 5))
    # get threshold image
    r, thresh_img = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY)

    kernel = np.ones((5, 5), np.uint8)
    erosion = cv2.erode(thresh_img, kernel, iterations=1)

    contours, _ = cv2.findContours(erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    font = cv2.FONT_HERSHEY_DUPLEX
    points = []
    # print(contours)
    if os.path.exists(text_name):
        os.remove(text_name)

    for cnt in contours:
        # print(len(cnt))
        epsilon = 0.0001 * cv2.arcLength(cnt, True)  # adjust arcLength for controlling number of points
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # create an empty image for contours
        img_contours = np.zeros(image.shape)
        # draw the contours on the empty image
        final = cv2.drawContours(img_contours, [approx], 0, (200, 0, 0), 3)

        # Used to flatted the array containing
        # the co-ordinates of the vertices.
        n = approx.ravel()
        i = 0
        x_coordinate1 = 0.0
        y_coordinate1 = 0.0
        x1 = []
        y1 = []
        for j in n:
            if i % 2 == 0:
                x = n[i]
                y = n[i + 1]
                if i == 0:
                    x_1 = n[0]
                    y_1 = n[1]
                    x_coordinate1 = x_1 / h
                    y_coordinate1 = y_1 / h
                    string_0 = str(x_coordinate1) + 'f' + "," + str(y_coordinate1) + 'f'
                # x1.append(x)
                # y1.append(y)
                x_coordinate = x / h
                y_coordinate = y / h
                x1.append(x_coordinate)
                y1.append(y_coordinate)

                string = str(x_coordinate) + 'f' + "," + str(y_coordinate) + 'f' + ","

                with open(text_name, 'a+') as the_file:
                    the_file.write(string)
                    the_file.write('\n')
            i = i + 1

        x1.append(x_coordinate1)
        y1.append(y_coordinate1)

        with open(text_name, 'a+') as the_file:
            the_file.write(string_0)
            the_file.write('\n')


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

        find_bezier_points(text_name, image)

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
            find_bezier_points(text_name, image)
            #send_file(text_name, as_attachment=True)

        if success:
            resp = jsonify({'message': 'Files successfully uploaded'})
            resp.status_code = 201
            return resp
            # print(url_for('upload-image'))
    return "OK"
    
    
if __name__ == '__main__':
    app.run(debug=True)