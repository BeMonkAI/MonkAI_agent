"""
Example demonstrating how to use the prompt testing and optimization features of MonkAI.
This example compares different prompts for a complex query.
"""

import asyncio
import os
from openai import OpenAI
from monkai_agent import Agent, PromptTest, PromptOptimizerManager, AgentManager
from typing import List, Dict
import json

async def generate_enhanced_prompt(client: OpenAI, base_prompts: Dict[str, str]) -> str:
    """Generate an enhanced prompt using AI by analyzing existing prompts."""
    prompt_analysis = "\n".join([
        f"Prompt {i+1}:\n{prompt}\n"
        for i, prompt in enumerate(base_prompts.values())
    ])
    
    messages = [
        {"role": "system", "content": "You are an expert in prompt engineering and optimization."},
        {"role": "user", "content": f"""Analyze these prompts and create an enhanced version that combines their strengths:
        
{prompt_analysis}

Create a new prompt that:
1. Synthesizes the best aspects of all prompts
2. Adds improvements and optimizations
3. Maintains clarity and structure
4. Is more comprehensive and effective

Format the response as a complete system prompt."""}
    ]
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=500
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
    
    # Define different prompts to test
    base_prompts = {
        "Basic Prompt": "You are a helpful assistant that provides concise answers.",
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
    
    # Enable/disable AI prompt generation
    AI_PROMPT_GENERATE = True
    
    # Generate enhanced prompt if enabled
    prompts = base_prompts.copy()
    if AI_PROMPT_GENERATE:
        print("\nGenerating AI-enhanced prompt...")
        enhanced_prompt = await generate_enhanced_prompt(client, base_prompts)
        prompts["AI-Enhanced Expert"] = enhanced_prompt
        print("AI-enhanced prompt generated successfully!")
    
    # Create a complex test case
    test_case = PromptTest(
        name="Complex Technical Query",
        input_text="Explain quantum computing in one sentence.",
        expected_output="Quantum computing uses quantum-mechanical phenomena to perform calculations that would be impossible for classical computers."
    )
    
    # Create agent manager
    agent_manager = AgentManager(client=client, agents_creators=[])
    
    print("\nComplex Query Comparison")
    print("=" * 80)
    print(f"User Message: {test_case.input_text}")
    print("\nResponses from different prompts:")
    print("-" * 80)
    
    results_data = {}
    
    for prompt_name, prompt_text in prompts.items():
        try:
            # Create agent with current prompt
            agent = Agent(
                name=f"TestAgent_{prompt_name}",
                instructions=prompt_text,
                model="gpt-4"
            )
            agent_manager.agent = agent
            
            # Run test
            messages = [{"role": "user", "content": test_case.input_text}]
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
            
            # Print results
            print(f"\n{prompt_name}:")
            print(f"System Prompt: {prompt_text}")
            print(f"User Message: {test_case.input_text}")
            print(f"Answer: {response.choices[0].message.content}")
            print("-" * 80)
            
            # Store results
            results_data[prompt_name] = {
                "system_prompt": prompt_text,
                "input": test_case.input_text,
                "response": response.choices[0].message.content
            }
            
        except Exception as e:
            print(f"\nError with {prompt_name}:")
            print(f"System Prompt: {prompt_text}")
            print(f"Error message: {str(e)}")
            print("-" * 80)
            results_data[prompt_name] = {
                "system_prompt": prompt_text,
                "input": test_case.input_text,
                "error": str(e)
            }
    
    # Save results to JSON for reference
    with open("complex_query_comparison.json", "w") as f:
        json.dump(results_data, f, indent=2)
    
    print("\nResults have been saved to 'complex_query_comparison.json'")

if __name__ == "__main__":
    asyncio.run(main())