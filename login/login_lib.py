import json


def decrypt(data):
    import os
    from dotenv import load_dotenv
    from Crypto.Cipher import AES
    load_dotenv()

    key = bytes(os.getenv('AES_KEY'), 'utf-8')

    nonce = bytes(data['nonce'][:len(data['nonce'])-1].replace("b'", ""), 'utf-8')
    tag = bytes(data['tag'][:len(data['tag'])-1].replace("b'", ""), 'utf-8')
    ciphertext = bytes(data['ciphertext'][:len(data['ciphertext'])-1].replace("b'", ""), 'utf-8')

    cipher = AES.new(key, AES.MODE_EAX, nonce)

    return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')


def generate_token_by_user(data):
    print(data)
    # decrypt data
    decrypted = json.loads(decrypt(data))
    user, password = decrypted['user'], decrypted['password']

    # read database
    if user != 'test' or password != 'test':
        return 'user or password error', 404
    # compare password

    # get existent token from database
    existent_token = 'get_existing_token_method'

    # generate a new token if needed
    if not is_token_still_valid(existent_token):
        existent_token = 'create_new_token_method'

    # save it to database

    # return json with success and token objects
    return json.loads("{'success':True, 'token':%s}" % existent_token), 200


def is_token_still_valid(token):
    # read database
    # compare token
    # compare timestamp
    # return if it is valid
    return True
