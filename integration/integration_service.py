import os

from utils import login_utils
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin

HTML_PATH = os.path.abspath(os.path.dirname(__file__)) + '../frontend/'
app = Flask(__name__, template_folder=HTML_PATH, static_folder=HTML_PATH)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/login", methods=['POST', 'GET'])
@cross_origin()
def login():
    if request.method == 'GET':
        return render_template('index.html')
    response = login_utils.call_login(request)
    return response[0], response[1]


if __name__ == '__main__':
    app.run(host="0.0.0.0")
