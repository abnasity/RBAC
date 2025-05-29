from flask import Blueprint

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/') 
def home():
    return "Welcome to the Home Page!"

@main_bp.route('/about')
def about():
    return "This is the county portal, providing information about local governance and services."