import React, { useState } from 'react';
import './MessageActions.css';
const MessageActions = ({ message, onDelete }) => {
  const [showActions, setShowActions] = useState(false);
  const [copied, setCopied] = useState(false);
  const handleCopy = () => {
    navigator.clipboard.writeText(message.message_text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  return (
    <div 
      className="message-actions-container"
      onMouseEnter={() => setShowActions(true)}
      onMouseLeave={() => setShowActions(false)}
    >
      {showActions && (
        <div className="message-actions">
          <button 
            className="action-btn copy-btn" 
            onClick={handleCopy}
            title="Copy message"
          >
            {copied ? '✓' : '📋'}
          </button>
          {message.sender === 'user' && onDelete && (
            <button 
              className="action-btn delete-btn" 
              onClick={() => onDelete(message.id)}
              title="Delete message"
            >
              🗑️
            </button>
          )}
        </div>
      )}
    </div>
  );
};
export default MessageActions;