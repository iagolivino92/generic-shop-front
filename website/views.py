import json

from . import db
from flask import request
from flask import Blueprint
from flask import render_template
from flask import flash
from flask import jsonify
from flask_login import login_required
from flask_login import current_user

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/')
@login_required
def emp_home():
    return render_template("employee.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    # data = json.loads(request.data)
    # note_id = data['noteId']
    # note = Note.query.get(note_id)
    # if note:
    # if note.user_id == current_user.id:
    # db.session.delete(note)
    # db.session.commit()
    return jsonify({})
