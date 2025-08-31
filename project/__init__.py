from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # or your database URI
    
    db.init_app(app)
    login_manager.init_app(app)
    
    from .website import routes
    routes.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    return app 