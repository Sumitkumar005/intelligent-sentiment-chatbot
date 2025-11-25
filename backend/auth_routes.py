from flask import Blueprint, request
from auth_controller import check_email, request_otp, verify_otp, get_current_user
from auth_middleware import authenticate
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
@auth_bp.route('/check-email', methods=['POST'])
def check_email_route():
    return check_email(request.json or {})
@auth_bp.route('/request-otp', methods=['POST'])
def request_otp_route():
    return request_otp(request.json or {})
@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp_route():
    return verify_otp(request.json or {})
@auth_bp.route('/me', methods=['GET'])
@authenticate
def get_me():
    return get_current_user(request.user_id)