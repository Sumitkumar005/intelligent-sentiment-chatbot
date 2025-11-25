import React, { useState } from 'react';
import './EmojiReactions.css';
const EmojiReactions = ({ message, onReact }) => {
  const [showReactions, setShowReactions] = useState(false);
  const [selectedReaction, setSelectedReaction] = useState(message.reaction || null);
  const reactions = ['👍', '👎', '❤️', '😂', '😮', '🎉'];
  const handleReact = (emoji) => {
    setSelectedReaction(emoji);
    onReact(message.id, emoji);
    setShowReactions(false);
  };
  if (message.sender !== 'bot') return null;
  return (
    <div 
      className="emoji-reactions-container"
      onMouseEnter={() => setShowReactions(true)}
      onMouseLeave={() => setShowReactions(false)}
    >
      {selectedReaction && (
        <span className="selected-reaction">{selectedReaction}</span>
      )}
      {showReactions && (
        <div className="emoji-reactions-picker">
          {reactions.map((emoji) => (
            <button
              key={emoji}
              className={`reaction-btn ${selectedReaction === emoji ? 'selected' : ''}`}
              onClick={() => handleReact(emoji)}
            >
              {emoji}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};
export default EmojiReactions;