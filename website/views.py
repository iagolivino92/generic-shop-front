import json
import requests
from flask import Blueprint, redirect, url_for, flash
from flask import render_template
from .utils import emp_required, admin_required, read_required, mgr_required
from . import utils, API_URL

views = Blueprint('views', __name__)


@views.errorhandler(401)
def not_authorized(e):
    flash('user not logged!', category='error')
    return redirect(url_for('auth.login'))


@views.route('/')
@read_required
def home():
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect(url_for('auth.login'))
    return render_template("home.html", user=user)


@views.route('/', subdomain='employee')
@emp_required
def emp_home():
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect(url_for('auth.login'))
    return render_template("employee.html", user=user)


@views.route('/employees')
@read_required
def employees():
    emps = {}
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect(url_for('auth.login'))
    if user.role == 'admin':
        r = requests.get(API_URL + 'employees')
    else:
        r = requests.get(API_URL + f'employees/shop/{user.shop_id}')
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
        return redirect(url_for('auth.login'))
    jrs = {}
    if user.role == 'admin':
        r = requests.get(API_URL + 'join-requests')
    else:
        r = requests.get(API_URL + f'join-requests/shop/{user.shop_id}')
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
        return redirect(url_for('auth.login'))
    s = requests.get(API_URL + 'shops').json()
    return render_template('shops.html', user=user, shops=s)


@views.route('/users')
@mgr_required
def users():
    user = utils.get_current_user()
    if not user.is_authenticated:
        flash('session expired')
        utils.logout_user()
        return redirect(url_for('auth.login'))
    _users = {}
    if user.role == 'admin':
        r = requests.get(API_URL + 'users')
    else:
        r = requests.get(API_URL + f'users/shop/{user.shop_id}')
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
        return redirect(url_for('auth.login'))
    r = requests.patch(API_URL + f'join-request/{id}', data={"email": user.email, "action": "accept"})
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
        return redirect(url_for('auth.login'))
    r = requests.patch(API_URL + f'join-request/{id}', data={"email": user.email, "action": "decline"})
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
        return redirect(url_for('auth.login'))
    r = requests.delete(API_URL + f'employee/{id}')
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
        return redirect(url_for('auth.login'))
    r = requests.delete(API_URL + f'user/{id}')
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
        return redirect(url_for('auth.login'))
    r = requests.delete(API_URL + f'shop/{id}')
    if r.status_code == 201:
        flash('shop deleted', category='success')
    else:
        flash(f'could not delete shop. Server error: {r.json()}', category='error')
    return redirect(url_for('.shops'))

