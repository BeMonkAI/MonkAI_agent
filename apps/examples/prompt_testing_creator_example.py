"""
Example demonstrating how to use the PromptTestingAgentCreator for testing and optimizing prompts.
This example shows how to:
1. Create a PromptTestingAgentCreator with multiple prompts
2. Enable AI prompt generation
3. Test different prompts with the same query
4. Compare responses
"""

import asyncio
import os
from openai import OpenAI
from monkai_agent import AgentManager
from monkai_agent.monkai_agent_creator import PromptTestingAgentCreator
from typing import Dict, List

async def test_prompt(agent_manager: AgentManager, agent_creator: PromptTestingAgentCreator, 
                     prompt_name: str, query: str) -> str:
    """
    Test a specific prompt with a query.
    
    Args:
        agent_manager: The agent manager instance
        agent_creator: The prompt testing agent creator
        prompt_name: Name of the prompt to test
        query: The query to test with
        
    Returns:
        str: The response from the agent
    """
    # Set the current prompt
    agent_creator.set_current_prompt(prompt_name)
    
    # Get the agent with current prompt
    agent = agent_creator.get_agent()
    agent_manager.agent = agent
    
    # Run the query
    messages = [{"role": "user", "content": query}]
    response = agent_manager.get_chat_completion(
        agent=agent,
        history=messages,
        context_variables={},
        model_override=None,
        temperature=0.7,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stream=False,
        debug=False
    )
    
    return response.choices[0].message.content

async def main():
    # Get API key from environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is not set")
        return
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Define base prompt and additional prompts
    base_prompt = "You are a helpful assistant that provides concise answers."
    
    additional_prompts = {
        "Technical Expert": """You are an expert in technical fields with deep knowledge of advanced concepts.
        Your responses should be precise, technically accurate, and use appropriate terminology.
        Focus on explaining complex concepts in a clear and concise manner.""",
        
        "Scientific Writer": """You are a scientific writer specializing in making complex concepts accessible.
        Your explanations should:
        1. Use precise scientific terminology
        2. Maintain technical accuracy
        3. Be concise and well-structured
        4. Focus on key concepts and relationships""",
        
        "Research Analyst": """You are a research analyst with expertise in emerging technologies.
        When explaining concepts:
        - Use precise technical language
        - Include key technical terms
        - Focus on fundamental principles
        - Maintain scientific accuracy
        - Be concise and direct"""
    }
    
    # Create the prompt testing agent creator
    agent_creator = PromptTestingAgentCreator(
        client=client,
        base_prompt=base_prompt,
        additional_prompts=additional_prompts,
        enable_ai_prompt_generation=True,  # Enable AI prompt generation
        model="gpt-4"
    )
    
    # Initialize the agent creator (generates AI-enhanced prompt if enabled)
    print("\nInitializing PromptTestingAgentCreator...")
    await agent_creator.initialize()
    
    # Create agent manager
    agent_manager = AgentManager(client=client, agents_creators=[])
    
    # Define test query
    test_query = "Explain quantum computing in one sentence."
    
    print("\nPrompt Testing Results")
    print("=" * 80)
    print(f"Test Query: {test_query}")
    print("\nResponses from different prompts:")
    print("-" * 80)
    
    # Test each prompt
    results: Dict[str, str] = {}
    for prompt_name in agent_creator.available_prompts:
        try:
            print(f"\nTesting {prompt_name}...")
            response = await test_prompt(agent_manager, agent_creator, prompt_name, test_query)
            
            print(f"\n{prompt_name}:")
            print(f"System Prompt: {agent_creator._current_prompt}")
            print(f"Response: {response}")
            print("-" * 80)
            
            results[prompt_name] = response
            
        except Exception as e:
            print(f"\nError with {prompt_name}:")
            print(f"Error message: {str(e)}")
            print("-" * 80)
            results[prompt_name] = f"Error: {str(e)}"
    
    # Save results to JSON
    import json
    with open("prompt_testing_creator_results.json", "w") as f:
        json.dump({
            "query": test_query,
            "results": results
        }, f, indent=2)
    
    print("\nResults have been saved to 'prompt_testing_creator_results.json'")

if __name__ == "__main__":
    asyncio.run(main()) 