import json


def decrypt(data):
    import os
    import rsa
    from dotenv import load_dotenv
    load_dotenv()

    raw_key = os.getenv('PRIVATE').split(',')
    private_key = rsa.PrivateKey(int(raw_key[0].strip()), int(raw_key[1].strip()), int(raw_key[2].strip()), int(raw_key[3].strip()), int(raw_key[4].strip()))
    return rsa.decrypt(data, private_key).decode()


def generate_token_by_user(request):
    # decrypt data
    tt = decrypt(request.data)
    decrypted = json.loads(tt.replace("'", '"'))
    user, password = decrypted['username'], decrypted['password']

    # read database
    if user != 'test' or password != 'test':
        return json.loads('{"token":"", "message":"user or password error"}'), 404
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
