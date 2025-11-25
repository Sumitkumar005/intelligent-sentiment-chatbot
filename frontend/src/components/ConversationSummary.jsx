import React from 'react';
import SentimentBadge from './SentimentBadge';
import './ConversationSummary.css';
const ConversationSummary = ({ sentimentData }) => {
  if (!sentimentData || !sentimentData.overall_sentiment) {
    return null;
  }
  const { overall_sentiment, explanation, sentiment_distribution } = sentimentData;
  const total = sentiment_distribution
    ? sentiment_distribution.positive + sentiment_distribution.negative + sentiment_distribution.neutral
    : 0;
  const getPercentage = (count) => {
    if (total === 0) return 0;
    return Math.round((count / total) * 100);
  };
  return (
    <div className="conversation-summary">
      <h3 className="summary-title">Conversation Sentiment Summary</h3>
      <div className="summary-overall">
        <span className="summary-label">Overall Sentiment:</span>
        <SentimentBadge sentiment={overall_sentiment} />
      </div>
      {explanation && (
        <p className="summary-explanation">{explanation}</p>
      )}
      {sentiment_distribution && (
        <div className="summary-distribution">
          <h4 className="distribution-title">Sentiment Distribution</h4>
          <div className="distribution-bars">
            <div className="distribution-item">
              <div className="distribution-label">
                <span className="distribution-icon">😊</span>
                <span>Positive</span>
                <span className="distribution-count">
                  {sentiment_distribution.positive} ({getPercentage(sentiment_distribution.positive)}%)
                </span>
              </div>
              <div className="distribution-bar">
                <div
                  className="distribution-fill distribution-fill-positive"
                  style={{ width: `${getPercentage(sentiment_distribution.positive)}%` }}
                />
              </div>
            </div>
            <div className="distribution-item">
              <div className="distribution-label">
                <span className="distribution-icon">😐</span>
                <span>Neutral</span>
                <span className="distribution-count">
                  {sentiment_distribution.neutral} ({getPercentage(sentiment_distribution.neutral)}%)
                </span>
              </div>
              <div className="distribution-bar">
                <div
                  className="distribution-fill distribution-fill-neutral"
                  style={{ width: `${getPercentage(sentiment_distribution.neutral)}%` }}
                />
              </div>
            </div>
            <div className="distribution-item">
              <div className="distribution-label">
                <span className="distribution-icon">😞</span>
                <span>Negative</span>
                <span className="distribution-count">
                  {sentiment_distribution.negative} ({getPercentage(sentiment_distribution.negative)}%)
                </span>
              </div>
              <div className="distribution-bar">
                <div
                  className="distribution-fill distribution-fill-negative"
                  style={{ width: `${getPercentage(sentiment_distribution.negative)}%` }}
                />
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
export default ConversationSummary;