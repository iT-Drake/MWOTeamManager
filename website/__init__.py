from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path, getenv
from dotenv import load_dotenv

db = SQLAlchemy()

load_dotenv()
SECRET_KEY = getenv("SECRET_KEY")
DB_NAME = getenv("DB_NAME")
MECH_DATA = getenv("MECH_DATA")
DEFAULT_USER = getenv("DEFAULT_USER")

def create_admin_user():
    from .models import User
    from werkzeug.security import generate_password_hash

    new_user = User(name=DEFAULT_USER, in_game_name=DEFAULT_USER, password=generate_password_hash(DEFAULT_USER), admin=True)
    db.session.add(new_user)
    db.session.commit()

def initialize_tables():
    from .parser import get_mech_data
    from .models import Mech
    mechs = get_mech_data()
    for line in mechs.values():
        omni = line['OmniMech'] == "TRUE"
        mech = Mech(name=line['Name'], chassis=line['Chassis'], tonnage=line['Tonnage'],
                    weight_class=line['Class'], chassis_type=line['Type'], omni_mech=omni, side=line['Side'])
        db.session.add(mech)

    db.session.commit()

def create_database(app):
    if not path.exists('instance/' + DB_NAME):
        from . import models
        with app.app_context():
            db.create_all()
            create_admin_user()
            initialize_tables()
        print('Database created!')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app
