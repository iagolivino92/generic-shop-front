import requests


def call_login(request=None):
    r_data = request.authorization
    if not r_data:
        try:
            r_data = {"username": request.form['user'], "password": request.form['pass']}
        except Exception as e:
            return f"Error while getting user and pass: {e}", e.code

    # login_request = requests.post("http://url-to-login-service", data=r_data)
    # return login_request.token, login_request.code
    return "hello", 200
