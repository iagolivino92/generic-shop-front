import flask
from flask import redirect, url_for, flash

from website import create_app
from website.utils import get_current_user, redirect_to_login

app = create_app()


@app.errorhandler(404)
def not_found(e):
    flash('page not found', category='error')
    return redirect_to_login(get_current_user())


if __name__ == '__main__':
    app.run(debug=True)
