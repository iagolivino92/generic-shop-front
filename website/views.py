import json

import requests
from flask import Blueprint, redirect, url_for, request, flash
from flask import render_template
from flask_login import current_user
from sqlalchemy import or_

from .models import JoinRequest, Shop

from .models import User
from .utils import emp_required, admin_required, read_required, mgr_required
from . import db, auth, utils

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
    if current_user.role == 'admin':
        emps = User.query.filter_by(role='emp').all()
    else:
        emps = User.query.filter_by(shop_id=current_user.shop_id, role='emp').all()
    return render_template("employees.html", user=current_user, employees=emps)


@views.route('/delete-employee/<id>')
@mgr_required
def delete_emp(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('.employees'))


@views.route('/join-requests')
@mgr_required
def join_requests():
    if current_user.role == 'admin':
        jrs = JoinRequest.query.all()
    else:
        jrs = JoinRequest.query.filter_by(shop_id=current_user.shop_id).all()
    return render_template('join-requests.html', user=current_user, join_requests=jrs, json=json)


@views.route('/shops')
@admin_required
def shops():
    shops = Shop.query.all()
    return render_template('shops.html', user=current_user, shops=shops)


@views.route('/accept-join/<id>')
@mgr_required
def accept_join(id):
    try:
        jr = JoinRequest.query.filter_by(id=id).first()
    except:
        flash('something went wrong loading request!', category='error')
        return redirect(url_for('.join_requests'))
    if jr.status:
        flash('join request already processed!', category='error')
        return redirect(url_for('.join_requests'))
    data = json.loads(jr.data)
    utils.create_user(data, shop=Shop.query.filter_by(id=jr.shop_id).first())
    if User.query.filter_by(email=data.get('email')).first():
        jr.processed_by = current_user.email
        jr.status = 'approved'
        db.session.commit()
    return redirect(url_for('.join_requests'))


@views.route('/decline-join/<id>')
@mgr_required
def decline_join(id):
    try:
        jr = JoinRequest.query.filter_by(id=id).first()
    except:
        flash('something went wrong loading request!', category='error')
        return redirect(url_for('.join_requests'))
    if jr.status:
        flash('join request already processed!', category='error')
        return redirect(url_for('.join_requests'))
    jr.processed_by = current_user.email
    jr.status = 'declined'
    db.session.commit()
    return redirect(url_for('.join_requests'))


@views.route('/users')
@mgr_required
def users():
    if current_user.role == 'admin':
        _users = User.query.all()
    else:
        _users = User.query.filter((User.shop_id == current_user.shop_id) | (or_(User.role == 'mgr', User.role == 'read'))).all()
    return render_template('users.html', user=current_user, users=_users)
