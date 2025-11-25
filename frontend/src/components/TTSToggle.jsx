import React from 'react';
import './TTSToggle.css';
const TTSToggle = ({ isEnabled, onToggle }) => {
  return (
    <button 
      className={`tts-toggle ${isEnabled ? 'active' : ''}`}
      onClick={onToggle}
      title={isEnabled ? 'Disable bot voice' : 'Enable bot voice'}
    >
      {isEnabled ? '🗣️' : '🔇'}
    </button>
  );
};
export default TTSToggle;