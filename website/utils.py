import json
import flask
import requests
from json import JSONEncoder
from flask import abort, redirect, url_for
from . import API_URL
from .foreign_user import ForeignUser
from .user import _User


class UserEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def is_user_allowed(token):
    r = requests.post(API_URL + 'token', headers={'authorization': f'{token}'})
    return r.status_code == 200


def get_current_user():
    try:
        _user = _User()
        _user.set_data(json.loads(flask.session['user']))
        _user.token = json.loads(flask.session['user']).get('token')
        _user.is_authenticated = is_user_allowed(_user.token)
    except Exception as e:
        print(e)
        _user = _User()
    return _user


def get_foreign_user():
    try:
        _foreign = ForeignUser()
        _foreign.set_data(json.loads(flask.session['foreign_user']))
    except Exception as e:
        print(e)
        _foreign = ForeignUser()
    return _foreign


def login_user(user):
    user.is_authenticated = True
    flask.session['user'] = UserEncoder().encode(user)


def logout_user():
    try:
        flask.session.pop('user')
    except KeyError as e:
        print(e)


def save_foreign_user(user):
    flask.session['foreign_user'] = UserEncoder().encode(user)


def redirect_to_login(user):
    return redirect(url_for('auth.login') + f'?shop={user.shop_id}')


def _login_required(f, role='read'):
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            user_role = json.loads(flask.session['user']).get('role')
            if user_role == 'admin' and (role == 'read' or role == 'mgr'):
                user = True
            elif user_role == 'mgr' and role == 'read':
                user = True
            else:
                user = user_role == role
        except (AttributeError, KeyError) as e:
            print(e)
            user = None
        if not user:
            abort(401)
        return f(*args, **kwargs)

    return decorated_function


def emp_required(f):
    return _login_required(f, 'emp')


def admin_required(f):
    return _login_required(f, 'admin')


def read_required(f):
    return _login_required(f)


def mgr_required(f):
    return _login_required(f, 'mgr')
