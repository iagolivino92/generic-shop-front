import json
import requests
import os
import rsa
from Crypto.Cipher import AES
from dotenv import load_dotenv


def call_login(request=None):
    load_dotenv()
    if not request.authorization:
        try:
            r_data = {"username": request.form['user'], "password": request.form['pass']}
        except Exception as e:
            return f"Error while getting user and pass: {e}", e.code
    else:
        r_data = {'username': request.authorization['username'], 'password': request.authorization['password']}
    r_data = encrypt(requests.get('http://localhost:8081/pbc_k').text, str(r_data))
    login_request = requests.post("http://localhost:8081/perform_login", data=r_data, headers={'Content-Type': 'application/octet-stream'})
    if json.loads(login_request.text)['message']:
        return json.loads(login_request.text)['message'], login_request.status_code
    return json.loads(login_request.text)['token'], login_request.status_code


def encrypt(key, data):
    raw_key = key.split(",")
    public_key = rsa.PublicKey(int(raw_key[0].strip()), int(raw_key[1].strip()))
    return rsa.encrypt(data.encode(), public_key)
