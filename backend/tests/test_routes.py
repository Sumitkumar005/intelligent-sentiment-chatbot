import os
import tempfile
from unittest.mock import Mock
from flask import Flask
from routes import api, init_routes
from database import DatabaseManager
from sentiment import SentimentAnalyzer
def create_test_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app
def test_endpoint_existence_and_routing():
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
        db_path = tmp.name
    try:
        app = create_test_app()
        db_manager = DatabaseManager(db_path)
        sentiment_service = SentimentAnalyzer()
        mock_llm = Mock()
        mock_llm.generate_response.return_value = "Test response"
        init_routes(db_manager, sentiment_service, mock_llm)
        client = app.test_client()
        response = client.post('/api/conversations')
        assert response.status_code == 201, "Create conversation should return 201"
        response = client.get('/api/conversations')
        assert response.status_code == 200, "List conversations should return 200"
        conv_response = client.post('/api/conversations')
        conv_id = conv_response.get_json()['conversation_id']
        response = client.get(f'/api/conversations/{conv_id}')
        assert response.status_code == 200, "Get conversation should return 200"
        response = client.post(
            f'/api/conversations/{conv_id}/messages',
            json={'message': 'Hello'}
        )
        assert response.status_code == 200, "Send message should return 200"
        response = client.get(f'/api/conversations/{conv_id}/sentiment')
        assert response.status_code == 200, "Get sentiment should return 200"
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
def test_missing_message_field_returns_400():
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
        db_path = tmp.name
    try:
        app = create_test_app()
        db_manager = DatabaseManager(db_path)
        sentiment_service = SentimentAnalyzer()
        mock_llm = Mock()
        init_routes(db_manager, sentiment_service, mock_llm)
        client = app.test_client()
        conv_response = client.post('/api/conversations')
        conv_id = conv_response.get_json()['conversation_id']
        response = client.post(
            f'/api/conversations/{conv_id}/messages',
            json={'text': 'Hello'}
        )
        assert response.status_code == 400, "Missing message field should return 400"
        data = response.get_json()
        assert 'error' in data
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
def test_empty_message_returns_400():
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
        db_path = tmp.name
    try:
        app = create_test_app()
        db_manager = DatabaseManager(db_path)
        sentiment_service = SentimentAnalyzer()
        mock_llm = Mock()
        init_routes(db_manager, sentiment_service, mock_llm)
        client = app.test_client()
        conv_response = client.post('/api/conversations')
        conv_id = conv_response.get_json()['conversation_id']
        response = client.post(
            f'/api/conversations/{conv_id}/messages',
            json={'message': '   '}
        )
        assert response.status_code == 400, "Empty message should return 400"
        data = response.get_json()
        assert 'error' in data
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
def test_nonexistent_conversation_returns_404():
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
        db_path = tmp.name
    try:
        app = create_test_app()
        db_manager = DatabaseManager(db_path)
        sentiment_service = SentimentAnalyzer()
        mock_llm = Mock()
        init_routes(db_manager, sentiment_service, mock_llm)
        client = app.test_client()
        response = client.get('/api/conversations/nonexistent-id')
        assert response.status_code == 404, "Nonexistent conversation should return 404"
        data = response.get_json()
        assert 'error' in data
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
def test_non_json_request_returns_400():
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
        db_path = tmp.name
    try:
        app = create_test_app()
        db_manager = DatabaseManager(db_path)
        sentiment_service = SentimentAnalyzer()
        mock_llm = Mock()
        init_routes(db_manager, sentiment_service, mock_llm)
        client = app.test_client()
        conv_response = client.post('/api/conversations')
        conv_id = conv_response.get_json()['conversation_id']
        response = client.post(
            f'/api/conversations/{conv_id}/messages',
            data='not json',
            content_type='text/plain'
        )
        assert response.status_code == 400, "Non-JSON request should return 400"
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)