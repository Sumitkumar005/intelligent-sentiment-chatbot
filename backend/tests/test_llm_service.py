import pytest
from unittest.mock import Mock, patch
from llm_service import GroqService
def test_api_unavailable_returns_error_message():
    with patch('llm_service.Groq') as MockGroq:
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("Connection timeout")
        MockGroq.return_value = mock_client
        service = GroqService(api_key="test_key")
        with pytest.raises(Exception) as exc_info:
            service.generate_response("Hello")
        assert "temporarily unavailable" in str(exc_info.value).lower()
def test_invalid_api_key_handling():
    with patch('llm_service.Groq') as MockGroq:
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("Invalid API key")
        MockGroq.return_value = mock_client
        service = GroqService(api_key="test_key")
        with pytest.raises(Exception) as exc_info:
            service.generate_response("Hello")
        error_msg = str(exc_info.value).lower()
        assert "configuration error" in error_msg or "contact support" in error_msg
def test_rate_limit_error():
    with patch('llm_service.Groq') as MockGroq:
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("Rate limit exceeded")
        MockGroq.return_value = mock_client
        service = GroqService(api_key="test_key")
        with pytest.raises(Exception) as exc_info:
            service.generate_response("Hello")
        assert "too many requests" in str(exc_info.value).lower()
def test_missing_api_key():
    with patch.dict('os.environ', {}, clear=True):
        with pytest.raises(ValueError) as exc_info:
            GroqService()
        assert "api key is required" in str(exc_info.value).lower()
def test_successful_response():
    with patch('llm_service.Groq') as MockGroq:
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Hello! How can I help you?"))]
        mock_client.chat.completions.create.return_value = mock_response
        MockGroq.return_value = mock_client
        service = GroqService(api_key="test_key")
        response = service.generate_response("Hi there")
        assert response == "Hello! How can I help you?"
        assert mock_client.chat.completions.create.called