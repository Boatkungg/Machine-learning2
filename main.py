from flask import Flask, request, flash, redirect, url_for
import flask
from werkzeug.utils import secure_filename

import tensorflow as tf
from tensorflow import keras

from time import time
import os

STATIC_FOLDER = "static"
UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, "upload")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__, static_folder="STATIC_FOLDER", template_folder=".", )
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

rock_model = tf.saved_model.load("rock_resnet")

@app.route('/')
def hello_world():
    return flask.render_template('index.html')


def check_allow_file(filename):
    if str(filename).split(".")[-1] in ALLOWED_EXTENSIONS:
        return True
    else:
        return False

@app.route("/test", methods=["GET", "POST"])
def test_index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("no file provided")
            return redirect(request.url)

        image = request.files['file']

        if image.filename == "":
            flash("no file provided")
            return redirect(request.url)

        if image and check_allow_file(image.filename):
            image_name = secure_filename(f"{round(time())}.{str(image.filename).split(".")[-1]}")
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], image_name))
            return redirect(url_for('inference', filename=image_name))



    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    """

@app.route("/inference/<filename>")
def inference(filename):
    if str(filename).split(".")[-1] not in ALLOWED_EXTENSIONS:
        flash("file extension not supported")
        # TODO: change this in future
        return redirect(url_for("test_index"))

    try:
        img = keras.utils.load_image(
            os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(filename)),
            target_size=(224, 224))
    # TODO: may check this in future
    except FileNotFoundError:
        flash("file not found")
        # TODO: change this in future
        return redirect(url_for("test_index"))

    input_array = keras.utils.img_to_array(img)

    prediction, label = rock_model(input_array)

    label = [i.numpy().decode("utf-8") for i in label]
    
    # TODO: change this in future
    return redirect(url_for("test_index", label[prediction.numpy().argmax()]))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)