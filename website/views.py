import json
import requests
from flask import Blueprint, redirect, url_for, flash, request
from flask import render_template
from .utils import emp_required, admin_required, read_required, mgr_required, redirect_to_login
from . import utils, API_URL

views = Blueprint('views', __name__)


@views.errorhandler(401)
def not_authorized(e):
    flash('user cannot access this page', category='error')
    return redirect_to_login(utils.get_current_user())


@views.errorhandler(404)
def not_found(e):
    flash('page not found', category='error')
    return redirect_to_login(utils.get_current_user())


@views.route('/')
@read_required
def home():
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect_to_login(user)
    return render_template("home.html", user=user)


@views.route('/', subdomain='employee')
@emp_required
def emp_home():
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect_to_login(user)
    return render_template("employee.html", user=user)


@views.route('/employees')
@read_required
def employees():
    emps = {}
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect_to_login(user)
    if user.role == 'admin':
        r = requests.get(API_URL + 'employees', headers={"authorization": user.token})
    else:
        r = requests.get(API_URL + f'employees/shop/{user.shop_id}', headers={"authorization": user.token})
    if r.status_code == 200:
        emps = r.json()
    return render_template("employees.html", user=user, employees=emps)


@views.route('/join-requests')
@mgr_required
def join_requests():
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect_to_login(user)
    jrs = {}
    if user.role == 'admin':
        r = requests.get(API_URL + 'join-requests', headers={"authorization": user.token})
    else:
        r = requests.get(API_URL + f'join-requests/shop/{user.shop_id}', headers={"authorization": user.token})
    if r.status_code != 204:
        jrs = r.json()
    return render_template('join-requests.html', user=user, join_requests=jrs, json=json)


@views.route('/shops')
@admin_required
def shops():
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect_to_login(user)
    s = requests.get(API_URL + 'shops', headers={"authorization": user.token}).json()
    return render_template('shops.html', user=user, shops=s)


@views.route('/users')
@mgr_required
def users():
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect_to_login(user)
    _users = {}
    if user.role == 'admin':
        r = requests.get(API_URL + 'users', headers={"authorization": user.token})
    else:
        r = requests.get(API_URL + f'users/shop/{user.shop_id}', headers={"authorization": user.token})
    if r.status_code == 200:
        _users = r.json()
    return render_template('users.html', user=user, users=_users)


@views.route('/accept-join/<id>')
@mgr_required
def accept_join(id):
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect_to_login(user)
    r = requests.patch(API_URL + f'join-request/{id}', data={"email": user.email, "action": "accept"},
                       headers={"authorization": user.token})
    if r.status_code == 200:
        flash('join request processed', category='success')
    else:
        flash(f'could not process join request. Server error: {r.json()}', category='error')
    return redirect(url_for('.join_requests'))


@views.route('/decline-join/<id>')
@mgr_required
def decline_join(id):
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect_to_login(user)
    r = requests.patch(API_URL + f'join-request/{id}', data={"email": user.email, "action": "decline"},
                       headers={"authorization": user.token})
    if r.status_code == 200:
        flash('join request processed', category='success')
    else:
        flash(f'could not process join request. Server error: {r.json()}', category='error')
    return redirect(url_for('.join_requests'))


@views.route('/remove-employee/<id>')
@mgr_required
def delete_emp(id):
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect_to_login(user)
    r = requests.delete(API_URL + f'employee/{id}', headers={"authorization": user.token})
    if r.status_code == 201:
        flash('employee deleted', category='success')
    else:
        flash(f'could not delete employee. Server error: {r.json()}', category='error')
    return redirect(url_for('.employees'))


@views.route('/remove-user/<id>')
@mgr_required
def delete_user(id):
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect_to_login(user)
    r = requests.delete(API_URL + f'user/{id}', headers={"authorization": user.token})
    if r.status_code == 201:
        flash('user deleted', category='success')
    else:
        flash(f'could not delete user. Server error: {r.json()}', category='error')
    return redirect(url_for('.users'))


@views.route('/remove-shop/<id>')
@admin_required
def delete_shop(id):
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect_to_login(user)
    r = requests.delete(API_URL + f'shop/{id}', headers={"authorization": user.token})
    if r.status_code == 201:
        flash('shop deleted', category='success')
    else:
        flash(f'could not delete shop. Server error: {r.json()}', category='error')
    return redirect(url_for('.shops'))


@views.route('/entries')
@mgr_required
def entries():
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect_to_login(user)
    _keys = {}
    if user.role == 'admin':
        r = requests.get(API_URL + 'keys', headers={"authorization": user.token})
    else:
        r = requests.get(API_URL + f'shop/keys/{user.shop_id}', headers={"authorization": user.token})
    if r.status_code == 200:
        _keys = r.json()
    return render_template('entries.html', user=user, entries=_keys)


@views.route('/create-entry', methods=['GET', 'POST'])
@mgr_required
def create_entry():
    user = utils.get_current_user()
    shop_id = user.shop_id
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect_to_login(user)
    if user.role == 'admin' and request.method == 'GET':
        return render_template('create-entry-admin.html', user=user)
    if user.role == 'admin' and request.method == 'POST':
        shop_id = request.form.get('shop_id')
    r = requests.post(API_URL + 'keys', headers={"authorization": user.token}, data={f"shop_id": str(shop_id)})
    if r.status_code == 201:
        flash('entry created', category='success')
    else:
        flash(f'could not create entry. Server error: {r.json()}', category='error')
    return redirect(url_for('.entries'))


@views.route('/sales', methods=['GET', 'POST'])
@read_required
def sales():
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect_to_login(user)
    if request.method == 'GET':
        if user.role == 'emp':
            return redirect(url_for('.my_sales'))
        if user.role == 'mgr':
            r = requests.get(API_URL + f'users/shop/{user.shop_id}', headers={"authorization": user.token})
            users_ = r.json()
            r_ = requests.get(API_URL + f'shop/{user.shop_id}', headers={"authorization": user.token})
            shop = r_.json()
            sid = shop.get('shop_name')
            return render_template('sales.html', user=user, users=users_, sid=sid)
        r = requests.get(API_URL + 'shops', headers={"authorization": user.token})
        shops_ = r.json()
        return render_template('sales.html', user=user, shops=shops_)
    elif request.method == 'POST':
        shop_ = request.form.get('shops_drop')
        user_ = request.form.get('users')
        if shop_:
            shop_by_name = requests.get(API_URL + f'/shop/{shop_}', headers={"authorization": user.token})
            shop_id = shop_by_name.json().get('id')
            r_ = requests.get(API_URL + f'users/shop/{shop_id}', headers={"authorization": user.token})
            users_ = r_.json()
            return render_template('sales.html', user=user, users=users_, sid=shop_)
        elif user_:
            return redirect(url_for('.sales_details'))
    return render_template('sales.html', user=user)


@views.route('/my-sales')
@read_required
def my_sales():
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect_to_login(user)
    return render_template('my-sales.html', user=user, sales='')


@views.route('/sales-details')
@mgr_required
def sales_details():
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect_to_login(user)
    return render_template('sales-details.html', user=user)


@views.route('/add-sale', methods=['GET', 'POST'])
@read_required
def add_sale():
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect_to_login(user)
    if request.method == 'POST':
        r = requests.post(API_URL + 'sales', headers={"authorization": user.token}, data=request.form)

    return render_template('add-sale.html', user=user)
