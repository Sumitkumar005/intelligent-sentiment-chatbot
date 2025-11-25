import React, { useState, useEffect } from 'react';
import { getAllConversations, deleteConversation } from '../services/api';
import './ConversationList.css';
const ConversationList = ({ currentConversationId, onSelectConversation, onNewConversation, onDeleteConversation }) => {
  const [conversations, setConversations] = useState([]);
  const [filteredConversations, setFilteredConversations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [deletingId, setDeletingId] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  useEffect(() => {
    loadConversations();
  }, []);
  useEffect(() => {
    if (searchQuery.trim() === '') {
      setFilteredConversations(conversations);
    } else {
      const query = searchQuery.toLowerCase();
      const filtered = conversations.filter(conv => 
        conv.title?.toLowerCase().includes(query) ||
        conv.overall_sentiment?.toLowerCase().includes(query)
      );
      setFilteredConversations(filtered);
    }
  }, [searchQuery, conversations]);
  const loadConversations = async () => {
    try {
      setLoading(true);
      const data = await getAllConversations();
      setConversations(data);
      setFilteredConversations(data);
      setError(null);
    } catch (err) {
      setError('Failed to load conversations');
    } finally {
      setLoading(false);
    }
  };
  const handleDeleteConversation = async (conversationId, e) => {
    e.stopPropagation(); 
    if (!confirm('Are you sure you want to delete this conversation? This cannot be undone.')) {
      return;
    }
    try {
      setDeletingId(conversationId);
      await deleteConversation(conversationId);
      setConversations(conversations.filter(c => c.conversation_id !== conversationId));
      if (conversationId === currentConversationId) {
        onDeleteConversation(conversationId);
      }
    } catch (err) {
      alert('Failed to delete conversation. Please try again.');
    } finally {
      setDeletingId(null);
    }
  };
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  };
  const getSentimentEmoji = (sentiment) => {
    switch (sentiment?.toLowerCase()) {
      case 'positive': return '😊';
      case 'negative': return '😞';
      case 'neutral': return '😐';
      default: return '💬';
    }
  };
  return (
    <div className="conversation-list">
      <div className="conversation-list-header">
        <h3>Conversations</h3>
        <button 
          className="new-conversation-btn" 
          onClick={onNewConversation}
          title="Start new conversation"
        >
          ➕
        </button>
      </div>
      <div className="conversation-search">
        <input
          type="text"
          placeholder="🔍 Search conversations..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="search-input"
        />
      </div>
      {loading && (
        <div className="conversation-list-loading">
          <span className="loading-spinner">⏳</span>
          <p>Loading...</p>
        </div>
      )}
      {error && (
        <div className="conversation-list-error">
          <p>{error}</p>
          <button onClick={loadConversations}>Retry</button>
        </div>
      )}
      {!loading && !error && conversations.length === 0 && (
        <div className="conversation-list-empty">
          <p>No conversations yet</p>
          <p className="empty-hint">Start chatting to create one!</p>
        </div>
      )}
      {!loading && !error && filteredConversations.length > 0 && (
        <div className="conversation-items">
          {filteredConversations.map((conv) => (
            <div
              key={conv.conversation_id}
              className={`conversation-item ${
                conv.conversation_id === currentConversationId ? 'active' : ''
              } ${deletingId === conv.conversation_id ? 'deleting' : ''}`}
              onClick={() => onSelectConversation(conv.conversation_id)}
            >
              <div className="conversation-item-content">
                <div className="conversation-item-header">
                  <span className="conversation-emoji">
                    {getSentimentEmoji(conv.overall_sentiment)}
                  </span>
                  <span className="conversation-date">
                    {formatDate(conv.created_at)}
                  </span>
                </div>
                {conv.title && (
                  <div className="conversation-title">
                    {conv.title}
                  </div>
                )}
                <div className="conversation-item-info">
                  <span className="message-count">
                    {conv.message_count} message{conv.message_count !== 1 ? 's' : ''}
                  </span>
                  {conv.overall_sentiment && (
                    <span className={`sentiment-label sentiment-${conv.overall_sentiment}`}>
                      {conv.overall_sentiment}
                    </span>
                  )}
                </div>
              </div>
              <button
                className="delete-conversation-btn"
                onClick={(e) => handleDeleteConversation(conv.conversation_id, e)}
                disabled={deletingId === conv.conversation_id}
                title="Delete conversation"
              >
                {deletingId === conv.conversation_id ? '⏳' : '🗑️'}
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
export default ConversationList;