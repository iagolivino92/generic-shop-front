import os

import requests
from flask import Flask, request
from flask_cors import CORS, cross_origin

from mbway import send_utils
from dotenv import load_dotenv

HTML_PATH = os.path.abspath(os.path.dirname(__file__)) + '/../frontend/'
app = Flask(__name__, template_folder=HTML_PATH, static_folder=HTML_PATH)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
load_dotenv()


@app.route("/mb_request")
@cross_origin()
def send_mb_request():
    # get all the args and sent it to the mb api (external)
    parsed_args = send_utils.parse_args(request.args)
    response = requests.get(f'https://catfact.ninja/fact?{parsed_args}')
    # treat the response and return
    parse_response = send_utils.parse_response(response)
    return parse_response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8082)
