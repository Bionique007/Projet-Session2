import os  # Add this at the top of the file
import locale
from flask import Flask
from app.models.user import db, bcrypt
from app.routes.main_routes import main
from app.models.reservation import Reservation
from app.routes.admin_routes import admin

def create_app():
    app = Flask(__name__)
    # Use an absolute path for the SQLite database file
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.abspath('bionics.db')}"
    app.config['SECRET_KEY'] = 'supersecret'

    locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")

    db.init_app(app)
    bcrypt.init_app(app)
    app.register_blueprint(main)
    app.register_blueprint(admin)
    
    return app