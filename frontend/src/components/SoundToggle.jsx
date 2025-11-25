import React from 'react';
import './SoundToggle.css';
const SoundToggle = ({ isEnabled, onToggle }) => {
  return (
    <button 
      className="sound-toggle" 
      onClick={onToggle}
      title={isEnabled ? 'Mute sounds' : 'Enable sounds'}
    >
      {isEnabled ? '🔊' : '🔇'}
    </button>
  );
};
export default SoundToggle;