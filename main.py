import flask
from flask import redirect, url_for, flash, request

from website import create_app
from website.utils import get_current_user, redirect_to_login

app = create_app()


@app.errorhandler(500)
def internal_error(e):
    return not_found


@app.errorhandler(404)
def not_found(e):
    skipped_files = ['favicon.ico', 'index.js']
    if not any([file_ in request.base_url for file_ in skipped_files]):
        flash('page not found', category='error')
    return redirect(request.referrer)


if __name__ == '__main__':
    app.run()
