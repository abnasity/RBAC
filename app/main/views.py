from flask import Blueprint
from flask_security import login_required, current_user, roles_required




main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/') 
@login_required
def home():
    return f"Welcome to the County Portal, {current_user.email}!"

@main_bp.route('/about')
def about():
    return "This is the county portal, providing information about local governance and services."


@main_bp.route('/dashboard')
@roles_required('super_admin')  # Only users with the 'super_admin' role can access this route
def dashboard():
    return "This dashboard is accessible to admins only."