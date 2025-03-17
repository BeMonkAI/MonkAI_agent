"""
Example demonstrating the use of different Groq models with MonkAI framework.
This example shows how to:
1. Use different Groq models
2. Compare responses between models
3. Handle model-specific parameters
"""

import os
from typing import Dict, List
from monkai_agent.monkai_agent_creator import MonkaiAgentCreator
from monkai_agent.llm_providers import GROQ_MODELS
from openai import OpenAI

def create_agent_with_model(model: str) -> MonkaiAgentCreator:
    """
    Create an agent with a specific Groq model.
    
    Args:
        model: The Groq model to use
        
    Returns:
        MonkaiAgentCreator instance
    """
    return MonkaiAgentCreator(
        base_prompt="You are a helpful AI assistant specializing in technical explanations.",
        model=model,
        provider="groq"
    )

def test_model(model: str, query: str) -> Dict:
    """
    Test a specific model with a query.
    
    Args:
        model: The Groq model to test
        query: The query to send to the model
        
    Returns:
        Dict containing the model name and response
    """
    print(f"\nTesting model: {model}")
    
    # Create agent creator
    agent_creator = create_agent_with_model(model)
    
    # Run the query
    response = agent_creator.get_chat_completion(
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant specializing in technical explanations."},
            {"role": "user", "content": query}
        ]
    )
    
    return {
        "model": model,
        "response": response.choices[0].message.content
    }

def main():
    # Example queries to test different aspects
    queries = [
        "Explain quantum computing in simple terms.",
        "Write a Python function to calculate the Fibonacci sequence.",
        "What are the key principles of machine learning?"
    ]
    
    # Test each model with each query
    for query in queries:
        print(f"\n{'='*50}")
        print(f"Query: {query}")
        print(f"{'='*50}")
        
        results = []
        for model in GROQ_MODELS:
            try:
                result = test_model(model, query)
                results.append(result)
                print(f"\n{model}:")
                print(result["response"])
            except Exception as e:
                print(f"Error with {model}: {str(e)}")
        
        # Save results to a file
        with open(f"groq_comparison_{query[:30].replace(' ', '_')}.json", "w") as f:
            import json
            json.dump(results, f, indent=2)

if __name__ == "__main__":
    # Make sure GROQ_API_KEY is set
    if not os.getenv("GROQ_API_KEY"):
        print("Please set your GROQ_API_KEY environment variable")
        exit(1)
    
    main() 