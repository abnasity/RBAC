from flask import Flask
from app.extensions import db, migrate

from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    
    #Register blueprints or routes here
    #Blueprints imports
    from app.main.views import main_bp
    from app.api.routes import api_bp
    
    #Register the blueprint
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    
    with app.app_context():
        db.create_all()
    
    
  
    return app



