import os
import jwt
from flask import request, jsonify
from functools import wraps
import logging

logger = logging.getLogger(__name__)

# Determine which user database to use
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    try:
        logger.info("🐘 Using PostgreSQL for user database in middleware")
        from user_database_postgres import UserDatabaseManager
    except ImportError as e:
        logger.warning(f"⚠️ PostgreSQL user database import failed: {e}")
        logger.info("📁 Falling back to SQLite for user database")
        from user_database import UserDatabaseManager
else:
    logger.info("📁 Using SQLite for user database in middleware")
    from user_database import UserDatabaseManager

user_db = UserDatabaseManager()
def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({
                'success': False,
                'message': 'No token provided. Please login first.'
            }), 401
        try:
            token = auth_header.split(' ')[1] if ' ' in auth_header else auth_header
        except IndexError:
            return jsonify({
                'success': False,
                'message': 'Invalid token format. Use: Bearer <token>'
            }), 401
        try:
            jwt_secret = os.getenv('JWT_SECRET', 'your-secret-key-change-in-production')
            payload = jwt.decode(token, jwt_secret, algorithms=['HS256'])
            request.user_id = payload['userId']
            request.user_email = payload['email']
            request.user_type = payload.get('type', 'user')
            logger.info(f"✅ Token validated for user: {payload['userId']}")
            user = user_db.get_user_by_id(payload['userId'])
            if user:
                request.user_data = user
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            logger.warning(f"❌ Expired token")
            return jsonify({
                'success': False,
                'message': 'Token has expired. Please login again.'
            }), 401
        except jwt.InvalidTokenError as e:
            logger.warning(f"❌ Invalid token: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Invalid token. Please login again.'
            }), 401
        except Exception as e:
            logger.error(f"❌ Auth error: {str(e)}", exc_info=True)
            return jsonify({
                'success': False,
                'message': 'Authentication failed'
            }), 401
    return decorated_function