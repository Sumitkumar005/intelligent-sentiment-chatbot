from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict, List, Optional
import logging
logger = logging.getLogger(__name__)
class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
    def analyze_message(self, text: str, conversation_history: List[Dict] = None) -> Dict:
        """
        Context-aware sentiment analysis
        Considers conversation history to avoid misclassifying messages in emotional contexts
        """
        try:
            scores = self.analyzer.polarity_scores(text)
            compound = scores['compound']
            
            # Check conversation context for ongoing emotional topics
            ongoing_negative_context = False
            if conversation_history:
                # Check last 5 messages for emotional keywords
                recent_messages = conversation_history[-5:]
                sad_keywords = [
                    'breakup', 'break up', 'broke up', 'died', 'death', 'sad', 
                    'cry', 'crying', 'devastated', 'hurt', 'hurting', 'pain', 
                    'painful', 'depressed', 'lonely', 'heartbroken', 'grief',
                    'miss her', 'miss him', 'lost', 'divorce', 'separated'
                ]
                
                for msg in recent_messages:
                    if msg.get('sender') == 'user':
                        msg_text = msg.get('message_text', '').lower()
                        if any(keyword in msg_text for keyword in sad_keywords):
                            ongoing_negative_context = True
                            break
            
            # CRITICAL FIX: Override sentiment if in negative context
            # Example: "Her name was Sarah" after breakup should be negative, not positive
            if ongoing_negative_context:
                # If message is neutral or slightly positive but we're in sad context
                if compound > -0.3:  # Not strongly positive
                    # Check if message is actually trying to be positive
                    positive_indicators = [
                        'happy', 'great', 'wonderful', 'excited', 'better', 
                        'good', 'ready', 'moving on', 'feeling better'
                    ]
                    is_genuinely_positive = any(word in text.lower() for word in positive_indicators)
                    
                    if not is_genuinely_positive:
                        # Force negative/neutral for context continuity
                        compound = -0.15
                        sentiment = 'negative'
                    else:
                        # User is genuinely trying to be positive
                        if compound >= 0.05:
                            sentiment = 'positive'
                        else:
                            sentiment = 'neutral'
                else:
                    sentiment = 'negative'
            else:
                # Normal classification when no negative context
                if compound >= 0.05:
                    sentiment = 'positive'
                elif compound <= -0.05:
                    sentiment = 'negative'
                else:
                    sentiment = 'neutral'
            
            confidence = abs(compound)
            return {
                'sentiment': sentiment,
                'score': compound,
                'confidence': confidence,
                'compound_score': compound
            }
        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")
            return {
                'sentiment': 'neutral',
                'score': 0.0,
                'confidence': 0.0,
                'compound_score': 0.0
            }
    def analyze_conversation(self, messages: List[Dict]) -> Dict:
        user_messages = [m for m in messages if m.get('sender') == 'user']
        if not user_messages:
            return {
                'overall_sentiment': None,
                'explanation': 'No user messages to analyze',
                'sentiment_distribution': {
                    'positive': 0,
                    'negative': 0,
                    'neutral': 0
                },
                'average_score': 0.0
            }
        scores = []
        sentiments = []
        for msg in user_messages:
            analysis = self.analyze_message(msg.get('message_text', ''))
            scores.append(analysis['score'])
            sentiments.append(analysis['sentiment'])
        avg_score = sum(scores) / len(scores)
        if avg_score >= 0.05:
            overall = 'positive'
            explanation = f'Overall positive sentiment across {len(user_messages)} messages'
        elif avg_score <= -0.05:
            overall = 'negative'
            explanation = f'Overall negative sentiment across {len(user_messages)} messages'
        else:
            overall = 'neutral'
            explanation = f'Overall neutral sentiment across {len(user_messages)} messages'
        distribution = {
            'positive': sum(1 for s in scores if s >= 0.05),
            'negative': sum(1 for s in scores if s <= -0.05),
            'neutral': sum(1 for s in scores if -0.05 < s < 0.05)
        }
        return {
            'overall_sentiment': overall,
            'explanation': explanation,
            'sentiment_distribution': distribution,
            'average_score': avg_score
        }