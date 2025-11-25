import React, { useState, useEffect } from 'react';
import './VoiceInput.css';
const VoiceInput = ({ onTranscript }) => {
  const [isListening, setIsListening] = useState(false);
  const [recognition, setRecognition] = useState(null);
  const [isSupported, setIsSupported] = useState(true);
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setIsSupported(false);
      return;
    }
    const recognitionInstance = new SpeechRecognition();
    recognitionInstance.continuous = false;
    recognitionInstance.interimResults = false;
    recognitionInstance.lang = 'en-US';
    recognitionInstance.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      onTranscript(transcript);
      setIsListening(false);
    };
    recognitionInstance.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
      setIsListening(false);
      
      // Show user-friendly error messages
      if (event.error === 'not-allowed') {
        alert('Microphone access denied. Please allow microphone access in your browser settings.');
      } else if (event.error === 'no-speech') {
        alert('No speech detected. Please try again.');
      } else if (event.error === 'network') {
        alert('Network error. Please check your internet connection.');
      } else {
        alert(`Speech recognition error: ${event.error}`);
      }
    };
    recognitionInstance.onend = () => {
      setIsListening(false);
    };
    setRecognition(recognitionInstance);
  }, [onTranscript]);
  const toggleListening = () => {
    if (!recognition) return;
    
    if (isListening) {
      recognition.stop();
      setIsListening(false);
    } else {
      try {
        recognition.start();
        setIsListening(true);
      } catch (error) {
        console.error('Failed to start recognition:', error);
        alert('Failed to start microphone. Please check browser permissions.');
      }
    }
  };
  if (!isSupported) {
    return null; 
  }
  return (
    <button
      type="button"
      className={`voice-input-btn ${isListening ? 'listening' : ''}`}
      onClick={toggleListening}
      title={isListening ? 'Stop listening' : 'Voice input'}
    >
      <img 
        src="/microphone.png" 
        alt="Microphone" 
        className="mic-icon"
      />
    </button>
  );
};
export default VoiceInput;