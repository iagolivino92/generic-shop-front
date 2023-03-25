from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# database object
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    """
    app initialization
    secret_key is a sha256 for 'giftipapp' string
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'AF662CA93EE8375AF4D4C9A68FC975102AF31297C3DD2801DB655D8CA005EEA0'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    register_pages(app)

    # load user class - mandatory
    from .models import Shop, User, Employee
    create_start_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

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


def create_start_database(app):
    """
    start database
    :param app:
    :return: None
    """
    # create/start database
    db.init_app(app)
    with app.app_context():
        db.create_all()
