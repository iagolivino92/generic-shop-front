from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from website.user import _User

# database object
db = SQLAlchemy()
DB_NAME = "database.db"
API_URL = 'http://giftip.com:5001/api/v1/'


def create_app():
    """
    app initialization
    secret_key is a sha256 for 'giftipapp' string
    """
    app = Flask(__name__)
    app.config['SERVER_NAME'] = 'giftip.com:5000'
    app.config['SECRET_KEY'] = 'AF662CA93EE8375AF4D4C9A68FC975102AF31297C3DD2801DB655D8CA005EEA0'
    register_pages(app)

    return app


def register_pages(app):
    """
    Register blueprints (pages/endpoints)
    :param app: flask application
    :return: None
    """
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
