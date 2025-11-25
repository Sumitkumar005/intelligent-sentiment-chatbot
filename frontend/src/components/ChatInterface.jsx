import React, { useState, useEffect, useRef } from 'react';
import Message from './Message';
import ConversationSummary from './ConversationSummary';
import ConversationStats from './ConversationStats';
import TypingIndicator from './TypingIndicator';
import ThemeToggle from './ThemeToggle';
import SoundToggle from './SoundToggle';
import TTSToggle from './TTSToggle';
import VoiceInput from './VoiceInput';
import LanguageSelector from './LanguageSelector';
import ImageUpload from './ImageUpload';
import { sendMessage, getConversationSentiment } from '../services/api';
import { exportAsText, exportAsJSON } from '../utils/exportConversation';
import soundEffects from '../utils/soundEffects';
import textToSpeech from '../utils/textToSpeech';
import './ChatInterface.css';
const ChatInterface = ({ conversationId, user, onLogout, showSidebar, onToggleSidebar, isDarkMode, onToggleDarkMode }) => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sentimentSummary, setSentimentSummary] = useState(null);
  const [showSummary, setShowSummary] = useState(false);
  const [loadingHistory, setLoadingHistory] = useState(true);
  const [soundEnabled, setSoundEnabled] = useState(soundEffects.isEnabled());
  const [ttsEnabled, setTtsEnabled] = useState(textToSpeech.isEnabled());
  const [currentLanguage, setCurrentLanguage] = useState(localStorage.getItem('language') || 'en');
  const [selectedImage, setSelectedImage] = useState(null);
  const [showHeader, setShowHeader] = useState(true);
  const [alienPosition, setAlienPosition] = useState({ x: 50, y: 30 }); 
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const alienRef = useRef(null);
  const toggleFullscreen = () => {
    const newShowHeader = !showHeader;
    setShowHeader(newShowHeader);
    if (!newShowHeader && showSidebar) {
      onToggleSidebar();
    }
  };
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  useEffect(() => {
    loadConversationHistory();
  }, [conversationId]);
  useEffect(() => {
    if (!loadingHistory) {
      inputRef.current?.focus();
    }
  }, [loadingHistory]);
  useEffect(() => {
    if (messages.length === 0) return; 
    const moveAlien = () => {
      const safePositions = [
        { x: 5, y: 5 },     { x: 15, y: 5 },    { x: 25, y: 5 },
        { x: 35, y: 5 },    { x: 45, y: 5 },    { x: 55, y: 5 },
        { x: 65, y: 5 },    { x: 75, y: 5 },    { x: 85, y: 5 },
        { x: 5, y: 20 },    { x: 20, y: 20 },   { x: 40, y: 20 },
        { x: 60, y: 20 },   { x: 80, y: 20 },   { x: 90, y: 20 },
        { x: 5, y: 35 },    { x: 15, y: 35 },   { x: 85, y: 35 },   { x: 90, y: 35 },
        { x: 5, y: 50 },    { x: 20, y: 50 },   { x: 40, y: 50 },
        { x: 60, y: 50 },   { x: 80, y: 50 },   { x: 90, y: 50 },
        { x: 5, y: 65 },    { x: 15, y: 65 },   { x: 85, y: 65 },   { x: 90, y: 65 },
        { x: 5, y: 80 },    { x: 15, y: 80 },   { x: 25, y: 80 },
        { x: 35, y: 80 },   { x: 45, y: 80 },   { x: 55, y: 80 },
        { x: 65, y: 80 },   { x: 75, y: 80 },   { x: 85, y: 80 },
      ];
      let newPosition;
      do {
        newPosition = safePositions[Math.floor(Math.random() * safePositions.length)];
      } while (newPosition.x === alienPosition.x && newPosition.y === alienPosition.y);
      setAlienPosition(newPosition);
    };
    const getRandomDelay = () => Math.random() * 10000 + 10000;
    const timeoutId = setTimeout(moveAlien, getRandomDelay());
    return () => clearTimeout(timeoutId);
  }, [alienPosition, messages.length]);
  const loadConversationHistory = async () => {
    try {
      setLoadingHistory(true);
      const { getConversation } = await import('../services/api');
      const conversation = await getConversation(conversationId);
      if (conversation.messages && conversation.messages.length > 0) {
        setMessages(conversation.messages);
      } else {
        setMessages([]);
      }
      if (conversation.overall_sentiment) {
        setSentimentSummary({
          overall_sentiment: conversation.overall_sentiment,
          explanation: conversation.sentiment_explanation,
        });
      }
    } catch (err) {
      setMessages([]);
    } finally {
      setLoadingHistory(false);
    }
  };
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        window.location.reload(); 
      }
      if (e.key === 'Escape' && showSidebar) {
        onToggleSidebar();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [showSidebar, onToggleSidebar]);
  const handleSendMessage = async (e) => {
    e.preventDefault();
    if ((!inputMessage.trim() && !selectedImage) || loading) {
      return;
    }
    const messageText = inputMessage.trim() || (selectedImage ? "What's in this image?" : "");
    const imageToSend = selectedImage?.data || null;
    setInputMessage('');
    setSelectedImage(null); 
    setError(null);
    setLoading(true);
    soundEffects.sendMessage();
    try {
      const response = await sendMessage(conversationId, messageText, imageToSend);
      const userMessage = {
        id: response.user_message_id,
        sender: 'user',
        message_text: response.user_message,
        sentiment: response.user_sentiment,
        sentiment_score: response.user_sentiment_score,
        timestamp: new Date().toISOString(),
      };
      const botMessage = {
        id: response.bot_message_id,
        sender: 'bot',
        message_text: response.bot_message,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, userMessage, botMessage]);
      soundEffects.receiveMessage();
      textToSpeech.speak(botMessage.message_text, currentLanguage);
    } catch (err) {
      setError(err.message || 'Failed to send message. Please try again.');
      soundEffects.error();
      setInputMessage(messageText);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };
  const handleDeleteMessage = (messageId) => {
    if (confirm('Delete this message?')) {
      setMessages(messages.filter(msg => msg.id !== messageId));
    }
  };
  const handleExport = (format) => {
    if (messages.length === 0) {
      alert('No messages to export');
      return;
    }
    if (format === 'text') {
      exportAsText(messages, 'Sentiment Chat');
    } else if (format === 'json') {
      exportAsJSON(messages, 'Sentiment Chat');
    }
  };
  const toggleSound = () => {
    const newState = soundEffects.toggle();
    setSoundEnabled(newState);
  };
  const toggleTTS = () => {
    const newState = textToSpeech.toggle();
    setTtsEnabled(newState);
    if (newState) {
      const testMessages = {
        'en': 'Text to speech is now enabled',
        'es': 'El texto a voz está ahora habilitado',
        'fr': 'La synthèse vocale est maintenant activée',
        'de': 'Text-zu-Sprache ist jetzt aktiviert',
        'zh': '文字转语音现已启用',
        'ja': 'テキスト読み上げが有効になりました',
        'hi': 'टेक्स्ट टू स्पीच अब सक्षम है',
        'ar': 'تم تمكين تحويل النص إلى كلام الآن'
      };
      textToSpeech.speak(testMessages[currentLanguage] || testMessages['en'], currentLanguage);
    }
  };
  const handleVoiceTranscript = (transcript) => {
    setInputMessage(transcript);
    inputRef.current?.focus();
  };
  const handleReaction = (messageId, emoji) => {
    setMessages(messages.map(msg => 
      msg.id === messageId ? { ...msg, reaction: emoji } : msg
    ));
  };
  const handleLanguageChange = (langCode) => {
    setCurrentLanguage(langCode);
    localStorage.setItem('language', langCode);
  };
  const handleImageSelect = (imageData) => {
    setSelectedImage({
      preview: imageData.preview,
      data: imageData.preview, 
      name: imageData.name
    });
  };
  const removeImage = () => {
    setSelectedImage(null);
  };
  const handleLoadSummary = async () => {
    if (messages.length === 0) {
      setError('No messages to analyze yet.');
      return;
    }
    
    // Toggle summary if already showing
    if (showSummary) {
      setShowSummary(false);
      return;
    }
    
    setLoading(true);
    setError(null);
    try {
      const summary = await getConversationSentiment(conversationId);
      setSentimentSummary(summary);
      setShowSummary(true);
    } catch (err) {
      setError(err.message || 'Failed to load sentiment summary.');
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="chat-interface">
      {}
      <button 
        className="header-toggle-btn" 
        onClick={toggleFullscreen}
        title={showHeader ? 'Fullscreen mode (Hide header & sidebar)' : 'Exit fullscreen'}
      >
        {showHeader ? '⬆️' : '⬇️'}
      </button>
      {showHeader && (
        <div className="chat-header">
          <div className="header-left">
            <button className="sidebar-toggle" onClick={onToggleSidebar}>
              {showSidebar ? '☰' : '☰'}
            </button>
            <h2>Sentiment Chatbot</h2>
          </div>
          <div className="header-right">
            <LanguageSelector currentLang={currentLanguage} onLanguageChange={handleLanguageChange} />
            <TTSToggle isEnabled={ttsEnabled} onToggle={toggleTTS} />
            <SoundToggle isEnabled={soundEnabled} onToggle={toggleSound} />
            <ThemeToggle isDark={isDarkMode} onToggle={onToggleDarkMode} />
            <div className="export-dropdown">
              <button
                className="summary-button"
                onClick={() => handleExport('text')}
                disabled={messages.length === 0}
                title="Export as Text"
              >
                📥
              </button>
            </div>
            <button
              className="summary-button"
              onClick={handleLoadSummary}
              disabled={loading || messages.length === 0}
            >
              {showSummary ? 'Hide' : 'Summary'}
            </button>
            <div className="user-info">
              <img src="/user-avatar.png" alt="User" className="user-avatar" />
              <span>{user?.name || user?.email}</span>
              <button className="logout-button" onClick={onLogout}>
                Logout
              </button>
            </div>
          </div>
        </div>
      )}
      {error && (
        <div className="chat-error">
          <span className="error-icon">⚠️</span>
          <span>{error}</span>
          <button className="error-close" onClick={() => setError(null)}>
            ×
          </button>
        </div>
      )}
      {showSummary && sentimentSummary && (
        <ConversationSummary sentimentData={sentimentSummary} />
      )}
      {showSummary && messages.length > 0 && (
        <ConversationStats messages={messages} />
      )}
      <div className={`chat-messages ${messages.length === 0 ? 'empty' : 'has-messages'}`}>
        {}
        <div 
          ref={alienRef}
          className="floating-alien"
          style={{
            left: `${alienPosition.x}%`,
            top: `${alienPosition.y}%`,
          }}
        >
          <img src="/alien.png" alt="Alien Mascot" />
        </div>
        {loadingHistory ? (
          <div className="chat-loading">
            <p>Loading conversation...</p>
          </div>
        ) : messages.length === 0 ? (
          <div className="chat-empty">
            <h2>How can I help you today?</h2>
            <p>Start a conversation by typing a message below</p>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <Message 
                key={message.id} 
                message={message} 
                onDelete={handleDeleteMessage}
                onReact={handleReaction}
              />
            ))}
            {loading && <TypingIndicator />}
          </>
        )}
        <div ref={messagesEndRef} />
      </div>
      <form className="chat-input-form" onSubmit={handleSendMessage}>
        <ImageUpload onImageSelect={handleImageSelect} />
        <VoiceInput onTranscript={handleVoiceTranscript} />
        <div className="input-wrapper">
          {selectedImage && (
            <div className="image-preview-container">
              <img src={selectedImage.preview} alt="Preview" className="image-preview" />
              <button type="button" className="image-remove-btn" onClick={removeImage}>
                ×
              </button>
            </div>
          )}
          <input
            ref={inputRef}
            type="text"
            className="chat-input"
            placeholder="Type your message... (Ctrl+Enter to send)"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyDown={(e) => {
              if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                e.preventDefault();
                handleSendMessage(e);
              }
            }}
            disabled={loading}
          />
        </div>
        <button
          type="submit"
          className="chat-send-button"
          disabled={loading || (!inputMessage.trim() && !selectedImage)}
        >
          {loading ? (
            <span className="loading-spinner">⏳</span>
          ) : (
            <span>Send</span>
          )}
        </button>
      </form>
    </div>
  );
};
export default ChatInterface;