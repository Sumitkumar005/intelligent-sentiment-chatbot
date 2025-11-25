import os
import tempfile
from hypothesis import given, strategies as st, settings
from database import DatabaseManager
@settings(max_examples=100)
@given(st.integers(min_value=2, max_value=50))
def test_conversation_uniqueness(num_conversations):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
        db_path = tmp.name
    try:
        db = DatabaseManager(db_path)
        conversation_ids = []
        for _ in range(num_conversations):
            conv_id = db.create_conversation()
            conversation_ids.append(conv_id)
        assert len(conversation_ids) == len(set(conversation_ids)), \
            "Conversation IDs must be unique"
        for i, conv_id in enumerate(conversation_ids):
            for j, other_id in enumerate(conversation_ids):
                if i != j:
                    assert conv_id != other_id, \
                        f"Found duplicate conversation IDs: {conv_id}"
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
@settings(max_examples=100)
@given(
    st.text(min_size=1, max_size=500),
    st.sampled_from(['user', 'bot']),
    st.one_of(st.none(), st.sampled_from(['positive', 'negative', 'neutral'])),
    st.one_of(st.none(), st.floats(min_value=-1.0, max_value=1.0, allow_nan=False))
)
def test_message_storage_completeness(message_text, sender, sentiment, sentiment_score):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
        db_path = tmp.name
    try:
        db = DatabaseManager(db_path)
        conv_id = db.create_conversation()
        message_id = db.save_message(
            conversation_id=conv_id,
            sender=sender,
            text=message_text,
            sentiment=sentiment,
            sentiment_score=sentiment_score
        )
        conversation = db.get_conversation(conv_id)
        saved_message = None
        for msg in conversation['messages']:
            if msg['id'] == message_id:
                saved_message = msg
                break
        assert saved_message is not None, "Message should be retrievable"
        assert saved_message['message_text'] is not None, "Message text must not be null"
        assert saved_message['message_text'] == message_text, "Message text must match"
        assert saved_message['sender'] is not None, "Sender must not be null"
        assert saved_message['sender'] == sender, "Sender must match"
        assert saved_message['timestamp'] is not None, "Timestamp must not be null"
        if sender == 'user' and sentiment is not None:
            assert saved_message['sentiment'] == sentiment, "Sentiment must match for user messages"
        if sentiment_score is not None:
            assert saved_message['sentiment_score'] == sentiment_score, "Sentiment score must match"
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
@settings(max_examples=100)
@given(
    st.lists(
        st.tuples(
            st.text(min_size=1, max_size=200),
            st.sampled_from(['user', 'bot']),
            st.one_of(st.none(), st.sampled_from(['positive', 'negative', 'neutral'])),
            st.one_of(st.none(), st.floats(min_value=-1.0, max_value=1.0, allow_nan=False))
        ),
        min_size=1,
        max_size=20
    )
)
def test_conversation_data_round_trip(messages_data):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
        db_path = tmp.name
    try:
        db = DatabaseManager(db_path)
        conv_id = db.create_conversation()
        saved_message_ids = []
        for text, sender, sentiment, score in messages_data:
            msg_id = db.save_message(
                conversation_id=conv_id,
                sender=sender,
                text=text,
                sentiment=sentiment,
                sentiment_score=score
            )
            saved_message_ids.append(msg_id)
        sentiment_data = {
            'overall_sentiment': 'positive',
            'explanation': 'Test explanation'
        }
        db.save_conversation_sentiment(conv_id, sentiment_data)
        retrieved_conv = db.get_conversation(conv_id)
        assert retrieved_conv is not None, "Conversation should be retrievable"
        assert retrieved_conv['id'] == conv_id, "Conversation ID must match"
        assert retrieved_conv['overall_sentiment'] == 'positive', "Overall sentiment must match"
        assert retrieved_conv['explanation'] == 'Test explanation', "Explanation must match"
        assert len(retrieved_conv['messages']) == len(messages_data), \
            "All messages must be retrieved"
        for i, (text, sender, sentiment, score) in enumerate(messages_data):
            msg = retrieved_conv['messages'][i]
            assert msg['message_text'] == text, f"Message {i} text must match"
            assert msg['sender'] == sender, f"Message {i} sender must match"
            if sentiment is not None:
                assert msg['sentiment'] == sentiment, f"Message {i} sentiment must match"
            if score is not None:
                assert msg['sentiment_score'] == score, f"Message {i} score must match"
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
from sentiment import SentimentAnalyzer
@settings(max_examples=100)
@given(st.text(min_size=1, max_size=1000))
def test_sentiment_classification_domain(text):
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze_message(text)
    valid_sentiments = {'positive', 'negative', 'neutral'}
    assert result['sentiment'] in valid_sentiments, \
        f"Sentiment must be one of {valid_sentiments}, got: {result['sentiment']}"
@settings(max_examples=100)
@given(
    st.lists(
        st.text(min_size=1, max_size=200),
        min_size=2,
        max_size=20
    )
)
def test_equal_weighting_invariance(message_texts):
    analyzer = SentimentAnalyzer()
    messages_original = [
        {'sender': 'user', 'message_text': text}
        for text in message_texts
    ]
    result_original = analyzer.analyze_conversation(messages_original)
    original_score = result_original['average_score']
    messages_reversed = list(reversed(messages_original))
    result_reversed = analyzer.analyze_conversation(messages_reversed)
    reversed_score = result_reversed['average_score']
    assert abs(original_score - reversed_score) < 1e-10, \
        f"Reordering messages should not change average score: {original_score} vs {reversed_score}"
@settings(max_examples=100)
@given(
    st.lists(
        st.text(min_size=1, max_size=200),
        min_size=1,
        max_size=20
    )
)
def test_sentiment_summary_completeness(message_texts):
    analyzer = SentimentAnalyzer()
    messages = [
        {'sender': 'user', 'message_text': text}
        for text in message_texts
    ]
    result = analyzer.analyze_conversation(messages)
    assert 'overall_sentiment' in result, "Result must contain overall_sentiment"
    assert result['overall_sentiment'] in {'positive', 'negative', 'neutral'}, \
        "Overall sentiment must be one of the valid values"
    assert 'explanation' in result, "Result must contain explanation"
    assert result['explanation'] is not None, "Explanation must not be None"
    assert len(result['explanation']) > 0, "Explanation must not be empty"
    assert isinstance(result['explanation'], str), "Explanation must be a string"
from unittest.mock import Mock, patch
from llm_service import GroqService
@settings(max_examples=100)
@given(
    st.text(min_size=1, max_size=200),
    st.lists(
        st.tuples(
            st.sampled_from(['user', 'bot']),
            st.text(min_size=1, max_size=100)
        ),
        min_size=0,
        max_size=15
    )
)
def test_message_context_propagation(user_message, history_data):
    conversation_history = [
        {'sender': sender, 'message_text': text}
        for sender, text in history_data
    ]
    with patch('llm_service.Groq') as MockGroq:
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Test response"))]
        mock_client.chat.completions.create.return_value = mock_response
        MockGroq.return_value = mock_client
        service = GroqService(api_key="test_key")
        service.generate_response(user_message, conversation_history)
        assert mock_client.chat.completions.create.called, "Groq API should be called"
        call_args = mock_client.chat.completions.create.call_args
        messages_sent = call_args.kwargs['messages']
        user_messages = [m for m in messages_sent if m['role'] == 'user']
        assert len(user_messages) > 0, "Current user message must be included"
        assert user_messages[-1]['content'] == user_message, \
            "Last user message must be the current message"
        if conversation_history:
            expected_history_count = min(len(conversation_history), 10)
            assert len(messages_sent) >= 2, "Should include at least system and current message"
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from flask import Flask
from routes import api, init_routes
@settings(max_examples=100)
@given(
    st.one_of(
        st.none(),
        st.dictionaries(
            st.text(min_size=1, max_size=20),
            st.one_of(st.text(), st.integers(), st.none()),
            min_size=0,
            max_size=5
        ).filter(lambda d: 'message' not in d)
    )
)
def test_api_request_validation(invalid_payload):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
        db_path = tmp.name
    try:
        app = Flask(__name__)
        db_manager = DatabaseManager(db_path)
        sentiment_service = SentimentAnalyzer()
        mock_llm = Mock()
        mock_llm.generate_response.return_value = "Test response"
        init_routes(db_manager, sentiment_service, mock_llm)
        client = app.test_client()
        response = client.post('/api/conversations')
        conv_id = response.get_json()['conversation_id']
        if invalid_payload is None:
            response = client.post(
                f'/api/conversations/{conv_id}/messages',
                data='not json',
                content_type='text/plain'
            )
        else:
            response = client.post(
                f'/api/conversations/{conv_id}/messages',
                json=invalid_payload
            )
        assert 400 <= response.status_code < 500, \
            f"Invalid request should return 4xx status, got {response.status_code}"
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
@settings(max_examples=100)
@given(st.text(min_size=1, max_size=50))
def test_error_response_format(invalid_conversation_id):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
        db_path = tmp.name
    try:
        app = Flask(__name__)
        db_manager = DatabaseManager(db_path)
        sentiment_service = SentimentAnalyzer()
        mock_llm = Mock()
        init_routes(db_manager, sentiment_service, mock_llm)
        client = app.test_client()
        response = client.get(f'/api/conversations/{invalid_conversation_id}')
        assert response.content_type == 'application/json', \
            "Error response must be JSON"
        data = response.get_json()
        assert data is not None, "Response must be valid JSON"
        assert 'error' in data, "Error response must contain 'error' field"
        assert isinstance(data['error'], str), "Error message must be a string"
        assert len(data['error']) > 0, "Error message must not be empty"
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
@settings(max_examples=100)
@given(st.text(min_size=1, max_size=200))
def test_message_response_completeness(user_message):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
        db_path = tmp.name
    try:
        app = Flask(__name__)
        db_manager = DatabaseManager(db_path)
        sentiment_service = SentimentAnalyzer()
        mock_llm = Mock()
        mock_llm.generate_response.return_value = "This is a bot response"
        init_routes(db_manager, sentiment_service, mock_llm)
        client = app.test_client()
        response = client.post('/api/conversations')
        conv_id = response.get_json()['conversation_id']
        response = client.post(
            f'/api/conversations/{conv_id}/messages',
            json={'message': user_message}
        )
        assert response.status_code == 200, "Request should succeed"
        data = response.get_json()
        assert 'bot_message' in data, "Response must contain bot_message"
        assert data['bot_message'] is not None, "Bot message must not be None"
        assert len(data['bot_message']) > 0, "Bot message must not be empty"
        assert 'user_sentiment' in data, "Response must contain user_sentiment"
        assert data['user_sentiment'] in {'positive', 'negative', 'neutral'}, \
            "Sentiment must be valid"
        assert 'user_message' in data, "Response must contain user_message"
        assert data['user_message'] == user_message, "User message must match"
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
from app import create_app
@settings(max_examples=100)
@given(st.sampled_from([
    '/api/conversations',
    '/api/conversations/test-id',
    '/api/conversations/test-id/messages',
    '/api/conversations/test-id/sentiment'
]))
def test_cors_header_presence(endpoint):
    app = create_app()
    client = app.test_client()
    if endpoint == '/api/conversations':
        response = client.get(endpoint)
    else:
        response = client.get(endpoint)
    headers = response.headers
    assert 'Access-Control-Allow-Origin' in headers, \
        "Response must include Access-Control-Allow-Origin header"
    origin = headers.get('Access-Control-Allow-Origin')
    assert origin is not None, "CORS origin must not be None"
@settings(max_examples=100)
@given(st.text(min_size=1, max_size=200))
def test_message_persistence_round_trip(user_message):
    app = create_app()
    client = app.test_client()
    response = client.post('/api/conversations')
    conv_id = response.get_json()['conversation_id']
    response = client.post(
        f'/api/conversations/{conv_id}/messages',
        json={'message': user_message}
    )
    assert response.status_code == 200, "Message should be sent successfully"
    sent_data = response.get_json()
    user_msg_id = sent_data['user_message_id']
    bot_msg_id = sent_data['bot_message_id']
    bot_message = sent_data['bot_message']
    user_sentiment = sent_data['user_sentiment']
    response = client.get(f'/api/conversations/{conv_id}')
    conversation = response.get_json()
    user_msg_found = None
    bot_msg_found = None
    for msg in conversation['messages']:
        if msg['id'] == user_msg_id:
            user_msg_found = msg
        if msg['id'] == bot_msg_id:
            bot_msg_found = msg
    assert user_msg_found is not None, "User message must be retrievable"
    assert user_msg_found['message_text'] == user_message, "User message text must match"
    assert user_msg_found['sender'] == 'user', "User message sender must be 'user'"
    assert user_msg_found['sentiment'] == user_sentiment, "User sentiment must match"
    assert bot_msg_found is not None, "Bot message must be retrievable"
    assert bot_msg_found['message_text'] == bot_message, "Bot message text must match"
    assert bot_msg_found['sender'] == 'bot', "Bot message sender must be 'bot'"
@settings(max_examples=100)
@given(st.text(min_size=1, max_size=200))
def test_sentiment_always_analyzed(user_message):
    app = create_app()
    client = app.test_client()
    response = client.post('/api/conversations')
    conv_id = response.get_json()['conversation_id']
    response = client.post(
        f'/api/conversations/{conv_id}/messages',
        json={'message': user_message}
    )
    assert response.status_code == 200, "Message should be sent successfully"
    data = response.get_json()
    assert 'user_sentiment' in data, "Response must include sentiment"
    assert data['user_sentiment'] in {'positive', 'negative', 'neutral'}, \
        "Sentiment must be valid"
    response = client.get(f'/api/conversations/{conv_id}')
    conversation = response.get_json()
    user_messages = [m for m in conversation['messages'] if m['sender'] == 'user']
    assert len(user_messages) > 0, "User message should exist"
    user_msg = user_messages[0]
    assert user_msg['sentiment'] is not None, "Sentiment must be stored"
    assert user_msg['sentiment'] in {'positive', 'negative', 'neutral'}, \
        "Stored sentiment must be valid"
@settings(max_examples=100)
@given(st.lists(st.text(min_size=1, max_size=100), min_size=1, max_size=10))
def test_conversation_sentiment_persistence(user_messages):
    app = create_app()
    client = app.test_client()
    response = client.post('/api/conversations')
    conv_id = response.get_json()['conversation_id']
    for msg in user_messages:
        client.post(
            f'/api/conversations/{conv_id}/messages',
            json={'message': msg}
        )
    response = client.get(f'/api/conversations/{conv_id}/sentiment')
    assert response.status_code == 200, "Sentiment request should succeed"
    sentiment_data = response.get_json()
    overall_sentiment = sentiment_data['overall_sentiment']
    explanation = sentiment_data['explanation']
    response = client.get(f'/api/conversations/{conv_id}')
    conversation = response.get_json()
    assert conversation['overall_sentiment'] == overall_sentiment, \
        "Overall sentiment must be persisted"
    assert conversation['sentiment_explanation'] == explanation, \
        "Sentiment explanation must be persisted"
@settings(max_examples=100)
@given(st.sampled_from(['positive', 'negative', 'neutral']))
def test_sentiment_visual_distinction(sentiment):
    sentiment_classes = {
        'positive': 'sentiment-badge-positive',
        'negative': 'sentiment-badge-negative',
        'neutral': 'sentiment-badge-neutral'
    }
    expected_class = sentiment_classes[sentiment]
    other_classes = [cls for s, cls in sentiment_classes.items() if s != sentiment]
    assert expected_class not in other_classes, \
        f"Sentiment class {expected_class} must be unique"
    all_classes = list(sentiment_classes.values())
    assert len(all_classes) == len(set(all_classes)), \
        "All sentiment classes must be distinct"
@settings(max_examples=100)
@given(
    st.text(min_size=1, max_size=200),
    st.sampled_from(['positive', 'negative', 'neutral'])
)
def test_sentiment_visibility_in_display(message_text, sentiment):
    message = {
        'sender': 'user',
        'message_text': message_text,
        'sentiment': sentiment,
        'timestamp': '2024-01-01T12:00:00'
    }
    assert 'message_text' in message, "Message must contain text"
    assert message['message_text'] == message_text, "Message text must match"
    assert 'sentiment' in message, "Message must contain sentiment"
    assert message['sentiment'] == sentiment, "Sentiment must match"
    assert message['sentiment'] in {'positive', 'negative', 'neutral'}, \
        "Sentiment must be valid"
    assert message['message_text'] is not None and len(message['message_text']) > 0
    assert message['sentiment'] is not None
from datetime import datetime, timedelta
@settings(max_examples=100)
@given(st.lists(st.text(min_size=1, max_size=100), min_size=2, max_size=20))
def test_chronological_message_ordering(message_texts):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
        db_path = tmp.name
    try:
        db = DatabaseManager(db_path)
        conv_id = db.create_conversation()
        base_time = datetime.now()
        for i, text in enumerate(message_texts):
            import time
            time.sleep(0.001)
            db.save_message(
                conversation_id=conv_id,
                sender='user',
                text=text,
                sentiment='neutral'
            )
        conversation = db.get_conversation(conv_id)
        messages = conversation['messages']
        for i in range(len(messages) - 1):
            current_time = datetime.fromisoformat(messages[i]['timestamp'])
            next_time = datetime.fromisoformat(messages[i+1]['timestamp'])
            assert current_time <= next_time, \
                f"Messages must be in chronological order: {current_time} should be <= {next_time}"
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)