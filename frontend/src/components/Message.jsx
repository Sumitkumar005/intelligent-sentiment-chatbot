import React from 'react';
import SentimentBadge from './SentimentBadge';
import MessageActions from './MessageActions';
import EmojiReactions from './EmojiReactions';
import './Message.css';
const Message = ({ message, onDelete, onReact }) => {
  const { sender, message_text, sentiment, timestamp } = message;
  const isUser = sender === 'user';
  const formatTimestamp = (timestamp) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };
  return (
    <div className={`message ${isUser ? 'message-user' : 'message-bot'}`}>
      <div className="message-content">
        <MessageActions message={message} onDelete={onDelete} />
        <EmojiReactions message={message} onReact={onReact} />
        <div className="message-header">
          <span className="message-sender">
            {isUser ? 'You' : 'Bot'}
          </span>
          <span className="message-timestamp">
            {formatTimestamp(timestamp)}
          </span>
        </div>
        <div className="message-text">{message_text}</div>
        {isUser && sentiment && (
          <div className="message-sentiment">
            <SentimentBadge sentiment={sentiment} />
          </div>
        )}
      </div>
    </div>
  );
};
export default Message;