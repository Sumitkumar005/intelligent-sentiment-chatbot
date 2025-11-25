# 🤖 Intelligent Sentiment Chatbot

> An advanced AI chatbot with real-time sentiment analysis, chain-of-thought reasoning, multi-language support, and voice interaction capabilities.

![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Features](https://img.shields.io/badge/Features-17%20Complete-blue)
![Languages](https://img.shields.io/badge/Languages-8%20Supported-orange)

---

## 📋 Table of Contents
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Usage Guide](#-usage-guide)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)

---

## ✨ Features

### Core Capabilities
- ✅ **Real-time Sentiment Analysis** - VADER-based emotion detection for every message
- ✅ **Chain-of-Thought Reasoning** - Step-by-step problem solving for complex queries
- ✅ **Agentic AI System** - Automatic task detection and adaptive responses
- ✅ **Multi-Language Support** - 8 languages with native voice synthesis
- ✅ **Voice Interaction** - Speech-to-text input and text-to-speech output
- ✅ **Smart Authentication** - OTP-based login with JWT tokens
- ✅ **Conversation Management** - Full history, search, export, and analytics
- ✅ **Glass-Morphism UI** - Modern, beautiful interface with dark/light modes
- ✅ **Image Upload** - Support for image attachments (with helpful guidance)
- ✅ **Emoji Reactions** - React to messages with 6 different emojis
- ✅ **Sound Effects** - Audio feedback for enhanced UX
- ✅ **Keyboard Shortcuts** - Power user features (Ctrl+Enter, Ctrl+K, Esc)
- ✅ **Mobile Responsive** - Works perfectly on all devices
- ✅ **Floating Alien Mascot** - Animated character that moves around
- ✅ **Message Actions** - Copy, delete, and interact with messages
- ✅ **Quick Statistics** - Real-time conversation analytics
- ✅ **Export Conversations** - Download as TXT or JSON

### AI Intelligence
- **15+ Task Types**: Code help, debugging, math, creative writing, emotional support, career advice, and more
- **Sentiment-Aware**: Adapts tone based on user emotions (positive, negative, neutral)
- **Context Understanding**: Maintains conversation flow and remembers context
- **Automatic Detection**: Identifies task type from user message
- **Adaptive Parameters**: Adjusts temperature and response length per task

---

## 🛠️ Tech Stack

### Frontend
- **React 18** - Modern UI framework
- **Vite** - Fast build tool
- **CSS3** - Glass-morphism design
- **Web Speech API** - Voice input/output
- **Axios** - HTTP client

### Backend
- **Flask** - Python web framework
- **SQLite** - Lightweight database
- **VADER** - Sentiment analysis
- **Groq API** - LLM (llama-3.1-8b-instant)
- **JWT** - Authentication
- **SMTP** - Email delivery

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Groq API key ([Get one free](https://console.groq.com))
- Gmail account (for OTP emails)

### Installation

#### 1. Clone Repository
```bash
git clone <your-repo-url>
cd sentiment-chatbot
```

#### 2. Backend Setup
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your credentials
# Required: GROQ_API_KEY, SMTP credentials
```

#### 3. Database Migration
```bash
# Run migration to add user_id column
python migrate_add_user_id.py
```

#### 4. Start Backend
```bash
python app.py
# Server runs on http://localhost:5000
```

#### 5. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
# App runs on http://localhost:5173
```

#### 6. Open Browser
Navigate to `http://localhost:5173` and start chatting!

---

## 📁 Project Structure

```
sentiment-chatbot/
├── backend/
│   ├── app.py                    # Flask application entry
│   ├── routes.py                 # API endpoints
│   ├── auth_routes.py            # Authentication endpoints
│   ├── auth_middleware.py        # JWT authentication
│   ├── auth_controller.py        # Auth logic
│   ├── database.py               # Database operations
│   ├── user_database.py          # User management
│   ├── sentiment.py              # Sentiment analysis
│   ├── llm_service.py            # Agentic LLM service
│   ├── prompts.py                # Modular prompt system
│   ├── vision_service.py         # Image handling
│   ├── email_service.py          # Email delivery
│   ├── migrate_add_user_id.py    # Database migration
│   ├── requirements.txt          # Python dependencies
│   └── .env.example              # Environment template
│
├── frontend/
│   ├── src/
│   │   ├── components/           # React components
│   │   │   ├── ChatInterface.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Message.jsx
│   │   │   ├── ConversationList.jsx
│   │   │   ├── VoiceInput.jsx
│   │   │   ├── LanguageSelector.jsx
│   │   │   └── ...
│   │   ├── services/
│   │   │   └── api.js            # API integration
│   │   ├── utils/
│   │   │   ├── textToSpeech.js
│   │   │   ├── soundEffects.js
│   │   │   └── exportConversation.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── public/
│   │   ├── alien.png             # Mascot image
│   │   └── sounds/               # Audio files
│   └── package.json
│
└── README.md                     # This file
```

---

## ⚙️ Configuration

### Environment Variables (.env)

```env
# Groq API (Required)
GROQ_API_KEY=gsk_your_groq_api_key_here

# Email Configuration (Required for OTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
EMAIL_SENDER=Chatbot <noreply@yourapp.com>

# Security
JWT_SECRET=your-super-secret-jwt-key-change-in-production

# Database
DATABASE_PATH=./chatbot.db

# Server
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_ENV=development
```

### Getting Gmail App Password
1. Go to Google Account settings
2. Enable 2-Factor Authentication
3. Generate App Password for "Mail"
4. Use that password in SMTP_PASS

---

## 📖 Usage Guide

### First Time Login
1. Enter your email address
2. Receive OTP code via email
3. Enter 6-digit code
4. Start chatting!

### Returning Users
- Just enter email - instant login (no OTP needed)

### Chat Features

#### Voice Input
- Click 🎤 microphone button
- Speak your message
- Auto-transcribed to text

#### Text-to-Speech
- Click 🗣️ button to enable
- Bot speaks responses aloud
- Select language with flag icon 🇺🇸

#### Image Upload
- Click 📎 button
- Upload image
- Bot provides guidance on how to help

#### Keyboard Shortcuts
- `Ctrl+Enter` - Send message
- `Ctrl+K` - New conversation
- `Esc` - Close sidebar

#### Message Actions
- **Copy** - Click 📋 on message
- **Delete** - Click 🗑️ on your messages
- **React** - Hover and click emoji (👍👎❤️😂😮🎉)

#### Conversation Management
- **Search** - Find conversations by title
- **Export** - Download as TXT or JSON
- **Delete** - Remove conversations
- **Stats** - View analytics and sentiment trends

---

## 🎯 AI Capabilities

### Automatic Task Detection

The bot automatically detects what you need:

| Your Message | Detected Task | Response Style |
|--------------|---------------|----------------|
| "Debug this code" | Debugging | Step-by-step analysis |
| "Calculate 15% of 200" | Math Help | Numbered solution |
| "Write me a story" | Creative Writing | Imaginative content |
| "I'm feeling sad" | Emotional Support | Empathetic, caring |
| "Explain quantum physics" | Learning Tutor | Clear, educational |
| "Career advice needed" | Career Advice | Practical guidance |

### Chain-of-Thought Reasoning

For complex tasks, the bot shows its thinking:

```
User: "Why is my app slow?"

Bot: 🤔 Let me analyze this:
1. Common causes: Database queries, inefficient code, network latency
2. Most likely: Database queries without indexes
3. Solution: Add indexes and optimize queries
✅ This should improve performance significantly!
```

### Sentiment Adaptation

The bot adjusts its tone based on your emotion:

- **Happy** → Enthusiastic and energetic
- **Sad/Frustrated** → Empathetic and supportive
- **Neutral** → Helpful and informative

---

## 🌍 Supported Languages

| Language | Code | Voice | Flag |
|----------|------|-------|------|
| English | en | ✅ | 🇺🇸 |
| Spanish | es | ✅ | 🇪🇸 |
| French | fr | ✅ | 🇫🇷 |
| German | de | ✅ | 🇩🇪 |
| Chinese | zh | ✅ | 🇨🇳 |
| Japanese | ja | ✅ | 🇯🇵 |
| Hindi | hi | ✅ | 🇮🇳 |
| Arabic | ar | ✅ | 🇸🇦 |

---

## 🔌 API Documentation

### Authentication

#### Request OTP
```http
POST /api/auth/request-otp
Content-Type: application/json

{
  "email": "user@example.com",
  "name": "John Doe" (optional)
}
```

#### Verify OTP
```http
POST /api/auth/verify-otp
Content-Type: application/json

{
  "email": "user@example.com",
  "otp": "123456"
}
```

### Conversations

#### Create Conversation
```http
POST /api/conversations
Authorization: Bearer <token>
```

#### Send Message
```http
POST /api/conversations/{id}/messages
Authorization: Bearer <token>
Content-Type: application/json

{
  "message": "Hello!",
  "image": "base64..." (optional)
}
```

#### Get Conversation
```http
GET /api/conversations/{id}
Authorization: Bearer <token>
```

#### List Conversations
```http
GET /api/conversations
Authorization: Bearer <token>
```

#### Delete Conversation
```http
DELETE /api/conversations/{id}
Authorization: Bearer <token>
```

---

## 🧪 Testing

### Manual Testing

1. **Login Flow**
   - New user with OTP
   - Returning user instant login

2. **Chat Features**
   - Send text messages
   - Use voice input
   - Upload images
   - React to messages
   - Delete messages

3. **AI Capabilities**
   - Try: "Debug this code"
   - Try: "Calculate 25 × 4"
   - Try: "I'm feeling stressed"
   - Try: "Write me a poem"

4. **Multi-Language**
   - Change language (flag icon)
   - Enable TTS
   - Test voice in different languages

5. **Conversation Management**
   - Create multiple conversations
   - Search conversations
   - Export conversations
   - Delete conversations

### Test Accounts
- Use any email for testing
- OTP codes sent to that email
- Each email gets separate conversations

---

## 🎨 Customization

### Add New Task Type

Edit `backend/prompts.py`:

```python
# Add to TASK_PROMPTS
TASK_PROMPTS = {
    "your_task": """Your instructions here..."""
}

# Add detection in detect_task_type()
if any(word in message_lower for word in ['keyword1', 'keyword2']):
    return "your_task"
```

### Change Bot Personality

Edit `backend/prompts.py`:

```python
SYSTEM_PROMPTS = {
    "your_style": """Your personality description..."""
}
```

### Adjust Response Length

Edit `backend/llm_service.py`:

```python
def _get_max_tokens(self, task_type: str, user_message: str) -> int:
    if task_type == 'your_task':
        return 200  # Adjust as needed
```

---

## 🐛 Troubleshooting

### Voice Input Not Working
- Check microphone permissions
- Use Chrome or Edge browser
- Ensure HTTPS or localhost

### TTS Not Speaking
- Check system volume
- Enable TTS with 🗣️ button
- Try different browser

### Login Issues
- Verify SMTP settings in .env
- Check spam folder for OTP
- Ensure Gmail app password is correct

### API Errors
- Verify Groq API key
- Check internet connection
- Review backend logs

---

## 📊 Project Statistics

- **Total Features**: 17 complete
- **Languages Supported**: 8
- **Components**: 15+
- **API Endpoints**: 10+
- **Lines of Code**: 5,000+
- **Task Types**: 15+

---

## 🎓 Key Technologies Explained

### Sentiment Analysis
- Uses VADER (Valence Aware Dictionary and sEntiment Reasoner)
- Analyzes each message for positive/negative/neutral sentiment
- Provides sentiment scores and explanations

### Chain-of-Thought
- Shows step-by-step reasoning for complex problems
- Uses numbered points for clarity
- Helps users understand the thinking process

### Agentic AI
- Automatically detects task type from message
- Adapts response style based on context
- Uses specialized prompts for different scenarios

### JWT Authentication
- Secure token-based authentication
- Tokens stored in localStorage
- Automatic token refresh

---

## 📝 License

This project is for educational purposes.

---

## 🙏 Acknowledgments

- **Groq** - For excellent LLM API
- **VADER** - For sentiment analysis
- **React** - For the UI framework
- **Flask** - For the backend framework

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Check backend logs for errors

---

**Built with ❤️ for intelligent, empathetic conversations**

*A complete sentiment analysis chatbot with advanced AI capabilities*
