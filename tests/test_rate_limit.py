"""
Test script to verify the rate limiting functionality of MonkAI Framework.
This test will:
1. Create an agent with a specific rate limit
2. Make multiple requests in quick succession
3. Measure the time between requests to verify rate limiting
"""

import os
import time
from monkai_agent import MonkaiAgentCreator

def test_rate_limiting():
    """Test the rate limiting functionality"""
    
    # Create agent with a low rate limit (10 requests per minute) for testing
    agent_creator = MonkaiAgentCreator(
        base_prompt="You are a helpful AI assistant.",
        model="gpt-4o",
        provider="openai",
        rate_limit_rpm=10,  # 10 requests per minute = 1 request per 6 seconds
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Test messages
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Say hello!"}
    ]
    
    print("\nTesting rate limiting with 5 requests...")
    completion_times = []
    
    # Make 5 requests and record their completion times
    for i in range(5):
        try:
            response = agent_creator.get_chat_completion(
                messages=messages,
                max_tokens=50
            )
            completion_times.append(time.time())
            print(f"\nRequest {i+1}:")
            print(f"Response: {response.choices[0].message.content}")
                
        except Exception as e:
            print(f"Error in request {i+1}: {str(e)}")
    
    # Calculate and print the intervals between requests
    intervals = []
    for i in range(1, len(completion_times)):
        interval = completion_times[i] - completion_times[i-1]
        intervals.append(interval)
    
    print("\nTime intervals between requests:")
    expected_interval = 60 / 10  # 10 requests per minute
    for i, interval in enumerate(intervals):
        print(f"Between requests {i+1} and {i+2}: {interval:.2f}s (Expected: {expected_interval:.2f}s)")
    
    # Verify if rate limiting is working
    min_interval = min(intervals) if intervals else 0
    if min_interval >= (expected_interval * 0.9):  # Allow 10% margin
        print("\nRate limiting test PASSED! ✅")
        print(f"All intervals were at least {expected_interval * 0.9:.2f} seconds")
    else:
        print("\nRate limiting test FAILED! ❌")
        print(f"Some intervals were shorter than expected minimum of {expected_interval * 0.9:.2f} seconds")

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set OPENAI_API_KEY environment variable")
    else:
        test_rate_limiting() 