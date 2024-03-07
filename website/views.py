import json
import flask
import requests
from flask_cors import CORS
from flask import Blueprint, redirect, url_for, flash, request
from flask import render_template
from .utils import emp_required, admin_required, read_required, mgr_required, redirect_to_login
from . import utils, API_URL

views = Blueprint('views', __name__)
CORS(views)


@views.errorhandler(401)
def not_authorized(e):
    if flask.session.get('user'):
        flash('user cannot access this page', category='error')
    return redirect_to_login(request)


@views.errorhandler(404)
def not_found(e):
    flash('page not found', category='error')
    return redirect_to_login(request)


@views.route('/')
@views.route('/', subdomain='employee')
@emp_required
def home():
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect_to_login(request)
    return render_template("home.html", user=user)


# @views.route('/', subdomain='employee')
@emp_required
def emp_home():
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect_to_login(request)
    return render_template("employee.html", user=user)


@views.route('/employees')
@read_required
def employees():
    emps = {}
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect_to_login(request)
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
        return redirect_to_login(request)
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
        return redirect_to_login(request)
    s = requests.get(API_URL + 'shops', headers={"authorization": user.token}).json()
    return render_template('shops.html', user=user, shops=s)


@views.route('/users')
@mgr_required
def users():
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect_to_login(request)
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
        return redirect_to_login(request)
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
        return redirect_to_login(request)
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
        return redirect_to_login(request)
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
        return redirect_to_login(request)
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
        return redirect_to_login(request)
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
        return redirect_to_login(request)
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
        return redirect_to_login(request)
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
@views.route('/sales', methods=['GET', 'POST'], subdomain='employee')
@read_required
def sales():
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect_to_login(request)
    if request.method == 'GET':
        if user.role in ['emp', 'read']:
            return redirect(request.host_url+"my-sales", 302)
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
@views.route('/my-sales', subdomain='employee')
@emp_required
def my_sales():
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect_to_login(request)
    _sales = {}
    r = requests.get(API_URL + f'sales/user/{user.id}', headers={"authorization": user.token})
    if r.status_code == 200:
        _sales = r.json()
    else:
        flash(f'could not find sales. Server error: {r.json()}', category='error')
    return render_template('my-sales.html', user=user, sales=_sales)


@views.route('/sales-details')
@mgr_required
def sales_details():
    user = utils.get_current_user()
    foreign_user = utils.get_foreign_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect_to_login(request)
    sales_ = {}
    # get user by email (/user - args: &email=<user_email> - flask.session['foreign_user']
    r = requests.get(API_URL + f"user?email={foreign_user.get_email()}", headers={"authorization": user.token})
    if r.status_code != 200:
        flash(f'could not retrieve user information. Server error: {r.json()}')
    else:
        user_id = r.json().get('id')
        r_ = requests.get(API_URL + f'sales/user/{user_id}', headers={"authorization": user.token})
        sales_ = r_.json()
    return render_template('sales-details.html', user=user, sales=sales_)


@views.route('/add-sale', methods=['GET', 'POST'])
@views.route('/add-sale', methods=['GET', 'POST'], subdomain='employee')
@emp_required
def add_sale():
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect_to_login(request)
    if request.method == 'POST':
        r = requests.post(API_URL + 'sales', headers={"authorization": user.token}, data=request.form)
        if r.status_code != 201:
            flash(f'could not update sale. Server error: {r.json()}')
    return render_template('add-sale.html', user=user)


@views.route('/update-sale/<int:sale_id>')
@views.route('/update-sale/<int:sale_id>', subdomain='employee')
@emp_required
def update_sale(sale_id):
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect_to_login(request)
    form = {key: value for key, value in request.args.items()}
    r = requests.patch(API_URL + f'sale/{sale_id}', headers={"authorization": user.token}, data=form)
    if r.status_code == 201:
        flash('sale updated!', category='success')
    else:
        flash(f'could not update sale. Server error: {r.json()}', category='error')
    return redirect(url_for('.sales_details'))


@views.route('/save')
@views.route('/save', subdomain='employee')
@emp_required
def save_foreign_email():
    foreign_user = utils.get_foreign_user()
    email = request.args.get('u')
    if email:
        utils.clear_foreign_user()
        foreign_user.email = email
        utils.save_foreign_user(foreign_user)
        return redirect(url_for('.sales_details'))
    return redirect(url_for('.sales'))


@views.route('/reports', methods=['GET', 'POST'])
@read_required
def reports():
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect_to_login(request)
    _sales = {}
    if request.method == 'POST':
        # pass start_date and end_date as parameter for get method
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        r = requests.get(API_URL + f'sales?s={start_date}&e={end_date}', headers={"authorization": user.token})
        _sales = r.json()
    return render_template('reports.html', user=user, sales=_sales)


@views.route('/my-details', methods=['GET', 'POST'])
@views.route('/my-details', subdomain='employee', methods=['GET', 'POST'])
@emp_required
def my_details():
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect_to_login(request)
    if request.method == "POST":
        data = {}
        for item in request.form:
            if request.form.get(item) != '':
                data[item] = request.form.get(item)
        r = requests.patch(API_URL + f'user/{user.id}', data=data,
                           headers={"authorization": user.token})
        if r.status_code != 201:
            flash(f'Could not update user! Server error: {r.json()}', category='error')
        elif r.status_code == 201:
            utils.update_session_user_details(user)
            flash('Your details were updated!', category='success')
    return render_template('my-details.html', user=user)
