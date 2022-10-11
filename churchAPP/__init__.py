from datetime import timedelta
from distutils.command.config import config
from flask import Flask
from flask_session import Session
from flask_mail import Mail, Message
from cs50 import SQL
from tempfile import mkdtemp
from dotenv import dotenv_values

db = SQL('sqlite:///church.db')

def create_app():
    app = Flask(__name__)

    config = dotenv_values('.env')
    app.secret_key = config["SECRET_KEY"]
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config["SESSION_FILE_DIR"] = mkdtemp()
    app.config["SESSION_PERMANENT"] = True
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=3)
    Session(app)

    app.config['MAIL_SERVER']= config['MAIL_SERVER']
    app.config['MAIL_PORT'] = config['MAIL_PORT']
    app.config['MAIL_USERNAME'] = config['MAIL_USERNAME']
    app.config['MAIL_PASSWORD'] = config['MAIL_PASSWORD']
    app.config['MAIL_USE_TLS'] = True
    mail = Mail(app)
    # Initialize blueprints
    
    from .views import views
    from .auth import auth

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')  
    return app
    