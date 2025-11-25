import os
import logging
from flask import Flask
from flask_cors import CORS
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
    frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
    CORS(app, resources={
        r"/api/*": {
            "origins": [frontend_url, "http://localhost:5173"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
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
    except Exception as e:
        raise
    return app
if __name__ == '__main__':
    app = create_app()
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host=host, port=port, debug=debug)