"""
Test script to verify the timeout functionality of MonkAI Framework.
This test will:
1. Create an agent with a short timeout for long requests
2. Create an agent with a longer timeout for short requests
3. Verify that TimeoutError is raised appropriately
"""

import os
import time
from concurrent.futures import TimeoutError
from monkai_agent import MonkaiAgentCreator

def test_timeout():
    """Test the timeout functionality"""
    
    print("\nTesting timeout functionality...")
    timeout_occurred = False
    short_request_success = False
    
    # Test 1: Long request with short timeout
    print("\nTest 1: Long request with 5-second timeout")
    agent_creator_short = MonkaiAgentCreator(
        base_prompt="You are a helpful AI assistant.",
        model="gpt-4o",
        provider="openai",
        max_execution_time=5,  # 5 seconds timeout
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Test messages - make it a complex task that should take longer
    long_messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": """Please write a detailed 2000-word essay about the history of artificial intelligence, 
         including all major developments from the 1950s to present day. Include specific dates, names, and detailed explanations 
         of each breakthrough. Also analyze the potential future developments in the next 50 years."""}
    ]
    
    try:
        print("Making a request that should timeout...")
        start_time = time.time()
        response = agent_creator_short.get_chat_completion(
            messages=long_messages,
            model="gpt-4o",
            temperature=0.7,
            max_tokens=2000  # Request a long response
        )
        print(f"Request completed in {time.time() - start_time:.2f} seconds (unexpected)")
        
    except TimeoutError as e:
        timeout_occurred = True
        print(f"Timeout occurred as expected after {time.time() - start_time:.2f} seconds: {str(e)}")
    
    # Test 2: Short request with longer timeout
    print("\nTest 2: Short request with 15-second timeout")
    agent_creator_long = MonkaiAgentCreator(
        base_prompt="You are a helpful AI assistant.",
        model="gpt-4o",
        provider="openai",
        max_execution_time=15,  # 15 seconds timeout
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Test with a shorter request that should complete
    short_messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Say hello!"}
    ]
    
    try:
        print("Making a request that should complete quickly...")
        start_time = time.time()
        response = agent_creator_long.get_chat_completion(
            messages=short_messages,
            model="gpt-4o",
            temperature=0.7,
            max_tokens=50
        )
        elapsed = time.time() - start_time
        print(f"Quick request completed successfully in {elapsed:.2f} seconds:")
        print(f"Response: {response.choices[0].message.content}")
        short_request_success = True
        
    except TimeoutError as e:
        print(f"Unexpected timeout after {time.time() - start_time:.2f} seconds: {str(e)}")
    except Exception as e:
        print(f"Unexpected error after {time.time() - start_time:.2f} seconds: {str(e)}")
    
    # Print test results
    print("\nTest Results:")
    if timeout_occurred and short_request_success:
        print("Timeout test PASSED! ✅")
        print("- Long request timed out as expected")
        print("- Short request completed successfully")
    else:
        print("Timeout test FAILED! ❌")
        if not timeout_occurred:
            print("- Long request did not timeout as expected")
        if not short_request_success:
            print("- Short request failed to complete")

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set OPENAI_API_KEY environment variable")
    else:
        test_timeout() 