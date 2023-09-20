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
    secret_key is a sha256 for 'generic-shop' string
    """
    app = Flask(__name__)
    app.config['SERVER_NAME'] = 'generic-shop.com:5000'
    app.config['SECRET_KEY'] = 'fb857939e24a93872b67c392149b363ca0e988a3c7739325b38c913b234c3cfb'
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
