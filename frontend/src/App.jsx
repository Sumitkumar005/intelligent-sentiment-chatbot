import React, { useState, useEffect } from 'react';
import ChatInterface from './components/ChatInterface';
import ConversationList from './components/ConversationList';
import Login from './components/Login';
import { createConversation } from './services/api';
import './App.css';
function App() {
  const [conversationId, setConversationId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showSidebar, setShowSidebar] = useState(false); 
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [isDarkMode, setIsDarkMode] = useState(false);
  useEffect(() => {
    const token = localStorage.getItem('authToken');
    const savedUser = localStorage.getItem('user');
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
      setIsDarkMode(true);
      document.body.classList.add('dark-mode');
    }
    if (token && savedUser) {
      setIsAuthenticated(true);
      setUser(JSON.parse(savedUser));
      initConversation();
    } else {
      setLoading(false);
    }
  }, []);
  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
    if (!isDarkMode) {
      document.body.classList.add('dark-mode');
      localStorage.setItem('theme', 'dark');
    } else {
      document.body.classList.remove('dark-mode');
      localStorage.setItem('theme', 'light');
    }
  };
  const initConversation = async () => {
    try {
      const response = await createConversation();
      setConversationId(response.conversation_id);
    } catch (err) {
      setError('Failed to initialize chat. Please refresh the page.');
    } finally {
      setLoading(false);
    }
  };
  const handleLoginSuccess = (token, userData) => {
    setIsAuthenticated(true);
    setUser(userData);
    initConversation();
  };
  const handleLogout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    setIsAuthenticated(false);
    setUser(null);
    setConversationId(null);
  };
  const handleNewConversation = async () => {
    try {
      const response = await createConversation();
      setConversationId(response.conversation_id);
    } catch (err) {
      alert('Failed to create new conversation. Please try again.');
    }
  };
  const handleSelectConversation = (id) => {
    setConversationId(id);
    // Close sidebar on mobile after selecting conversation
    if (window.innerWidth <= 768) {
      setShowSidebar(false);
    }
  };
  const handleDeleteConversation = async (deletedId) => {
    if (deletedId === conversationId) {
      try {
        const response = await createConversation();
        setConversationId(response.conversation_id);
      } catch (err) {
      }
    }
  };
  const toggleSidebar = () => {
    setShowSidebar(!showSidebar);
  };
  if (!isAuthenticated) {
    return <Login onLoginSuccess={handleLoginSuccess} />;
  }
  if (loading) {
    return (
      <div className="app-loading">
        <div className="loading-spinner-large">⏳</div>
        <p>Initializing chat...</p>
      </div>
    );
  }
  if (error) {
    return (
      <div className="app-error">
        <div className="error-icon-large">⚠️</div>
        <h2>Oops! Something went wrong</h2>
        <p>{error}</p>
        <button onClick={() => window.location.reload()} className="retry-button">
          Retry
        </button>
      </div>
    );
  }
  return (
    <div className={`app ${isDarkMode ? 'dark-mode' : ''}`}>
      {showSidebar && (
        <>
          <div 
            className={`sidebar-overlay ${showSidebar ? 'active' : ''}`}
            onClick={toggleSidebar}
          />
          <ConversationList
            currentConversationId={conversationId}
            onSelectConversation={handleSelectConversation}
            onNewConversation={handleNewConversation}
            onDeleteConversation={handleDeleteConversation}
          />
        </>
      )}
      <ChatInterface 
        key={conversationId} 
        conversationId={conversationId}
        user={user}
        onLogout={handleLogout}
        showSidebar={showSidebar}
        onToggleSidebar={toggleSidebar}
        isDarkMode={isDarkMode}
        onToggleDarkMode={toggleDarkMode}
      />
    </div>
  );
}
export default App;