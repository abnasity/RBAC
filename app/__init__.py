import os
from flask import Flask
from flask_security import SQLAlchemyUserDatastore, hash_password
from app.extensions import db, migrate, mail, security
from config import Config
import uuid

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # Import models here to avoid circular imports
    from app.models.user import User, Role

    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore)

    # Register Blueprints
    from app.main.views import main_bp
    from app.api.routes import api_bp
    from app.auth.routes import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)

    # Initialize database and create roles/admin/user accounts
    with app.app_context():
        db.create_all()

        # Create roles
        roles_data = [
            {'name': 'super_admin', 'description': 'Administrator role with full access'},
            {'name': 'staff', 'description': 'County staff with limited access'},
            {'name': 'citizen', 'description': 'Regular citizen with basic access'},
            {'name': 'guest', 'description': 'Guest user with minimal access'},
        ]
        for role_data in roles_data:
            role = Role.query.filter_by(name=role_data['name']).first()
            if not role:
                db.session.add(Role(**role_data))
        db.session.commit()

        # Create super admin user
        admin_email = 'jerryparks@gmail.com'
        admin_password = os.getenv("ADMIN_PASSWORD", "@bd1998z")

        admin_user = User.query.filter_by(email=admin_email).first()
        if not admin_user:
            admin_role = Role.query.filter_by(name='super_admin').first()
            admin_user = User(
                email=admin_email,
                password=hash_password(admin_password),
                active=True,
                fs_uniquifier=str(uuid.uuid4()),
                roles=[admin_role]
            )
            db.session.add(admin_user)
            app.logger.info("Superuser created.")
        else:
            app.logger.info("Superuser already exists.")

        # Create staff and citizen users
        other_users = [
            {'email': 'calvin@gmail.com', 'password': 'password123', 'role_name': 'staff'},
            {'email': 'jethro@gmail.com', 'password': 'password1234', 'role_name': 'citizen'}
        ]

        for user_data in other_users:
            user = User.query.filter_by(email=user_data['email']).first()
            if not user:
                role = Role.query.filter_by(name=user_data['role_name']).first()
                new_user = User(
                    email=user_data['email'],
                    password=hash_password(user_data['password']),
                    active=True,
                    roles=[role]
                )
                db.session.add(new_user)
                app.logger.info(f"User {user_data['email']} created with role {user_data['role_name']}.")

        db.session.commit()  


     
    
            
    return app
