import axios from 'axios';
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      throw new Error(error.response.data.error || 'An error occurred');
    } else if (error.request) {
      throw new Error('Unable to connect to server. Please check your connection.');
    } else {
      throw new Error(error.message);
    }
  }
);
export const createConversation = async () => {
  const response = await api.post('/conversations');
  return response.data;
};
export const sendMessage = async (conversationId, message, image = null) => {
  const payload = { message };
  if (image) {
    payload.image = image;
  }
  const response = await api.post(`/conversations/${conversationId}/messages`, payload);
  return response.data;
};
export const getConversation = async (conversationId) => {
  const response = await api.get(`/conversations/${conversationId}`);
  return response.data;
};
export const getConversationSentiment = async (conversationId) => {
  const response = await api.get(`/conversations/${conversationId}/sentiment`);
  return response.data;
};
export const getAllConversations = async () => {
  const response = await api.get('/conversations');
  return response.data;
};
export const deleteConversation = async (conversationId) => {
  const response = await api.delete(`/conversations/${conversationId}`);
  return response.data;
};
export default {
  createConversation,
  sendMessage,
  getConversation,
  getConversationSentiment,
  getAllConversations,
  deleteConversation,
};