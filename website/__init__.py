from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from os import path, getenv
from dotenv import load_dotenv

from .utility import UTC
from .roles import Role

db = SQLAlchemy()
migrate = Migrate()
version = 'ce4e0697f426'

load_dotenv()
SECRET_KEY = getenv("SECRET_KEY")
DB_NAME = getenv("DB_NAME")
MECH_DATA = getenv("MECH_DATA")
MAP_DATA = getenv("MAP_DATA")
DEFAULT_USER = getenv("DEFAULT_USER")
SQL_USER = getenv("SQL_USER")
SQL_PASSWORD = getenv("SQL_PASSWORD")

def create_admin_user():
    from .models import User
    from werkzeug.security import generate_password_hash

    new_user = User(name=DEFAULT_USER, in_game_name=DEFAULT_USER, timezone=UTC(), password=generate_password_hash(DEFAULT_USER), admin=True, role=Role.Admin.value)
    db.session.add(new_user)
    db.session.commit()

def initialize_mechs_table():
    from .parser import get_mech_data
    from .models import Mech

    mechs = get_mech_data()
    for line in mechs.values():
        omni = line['OmniMech'] == "TRUE"
        mech = Mech(name=line['Name'], chassis=line['Chassis'], tonnage=line['Tonnage'],
                    weight_class=line['Class'], chassis_type=line['Type'], omni_mech=omni, side=line['Side'])
        db.session.add(mech)
    db.session.commit()

def initialize_maps_table():
    from .parser import get_map_data
    from .models import Map

    maps = get_map_data()
    for name in maps.values():
        map = Map(name=name)
        db.session.add(map)
    db.session.commit()

def initialize_database_version():
    from sqlalchemy import text
    db.session.execute(text("CREATE TABLE alembic_version (version_num VARCHAR(32) NOT NULL PRIMARY KEY)"))
    db.session.execute(text("INSERT INTO alembic_version (version_num) VALUES (:version)"), {"version": version})
    db.session.commit()

def create_database(app):
    if not path.exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
            create_admin_user()
            initialize_mechs_table()
            initialize_maps_table()
            initialize_database_version()
        print('Database created!')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{SQL_USER}:{SQL_PASSWORD}@localhost:5432/{DB_NAME}'

    db.init_app(app)
    migrate.init_app(app, db)

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
