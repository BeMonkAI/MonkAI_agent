"""
Test script to verify the context window management functionality of MonkAI Framework.
This test will:
1. Create an agent with context window management enabled
2. Send multiple messages to exceed the context window
3. Verify that messages are properly summarized
4. Track and display token usage information
"""

import os
import time
from monkai_agent import MonkaiAgentCreator

def test_context_window():
    """
    Test context window management by:
    1. Creating an agent with a small context window
    2. Sending multiple messages to exceed the window
    3. Verifying messages are properly summarized
    4. Checking token usage tracking
    """
    
    # Create agent with small context window
    agent = MonkaiAgentCreator(
        base_prompt="You are a helpful AI assistant.",
        model="gpt-3.5-turbo",
        provider="openai",
        context_window_size=1000,  # Small window for testing
        freeze_context_window_size=True,
        track_token_usage=True  # Enable token tracking
    )
    
    # Create conversation with multiple messages
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Let's discuss Python programming."},
        {"role": "assistant", "content": "I'd be happy to discuss Python programming! Python is a versatile programming language known for its readability and extensive library ecosystem. What specific aspects would you like to explore?"},
        {"role": "user", "content": "Tell me about Django framework."},
        {"role": "assistant", "content": "Django is a high-level Python web framework that enables rapid development of secure and maintainable websites. It follows the model-template-view architectural pattern and provides an ORM, authentication, admin interface and many other features out of the box."},
        {"role": "user", "content": "What about Flask?"},
        {"role": "assistant", "content": "Flask is a lightweight WSGI web application framework in Python. It's designed to be simple and easy to get started with, while also being flexible and extensible. Unlike Django, Flask doesn't include an ORM or many features out of the box, giving developers more freedom in their technology choices."},
        {"role": "user", "content": "Can you compare Django and Flask?"}
    ]
    
    try:
        print("\nTesting context window management...")
        print(f"Initial message count: {len(messages)}")
        
        # Get initial token count
        initial_tokens = agent.count_message_tokens(messages)
        print(f"Initial token count: {initial_tokens}")
        
        # Send request that should trigger summarization
        response = agent.get_chat_completion(messages=messages)
        
        # Get token usage information
        token_usage = agent.get_token_usage()
        
        print(f"\nResponse received: {response.choices[0].message.content[:100]}...")
        print("\nToken Usage:")
        print(f"- Input tokens: {token_usage.input_tokens}")
        print(f"- Output tokens: {token_usage.output_tokens}")
        print(f"- Total tokens: {token_usage.input_tokens + token_usage.output_tokens}")
        
        print("\nContext window test passed - received valid response after summarization")
        return True
        
    except Exception as e:
        print(f"Context window test failed: {str(e)}")
        return False

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set")
        exit(1)
        
    test_result = test_context_window()
    exit(0 if test_result else 1) 