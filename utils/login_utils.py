import json
import requests
import os
from Crypto.Cipher import AES
from dotenv import load_dotenv


def call_login(request=None):
    load_dotenv()
    r_data = request.authorization
    if not r_data:
        try:
            r_data = {"username": request.form['user'], "password": request.form['pass']}
        except Exception as e:
            return f"Error while getting user and pass: {e}", e.code
    r_data = encrypt(bytes(os.getenv('AES_KEY'), 'utf-8'), bytes(str(r_data), 'utf-8'))
    data_send = {'nonce': str(r_data[0]), 'tag': str(r_data[1]), 'ciphertext': str(r_data[2])}
    login_request = requests.post("http://localhost:8081/perform_login", json=data_send)
    return login_request.content.token, login_request.code


def encrypt(key, data):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    nonce = cipher.nonce
    return nonce, tag, ciphertext
