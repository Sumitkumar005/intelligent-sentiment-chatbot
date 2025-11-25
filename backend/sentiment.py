from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict, List
import logging
logger = logging.getLogger(__name__)
class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
    def analyze_message(self, text: str) -> Dict:
        try:
            scores = self.analyzer.polarity_scores(text)
            compound = scores['compound']
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