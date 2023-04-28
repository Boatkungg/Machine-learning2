from flask import Flask, request
import flask
import os

STATIC_FOLDER = "static"
UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, "upload")

ALLOWED_EXTENTIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__, static_folder="STATIC_FOLDER", template_folder=".", )
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER




@app.route('/')
def hello_world():
    return flask.render_template('index.html')


def check_allow_file(filename):
    if str(filename).split(".")[-1] in ALLOWED_EXTENTIONS:
        return True
    else:
        return False

@app.route("/test", methods=["GET", "POST"])
def test_index():
    if request.method == "POST":
        print(request.files)

    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    """


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)