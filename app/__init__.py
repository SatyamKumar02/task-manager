from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from pymongo import MongoClient
from config import Config

login_manager = LoginManager()
csrf = CSRFProtect()

# MongoDB client object (accessible globally)
client = MongoClient(Config.MONGO_URI)
db = client.get_database()  # Uses DB name from URI

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'  # Redirect here if user not logged in

    # Register routes
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
