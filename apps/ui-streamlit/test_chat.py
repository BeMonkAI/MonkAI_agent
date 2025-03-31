"""Test script for MonkAI Framework Developer chat completion"""

import os
from monkai_agent import MonkaiAgentCreator
from monkai_agent.groq.providers import GROQ_MODELS

# Test prompt
FRAMEWORK_DEVELOPER_PROMPT = """You are a specialized AI framework developer for the MonkAI framework.
Your role is to help users understand and develop code for the MonkAI framework."""

def test_chat_completion(provider: str, api_key: str):
    """Test the chat completion functionality"""
    
    # Select model based on provider
    model = "gpt-4o" if provider == "openai" else GROQ_MODELS[0]
    
    print(f"\nTesting {provider.upper()} provider with model: {model}")
    
    # Create agent
    agent_creator = MonkaiAgentCreator(
        base_prompt=FRAMEWORK_DEVELOPER_PROMPT,
        model=model,
        provider=provider,
        api_key=api_key
    )
    
    # Test messages
    messages = [
        {"role": "system", "content": FRAMEWORK_DEVELOPER_PROMPT},
        {"role": "user", "content": "How do I create a new agent type?"}
    ]
    
    # Get completion
    try:
        response = agent_creator.get_chat_completion(
            messages=messages,
            model=model,
            temperature=0.7,
            max_tokens=2048
        )
        print("\nResponse:")
        print(response.choices[0].message.content)
        return True
    except Exception as e:
        print(f"\nError: {str(e)}")
        return False

if __name__ == "__main__":
    # Test OpenAI
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        success = test_chat_completion("openai", openai_key)
        if success:
            print("\nOpenAI test successful!")
        else:
            print("\nOpenAI test failed!")
    
    # Test Groq
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        success = test_chat_completion("groq", groq_key)
        if success:
            print("\nGroq test successful!")
        else:
            print("\nGroq test failed!")
    
    if not openai_key and not groq_key:
        print("\nPlease set either OPENAI_API_KEY or GROQ_API_KEY environment variable") 