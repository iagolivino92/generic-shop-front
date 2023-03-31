from flask import abort, jsonify
from flask_login import current_user


def get_form_request_data(request):
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        return email, password
    return None, None


def get_user_data(request, user_type, shop):
    shop_name = request.args.get('shop', type=str)
    if shop_name:
        shop_ = shop.query.filter_by(shop_name=shop_name).first()
        email, password = get_form_request_data(request)
        if email:
            try:
                user = user_type.query.filter_by(shop_id=shop_.id, email=email).first()
            except AttributeError as e:
                return False, email, password, None
            return True, email, password, user
    return False, None, None, None


def _login_required(f, role='Read'):
    from functools import wraps
    from .models import User

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            user_role = current_user.role
            if user_role == 'Admin' and role == 'Read':
                user = User.query.filter_by(shop_id=current_user.shop_id, email=current_user.email, role=user_role).first()
            else:
                user = User.query.filter_by(shop_id=current_user.shop_id, email=current_user.email, role=role).first()
        except AttributeError as e:
            user = None
        if not user:
            abort(401)
        return f(*args, **kwargs)

    return decorated_function


def emp_required(f):
    return _login_required(f, 'emp')


def admin_required(f):
    return _login_required(f, 'Admin')


def read_required(f):
    return _login_required(f)


def error_return(msg='', error=''):
    return jsonify('{"success":false, "message":"%s", "error":"%s"}' % (msg, error))


def success_return(msg=''):
    return jsonify('{"success":true, "message":"%s"}' % msg)
