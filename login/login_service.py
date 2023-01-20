import os

from flask import Flask, request
from flask_cors import CORS, cross_origin

from login import login_lib

HTML_PATH = os.path.abspath(os.path.dirname(__file__)) + '/../frontend/'
app = Flask(__name__, template_folder=HTML_PATH, static_folder=HTML_PATH)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/perform_login", methods=['POST'])
@cross_origin()
def perform_login():
    response = login_lib.generate_token_by_user(request.json)
    return response[0], response[1]


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081)
