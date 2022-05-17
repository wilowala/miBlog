from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


db = SQLAlchemy()
from .models import User

def create_app(config_name):
    app = Flask(__name__)

    from config import config_options
    app.config.from_object(config_options[config_name])

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    db.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)





    return app