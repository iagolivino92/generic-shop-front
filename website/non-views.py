from . import db
from flask import request
from flask import Blueprint
from flask_login import login_required

non_views = Blueprint('non-views', __name__)


@non_views.route('/delete-employee', methods=['POST'])
@login_required
def delete_employee():
    pass
