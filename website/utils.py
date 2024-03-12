import json
import flask
import requests
from json import JSONEncoder
from flask import abort, redirect, url_for
from . import API_URL
from .foreign_user import ForeignUser
from .user import _User

subdomain_url = "http://employee.generic-shop.com:5000/"


class UserEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def update_session_user_details(user=None):
    r = requests.get(API_URL + f'user?token={user.token}').json()
    user.set_data(r)
    user.is_authenticated = is_user_allowed(user.token)
    flask.session['user'] = UserEncoder().encode(user)


def is_user_allowed(token):
    r = requests.post(API_URL + 'token', headers={'authorization': f'{token}'})
    return r.status_code == 200


def get_current_user():
    try:
        _user = _User()
        _user.set_data(json.loads(flask.session['user']))
        _user.token = json.loads(flask.session['user']).get('token')
        _user.is_authenticated = is_user_allowed(_user.token)
    except KeyError:
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
    flask.session['current_shop'] = UserEncoder().encode(user.shop_id)


def logout_user():
    try:
        flask.session.pop('user')
    except KeyError as e:
        print(e)


def save_foreign_user(user):
    flask.session['foreign_user'] = UserEncoder().encode(user)


def clear_foreign_user():
    try:
        flask.session.pop('foreign_user')
    except KeyError as e:
        print(e)


def redirect_to_login(request, shop=None):
    shop_ = shop
    if not shop:
        shop_ = flask.session.get("current_shop")
    return redirect(request.host_url + f'login?shop={shop_}', code=302)


def get_admin_or_employee_portal_url(user, request):
    is_correct_url = True
    correct_url = request.host_url
    if user.role == 'emp':
        if "employee." not in request.host_url:
            is_correct_url = False
            correct_url = subdomain_url
    else:
        if "employee." in request.host_url:
            is_correct_url = False
            correct_url = request.host_url.replace("employee.", "")
    return is_correct_url, correct_url


def save_last_referrer(request):
    if request.base_url != request.referrer:
        flask.session['last_ref'] = request.referrer


def _login_required(f, role='read'):
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            user_role = json.loads(flask.session['user']).get('role')
            allow = (user_role == 'admin') or \
                    (user_role == 'mgr' and (role == 'read' or role == 'emp')) or \
                    (user_role == 'emp' and role == 'read') or \
                    (user_role == role)
        except (AttributeError, KeyError) as e:
            print(e)
            allow = False
        if not allow:
            abort(401)
        return f(*args, **kwargs)

    return decorated_function


def valid_reset_hash_required(request=None):
    r = requests.get(API_URL + f"/user/reset-password/validate/{request.args.get('h')}")
    return r.status_code == 200


def emp_required(f):
    return _login_required(f, 'emp')


def admin_required(f):
    return _login_required(f, 'admin')


def read_required(f):
    return _login_required(f)


def mgr_required(f):
    return _login_required(f, 'mgr')
