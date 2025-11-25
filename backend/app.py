import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from flask_compress import Compress
from dotenv import load_dotenv
from database import DatabaseManager
from sentiment import SentimentAnalyzer
from llm_service import GroqService
from vision_service import VisionService
from routes import api, init_routes
from auth_routes import auth_bp
load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
def create_app():
    app = Flask(__name__)
    
    # Enable response compression
    Compress(app)
    app.config['COMPRESS_MIMETYPES'] = ['application/json', 'text/html', 'text/css', 'application/javascript']
    app.config['COMPRESS_LEVEL'] = 6
    app.config['COMPRESS_MIN_SIZE'] = 500
    
    frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
    
    # Allow multiple origins for CORS
    allowed_origins = [
        frontend_url,
        "http://localhost:5173",
        "https://chatbot.sumitsaini.com"
    ]
    
    CORS(app, resources={
        r"/api/*": {
            "origins": allowed_origins,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    try:
        db_manager = DatabaseManager()
        sentiment_analyzer = SentimentAnalyzer()
        llm_service = GroqService()
        try:
            vision_service = VisionService()
        except Exception as e:
            vision_service = None
        init_routes(db_manager, sentiment_analyzer, llm_service, vision_service)
        app.register_blueprint(api)
        app.register_blueprint(auth_bp)
        
        # Health check endpoint
        @app.route('/health')
        def health_check():
            return jsonify({
                'status': 'healthy',
                'service': 'sentiment-chatbot',
                'database': 'connected' if db_manager else 'disconnected'
            }), 200
        
        # Root endpoint
        @app.route('/')
        def root():
            return jsonify({
                'message': 'Sentiment Chatbot API',
                'version': '1.0.0',
                'endpoints': {
                    'health': '/health',
                    'api': '/api'
                }
            }), 200
            
    except Exception as e:
        raise
    return app
# Create app instance at module level for gunicorn
app = create_app()

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host=host, port=port, debug=debug)