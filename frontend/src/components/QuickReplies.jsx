import React from 'react';
import './QuickReplies.css';
const QuickReplies = ({ onSelect }) => {
  const suggestions = [
    { text: "How are you?", emoji: "👋" },
    { text: "Tell me a joke", emoji: "😄" },
    { text: "I'm feeling great!", emoji: "😊" },
    { text: "I need help", emoji: "🆘" },
    { text: "Thank you", emoji: "🙏" },
    { text: "What can you do?", emoji: "❓" }
  ];
  return (
    <div className="quick-replies">
      <div className="quick-replies-label">Quick replies:</div>
      <div className="quick-replies-list">
        {suggestions.map((suggestion, index) => (
          <button
            key={index}
            className="quick-reply-btn"
            onClick={() => onSelect(suggestion.text)}
          >
            <span className="quick-reply-emoji">{suggestion.emoji}</span>
            <span className="quick-reply-text">{suggestion.text}</span>
          </button>
        ))}
      </div>
    </div>
  );
};
export default QuickReplies;