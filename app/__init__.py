from flask import Flask
from flask_security import SQLAlchemyUserDatastore
from app.extensions import db, migrate, mail, security

from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
   
    
    
    #Register blueprints or routes here
    #Blueprints imports
    from app.main.views import main_bp
    from app.api.routes import api_bp
    
    #Register the blueprint
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    
    #import models and initialize flask_security
    from app.models.user import User, Role
    
    
   # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore)
    
    with app.app_context():
        db.create_all()
    
    
  
    return app



