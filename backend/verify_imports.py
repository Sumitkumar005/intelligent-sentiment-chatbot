"""
Verification script to ensure all exports and imports are correct
"""

print("=" * 80)
print("VERIFYING PROMPTS MODULE EXPORTS AND IMPORTS")
print("=" * 80)

# Test 1: Import all exported items from prompts
print("\n1. Testing prompts.__all__ exports...")
try:
    from prompts import (
        SYSTEM_PROMPTS,
        SENTIMENT_MODIFIERS,
        TASK_PROMPTS,
        CONTEXT_PROMPTS,
        MEMORY_SYSTEM_PROMPT,
        SENTIMENT_CONTINUITY_PROMPT,
        RESPONSE_STRATEGY_PROMPT,
        build_system_prompt,
        build_conversation_summary,
        detect_task_type,
        detect_context,
        get_sentiment_emoji
    )
    print("   ✅ All exports from __all__ imported successfully!")
except ImportError as e:
    print(f"   ❌ Import error: {e}")
    exit(1)

# Test 2: Verify each export exists and is correct type
print("\n2. Verifying export types...")
exports_check = {
    'SYSTEM_PROMPTS': (dict, SYSTEM_PROMPTS),
    'SENTIMENT_MODIFIERS': (dict, SENTIMENT_MODIFIERS),
    'TASK_PROMPTS': (dict, TASK_PROMPTS),
    'CONTEXT_PROMPTS': (dict, CONTEXT_PROMPTS),
    'MEMORY_SYSTEM_PROMPT': (str, MEMORY_SYSTEM_PROMPT),
    'SENTIMENT_CONTINUITY_PROMPT': (str, SENTIMENT_CONTINUITY_PROMPT),
    'RESPONSE_STRATEGY_PROMPT': (str, RESPONSE_STRATEGY_PROMPT),
    'build_system_prompt': ('function', build_system_prompt),
    'build_conversation_summary': ('function', build_conversation_summary),
    'detect_task_type': ('function', detect_task_type),
    'detect_context': ('function', detect_context),
    'get_sentiment_emoji': ('function', get_sentiment_emoji),
}

for name, (expected_type, obj) in exports_check.items():
    if expected_type == 'function':
        if callable(obj):
            print(f"   ✅ {name}: function")
        else:
            print(f"   ❌ {name}: expected function, got {type(obj)}")
    else:
        if isinstance(obj, expected_type):
            print(f"   ✅ {name}: {expected_type.__name__}")
        else:
            print(f"   ❌ {name}: expected {expected_type.__name__}, got {type(obj).__name__}")

# Test 3: Verify llm_service imports work
print("\n3. Testing llm_service.py imports...")
try:
    from llm_service import GroqService
    print("   ✅ llm_service imports successfully!")
except ImportError as e:
    print(f"   ❌ llm_service import error: {e}")

# Test 4: Test function calls
print("\n4. Testing function calls...")

# Test detect_task_type
try:
    task = detect_task_type("I'm feeling sad")
    print(f"   ✅ detect_task_type('I'm feeling sad') = '{task}'")
    assert task == "emotional_support", f"Expected 'emotional_support', got '{task}'"
except Exception as e:
    print(f"   ❌ detect_task_type error: {e}")

# Test detect_context
try:
    context = detect_context([], "Hello")
    print(f"   ✅ detect_context([], 'Hello') = '{context}'")
    assert context == "first_message", f"Expected 'first_message', got '{context}'"
except Exception as e:
    print(f"   ❌ detect_context error: {e}")

# Test get_sentiment_emoji
try:
    emoji = get_sentiment_emoji("negative")
    print(f"   ✅ get_sentiment_emoji('negative') = '{emoji}'")
    assert emoji == "😞", f"Expected '😞', got '{emoji}'"
except Exception as e:
    print(f"   ❌ get_sentiment_emoji error: {e}")

# Test build_conversation_summary
try:
    history = [
        {'role': 'user', 'content': 'Hello', 'sentiment': 'neutral'},
        {'role': 'assistant', 'content': 'Hi there!', 'sentiment': None}
    ]
    summary = build_conversation_summary(history)
    print(f"   ✅ build_conversation_summary() works")
    print(f"      Summary preview: {summary[:50]}...")
except Exception as e:
    print(f"   ❌ build_conversation_summary error: {e}")

# Test build_system_prompt
try:
    prompt = build_system_prompt(
        base_style="default",
        user_sentiment="negative",
        task_type="emotional_support",
        context="follow_up",
        conversation_history=[],
        enable_memory=True
    )
    print(f"   ✅ build_system_prompt() works")
    print(f"      Prompt length: {len(prompt)} characters")
    
    # Check for key memory indicators
    memory_keywords = ["MEMORY", "remember", "REMEMBER", "previous"]
    found = [kw for kw in memory_keywords if kw in prompt]
    print(f"      Memory keywords found: {len(found)}")
    
except Exception as e:
    print(f"   ❌ build_system_prompt error: {e}")

# Test 5: Check for removed/deprecated exports
print("\n5. Checking for removed exports (should fail)...")
try:
    from prompts import AGENTIC_CAPABILITIES
    print(f"   ⚠️  AGENTIC_CAPABILITIES still exists (should be removed)")
except ImportError:
    print(f"   ✅ AGENTIC_CAPABILITIES correctly removed")

try:
    from prompts import RESPONSE_TEMPLATES
    print(f"   ⚠️  RESPONSE_TEMPLATES still exists (should be removed)")
except ImportError:
    print(f"   ✅ RESPONSE_TEMPLATES correctly removed")

print("\n" + "=" * 80)
print("VERIFICATION COMPLETE!")
print("=" * 80)
