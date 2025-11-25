from sentiment import SentimentAnalyzer
def test_clearly_positive_message():
    analyzer = SentimentAnalyzer()
    positive_messages = [
        "I love this! It's amazing and wonderful!",
        "This is the best day ever! So happy!",
        "Excellent work! I'm very pleased and excited!"
    ]
    for msg in positive_messages:
        result = analyzer.analyze_message(msg)
        assert result['sentiment'] == 'positive', \
            f"Message '{msg}' should be classified as positive"
        assert result['score'] > 0, "Positive message should have positive score"
def test_clearly_negative_message():
    analyzer = SentimentAnalyzer()
    negative_messages = [
        "This is terrible and awful. I hate it!",
        "Worst experience ever. Very disappointed and angry.",
        "Horrible service. Completely unsatisfied and frustrated."
    ]
    for msg in negative_messages:
        result = analyzer.analyze_message(msg)
        assert result['sentiment'] == 'negative', \
            f"Message '{msg}' should be classified as negative"
        assert result['score'] < 0, "Negative message should have negative score"
def test_neutral_message():
    analyzer = SentimentAnalyzer()
    neutral_messages = [
        "The meeting is at 3pm.",
        "I went to the store today.",
        "The document has been updated."
    ]
    for msg in neutral_messages:
        result = analyzer.analyze_message(msg)
        assert result['sentiment'] == 'neutral', \
            f"Message '{msg}' should be classified as neutral"
        assert abs(result['score']) < 0.05, "Neutral message should have score near zero"
def test_empty_conversation_sentiment():
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze_conversation([])
    assert result['overall_sentiment'] is None, "Empty conversation should have None sentiment"
    assert result['explanation'] == 'No user messages to analyze'
    messages = [
        {'sender': 'bot', 'message_text': 'Hello!'},
        {'sender': 'bot', 'message_text': 'How can I help?'}
    ]
    result = analyzer.analyze_conversation(messages)
    assert result['overall_sentiment'] is None, "Conversation with no user messages should have None sentiment"
    assert result['explanation'] == 'No user messages to analyze'
def test_conversation_with_mixed_sentiments():
    analyzer = SentimentAnalyzer()
    messages = [
        {'sender': 'user', 'message_text': 'I love this product!'},
        {'sender': 'bot', 'message_text': 'Great to hear!'},
        {'sender': 'user', 'message_text': 'But the shipping was terrible.'},
        {'sender': 'user', 'message_text': 'Overall it was okay.'}
    ]
    result = analyzer.analyze_conversation(messages)
    assert result['overall_sentiment'] in {'positive', 'negative', 'neutral'}
    assert len(result['explanation']) > 0
    assert 'sentiment_distribution' in result
    assert sum(result['sentiment_distribution'].values()) == 3