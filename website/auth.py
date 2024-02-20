from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash
from flask_cors import CORS

from .user import _User
from .utils import *
from .utils import _login_required

auth = Blueprint('auth', __name__)
CORS(auth)


@auth.errorhandler(401)
def not_authorized(e):
    flash('user not logged!', category='error')
    return redirect(url_for('.login')+f'?shop={get_current_user().shop_id}')


@auth.errorhandler(404)
def not_found(e):
    flash('page not found', category='error')
    return redirect(url_for('.login'))


@auth.route('/login', methods=['GET', 'POST'])
@auth.route('/login', methods=['GET', 'POST'], subdomain='employee')
def login():
    user = get_current_user()
    if user.is_authenticated:
        result = get_admin_or_employee_portal_url(user, request)
        if result[0]:
            return redirect(result[1], code=302)
        flash("wrong portal, please check if the url is correct!")

    if request.method == 'POST':
        args = request.url.split('?')[1] if 'shop' in request.args else ''
        r = requests.post(API_URL + f'token?{args}', data=request.form)
        if r.status_code == 201:
            token = json.loads(r.json()).get('access_token')
            user = _User()
            user.set_data(requests.get(API_URL + f'user?token={token}').json())
            user.token = token
            result = get_admin_or_employee_portal_url(user, request)
            if result[0]:
                login_user(user)
                flash('Logged in successfully!', category='success')
                return redirect(result[1], code=302)
            flash("wrong portal, please check if the url is correct!")
        else:
            flash(f'Failed to login. Error: {r.json()}', category='error')
    return render_template("login.html", user=user)


@auth.route('/logout')
@auth.route('/logout', subdomain='employee')
@_login_required
def logout():
    user = get_current_user()
    if user.is_authenticated:
        headers = {'Authorization': f'{user.token}'}
        r = requests.delete(API_URL + 'token', headers=headers)
        if r.status_code == 200:
            logout_user()
        else:
            flash(f'Could not logout. Server response: {r.json()}', category='error')
            return redirect(request.host_url, code=302)
    return redirect_to_login(request)


@auth.route('/sign-up', methods=['GET', 'POST'])
def join_signup():
    user = get_current_user()
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password = request.form.get('password')
        r = requests.get(API_URL + f'shop/unknown?api-key={request.args.get("key")}')
        if r.status_code == 204:
            flash('shop does not exist', category='error')
            return render_template("sign-up.html", user=user)
        shop_id = r.json().get('id')

        if len(email) < 4:
            flash('Email must be greater than 3 chars.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 chars.', category='error')
        elif len(password) < 7:
            flash('Password must be greater than 6 chars.', category='error')
        else:
            # add join request to database
            data = {"first_name": f"{request.form.get('first_name')}",
                    "last_name": f"{request.form.get('last_name')}",
                    "email": f"{request.form.get('email')}",
                    "contact": f"{request.form.get('contact')}",
                    "password": f"{request.form.get('password')}",
                    "role": f"{request.form.get('role')}",
                    "shop_id": shop_id}
            r = requests.put(API_URL + f'create-join-request?api-key={request.args.get("key")}', data=data)
            if r.status_code == 201:
                flash('Join request sent!', category='success')
                return redirect(url_for('.login') + f'?shop={shop_id}')
    _check = requests.get(API_URL + f'key/{request.args.get("key")}')
    if _check.status_code == 200:
        if not _check.json().get('join_id'):
            return render_template("sign-up.html", user=user)
        flash('key already used', category='error')
    return redirect_to_login(request)


# test method. signup endpoint should send a request to existing
@auth.route('/direct-signup', methods=['GET', 'POST'])
@mgr_required
def direct_signup():
    # put together
    user = get_current_user()
    shop = user.shop_id
    if not user.is_authenticated:
        flash('session expired')
        logout_user()
        return redirect_to_login(request)
    # all this

    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password = request.form.get('password')

        if len(email) < 4:
            flash('Email must be greater than 4 chars.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 2 chars.', category='error')
        elif len(password) < 7:
            flash('Password must be greater than 7 chars.', category='error')
        else:
            # add user to database
            if 'u' in request.args:
                r = requests.patch(API_URL + f'user/{request.args.get("u")}', data=request.form, headers={"authorization": user.token})
            else:
                r = requests.put(API_URL + 'user', data=request.form, headers={"authorization": user.token})
            if r.status_code != 201:
                flash(f'Could not create user! Server error: {r.json()}', category='error')
            return redirect(url_for('views.users'))

    if 'u' in request.args:
        r = requests.get(API_URL + f'user/{request.args.get("u")}', headers={"authorization": user.token})
        if r.status_code == 200:
            r2 = requests.get(API_URL + f'shop/{r.json().get("shop_id")}', headers={"authorization": user.token})
            data = r.json()
            data['shop_name'] = r2.json().get('shop_name')
            return render_template("direct-sign-up.html", user=user, prefill=data)

    return render_template("direct-sign-up.html", user=user, prefill=None)


@auth.route('/create-employee', methods=['GET', 'POST'])
@mgr_required
def create_emp():
    user = get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        logout_user()
        return redirect_to_login(request)

    if request.method == 'POST':
        request_type = request.form.get('type')
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password = request.form.get('password')
        if len(email) < 4:
            flash('Email must be greater than 4 chars.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 2 chars.', category='error')
        elif len(password) < 7:
            flash('Password must be greater than 7 chars.', category='error')
        else:
            data = request.form.to_dict()
            data['role'] = 'emp'
            if request_type == 'update':
                r = requests.patch(API_URL + f'employee/{request.args.get("e")}', data=data, headers={"authorization": user.token})
            else:
                r = requests.put(API_URL + 'employees', data=data, headers={"authorization": user.token})
            if r.status_code == 201:
                message = 'Employee added!' if request_type == 'create' else 'Employee updated!'
                flash(message, category='success')
                return redirect(url_for('views.employees'))
            flash(f'could not add employee! Server error: {r.json()}', category='success')

    if 'e' in request.args:
        r = requests.get(API_URL + f'employee/{request.args.get("e")}', headers={"authorization": user.token})
        if r.status_code == 200:
            r2 = requests.get(API_URL + f'shop/{r.json().get("shop_id")}', headers={"authorization": user.token})
            data = r.json()
            data['shop_name'] = r2.json().get('shop_name')
            return render_template("create-employee.html", user=user, prefill=data)

    return render_template("create-employee.html", user=user, prefill=None)


@auth.route('/create-shop', methods=['GET', 'POST'])
@admin_required
def create_shop():
    user = get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        logout_user()
        return redirect_to_login(request)

    if request.method == 'POST':
        shop_name = request.form.get('shop_name')
        email = request.form.get('email')
        contact = request.form.get('contact')
        address = request.form.get('address')

        if len(shop_name) < 4:
            flash('Shop name must be greater than 4 chars.', category='error')
        elif len(email) < 5:
            flash('Email must be greater than 5 chars.', category='error')
        elif len(contact) < 10:
            flash('Contact must be greater than 9 chars.', category='error')
        elif len(address) < 5:
            flash('Address must be greater than 5 chars.', category='error')
        else:
            if 's' in request.args:
                r = requests.patch(API_URL + f'shop/{request.args.get("s")}', data=request.form, headers={"authorization": user.token})
            else:
                r = requests.put(API_URL + 'shops', data=request.form, headers={"authorization": user.token})
            if r.status_code == 201:
                flash('Shop created!', category='success')
                return redirect(url_for('views.shops'))
            flash(f'could not create shop. Server error: {r.json()}', category='success')

    if 's' in request.args:
        r = requests.get(API_URL + f'shop/{request.args.get("s")}', headers={"authorization": user.token})
        if r.status_code == 200:
            data = r.json()
            return render_template("create-shop.html", user=user, prefill=data)

    return render_template('create-shop.html', user=user, prefill=None)
