import os
from groq import Groq
from typing import List, Dict, Optional
import logging
import hashlib
import time
from prompts import (
    build_system_prompt,
    detect_task_type,
    detect_context,
    RESPONSE_TEMPLATES
)
logger = logging.getLogger(__name__)

# Simple in-memory cache
_response_cache = {}
_cache_timestamps = {}
CACHE_TTL = 3600  # 1 hour

class GroqService:
    def __init__(self, api_key: str = None):
        if api_key is None:
            api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError("Groq API key is required. Set GROQ_API_KEY environment variable.")
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"
        self.enable_reasoning = True
        self.enable_task_detection = True
        self.enable_sentiment_adaptation = True
        self.enable_cache = True
    def _get_cache_key(self, user_message: str, user_sentiment: str = None) -> str:
        """Generate cache key from message and sentiment"""
        cache_str = f"{user_message.lower().strip()}_{user_sentiment or 'neutral'}"
        return hashlib.md5(cache_str.encode()).hexdigest()
    
    def _get_cached_response(self, cache_key: str) -> Optional[str]:
        """Get cached response if valid"""
        if not self.enable_cache:
            return None
        
        if cache_key in _response_cache:
            timestamp = _cache_timestamps.get(cache_key, 0)
            if time.time() - timestamp < CACHE_TTL:
                logger.info(f"✅ Cache hit for key: {cache_key[:8]}...")
                return _response_cache[cache_key]
            else:
                # Expired, remove from cache
                del _response_cache[cache_key]
                del _cache_timestamps[cache_key]
        return None
    
    def _cache_response(self, cache_key: str, response: str):
        """Cache a response"""
        if not self.enable_cache:
            return
        
        _response_cache[cache_key] = response
        _cache_timestamps[cache_key] = time.time()
        logger.info(f"💾 Cached response for key: {cache_key[:8]}...")
    
    def generate_response(
        self,
        user_message: str,
        conversation_history: List[Dict] = None,
        user_sentiment: str = None,
        base_style: str = "default"
    ) -> str:
        if conversation_history is None:
            conversation_history = []
        
        # Check cache first
        cache_key = self._get_cache_key(user_message, user_sentiment)
        cached = self._get_cached_response(cache_key)
        if cached:
            return cached
        
        try:
            task_type = None
            if self.enable_task_detection:
                task_type = detect_task_type(user_message)
            context = detect_context(conversation_history, user_message)
            system_prompt = build_system_prompt(
                base_style=base_style,
                user_sentiment=user_sentiment if self.enable_sentiment_adaptation else None,
                task_type=task_type,
                context=context,
                enable_reasoning=self.enable_reasoning,
                enable_chain_of_thought=True
            )
            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                }
            ]
            for msg in conversation_history[-10:]:
                role = "user" if msg.get('sender') == 'user' else "assistant"
                messages.append({
                    "role": role,
                    "content": msg.get('message_text', '')
                })
            messages.append({
                "role": "user",
                "content": user_message
            })
            max_tokens = self._get_max_tokens(task_type, user_message)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self._get_temperature(task_type),
                max_tokens=max_tokens,
                top_p=0.9,
                frequency_penalty=0.3,
                presence_penalty=0.2
            )
            bot_response = response.choices[0].message.content
            bot_response = self._post_process_response(bot_response, user_sentiment)
            
            # Cache the response
            self._cache_response(cache_key, bot_response)
            
            return bot_response
        except Exception as e:
            return self._handle_error(e)
    def _get_max_tokens(self, task_type: str, user_message: str) -> int:
        # Emotional support needs more tokens for empathetic responses
        if task_type in ['emotional_support', 'health_wellness']:
            return 200
        elif task_type in ['debugging', 'technical_explanation', 'math_help', 'data_analysis']:
            return 250
        elif task_type in ['code_help', 'learning_tutor', 'problem_solving', 'business_strategy']:
            return 150
        elif task_type in ['creative_writing', 'brainstorming', 'career_advice']:
            return 120
        else:
            return 100
    def _get_temperature(self, task_type: str) -> float:
        if task_type in ['creative_writing', 'brainstorming']:
            return 0.9
        elif task_type in ['math_help', 'debugging', 'data_analysis']:
            return 0.3
        elif task_type in ['code_help', 'problem_solving', 'technical_explanation']:
            return 0.5
        elif task_type in ['learning_tutor', 'business_strategy', 'career_advice']:
            return 0.6
        else:
            return 0.7
    def _post_process_response(self, response: str, user_sentiment: str = None) -> str:
        response = ' '.join(response.split())
        sentences = response.split('. ')
        if len(sentences) > 4:
            response = '. '.join(sentences[:4]) + '.'
        if user_sentiment == 'negative' and not any(word in response.lower() for word in ['sorry', 'understand', 'here for you']):
            pass
        return response.strip()
    def _handle_error(self, error: Exception) -> str:
        error_str = str(error).lower()
        if 'timeout' in error_str or 'connection' in error_str:
            raise Exception("I'm having trouble connecting right now. Please try again in a moment.")
        elif 'api key' in error_str or 'unauthorized' in error_str or 'authentication' in error_str:
            raise Exception("There's a configuration issue on my end. Please contact support.")
        elif 'rate limit' in error_str:
            raise Exception("I'm getting too many requests right now. Please wait a moment and try again.")
        else:
            raise Exception("I encountered an error. Please try rephrasing your message.")
    def set_agentic_features(
        self,
        enable_reasoning: bool = True,
        enable_task_detection: bool = True,
        enable_sentiment_adaptation: bool = True
    ):
        self.enable_reasoning = enable_reasoning
        self.enable_task_detection = enable_task_detection
        self.enable_sentiment_adaptation = enable_sentiment_adaptation