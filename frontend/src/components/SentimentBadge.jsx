import React from 'react';
import './SentimentBadge.css';
const SentimentBadge = ({ sentiment }) => {
  if (!sentiment) return null;
  const getSentimentConfig = (sentiment) => {
    switch (sentiment.toLowerCase()) {
      case 'positive':
        return {
          className: 'sentiment-badge-positive',
          icon: '😊',
          label: 'Happy',
        };
      case 'negative':
        return {
          className: 'sentiment-badge-negative',
          icon: '😢',
          label: 'Sad',
        };
      case 'neutral':
        return {
          className: 'sentiment-badge-neutral',
          icon: '😐',
          label: 'Neutral',
        };
      default:
        return {
          className: 'sentiment-badge-neutral',
          icon: '😐',
          label: 'Neutral',
        };
    }
  };
  const config = getSentimentConfig(sentiment);
  return (
    <span className={`sentiment-badge ${config.className}`}>
      <span className="sentiment-icon">{config.icon}</span>
      <span className="sentiment-label">{config.label}</span>
    </span>
  );
};
export default SentimentBadge;