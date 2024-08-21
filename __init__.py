from flask import Flask
from peewee import SqliteDatabase
from .models import *
from .utils import login_manager

def create_app():


    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'My APP'
    
    # Database setup
   
    
    with app.app_context():
        db.connect()
        db.create_tables([User, API, ACL,Doc])
        db.close()
    login_manager.init_app(app)
    from .routes import main
    app.register_blueprint(main)
    
    return app
