from flask import Flask
import flask

app = Flask(__name__, template_folder=".")

@app.route('/')
def hello_world():
    return flask.render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)