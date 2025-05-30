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
    from app.auth.routes import auth_bp
    
    #Register the blueprint
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    
    
    #import models and initialize flask_security
    from app.models.user import User, Role, uuid
    from flask_security import hash_password
    
    
   # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore)
    
    with app.app_context():
        db.create_all()
        roles_data = [
            {'name': 'super_admin', 'description': 'Administrator role with full access'},
            {'name': 'staff', 'description': 'County staff with limited access'},
            {'name': 'citizen', 'description': 'Regular  citizen with basic access'},
            {'name': 'guest', 'description': 'Guest user with minimal access'},
        ]
        for role_data in roles_data:
            role = Role.query.filter_by(name=role_data['name']).first()
            if not role:
                role = Role(**role_data)
                
                db.session.add(role)
                    
            admin_role = Role.query.filter_by(name='super_admin').first()
            admin_user = User.query.filter_by(email='abdkpng@gmail.com').first()
            
            if not admin_user:
                
                admin_user = User(
                    email='abdkpng@gmail.com',
                    password=hash_password("@bd1998z"),  # Use a hashed password in production
                    active=True,
                    roles=[admin_role],
                    
                )
                admin_user.roles.append(admin_role)
                db.session.add(admin_user)
            db.session.commit()
            print("Database initial and superuser created.")
                
  
    return app



