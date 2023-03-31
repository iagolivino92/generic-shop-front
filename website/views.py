import json

import requests
from flask import Blueprint, redirect, url_for, request, flash
from flask import render_template
from flask import jsonify
from flask_login import current_user
from .models import JoinRequest

from .models import User
from .utils import emp_required, admin_required, read_required
from . import db

views = Blueprint('views', __name__)


@views.route('/')
@read_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/', subdomain='employee')
@emp_required
def emp_home():
    return render_template("employee.html", user=current_user)


@views.route('/employees')
@read_required
def employees():
    emps = User.query.filter_by(shop_id=current_user.shop_id, role='emp').all()
    return render_template("employees.html", user=current_user, employees=emps)


@views.route('/delete-employee/<id>')
@admin_required
def delete_emp(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    # return jsonify({})
    return redirect(url_for('.employees'))


@views.route('/join-requests')
@admin_required
def join_requests():
    jrs = JoinRequest.query.filter_by(shop_id=current_user.shop_id).all()
    return render_template('join-requests.html', user=current_user, join_requests=jrs, json=json)


@views.route('/accept-join/<id>')
@admin_required
def accept_join(id):
    try:
        jr = JoinRequest.query.filter_by(id=id).first()
    except:
        flash('something went wrong loading request!', category='error')
        return redirect(url_for('.join_requests'))
    jr.processed_by = current_user.email
    db.session.commit()
    data = json.loads(jr.data)
    r = requests.post(request.url_root + '/direct-signup', data=data)
    print(r.status_code)
    if not r.status_code == 302:
        flash('something went wrong in creating the account!', category='error')
    return redirect(url_for('.join_requests'))


@views.route('/decline-join/<id>')
@admin_required
def decline_join(id):
    return 'ola'
