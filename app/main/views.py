from flask import Blueprint
from flask_security import login_required, current_user, roles_required, roles_accepted




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

@main_bp.route('/staff')
@roles_required('staff')  # Only users with the 'staff' role can access this route
def staff_only():
    return "This page is accessible to county staff only."

@main_bp.route('/citizen')
@roles_required('citizen')  # Only users with the 'citizen' role can access this route
def citizen_only():
    return "This page is accessible to citizens only."

@main_bp.route('/admin-panel')
@roles_accepted('super_admin', 'staff')
def admin_panel():
    return "Welcome to Admin Panel - accessible by Super Admin and Staff only"  


@main_bp.route('/support')
@roles_accepted('citizen', 'staff')
def citizen_staff():
    return "This dashboard is accessible to staff and citizen users."         