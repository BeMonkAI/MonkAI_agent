"""
A Streamlit UI for testing different LLM providers (OpenAI and Groq) and their models.
This example allows users to:
1. Choose the LLM provider
2. Input their API key
3. Select the model they want to use
4. Test the model with custom queries
"""

import os
import json
import streamlit as st
from typing import Dict, List
from monkai_agent.monkai_agent_creator import MonkaiAgentCreator
from monkai_agent.llm_providers import GROQ_MODELS
from openai import OpenAI

# Define OpenAI models
OPENAI_MODELS = [
    "gpt-4-turbo-preview",
    "gpt-4",
    "gpt-3.5-turbo"
]

def create_agent_with_model(provider: str, model: str, api_key: str) -> MonkaiAgentCreator:
    """
    Create an agent with a specific provider and model.
    
    Args:
        provider: The LLM provider (openai or groq)
        model: The model to use
        api_key: The API key for the provider
        
    Returns:
        MonkaiAgentCreator instance
    """
    return MonkaiAgentCreator(
        base_prompt="You are a helpful AI assistant specializing in technical explanations.",
        model=model,
        provider=provider
    )

def test_model(provider: str, model: str, api_key: str, query: str) -> Dict:
    """
    Test a specific model with a query.
    
    Args:
        provider: The LLM provider
        model: The model to test
        api_key: The API key
        query: The query to send to the model
        
    Returns:
        Dict containing the model name and response
    """
    # Set the API key in environment
    os.environ[f"{provider.upper()}_API_KEY"] = api_key
    
    # Create agent creator
    agent_creator = create_agent_with_model(provider, model, api_key)
    
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
    st.title("LLM Model Testing UI")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Provider selection
        provider = st.selectbox(
            "Select Provider",
            ["openai", "groq"],
            help="Choose between OpenAI and Groq"
        )
        
        # API key input
        api_key = st.text_input(
            f"Enter {provider.upper()} API Key",
            type="password",
            help=f"Enter your {provider.upper()} API key"
        )
        
        # Model selection based on provider
        available_models = OPENAI_MODELS if provider == "openai" else GROQ_MODELS
        model = st.selectbox(
            "Select Model",
            available_models,
            help="Choose the model to test"
        )
    
    # Main content area
    st.header("Test the Model")
    
    # Example queries
    example_queries = [
        "Explain quantum computing in simple terms.",
        "Write a Python function to calculate the Fibonacci sequence.",
        "What are the key principles of machine learning?"
    ]
    
    # Query input
    query = st.text_area(
        "Enter your query",
        help="Type your question or use one of the example queries below"
    )
    
    # Example query buttons
    st.subheader("Or try an example query:")
    cols = st.columns(len(example_queries))
    for i, example in enumerate(example_queries):
        if cols[i].button(f"Example {i+1}"):
            query = example
            st.session_state.query = example
    
    # Test button
    if st.button("Test Model", type="primary", disabled=not (api_key and query)):
        if not api_key:
            st.error("Please enter your API key")
        elif not query:
            st.error("Please enter a query")
        else:
            with st.spinner("Getting response..."):
                try:
                    result = test_model(provider, model, api_key, query)
                    
                    # Display results
                    st.subheader("Response:")
                    st.markdown(result["response"])
                    
                    # Save results
                    filename = f"{provider}_{model}_{query[:30].replace(' ', '_')}.json"
                    with open(filename, "w") as f:
                        json.dump(result, f, indent=2)
                    
                    st.success(f"Results saved to {filename}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 