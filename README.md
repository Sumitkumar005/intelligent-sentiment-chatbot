# 🤖 Sentiment Analysis Chatbot

> A production-ready chatbot with real-time sentiment analysis, chain-of-thought reasoning, and intelligent conversation management.

**🌐 Live Demo:** [chatbot.sumitsaini.com](https://chatbot.sumitsaini.com)

![Status](https://img.shields.io/badge/Status-Production-brightgreen) ![Tier](https://img.shields.io/badge/Tier%201-Complete-blue) ![Tier](https://img.shields.io/badge/Tier%202-Complete-blue) ![Bonus](https://img.shields.io/badge/Bonus-Implemented-orange)

---

## 📋 Assignment Completion Status

### ✅ Tier 1 - Mandatory (Complete)
- **Conversation-Level Sentiment Analysis**: Full conversation history maintained with overall sentiment evaluation
- **End-of-Interaction Analysis**: Comprehensive sentiment summary showing emotional direction across entire exchange
- **Clear Sentiment Output**: Visual indicators and detailed explanations for overall conversation mood

### ✅ Tier 2 - Additional Credit (Complete)
- **Statement-Level Sentiment Analysis**: Every user message analyzed individually with VADER sentiment engine
- **Real-Time Sentiment Display**: Each message shows sentiment badge (Positive/Negative/Neutral) with confidence scores
- **Mood Trend Analysis**: Conversation statistics track sentiment shifts and emotional journey throughout interaction
- **Sentiment Distribution**: Visual breakdown showing positive/negative/neutral message counts

### 🎁 Bonus Features Implemented
- **Agentic AI System**: Automatic task detection (15+ task types) with adaptive responses
- **Chain-of-Thought Reasoning**: Step-by-step problem solving for complex queries
- **Multi-Language Support**: 8 languages with native text-to-speech
- **Voice Interaction**: Speech-to-text input and voice output
- **Smart Authentication**: OTP-based login with Gmail API integration
- **Conversation Management**: Search, export (TXT/JSON), delete conversations
- **Mobile-Optimized UI**: Fully responsive design with glass-morphism effects
- **Production-Grade Architecture**: Modular, scalable, deployment-ready code

---

## 🎯 Key Technologies

### Backend
- **Python 3.8+** with Flask framework
- **VADER Sentiment Analysis** - Real-time emotion detection
- **Groq API** (llama-3.1-8b-instant) - Fast LLM responses
- **SQLite** - Lightweight conversation storage
- **Gmail API** - Secure OTP email delivery
- **JWT Authentication** - Token-based security

### Frontend
- **React 18** with Vite build tool
- **Web Speech API** - Voice input/output
- **CSS3** - Modern glass-morphism design
- **Axios** - API communication

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Groq API key ([Get free](https://console.groq.com))
- Gmail account with OAuth credentials

**OR**

- Docker 20.10+ and Docker Compose 2.0+ (for containerized deployment)

### Option 1: Docker Deployment (Recommended)

```bash
# 1. Clone repository
git clone <your-repo-url>
cd sentiment-chatbot

# 2. Create .env file
cp .env.example .env
# Edit .env with your credentials

# 3. Build and run with Docker Compose
docker-compose up -d

# 4. Access application
# Frontend: http://localhost:3000
# Backend: http://localhost:5000

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**See [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) for AWS, GCP, Azure deployment guides.**

### Option 2: Manual Installation

```bash
# 1. Clone repository
git clone <your-repo-url>
cd sentiment-chatbot

# 2. Backend setup
cd backend
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your credentials (see Configuration section)

# 4. Run database migration
python migrate_add_user_id.py

# 5. Start backend
python app.py
# Runs on http://localhost:5000

# 6. Frontend setup (new terminal)
cd frontend
npm install
npm run dev
# Runs on http://localhost:5173
```

---

## ⚙️ Configuration

Create `backend/.env` file:

```env
# Required: Groq API
GROQ_API_KEY=gsk_your_groq_api_key_here

# Required: Gmail API (OAuth token as JSON string)
GMAIL_TOKEN={"token":"ya29...","refresh_token":"1//...","token_uri":"..."}
EMAIL_SENDER=your-email@gmail.com

# Security
JWT_SECRET=your-secret-key-change-in-production

# Optional
DATABASE_PATH=./chatbot.db
FLASK_PORT=5000
```

### Setting Up Gmail API

1. **Get OAuth Credentials:**
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create project → Enable Gmail API
   - Create OAuth 2.0 credentials (Desktop app)
   - Download JSON file to `backend/` directory

2. **Generate Token:**
   ```bash
   cd backend
   python gmail_auth.py
   # Follow browser prompts to authorize
   # Copy token.json content to GMAIL_TOKEN env variable
   ```

**Note:** We use Gmail API (not SMTP) for reliable OTP delivery in production.

---

## 📖 Usage Guide

### Testing the Live Demo

**⏰ Important:** The deployed app on Render's free tier takes **15-20 seconds to wake up** on first visit. Please be patient!

1. **Visit:** [chatbot.sumitsaini.com](https://chatbot.sumitsaini.com)
2. **Wait 15-20 seconds** for server to wake (first load only)
3. **Login:** Enter your email → Receive OTP → Enter code
4. **Start Chatting:** Type messages and see real-time sentiment analysis

### Example Interactions

```
User: "Your service disappoints me"
→ Sentiment: Negative (Score: -0.52)
Bot: "I'm sorry to hear that. I'll make sure your concern is addressed."

User: "Last experience was better"
→ Sentiment: Positive (Score: 0.31)
Bot: "I'm glad your previous experience was positive. How can I help improve this one?"

Final Summary:
Overall Sentiment: Negative
Explanation: General dissatisfaction across conversation
Distribution: 1 positive, 1 negative, 0 neutral
```

### Features to Test

1. **Sentiment Analysis**
   - Send positive message: "I love this!"
   - Send negative message: "This is frustrating"
   - Send neutral message: "What time is it?"
   - Click "Summary" to see overall conversation sentiment

2. **AI Capabilities**
   - Code help: "Debug this Python code"
   - Math: "Calculate 15% of 200"
   - Emotional support: "I'm feeling stressed"
   - Creative: "Write me a short poem"

3. **Voice Features**
   - Click 🎤 to use voice input
   - Click 🗣️ to enable text-to-speech
   - Change language with flag icon 🇺🇸

4. **Conversation Management**
   - Click ☰ to open sidebar
   - Create new conversation
   - Search past conversations
   - Export as TXT or JSON

---

## � Dockeer Support

This project includes full Docker support for easy deployment:

- **docker-compose.yml** - Multi-container orchestration
- **backend/Dockerfile** - Backendiner configuration
- **frontend/Dockerfile** - Frontend container with Nginx
- **DOCKER_DEPLOYMENT.md** - Complete deploymentfor ACP, Azure, Digit
├── backend/
│*Deploy   ├──ere with Docker:**
- AWS ECS/EC2
- Google Cloud Run/GKE
- Azure Container Instances
- app.palOcean Apy         
- Any VP          ker

---

## # Flasjectk entry po

```
sentiment-chatbot/int
│   ├── routes.py                 # Chat API endpoints
│   ├── auth_routes.py            # Authentication endpoints
│   ├── auth_middleware.py        # JWT verification
│   ├── sentiment.py              # VADER sentiment analysis
│   ├── llm_service.py            # Agentic LLM with memory
│   ├── prompts.py                # Modular prompt system
│   ├── email_service.py          # Gmail API integration
│   ├── database.py               # Conversation storage
│   ├── user_database.py          # User management
│   ├── vision_service.py         # Image handling (placeholder)
│   └── requirements.txt          # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/           # React components
│   │   │   ├── ChatInterface.jsx # Main chat UI
│   │   │   ├── Message.jsx       # Message with sentiment
│   │   │   ├── ConversationList.jsx
│   │   │   ├── ConversationSummary.jsx
│   │   │   ├── ConversationStats.jsx
│   │   │   └── ...
│   │   ├── services/api.js       # Backend integration
│   │   ├── utils/
│   │   │   ├── textToSpeech.js
│   │   │   └── exportConversation.js
│   │   └── App.jsx
│   └── package.json
│
├── docker-compose.yml            # Docker orchestration
├── .dockerignore                 # Docker ignore patterns
├── DOCKER_DEPLOYMENT.md          # Docker deployment guide
├── DEPLOYMENT.md                 # General deployment guide
├── ASSIGNMENT_CHECKLIST.md       # Assignment completion status
├── SUBMISSION_SUMMARY.md         # Submission details
``` README.md                     # This file

---

## 🧠 Sentiment Analysis Logic

### VADER Sentiment Engine

We use **VADER** (Valence Aware Dictionary and sEntiment Reasoner) for sentiment analysis:

**Why VADER?**
- Specifically designed for social media text
- Handles emojis, slang, and informal language
- Provides compound scores (-1 to +1)
- No training data required

**Classification Logic:**
```python
compound_score = vader.polarity_scores(text)['compound']

if compound_score >= 0.05:
    sentiment = "positive"
elif compound_score <= -0.05:
    sentiment = "negative"
else:
    sentiment = "neutral"
```

**Context-Aware Enhancement:**
- Tracks conversation history for emotional context
- Detects ongoing emotional topics (breakup, grief, etc.)
- Adjusts sentiment classification based on conversation flow
- Prevents misclassification in emotional contexts

### Conversation-Level Analysis

```python
def analyze_conversation(messages):
    user_messages = [m for m in messages if m.sender == 'user']
    scores = [analyze_message(m.text).score for m in user_messages]
    
    avg_score = sum(scores) / len(scores)
    
    if avg_score >= 0.05:
        return "positive"
    elif avg_score <= -0.05:
        return "negative"
    else:
        return "neutral"
```

---

## 🎨 Advanced Features

### 1. Agentic AI System

Automatically detects task type and adapts response:

| Task Type | Detection Keywords | Response Style |
|-----------|-------------------|----------------|
| Debugging | "debug", "error", "fix" | Step-by-step analysis |
| Math Help | "calculate", "solve" | Numbered solution |
| Emotional Support | "sad", "stressed", "anxious" | Empathetic, caring |
| Code Help | "code", "function", "implement" | Technical guidance |
| Creative Writing | "write", "story", "poem" | Imaginative content |

**15+ Task Types Supported**

### 2. Chain-of-Thought Reasoning

For complex queries, shows thinking process:

```
User: "Why is my app slow?"

Bot: 🤔 Let me analyze:
1. Common causes: Database queries, network latency
2. Most likely: Unoptimized queries
3. Solution: Add indexes, use caching
✅ This should improve performance!
```

### 3. Intelligent Memory Management

- **Short-term memory**: Last 10 messages
- **Long-term memory**: Conversation summaries
- **Emotional memory**: Sentiment tracking across conversation
- **Context-aware**: Adapts to ongoing emotional topics

### 4. Multi-Language Support

8 languages with native TTS:
- 🇺🇸 English
- 🇪🇸 Spanish
- 🇫🇷 French
- 🇩🇪 German
- 🇨🇳 Chinese
- 🇯🇵 Japanese
- 🇮🇳 Hindi
- 🇸🇦 Arabic

---

## 🔌 API Documentation

### Authentication

**Request OTP**
```http
POST /api/auth/request-otp
Content-Type: application/json

{
  "email": "user@example.com",
  "name": "John Doe"
}

Response: { "message": "OTP sent", "user_id": 123 }
```

**Verify OTP**
```http
POST /api/auth/verify-otp
Content-Type: application/json

{
  "email": "user@example.com",
  "otp": "123456"
}

Response: { "token": "jwt_token", "user": {...} }
```

### Conversations

**Send Message**
```http
POST /api/conversations/{id}/messages
Authorization: Bearer <token>
Content-Type: application/json

{
  "message": "Hello!",
  "image": "base64..." (optional)
}

Response: {
  "user_message": "Hello!",
  "user_sentiment": "positive",
  "user_sentiment_score": 0.52,
  "bot_message": "Hi! How can I help?",
  "user_message_id": 1,
  "bot_message_id": 2
}
```

**Get Conversation Sentiment**
```http
GET /api/conversations/{id}/sentiment
Authorization: Bearer <token>

Response: {
  "overall_sentiment": "positive",
  "explanation": "Overall positive sentiment across 5 messages",
  "sentiment_distribution": {
    "positive": 3,
    "negative": 1,
    "neutral": 1
  },
  "average_score": 0.23
}
```

---

## 🧪 Testing

### Manual Test Cases

1. **Sentiment Detection**
   - Positive: "I love this chatbot!"
   - Negative: "This is terrible"
   - Neutral: "What's the weather?"

2. **Conversation Analysis**
   - Send 5+ messages with mixed sentiments
   - Click "Summary" button
   - Verify overall sentiment and distribution

3. **Task Detection**
   - "Debug this code: print('hello')"
   - "Calculate 25 × 4"
   - "I'm feeling sad today"

4. **Voice Features**
   - Enable microphone
   - Speak a message
   - Enable TTS and listen to response

5. **Mobile Responsiveness**
   - Open on mobile device
   - Verify input field is visible
   - Test all features work smoothly

---

## 🚧 Known Limitations & Future Improvements

### Current Limitations

1. **Conversation History**: Past conversations not synced on deployed app (local storage only)
2. **Image Analysis**: Image upload feature is placeholder - not fully implemented with vision model
3. **Cold Start**: Render free tier has 15-20 second wake-up time on first request

### Planned Improvements

1. **Cloud Database**: Migrate from SQLite to PostgreSQL for persistent conversation history
2. **Vision AI**: Implement full image analysis with Groq vision models
3. **Real-time Sync**: WebSocket support for instant message delivery
4. **Advanced Analytics**: Sentiment trends over time with charts
5. **Export Enhancements**: PDF export with sentiment visualizations
6. **Conversation Search**: Full-text search across all messages
7. **User Profiles**: Customizable preferences and themes

---

## 📊 Project Metrics

- **Total Features**: 20+ implemented
- **Languages Supported**: 8
- **Task Types**: 15+
- **API Endpoints**: 12
- **React Components**: 18
- **Lines of Code**: 6,000+
- **Test Coverage**: Manual testing complete

---

## 🎓 Technical Highlights

### Production-Ready Architecture

- **Modular Design**: Separated concerns (auth, sentiment, LLM, database)
- **Error Handling**: Graceful fallbacks for all API failures
- **Security**: JWT authentication, input validation, rate limiting
- **Scalability**: Stateless design, ready for horizontal scaling
- **Monitoring**: Comprehensive logging and metrics tracking

### Performance Optimizations

- **Smart Caching**: Response caching for repeated queries
- **Token Management**: Adaptive token limits per task type
- **Memory Optimization**: Conversation summarization for long chats
- **Lazy Loading**: Components loaded on demand

### Code Quality

- **Type Hints**: Python type annotations throughout
- **Documentation**: Comprehensive docstrings and comments
- **Consistent Style**: PEP 8 compliance, ESLint for JavaScript
- **Git Workflow**: Feature branches, meaningful commits

---

## 🎯 Assignment Deliverables

✅ **Source Code**: Complete, modular, production-ready  
✅ **README**: Comprehensive documentation (this file)  
✅ **Live Demo**: Deployed at [chatbot.sumitsaini.com](https://chatbot.sumitsaini.com)  
✅ **Tier 1**: Conversation-level sentiment analysis ✓  
✅ **Tier 2**: Statement-level sentiment + trend analysis ✓  
✅ **Bonus**: Agentic AI, voice features, multi-language, production deployment ✓

---

## 🙏 Acknowledgments

- **LiaPlus AI** - For the opportunity and clear assignment guidelines
- **Groq** - For excellent LLM API with fast inference
- **VADER** - For robust sentiment analysis
- **React & Flask** - For solid frameworks

---

## 📞 Contact

**Candidate**: Sumit Kumar
**Email**: SumitKumar969074@gmail.com 
**GitHub**: sumitkumar005
**Portfolio**: [sumitsaini.com](https://sumitsaini.com)

---

**Built with ❤️ for you**

*A complete sentiment analysis chatbot demonstrating production-grade AI engineering skills*
