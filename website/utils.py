from flask import abort, jsonify
from flask_login import current_user
from werkzeug.security import generate_password_hash

from website import db
from website.models import User, Shop


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


def _login_required(f, role='read'):
    from functools import wraps
    from .models import User

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            user_role = current_user.role
            if user_role == 'admin' and (role == 'read' or role == 'mgr'):
                user = User.query.filter_by(shop_id=current_user.shop_id, email=current_user.email,
                                            role=user_role).first()
            elif user_role == 'mgr' and role == 'read':
                user = User.query.filter_by(shop_id=current_user.shop_id, email=current_user.email,
                                            role=user_role).first()
            else:
                user = User.query.filter_by(shop_id=current_user.shop_id, email=current_user.email,
                                            role=role).first()
        except AttributeError as e:
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


def error_return(msg='', error=''):
    return jsonify('{"success":false, "message":"%s", "error":"%s"}' % (msg, error))


def success_return(msg=''):
    return jsonify('{"success":true, "message":"%s"}' % msg)


def create_admin_instance():
    from .models import User, Shop
    if not Shop.query.filter_by(shop_name='admin_local').first():
        create_admin_shop(Shop)
        create_admin_user(User, Shop)
    if not User.query.filter_by(email='admin@local').first():
        create_admin_user(User, Shop)


def create_admin_shop(shop):
    from . import db
    s = shop(
        shop_name='admin_local',
        email='admin@local',
        contact='0000000000',
        address='local_admin_shop'
    )
    db.session.add(s)
    db.session.commit()


def create_admin_user(user, shop):
    u = user(
        email='admin@local',
        contact='00000000',
        first_name='admin',
        last_name='local',
        password=generate_password_hash('localadministrator', method='sha256'),
        role='admin',
        shop_id=(shop.query.filter_by(shop_name='admin_local').first()).id
    )
    db.session.add(u)
    db.session.commit()


def create_user(data):
    shop = Shop.query.filter_by(id=Shop.query.filter_by(shop_name=data.get('shop')).first().id).first()
    new_user = User(
        email=data.get('email'),
        contact=data.get('contact'),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        password=generate_password_hash(data.get('password'), method='sha256'),
        role=data.get('role'),
        shop_id=shop.id
    )
    db.session.add(new_user)
    db.session.commit()
