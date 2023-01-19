import os

from Crypto.Cipher import AES
from dotenv import load_dotenv
load_dotenv()


def main():
    data = bytes('any information', 'utf-8')
    key = bytes(os.getenv('AES_KEY'), 'utf-8')
    encrypted = encrypt(key, data)
    print(encrypted)
    print(decrypt(key, encrypted))


def encrypt(key, data):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    nonce = cipher.nonce
    return nonce, tag, ciphertext


def decrypt(key, data):
    nonce, tag, ciphertext = data
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)


if __name__ == '__main__':
    main()
