from datetime import timedelta
from flask import Flask
from flask_session import Session
from flask_mail import Mail, Message
from cs50 import SQL
from tempfile import mkdtemp
db = SQL('sqlite:///church.db')

def create_app():
    app = Flask(__name__)
    mail = Mail(app)
    app.secret_key = 'SomeKinda secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config["SESSION_FILE_DIR"] = mkdtemp()
    app.config["SESSION_PERMANENT"] = True
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=3)
    Session(app)

    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'benjaminarkutl2017@gmail.com'
    app.config['MAIL_PASSWORD'] = 'aeszorrkndccadsm'
    app.config['MAIL_USE_TLS'] = True
    # app.config["MAIL_DEFAULT_SENDER"] = "benjaminarkutl2017@gmail.com"
    mail = Mail(app)
    # Initialize blueprints
    
    from .views import views
    from .auth import auth

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')  
    return app
    