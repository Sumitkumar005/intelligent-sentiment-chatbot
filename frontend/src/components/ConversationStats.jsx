import React from 'react';
import './ConversationStats.css';
const ConversationStats = ({ messages }) => {
  const userMessages = messages.filter(m => m.sender === 'user');
  const botMessages = messages.filter(m => m.sender === 'bot');
  const sentimentCounts = {
    positive: userMessages.filter(m => m.sentiment === 'positive').length,
    neutral: userMessages.filter(m => m.sentiment === 'neutral').length,
    negative: userMessages.filter(m => m.sentiment === 'negative').length
  };
  const totalWords = messages.reduce((sum, msg) => 
    sum + msg.message_text.split(' ').length, 0
  );
  const avgWordsPerMessage = messages.length > 0 
    ? Math.round(totalWords / messages.length) 
    : 0;
  return (
    <div className="conversation-stats">
      <h3 className="stats-title">📊 Conversation Stats</h3>
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value">{messages.length}</div>
          <div className="stat-label">Total Messages</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{userMessages.length}</div>
          <div className="stat-label">Your Messages</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{botMessages.length}</div>
          <div className="stat-label">Bot Replies</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{avgWordsPerMessage}</div>
          <div className="stat-label">Avg Words/Message</div>
        </div>
      </div>
      <div className="sentiment-stats">
        <h4>Sentiment Breakdown</h4>
        <div className="sentiment-bars">
          <div className="sentiment-bar-item">
            <span className="sentiment-bar-label">😊 Positive</span>
            <div className="sentiment-bar-track">
              <div 
                className="sentiment-bar-fill positive"
                style={{ width: `${(sentimentCounts.positive / userMessages.length * 100) || 0}%` }}
              />
            </div>
            <span className="sentiment-bar-count">{sentimentCounts.positive}</span>
          </div>
          <div className="sentiment-bar-item">
            <span className="sentiment-bar-label">😐 Neutral</span>
            <div className="sentiment-bar-track">
              <div 
                className="sentiment-bar-fill neutral"
                style={{ width: `${(sentimentCounts.neutral / userMessages.length * 100) || 0}%` }}
              />
            </div>
            <span className="sentiment-bar-count">{sentimentCounts.neutral}</span>
          </div>
          <div className="sentiment-bar-item">
            <span className="sentiment-bar-label">😞 Negative</span>
            <div className="sentiment-bar-track">
              <div 
                className="sentiment-bar-fill negative"
                style={{ width: `${(sentimentCounts.negative / userMessages.length * 100) || 0}%` }}
              />
            </div>
            <span className="sentiment-bar-count">{sentimentCounts.negative}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
export default ConversationStats;