from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask_login import current_user

from .models import User
from .utils import emp_required, admin_required, read_required

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


@views.route('/delete-employee', methods=['POST'])
@admin_required
def delete_emp():
    return jsonify({})
