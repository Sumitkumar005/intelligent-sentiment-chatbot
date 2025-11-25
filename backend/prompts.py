SYSTEM_PROMPTS = {
    "default": """You are a helpful, friendly, and empathetic AI assistant. Your goal is to provide accurate, clear, and useful responses while being conversational and engaging. Always be respectful and considerate of the user's needs and emotions."""
}
SENTIMENT_MODIFIERS = {
    "positive": """The user seems happy or positive. Match their energy with enthusiasm and positivity.""",
    "negative": """The user seems upset, sad, or frustrated. Show empathy, be supportive, and offer help. Use a gentle, understanding tone.""",
    "neutral": """The user has a neutral tone. Be helpful and informative while maintaining a friendly demeanor."""
}
TASK_PROMPTS = {
}
CONTEXT_PROMPTS = {
    "first_message": """This is the start of a new conversation. Be welcoming and set a positive tone. Introduce yourself briefly and show eagerness to help.""",
    "follow_up": """This is a follow-up in an ongoing conversation. Reference previous context naturally and maintain conversation flow.""",
    "topic_change": """The user is changing topics. Acknowledge the shift smoothly and adapt to the new subject.""",
    "clarification_needed": """The user's request is unclear. Politely ask for clarification while showing you're trying to understand."""
}
AGENTIC_CAPABILITIES = {
    "reasoning": "Think through problems step by step and explain your reasoning clearly.",
    "adaptive": "Adapt your communication style to match the user's needs and emotional state.",
    "chain_of_thought": "Break down complex problems into smaller steps and work through them systematically."
}
RESPONSE_TEMPLATES = {
    "greeting": [
        "Hi there! How can I help you today?",
        "Hello! What can I do for you?",
        "Hey! What's on your mind?",
        "Hi! I'm here to help. What do you need?"
    ],
    "farewell": [
        "Goodbye! Feel free to come back anytime!",
        "Take care! Happy to help again whenever you need.",
        "See you later! Don't hesitate to return if you need anything.",
        "Bye! It was great chatting with you!"
    ],
    "gratitude": [
        "You're very welcome! Happy to help!",
        "My pleasure! Let me know if you need anything else.",
        "Glad I could help! Feel free to ask more questions.",
        "Anytime! That's what I'm here for!"
    ],
    "confusion": [
        "I'm not quite sure I understand. Could you rephrase that?",
        "Could you clarify what you mean? I want to help accurately.",
        "I want to make sure I understand correctly. Can you elaborate?",
        "Let me make sure I've got this right - could you explain a bit more?"
    ],
    "apology": [
        "I apologize for any confusion. Let me try to help better.",
        "Sorry about that! Let me clarify.",
        "My apologies. Here's what I meant:",
        "I'm sorry if that wasn't clear. Let me explain better."
    ]
}
def build_system_prompt(
    base_style: str = "default",
    user_sentiment: str = None,
    task_type: str = None,
    context: str = None,
    enable_reasoning: bool = True,
    enable_chain_of_thought: bool = True
) -> str:
    prompt_parts = []
    prompt_parts.append(SYSTEM_PROMPTS.get(base_style, SYSTEM_PROMPTS["default"]))
    if user_sentiment and user_sentiment in SENTIMENT_MODIFIERS:
        prompt_parts.append(f"\n\nUser Sentiment: {SENTIMENT_MODIFIERS[user_sentiment]}")
    if task_type and task_type in TASK_PROMPTS:
        prompt_parts.append(f"\n\nTask Focus: {TASK_PROMPTS[task_type]}")
    if context and context in CONTEXT_PROMPTS:
        prompt_parts.append(f"\n\nContext: {CONTEXT_PROMPTS[context]}")
    if enable_chain_of_thought and task_type in ['problem_solving', 'debugging', 'technical_explanation', 'math_help', 'data_analysis']:
        prompt_parts.append(f"\n\n{AGENTIC_CAPABILITIES['chain_of_thought']}")
    if enable_reasoning:
        prompt_parts.append(f"\n\n{AGENTIC_CAPABILITIES['reasoning']}")
        prompt_parts.append(f"\n{AGENTIC_CAPABILITIES['adaptive']}")
    return "\n".join(prompt_parts)
def detect_task_type(user_message: str) -> str:
    message_lower = user_message.lower()
    if any(word in message_lower for word in ['debug', 'bug', 'error', 'not working', 'broken', 'crash', 'fix']):
        return "debugging"
    if any(word in message_lower for word in ['code', 'program', 'function', 'python', 'javascript', 'java', 'c++', 'algorithm']):
        return "code_help"
    if any(word in message_lower for word in ['math', 'calculate', 'equation', 'formula', 'solve for', 'algebra', 'calculus']):
        return "math_help"
    if any(word in message_lower for word in ['data', 'analyze', 'statistics', 'dataset', 'visualization', 'chart', 'graph']):
        return "data_analysis"
    if any(word in message_lower for word in ['how does', 'how do', 'technical', 'architecture', 'system', 'works']):
        return "technical_explanation"
    if any(word in message_lower for word in ['story', 'poem', 'write', 'creative', 'imagine', 'tale', 'narrative']):
        return "creative_writing"
    if any(word in message_lower for word in ['problem', 'solve', 'solution', 'help me', 'stuck', 'issue']):
        return "problem_solving"
    if any(word in message_lower for word in ['explain', 'teach', 'learn', 'understand', 'what is', 'definition']):
        return "learning_tutor"
    if any(word in message_lower for word in ['translate', 'grammar', 'vocabulary', 'language', 'pronunciation', 'conjugate']):
        return "language_learning"
    if any(word in message_lower for word in ['idea', 'brainstorm', 'suggest', 'think of', 'come up with', 'creative ideas']):
        return "brainstorming"
    if any(word in message_lower for word in ['career', 'job', 'interview', 'resume', 'professional', 'work advice']):
        return "career_advice"
    if any(word in message_lower for word in ['health', 'wellness', 'exercise', 'diet', 'sleep', 'mental health', 'meditation']):
        return "health_wellness"
    if any(word in message_lower for word in ['business', 'strategy', 'marketing', 'startup', 'entrepreneur', 'sales']):
        return "business_strategy"
    if any(word in message_lower for word in ['sad', 'upset', 'worried', 'anxious', 'stressed', 'depressed', 'lonely', 'scared', 'afraid']):
        return "emotional_support"
    return "casual_chat"
def detect_context(conversation_history: list, user_message: str) -> str:
    if not conversation_history or len(conversation_history) == 0:
        return "first_message"
    clarification_words = ['what do you mean', 'clarify', 'explain', 'i dont understand', "i don't understand"]
    if any(word in user_message.lower() for word in clarification_words):
        return "clarification_needed"
    return "follow_up"
__all__ = [
    'SYSTEM_PROMPTS',
    'SENTIMENT_MODIFIERS',
    'TASK_PROMPTS',
    'CONTEXT_PROMPTS',
    'AGENTIC_CAPABILITIES',
    'RESPONSE_TEMPLATES',
    'build_system_prompt',
    'detect_task_type',
    'detect_context'
]