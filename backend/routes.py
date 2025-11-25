from flask import Blueprint, request, jsonify
from database import DatabaseManager
from sentiment import SentimentAnalyzer
from llm_service import GroqService
from vision_service import VisionService
from auth_middleware import authenticate
import logging
logger = logging.getLogger(__name__)
api = Blueprint('api', __name__, url_prefix='/api')
db = None
sentiment_analyzer = None
llm_service = None
vision_service = None
def init_routes(database_manager, sentiment_service, llm, vision=None):
    global db, sentiment_analyzer, llm_service, vision_service
    db = database_manager
    sentiment_analyzer = sentiment_service
    llm_service = llm
    vision_service = vision
@api.route('/conversations', methods=['POST'])
@authenticate
def create_conversation():
    try:
        user_id = request.user_id
        logger.info(f"Creating conversation for user_id: {user_id}")
        conversation_id = db.create_conversation(user_id)
        conversation = db.get_conversation(conversation_id)
        return jsonify({
            'conversation_id': conversation_id,
            'created_at': conversation['created_at']
        }), 201
    except Exception as e:
        logger.error(f"Error creating conversation: {e}", exc_info=True)
        return jsonify({'error': 'Failed to create conversation'}), 500
@api.route('/conversations', methods=['GET'])
@authenticate
def list_conversations():
    try:
        user_id = request.user_id
        conversations = db.get_all_conversations(user_id)
        return jsonify(conversations), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve conversations'}), 500
@api.route('/conversations/<conversation_id>', methods=['GET'])
@authenticate
def get_conversation(conversation_id):
    try:
        user_id = request.user_id
        conversation = db.get_conversation(conversation_id)
        if not conversation:
            return jsonify({'error': 'Conversation not found'}), 404
        if conversation.get('user_id') != user_id:
            return jsonify({'error': 'Unauthorized access to conversation'}), 403
        return jsonify(conversation), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve conversation'}), 500
@api.route('/conversations/<conversation_id>/messages', methods=['POST'])
@authenticate
def send_message(conversation_id):
    try:
        user_id = request.user_id
        if not request.json:
            return jsonify({'error': 'Request must be JSON'}), 400
        if 'message' not in request.json:
            return jsonify({'error': 'Missing required field: message'}), 400
        user_message = request.json['message']
        image_data = request.json.get('image')
        if not user_message or not user_message.strip():
            if not image_data:
                return jsonify({'error': 'Message cannot be empty'}), 400
            user_message = "What's in this image?"
        conversation = db.get_conversation(conversation_id)
        if not conversation:
            return jsonify({'error': 'Conversation not found'}), 404
        if conversation.get('user_id') != user_id:
            return jsonify({'error': 'Unauthorized access to conversation'}), 403
        sentiment_result = sentiment_analyzer.analyze_message(user_message)
        user_message_id = db.save_message(
            conversation_id=conversation_id,
            sender='user',
            text=user_message,
            sentiment=sentiment_result['sentiment'],
            sentiment_score=sentiment_result['score']
        )
        if len(conversation['messages']) == 0:
            title = user_message[:50] + ('...' if len(user_message) > 50 else '')
            db.update_conversation_title(conversation_id, title)
        conversation = db.get_conversation(conversation_id)
        try:
            if image_data and vision_service:
                bot_response = vision_service.analyze_with_context(
                    image_data=image_data,
                    user_message=user_message,
                    conversation_history=conversation['messages'][:-1]
                )
                bot_response = f"📸 Image Analysis:\n\n{bot_response}"
            else:
                bot_response = llm_service.generate_response(
                    user_message,
                    conversation['messages'][:-1],
                    user_sentiment=sentiment_result['sentiment']
                )
        except Exception as e:
            logger.error(f"LLM service error: {e}", exc_info=True)
            return jsonify({'error': str(e)}), 503
        bot_message_id = db.save_message(
            conversation_id=conversation_id,
            sender='bot',
            text=bot_response
        )
        return jsonify({
            'user_message_id': user_message_id,
            'user_message': user_message,
            'user_sentiment': sentiment_result['sentiment'],
            'user_sentiment_score': sentiment_result['score'],
            'bot_message_id': bot_message_id,
            'bot_message': bot_response
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to process message'}), 500
@api.route('/conversations/<conversation_id>/sentiment', methods=['GET'])
@authenticate
def get_conversation_sentiment(conversation_id):
    try:
        user_id = request.user_id
        conversation = db.get_conversation(conversation_id)
        if not conversation:
            return jsonify({'error': 'Conversation not found'}), 404
        if conversation.get('user_id') != user_id:
            return jsonify({'error': 'Unauthorized access to conversation'}), 403
        sentiment_summary = sentiment_analyzer.analyze_conversation(
            conversation['messages']
        )
        db.save_conversation_sentiment(conversation_id, sentiment_summary)
        message_sentiments = [
            {
                'message_id': msg['id'],
                'message_text': msg['message_text'],
                'sentiment': msg['sentiment'],
                'sentiment_score': msg['sentiment_score']
            }
            for msg in conversation['messages']
            if msg['sender'] == 'user'
        ]
        return jsonify({
            'overall_sentiment': sentiment_summary['overall_sentiment'],
            'explanation': sentiment_summary['explanation'],
            'sentiment_distribution': sentiment_summary['sentiment_distribution'],
            'average_score': sentiment_summary['average_score'],
            'message_sentiments': message_sentiments
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to analyze conversation sentiment'}), 500
@api.route('/conversations/<conversation_id>', methods=['DELETE'])
@authenticate
def delete_conversation(conversation_id):
    try:
        user_id = request.user_id
        conversation = db.get_conversation(conversation_id)
        if not conversation:
            return jsonify({'error': 'Conversation not found'}), 404
        if conversation.get('user_id') != user_id:
            return jsonify({'error': 'Unauthorized access to conversation'}), 403
        deleted = db.delete_conversation(conversation_id)
        if deleted:
            return jsonify({
                'success': True,
                'message': 'Conversation deleted successfully'
            }), 200
        else:
            return jsonify({'error': 'Failed to delete conversation'}), 500
    except Exception as e:
        return jsonify({'error': 'Failed to delete conversation'}), 500
@api.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404
@api.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500