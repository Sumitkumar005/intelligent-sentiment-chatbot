import React from 'react';
import './TypingIndicator.css';
const TypingIndicator = () => {
  return (
    <div className="message message-bot">
      <div className="message-content typing-indicator">
        <div className="typing-dots">
          <span className="dot"></span>
          <span className="dot"></span>
          <span className="dot"></span>
        </div>
        <span className="typing-text">Bot is typing...</span>
      </div>
    </div>
  );
};
export default TypingIndicator;