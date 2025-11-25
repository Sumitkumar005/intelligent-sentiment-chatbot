"""Simple in-memory rate limiter"""
import time
from functools import wraps
from flask import request, jsonify
import logging

logger = logging.getLogger(__name__)

# Store: {ip: [(timestamp, count)]}
_rate_limit_store = {}
_cleanup_interval = 60  # Clean old entries every 60 seconds
_last_cleanup = time.time()

def rate_limit(max_requests=60, window=60):
    """
    Rate limit decorator
    max_requests: Maximum requests allowed
    window: Time window in seconds
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            global _last_cleanup
            
            # Get client IP
            ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            if ',' in ip:
                ip = ip.split(',')[0].strip()
            
            current_time = time.time()
            
            # Cleanup old entries periodically
            if current_time - _last_cleanup > _cleanup_interval:
                _cleanup_old_entries(current_time, window)
                _last_cleanup = current_time
            
            # Initialize or get existing records
            if ip not in _rate_limit_store:
                _rate_limit_store[ip] = []
            
            # Remove old requests outside the window
            _rate_limit_store[ip] = [
                (ts, count) for ts, count in _rate_limit_store[ip]
                if current_time - ts < window
            ]
            
            # Count requests in current window
            request_count = sum(count for _, count in _rate_limit_store[ip])
            
            if request_count >= max_requests:
                logger.warning(f"Rate limit exceeded for IP: {ip}")
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'message': f'Maximum {max_requests} requests per {window} seconds'
                }), 429
            
            # Add current request
            _rate_limit_store[ip].append((current_time, 1))
            
            return f(*args, **kwargs)
        return wrapped
    return decorator

def _cleanup_old_entries(current_time, window):
    """Remove old entries from store"""
    for ip in list(_rate_limit_store.keys()):
        _rate_limit_store[ip] = [
            (ts, count) for ts, count in _rate_limit_store[ip]
            if current_time - ts < window
        ]
        if not _rate_limit_store[ip]:
            del _rate_limit_store[ip]
