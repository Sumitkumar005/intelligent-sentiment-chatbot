import os
import random
from datetime import datetime, timedelta
from flask import jsonify
import jwt
import logging
from threading import Thread
from models.User import User
from user_database import UserDatabaseManager
from email_service import EmailService
logger = logging.getLogger(__name__)
user_db = UserDatabaseManager()
email_service = EmailService()
def check_email(data: dict):
    try:
        email = data.get('email')
        if not email:
            return jsonify({
                'success': False,
                'message': 'Email is required'
            }), 400
        user = user_db.get_user_by_email(email)
        if user and user.email_verified:
            token = generate_token(user)
            return jsonify({
                'success': True,
                'verified': True,
                'message': 'Login successful',
                'data': {
                    'token': token,
                    'user': user.to_public_dict()
                }
            }), 200
        else:
            return jsonify({
                'success': True,
                'verified': False,
                'message': 'OTP verification required'
            }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred. Please try again.'
        }), 500
def request_otp(data: dict):
    try:
        email = data.get('email')
        name = data.get('name')
        if not email:
            return jsonify({
                'success': False,
                'message': 'Email is required'
            }), 400
        otp = str(random.randint(100000, 999999))
        otp_expires_at = datetime.utcnow() + timedelta(minutes=10)
        user = user_db.get_user_by_email(email)
        if user:
            user_db.update_user_otp(user.id, otp, otp_expires_at)
            if name and not user.name:
                user_db.update_user_name(user.id, name)
        else:
            user = User(
                email=email,
                name=name or email.split('@')[0],
                otp=otp,
                otp_expires_at=otp_expires_at
            )
            user_db.create_user(user)
        
        # Log OTP in development mode
        print(f"🔐 OTP for {email}: {otp}")
        
        # Send email in background thread to avoid blocking
        def send_email_async():
            try:
                email_service.send_otp_email(email, otp, name)
            except Exception as e:
                logger.error(f"Failed to send email in background: {e}")
        
        Thread(target=send_email_async, daemon=True).start()
        
        response_data = {
            'success': True,
            'message': 'OTP sent to your email address'
        }
        return jsonify(response_data), 200
    except Exception as e:
        print(f"ERROR in request_otp: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': 'An error occurred. Please try again.'
        }), 500
def verify_otp(data: dict):
    try:
        email = data.get('email')
        otp = data.get('otp')
        if not email or not otp:
            return jsonify({
                'success': False,
                'message': 'Email and OTP are required'
            }), 400
        user = user_db.get_user_by_email(email)
        if not user:
            return jsonify({
                'success': False,
                'message': 'Invalid email or OTP'
            }), 401
        if not user.otp:
            return jsonify({
                'success': False,
                'message': 'No OTP found. Please request a new one.'
            }), 401
        if user.otp_expires_at and datetime.utcnow() > user.otp_expires_at:
            return jsonify({
                'success': False,
                'message': 'OTP has expired. Please request a new one.'
            }), 401
        if user.otp != otp:
            return jsonify({
                'success': False,
                'message': 'Invalid OTP'
            }), 401
        if user.status != 'active':
            return jsonify({
                'success': False,
                'message': 'Account is inactive. Please contact support.'
            }), 403
        user_db.verify_user_email(user.id)
        user_db.clear_user_otp(user.id)
        user = user_db.get_user_by_id(user.id)
        token = generate_token(user)
        return jsonify({
            'success': True,
            'message': 'OTP verified successfully',
            'data': {
                'token': token,
                'user': user.to_public_dict()
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred. Please try again.'
        }), 500
def generate_token(user: User) -> str:
    jwt_secret = os.getenv('JWT_SECRET', 'your-secret-key-change-in-production')
    jwt_expires_in = os.getenv('JWT_EXPIRES_IN', '7d')
    if jwt_expires_in.endswith('d'):
        expires_seconds = int(jwt_expires_in[:-1]) * 24 * 60 * 60
    elif jwt_expires_in.endswith('h'):
        expires_seconds = int(jwt_expires_in[:-1]) * 60 * 60
    else:
        expires_seconds = int(jwt_expires_in)
    token_payload = {
        'userId': user.id,
        'email': user.email,
        'type': user.type,
        'exp': datetime.utcnow() + timedelta(seconds=expires_seconds)
    }
    token = jwt.encode(token_payload, jwt_secret, algorithm='HS256')
    return token
def get_current_user(user_id: str):
    try:
        user = user_db.get_user_by_id(user_id)
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        return jsonify({
            'success': True,
            'data': {
                'user': user.to_public_dict()
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred'
        }), 500