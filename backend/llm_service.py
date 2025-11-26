"""
Advanced Production-Grade LLM Service with Intelligent Memory Management
Built for sentiment analysis chatbot with deep emotional intelligence

Key Features:
- Adaptive context window management
- Intelligent conversation summarization
- Emotion-aware response generation
- Smart caching with emotion exclusion
- Token optimization and cost management
- Multi-layer memory system
"""

import os
from groq import Groq
from typing import List, Dict, Optional, Tuple
import logging
import hashlib
import time
import json
from datetime import datetime

from prompts import (
    build_system_prompt,
    build_conversation_summary,
    detect_task_type,
    detect_context,
    get_sentiment_emoji,
    SENTIMENT_MODIFIERS
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# CACHING SYSTEM - Intelligent Response Caching
# ============================================================================

class IntelligentCache:
    """Smart caching system that respects emotional context"""
    
    def __init__(self, ttl: int = 3600):
        self._cache = {}
        self._timestamps = {}
        self._hit_count = {}
        self.ttl = ttl
    
    def get_key(self, user_message: str, sentiment: str = None, task_type: str = None) -> str:
        """Generate cache key with sentiment and task awareness"""
        cache_str = f"{user_message.lower().strip()}_{sentiment or 'neutral'}_{task_type or 'general'}"
        return hashlib.md5(cache_str.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[str]:
        """Retrieve cached response if valid"""
        if key in self._cache:
            timestamp = self._timestamps.get(key, 0)
            if time.time() - timestamp < self.ttl:
                self._hit_count[key] = self._hit_count.get(key, 0) + 1
                logger.info(f"✅ Cache HIT (#{self._hit_count[key]}): {key[:12]}...")
                return self._cache[key]
            else:
                # Expired - remove
                self._invalidate(key)
        return None
    
    def set(self, key: str, value: str):
        """Cache a response"""
        self._cache[key] = value
        self._timestamps[key] = time.time()
        self._hit_count[key] = 0
        logger.info(f"💾 Cached: {key[:12]}...")
    
    def _invalidate(self, key: str):
        """Remove expired cache entry"""
        if key in self._cache:
            del self._cache[key]
            del self._timestamps[key]
            if key in self._hit_count:
                del self._hit_count[key]
    
    def clear(self):
        """Clear entire cache"""
        self._cache.clear()
        self._timestamps.clear()
        self._hit_count.clear()
        logger.info("🗑️ Cache cleared")
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        total_hits = sum(self._hit_count.values())
        return {
            'total_entries': len(self._cache),
            'total_hits': total_hits,
            'avg_hits_per_entry': total_hits / len(self._cache) if self._cache else 0
        }


# ============================================================================
# CONVERSATION MEMORY MANAGER - Multi-Layer Memory System
# ============================================================================

class ConversationMemoryManager:
    """
    Advanced memory management with:
    - Short-term memory (recent messages)
    - Long-term memory (conversation summary)
    - Emotional memory (sentiment tracking)
    """
    
    def __init__(
        self,
        short_term_window: int = 10,
        max_tokens_per_message: int = 100
    ):
        self.short_term_window = short_term_window
        self.max_tokens_per_message = max_tokens_per_message
        self.emotional_journey = []
    
    def prepare_context(
        self,
        conversation_history: List[Dict],
        current_message: str,
        max_context_tokens: int = 3000
    ) -> Tuple[List[Dict], Dict]:
        """
        Intelligently prepare conversation context
        
        Returns:
            - messages: Formatted messages for API
            - memory_summary: Summary of older conversations
        """
        if not conversation_history:
            return [], {}
        
        # Step 1: Track emotional journey
        self._track_emotional_journey(conversation_history)
        
        # Step 2: Get recent messages (short-term memory)
        recent_messages = conversation_history[-self.short_term_window:]
        
        # Step 3: Summarize older messages if history is long (long-term memory)
        older_summary = None
        if len(conversation_history) > self.short_term_window:
            older_messages = conversation_history[:-self.short_term_window]
            older_summary = self._create_conversation_summary(older_messages)
        
        # Step 4: Format messages for API
        formatted_messages = []
        for msg in recent_messages:
            role = "user" if msg.get('sender') == 'user' else "assistant"
            content = msg.get('message_text', '')
            
            # Add sentiment indicator for user messages (helps AI track emotions)
            if role == "user" and msg.get('sentiment'):
                sentiment_emoji = get_sentiment_emoji(msg.get('sentiment'))
                content = f"{content} {sentiment_emoji}"
            
            formatted_messages.append({
                'role': role,
                'content': content,
                'timestamp': msg.get('timestamp'),
                'sentiment': msg.get('sentiment')
            })
        
        memory_summary = {
            'older_conversation_summary': older_summary,
            'emotional_journey': self.get_emotional_summary(),
            'total_messages': len(conversation_history)
        }
        
        return formatted_messages, memory_summary
    
    def _track_emotional_journey(self, conversation_history: List[Dict]):
        """Track user's emotional state throughout conversation"""
        self.emotional_journey = []
        for msg in conversation_history:
            if msg.get('sender') == 'user' and msg.get('sentiment'):
                self.emotional_journey.append({
                    'sentiment': msg.get('sentiment'),
                    'compound_score': msg.get('compound_score', 0),
                    'timestamp': msg.get('timestamp')
                })
    
    def _create_conversation_summary(self, messages: List[Dict]) -> str:
        """
        Create intelligent summary of older conversation
        Focus on: key topics, emotional context, important details
        """
        if not messages:
            return ""
        
        # Extract key information
        user_messages = [m for m in messages if m.get('sender') == 'user']
        
        # Identify emotional context
        negative_count = sum(1 for m in user_messages if m.get('sentiment') == 'negative')
        positive_count = sum(1 for m in user_messages if m.get('sentiment') == 'positive')
        
        # Build summary
        summary_parts = [f"Earlier in conversation ({len(messages)} messages):"]
        
        if negative_count > positive_count:
            summary_parts.append(
                f"User was experiencing emotional difficulty (mentioned: "
                f"{self._extract_key_topics(user_messages)})"
            )
        elif positive_count > 0:
            summary_parts.append("User had positive interactions")
        
        # Add key topics
        key_topics = self._extract_key_topics(user_messages)
        if key_topics:
            summary_parts.append(f"Key topics discussed: {key_topics}")
        
        return " ".join(summary_parts)
    
    def _extract_key_topics(self, messages: List[Dict], max_topics: int = 3) -> str:
        """Extract key topics from messages"""
        # Simple keyword extraction (can be enhanced with NLP)
        keywords = set()
        emotional_keywords = [
            'breakup', 'relationship', 'sad', 'happy', 'anxious', 
            'work', 'family', 'friend', 'love', 'hurt', 'pain'
        ]
        
        for msg in messages:
            text = msg.get('message_text', '').lower()
            for keyword in emotional_keywords:
                if keyword in text:
                    keywords.add(keyword)
        
        return ", ".join(list(keywords)[:max_topics]) if keywords else "general conversation"
    
    def get_emotional_summary(self) -> Dict:
        """Get summary of emotional journey"""
        if not self.emotional_journey:
            return {'status': 'no_data'}
        
        sentiments = [e['sentiment'] for e in self.emotional_journey]
        scores = [e['compound_score'] for e in self.emotional_journey]
        
        return {
            'current_sentiment': sentiments[-1] if sentiments else 'neutral',
            'dominant_sentiment': max(set(sentiments), key=sentiments.count) if sentiments else 'neutral',
            'sentiment_trend': 'improving' if len(scores) >= 2 and scores[-1] > scores[0] else 'stable/declining',
            'avg_score': sum(scores) / len(scores) if scores else 0,
            'journey_length': len(self.emotional_journey)
        }


# ============================================================================
# MAIN GROQ SERVICE - Production-Grade LLM Interface
# ============================================================================

class GroqService:
    """
    Production-grade LLM service with:
    - Intelligent memory management
    - Emotion-aware responses
    - Smart caching
    - Token optimization
    - Cost tracking
    """
    
    def __init__(self, api_key: str = None):
        # API Setup
        if api_key is None:
            api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError(
                "Groq API key is required. Set GROQ_API_KEY environment variable."
            )
        
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"  # Fast and capable
        
        # Feature Flags
        self.enable_reasoning = True
        self.enable_task_detection = True
        self.enable_sentiment_adaptation = True
        self.enable_cache = True
        self.enable_smart_memory = True
        
        # Components
        self.cache = IntelligentCache(ttl=3600)
        self.memory_manager = ConversationMemoryManager(
            short_term_window=10,  # Last 10 messages
            max_tokens_per_message=100
        )
        
        # Metrics
        self.total_requests = 0
        self.total_tokens_used = 0
        self.cache_hits = 0
        self.cache_misses = 0
        
        logger.info("✅ GroqService initialized with advanced features")
    
    def generate_response(
        self,
        user_message: str,
        conversation_history: List[Dict] = None,
        user_sentiment: str = None,
        base_style: str = "default",
        user_id: str = None
    ) -> str:
        """
        Generate intelligent, context-aware response
        
        Args:
            user_message: Current user message
            conversation_history: Previous conversation messages
            user_sentiment: Current sentiment (positive/negative/neutral)
            base_style: Response style
            user_id: User identifier for personalization
        
        Returns:
            Bot response string
        """
        self.total_requests += 1
        start_time = time.time()
        
        if conversation_history is None:
            conversation_history = []
        
        try:
            # Step 1: Detect task type and context
            task_type = self._detect_task_type(user_message, conversation_history)
            context = detect_context(conversation_history, user_message)
            
            logger.info(f"📊 Request #{self.total_requests} | Task: {task_type} | Context: {context} | Sentiment: {user_sentiment}")
            
            # Step 2: Check cache (skip for emotional support - needs fresh responses)
            if self.enable_cache and task_type != "emotional_support":
                cache_key = self.cache.get_key(user_message, user_sentiment, task_type)
                cached_response = self.cache.get(cache_key)
                if cached_response:
                    self.cache_hits += 1
                    return cached_response
                self.cache_misses += 1
            
            # Step 3: Prepare conversation memory
            formatted_history, memory_summary = self.memory_manager.prepare_context(
                conversation_history,
                user_message,
                max_context_tokens=3000
            )
            
            # Step 4: Build enhanced system prompt
            system_prompt = self._build_enhanced_system_prompt(
                base_style=base_style,
                user_sentiment=user_sentiment,
                task_type=task_type,
                context=context,
                formatted_history=formatted_history,
                memory_summary=memory_summary
            )
            
            # Step 5: Prepare messages for API
            messages = self._prepare_api_messages(
                system_prompt=system_prompt,
                formatted_history=formatted_history,
                current_message=user_message,
                user_sentiment=user_sentiment
            )
            
            # Step 6: Call LLM with optimized parameters
            response = self._call_llm(
                messages=messages,
                task_type=task_type,
                user_sentiment=user_sentiment
            )
            
            # Step 7: Post-process response
            bot_response = self._post_process_response(
                response,
                user_sentiment=user_sentiment,
                task_type=task_type
            )
            
            # Step 8: Cache if appropriate
            if self.enable_cache and task_type != "emotional_support":
                cache_key = self.cache.get_key(user_message, user_sentiment, task_type)
                self.cache.set(cache_key, bot_response)
            
            # Log metrics
            elapsed_time = time.time() - start_time
            logger.info(f"✅ Response generated in {elapsed_time:.2f}s | Length: {len(bot_response)} chars")
            
            return bot_response
            
        except Exception as e:
            logger.error(f"❌ Error generating response: {str(e)}", exc_info=True)
            return self._handle_error(e)
    
    def _detect_task_type(self, user_message: str, conversation_history: List[Dict]) -> str:
        """Enhanced task detection with conversation context"""
        if not self.enable_task_detection:
            return "casual_chat"
        
        return detect_task_type(user_message, conversation_history)
    
    def _build_enhanced_system_prompt(
        self,
        base_style: str,
        user_sentiment: str,
        task_type: str,
        context: str,
        formatted_history: List[Dict],
        memory_summary: Dict
    ) -> str:
        """Build comprehensive system prompt with memory integration"""
        
        # Base prompt with all features
        system_prompt = build_system_prompt(
            base_style=base_style,
            user_sentiment=user_sentiment if self.enable_sentiment_adaptation else None,
            task_type=task_type,
            context=context,
            conversation_history=formatted_history,
            enable_memory=self.enable_smart_memory
        )
        
        # Add memory summary if we have older conversation data
        if memory_summary.get('older_conversation_summary'):
            system_prompt += f"\n\n📚 **EARLIER CONVERSATION CONTEXT:**\n{memory_summary['older_conversation_summary']}"
        
        # Add emotional journey summary for ongoing emotional support
        if task_type == "emotional_support" and memory_summary.get('emotional_journey'):
            emotional_summary = memory_summary['emotional_journey']
            system_prompt += f"\n\n💭 **EMOTIONAL JOURNEY:**\n"
            system_prompt += f"- Current sentiment: {emotional_summary.get('current_sentiment', 'unknown')}\n"
            system_prompt += f"- Trend: {emotional_summary.get('sentiment_trend', 'unknown')}\n"
            system_prompt += f"- Average emotional score: {emotional_summary.get('avg_score', 0):.2f}\n"
            system_prompt += "CRITICAL: Acknowledge this emotional journey in your response!"
        
        return system_prompt
    
    def _prepare_api_messages(
        self,
        system_prompt: str,
        formatted_history: List[Dict],
        current_message: str,
        user_sentiment: str = None
    ) -> List[Dict]:
        """Prepare messages array for API call"""
        
        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]
        
        # Add conversation history (already formatted and limited)
        for msg in formatted_history:
            messages.append({
                "role": msg['role'],
                "content": msg['content']
            })
        
        # Add current message (with sentiment indicator if available)
        current_content = current_message
        if user_sentiment:
            sentiment_emoji = get_sentiment_emoji(user_sentiment)
            current_content = f"{current_message} {sentiment_emoji}"
        
        messages.append({
            "role": "user",
            "content": current_content
        })
        
        return messages
    
    def _call_llm(
        self,
        messages: List[Dict],
        task_type: str,
        user_sentiment: str = None
    ) -> str:
        """Call Groq API with optimized parameters"""
        
        # Get task-appropriate parameters
        max_tokens = self._get_max_tokens(task_type, user_sentiment)
        temperature = self._get_temperature(task_type)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=0.9,
                frequency_penalty=0.3,  # Reduce repetition
                presence_penalty=0.2,   # Encourage topic diversity
                stop=None  # Let model decide when to stop
            )
            
            # Track token usage
            if hasattr(response, 'usage'):
                self.total_tokens_used += response.usage.total_tokens
                logger.info(f"🎯 Tokens used: {response.usage.total_tokens} (Total: {self.total_tokens_used})")
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"❌ LLM API call failed: {str(e)}")
            raise
    
    def _get_max_tokens(self, task_type: str, user_sentiment: str = None) -> int:
        """
        REDUCED token allocation for brevity - 3-4 sentences max
        """
        # REDUCED: Emotional support should be brief but caring
        if task_type in ['emotional_support', 'health_wellness']:
            return 150  # ~3-4 sentences max
        
        elif task_type in ['debugging', 'technical_explanation', 'code_help']:
            return 180
        
        elif task_type in ['math_help', 'data_analysis', 'learning_tutor']:
            return 150
        
        elif task_type in ['creative_writing', 'brainstorming']:
            return 140
        
        elif task_type in ['career_advice', 'business_strategy']:
            return 130
        
        else:
            # Casual chat - keep SHORT
            return 100
    
    def _get_temperature(self, task_type: str) -> float:
        """
        Task-appropriate temperature settings
        
        Higher temperature = more creative/varied
        Lower temperature = more focused/consistent
        """
        temperature_map = {
            # Creative tasks - high temperature
            'creative_writing': 0.9,
            'brainstorming': 0.9,
            
            # Emotional support - balanced (empathetic but consistent)
            'emotional_support': 0.7,
            'health_wellness': 0.7,
            'casual_chat': 0.7,
            
            # Advisory tasks - moderate
            'career_advice': 0.6,
            'business_strategy': 0.6,
            'learning_tutor': 0.6,
            
            # Technical tasks - low temperature (precision matters)
            'code_help': 0.5,
            'problem_solving': 0.5,
            'technical_explanation': 0.4,
            'debugging': 0.3,
            'math_help': 0.3,
            'data_analysis': 0.3
        }
        
        return temperature_map.get(task_type, 0.7)
    
    def _post_process_response(
        self,
        response: str,
        user_sentiment: str = None,
        task_type: str = None
    ) -> str:
        """
        ENFORCES brevity - max 4 sentences for ALL responses
        """
        # Clean up whitespace
        response = ' '.join(response.split())
        
        # HARD LIMIT: Maximum 4 sentences for ANY response type
        sentences = response.split('. ')
        if len(sentences) > 4:
            response = '. '.join(sentences[:4])
            # Add period if needed
            if not response.endswith('.'):
                response += '.'
        
        # Remove any incomplete sentences at the end
        if response.count('.') > 0:
            # Keep only complete sentences
            parts = response.split('.')
            complete_parts = [p.strip() for p in parts if len(p.strip()) > 10]
            if complete_parts:
                response = '. '.join(complete_parts) + '.'
        
        # Quality check for negative sentiment responses
        if user_sentiment == 'negative':
            empathy_words = ['sorry', 'understand', 'hear', 'know', 'feel', 'here for you', 'difficult', 'hard']
            if not any(word in response.lower() for word in empathy_words):
                logger.warning(f"⚠️ Response to negative sentiment may lack empathy")
        
        return response.strip()
    
    def _handle_error(self, error: Exception) -> str:
        """Handle errors gracefully with user-friendly messages"""
        error_str = str(error).lower()
        
        if 'timeout' in error_str or 'connection' in error_str:
            return "I'm having trouble connecting right now. Could you try again in a moment?"
        
        elif 'api key' in error_str or 'unauthorized' in error_str or 'authentication' in error_str:
            logger.error("❌ Authentication error - check API key")
            return "There seems to be a configuration issue. Please contact support if this persists."
        
        elif 'rate limit' in error_str:
            return "I'm receiving a lot of requests right now. Please wait a moment and try again."
        
        elif 'context' in error_str or 'token' in error_str:
            return "Our conversation has gotten quite long. Would you like to start fresh?"
        
        else:
            logger.error(f"❌ Unexpected error: {error_str}")
            return "I encountered an unexpected issue. Could you try rephrasing your message?"
    
    # ========================================================================
    # CONFIGURATION & MONITORING
    # ========================================================================
    
    def set_agentic_features(
        self,
        enable_reasoning: bool = True,
        enable_task_detection: bool = True,
        enable_sentiment_adaptation: bool = True,
        enable_smart_memory: bool = True
    ):
        """Configure agentic features"""
        self.enable_reasoning = enable_reasoning
        self.enable_task_detection = enable_task_detection
        self.enable_sentiment_adaptation = enable_sentiment_adaptation
        self.enable_smart_memory = enable_smart_memory
        
        logger.info(f"🔧 Features updated - Reasoning: {enable_reasoning}, Task Detection: {enable_task_detection}, Sentiment: {enable_sentiment_adaptation}, Smart Memory: {enable_smart_memory}")
    
    def get_metrics(self) -> Dict:
        """Get service metrics"""
        cache_stats = self.cache.get_stats()
        
        return {
            'total_requests': self.total_requests,
            'total_tokens_used': self.total_tokens_used,
            'avg_tokens_per_request': self.total_tokens_used / self.total_requests if self.total_requests > 0 else 0,
            'cache_hit_rate': self.cache_hits / (self.cache_hits + self.cache_misses) if (self.cache_hits + self.cache_misses) > 0 else 0,
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'cache_entries': cache_stats['total_entries'],
            'timestamp': datetime.now().isoformat()
        }
    
    def reset_metrics(self):
        """Reset all metrics"""
        self.total_requests = 0
        self.total_tokens_used = 0
        self.cache_hits = 0
        self.cache_misses = 0
        logger.info("📊 Metrics reset")
    
    def clear_cache(self):
        """Clear response cache"""
        self.cache.clear()
    
    def export_metrics(self, filepath: str = "groq_service_metrics.json"):
        """Export metrics to file"""
        metrics = self.get_metrics()
        with open(filepath, 'w') as f:
            json.dump(metrics, f, indent=2)
        logger.info(f"📁 Metrics exported to {filepath}")


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    'GroqService',
    'IntelligentCache',
    'ConversationMemoryManager'
]