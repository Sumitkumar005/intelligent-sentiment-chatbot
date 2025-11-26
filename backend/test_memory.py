"""
Test script to verify memory and context awareness in the chatbot
"""
from prompts import (
    build_system_prompt,
    detect_task_type,
    detect_context,
    get_sentiment_emoji,
    build_conversation_summary
)

def test_memory_system():
    print("=" * 80)
    print("TESTING MEMORY & CONTEXT SYSTEM")
    print("=" * 80)
    
    # Simulate a conversation
    conversation_history = [
        {
            'role': 'user',
            'content': "I'm going through a breakup",
            'sentiment': 'negative'
        },
        {
            'role': 'assistant',
            'content': "I'm so sorry you're going through this painful experience...",
            'sentiment': None
        },
        {
            'role': 'user',
            'content': "I cry every night thinking about her",
            'sentiment': 'negative'
        }
    ]
    
    current_message = "What should I do?"
    current_sentiment = "negative"
    
    # Test task detection
    print("\n1. TASK DETECTION:")
    task = detect_task_type(current_message, conversation_history)
    print(f"   Detected task: {task}")
    print(f"   ✅ Should be 'emotional_support' due to conversation history")
    
    # Test context detection
    print("\n2. CONTEXT DETECTION:")
    context = detect_context(conversation_history, current_message)
    print(f"   Detected context: {context}")
    print(f"   ✅ Should be 'follow_up'")
    
    # Test sentiment emoji
    print("\n3. SENTIMENT EMOJI:")
    emoji = get_sentiment_emoji(current_sentiment)
    print(f"   Emoji for '{current_sentiment}': {emoji}")
    
    # Test conversation summary
    print("\n4. CONVERSATION SUMMARY:")
    summary = build_conversation_summary(conversation_history)
    print(f"   Summary:\n{summary}")
    
    # Test full system prompt
    print("\n5. FULL SYSTEM PROMPT (first 500 chars):")
    full_prompt = build_system_prompt(
        base_style="default",
        user_sentiment=current_sentiment,
        task_type=task,
        context=context,
        conversation_history=conversation_history,
        enable_memory=True
    )
    print(f"   {full_prompt[:500]}...")
    print(f"\n   Total prompt length: {len(full_prompt)} characters")
    
    # Check for key memory indicators
    print("\n6. MEMORY INDICATORS CHECK:")
    memory_keywords = [
        "remember", "REMEMBER", "previous", "earlier", 
        "breakup", "conversation history", "MEMORY"
    ]
    found_keywords = [kw for kw in memory_keywords if kw in full_prompt]
    print(f"   Found memory keywords: {found_keywords}")
    print(f"   ✅ Prompt includes {len(found_keywords)} memory-related terms")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE!")
    print("=" * 80)

if __name__ == "__main__":
    test_memory_system()
