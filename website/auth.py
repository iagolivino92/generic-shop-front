from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask_login import login_user
from flask_login import login_required
from flask_login import logout_user
from .models import User, JoinRequest
from .models import Shop
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, utils
from .utils import *

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'emp':
            return redirect(url_for('views.emp_home'))
        else:
            return redirect(url_for('views.home'))
    success, email, password, user = get_user_data(request, User, Shop)
    if success:
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                if current_user.role == 'emp':
                    return redirect(url_for('views.emp_home'))
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='error')
    if email and password:
        flash('User/Shop does not exist!', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/login', methods=['GET', 'POST'], subdomain='employee')
def emp_login():
    return login()


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))


@auth.route('/logout', subdomain='employee')
@emp_required
def emp_logout():
    logout_user()
    return redirect(url_for('.emp_login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def join_signup():
    shop_name = request.args.get('shop')
    if not shop_name:
        return render_template('notfound.html')
    shop = Shop.query.filter_by(shop_name=shop_name).first()
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password = request.form.get('password')

        try:
            user = User.query.filter_by(shop_id=shop.id, email=email).first()
        except AttributeError as e:
            flash(f'Shop does not exist!\nPlease add the correct shop in the URL!', category='error')
            return redirect('/direct-signup?shop=<existent_shop_here>')
        if user:
            flash('Email already exists!', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 chars.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 chars.', category='error')
        elif len(password) < 7:
            flash('Password must be greater than 6 chars.', category='error')
        else:
            # add join request to database
            data = '{"first_name":"%s",' \
                   '"last_name":"%s",' \
                   '"email":"%s",' \
                   '"contact":"%s",' \
                   '"password":"%s",' \
                   '"role":"%s"}' \
                   % (request.form.get('first_name'), request.form.get('last_name'), request.form.get('email'),
                      request.form.get('contact'), request.form.get('password'), request.form.get('role')
                      )
            new_join_request = JoinRequest(
                shop_id=shop.id,
                data=data
            )
            db.session.add(new_join_request)
            db.session.commit()
            flash('Join request sent!', category='success')
            return redirect(url_for('.login') + f'?shop={shop_name}')

    return render_template("sign-up.html", user=current_user)


# test method. signup endpoint should send a request to existing
@auth.route('/direct-signup', methods=['GET', 'POST'])
@admin_required
def direct_signup():
    if request.method == 'POST':
        data = request.form
        shop = Shop.query.filter_by(id=Shop.query.filter_by(shop_name=data.get('shop')).first().id).first()
        email = data.get('email')
        first_name = data.get('first_name')
        password = data.get('password')
        contact = data.get('contact')
        last_name = data.get('last_name')
        role = data.get('role')

        try:
            user = User.query.filter_by(shop_id=shop.id, email=email).first()
        except AttributeError as e:
            flash(f'Shop does not exist!\nPlease add the correct shop in the URL!', category='error')
            return redirect('/direct-signup?shop=<existent_shop_here>')
        if user:
            flash('Email already exists!', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 chars.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 2 chars.', category='error')
        elif len(password) < 7:
            flash('Password must be greater than 7 chars.', category='error')
        else:
            # add user to database
            utils.create_user(data)
            flash('Account created!', category='success')

            return redirect(url_for('views.users'))

    return render_template("direct-sign-up.html", user=current_user)


@auth.route('/create-employee', methods=['GET', 'POST'])
@mgr_required
def create_emp():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password = request.form.get('password')
        contact = request.form.get('contact')
        last_name = request.form.get('last_name')
        if current_user.role == 'admin':
            shop_id = Shop.query.filter_by(shop_name=request.form.get('shop_name')).first().id
        else:
            shop_id = current_user.shop_id

        try:
            user = User.query.filter_by(shop_id=current_user.shop_id, email=email, role='emp').first()
        except AttributeError as e:
            flash(f'Shop does not exist!\nPlease add the correct shop in the URL!', category='error')
            return redirect('/direct-signup?shop=<existent_shop_here>')
        if user:
            flash('Email already exists!', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 chars.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 2 chars.', category='error')
        elif len(password) < 7:
            flash('Password must be greater than 7 chars.', category='error')
        else:
            # add user to database
            new_user = User(
                email=email,
                contact=contact,
                first_name=first_name,
                last_name=last_name,
                password=generate_password_hash(password, method='sha256'),
                role='emp',
                shop_id=shop_id
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Employee added!', category='success')
            return redirect(url_for('views.employees'))

    return render_template("create-employee.html", user=current_user)


@auth.route('/create-shop', methods=['GET', 'POST'])
@admin_required
def create_shop():
    if request.method == 'POST':
        shop_name = request.form.get('shop_name')
        email = request.form.get('email')
        contact = request.form.get('contact')
        address = request.form.get('address')

        shop = Shop.query.filter_by(shop_name=shop_name).first()
        if shop:
            flash('Shop already exists!', category='error')
        elif len(shop_name) < 4:
            flash('Shop name must be greater than 4 chars.', category='error')
        elif len(email) < 5:
            flash('Email must be greater than 5 chars.', category='error')
        elif len(contact) < 10:
            flash('Contact must be greater than 9 chars.', category='error')
        elif len(address) < 5:
            flash('Address must be greater than 5 chars.', category='error')
        else:
            new_shop = Shop(
                shop_name=shop_name,
                email=email,
                contact=contact,
                address=address
            )
            db.session.add(new_shop)
            db.session.commit()
            flash('Shop created!', category='success')
            return redirect(url_for('views.shops'))

    return render_template('create-shop.html', user=current_user)
