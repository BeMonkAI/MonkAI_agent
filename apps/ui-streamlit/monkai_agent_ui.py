import streamlit as st
# Set page config as first Streamlit command
st.set_page_config(
    page_title="MonkAI Framework Developer",
    page_icon="🤖",
    layout="wide"
)

"""
A Streamlit UI for the MonkAI Framework Developer Agent.
This interface allows users to:
1. Choose the LLM provider (OpenAI or Groq)
2. Input their API key
3. Select the model they want to use
4. Interact with the specialized Framework Developer agent
5. Save and review conversation history
"""

import asyncio
import os
import json
from typing import Dict, List, Optional
from monkai_agent import AgentManager, MonkaiAgentCreator
from openai import OpenAI
from monkai_agent.groq import GroqProvider, GROQ_MODELS
from monkai_agent import OpenAIProvider, LLMProvider
from agent_architect_creator import AgentArchitectCreator
from apps.examples.triage.calculator_agents_creator import CalculatorAgentCriator

# Define OpenAI models
OPENAI_MODELS = [
    "gpt-4o",
    "gpt-4o-mini"
]

# Define the framework developer prompt
FRAMEWORK_DEVELOPER_PROMPT = """You are a specialized AI framework developer for the MonkAI framework.
Your role is to help users understand and develop code for the MonkAI framework.

Key Components of MonkAI:
1. AgentManager: Manages agent instances and handles chat completions
2. MonkaiAgentCreator: Abstract base class for creating different types of agents
3. PromptTestingAgentCreator: Specialized creator for testing and optimizing prompts
4. Types: Contains core types and interfaces

When helping users:
1. Always reference the correct MonkAI classes and methods
2. Follow the existing framework patterns and conventions
3. Include proper imports from monkai_agent
4. Provide examples that integrate with the framework
5. Explain parameters and their purposes
6. Include error handling specific to the framework
7. Consider framework-specific best practices

For code generation, format your response as:
{
    "code": "the generated code here",
    "dependencies": ["list", "of", "required", "dependencies"],
    "usage_example": "example of how to use the generated code with MonkAI",
    "notes": "any important notes about MonkAI integration"
}

For documentation questions, provide clear explanations about:
- Class purposes and relationships
- Method parameters and return types
- Framework-specific patterns
- Integration examples
"""

def get_provider(provider: str, model: str, api_key: str) -> MonkaiAgentCreator:
    """
    Create a specialized Framework Developer agent.
    
    Args:
        provider: The LLM provider (openai or groq)
        model: The model to use
        api_key: The API key for the provider
        
    Returns:
        MonkaiAgentCreator instance configured for framework development
    """
    if provider == "openai":
        llm_provider = OpenAIProvider(model=model, api_key=api_key)
    else:
        llm_provider = GroqProvider(model=model, api_key=api_key)
    return llm_provider 

def initialize_chat_history() -> List[Dict]:
    """Initialize an empty chat history"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "intro_shown" not in st.session_state:
        st.session_state.intro_shown = False
    return st.session_state.messages

def display_chat_message(message: Dict):
    """Display a chat message with the appropriate styling"""
    role = message["role"]
    content = message["content"]
    
    if role == "user":
        st.chat_message("user").write(content)
    elif role == "assistant":
        with st.chat_message("assistant"):
            try:
                # Try to parse the response as JSON if it's code generation
                response_data = json.loads(content)
                
                # Display code section
                if "code" in response_data:
                    st.markdown("### Generated Code")
                    st.code(response_data["code"], language="python")
                
                # Display dependencies
                if "dependencies" in response_data:
                    st.markdown("### Required Dependencies")
                    for dep in response_data["dependencies"]:
                        st.markdown(f"- `{dep}`")
                
                # Display usage example
                if "usage_example" in response_data:
                    st.markdown("### Usage Example")
                    st.code(response_data["usage_example"], language="python")
                
                # Display notes
                if "notes" in response_data:
                    st.markdown("### Notes")
                    st.markdown(response_data["notes"])
                    
            except json.JSONDecodeError:
                # If not JSON, display as regular markdown
                st.markdown(content)
    elif role == "system":
        st.chat_message("system").write(content)

def main():
    st.title("MonkAI Framework Developer Assistant")
    
    # Initialize chat history
    messages = initialize_chat_history()
    
    # Call chat interface
    asyncio.run(chat())

async def chat():
    messages = st.session_state.messages

    # Display chat history
    for message in messages:
        display_chat_message(message)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Provider selection with unique key
        provider = st.selectbox(
            "Select Provider",
            ["openai", "groq"],
            help="Choose between OpenAI and Groq",
            key="provider_selector"
        )
        
        # Model selection based on provider
        available_models = OPENAI_MODELS if provider == "openai" else GROQ_MODELS
        model = st.selectbox(
            "Select Model",
            available_models,
            help="Choose the model to use",
            key="model_selector"
        )
        
        # API key section
        st.subheader("API Key Configuration")
        api_key = st.text_input(
            f"Enter {provider.upper()} API Key",
            type="password",
            help=f"Enter your {provider.upper()} API key",
            key="api_key_input"
        )
        
        # Advanced settings matching AgentManager parameters
        with st.expander("Advanced Settings"):
            col1, col2 = st.columns(2)
            
            with col1:
                temperature = st.slider(
                    "Temperature", 
                    0.0, 2.0, 0.7, 
                    help="Controls randomness in responses",
                    key="temperature"
                )
                max_tokens = st.number_input(
                    "Max Tokens", 
                    1, 4096, 2048,
                    help="Maximum number of tokens to generate",
                    key="max_tokens"
                )
                max_retries = st.number_input(
                    "Max Retries", 
                    1, 10, 3,
                    help="Maximum number of retry attempts",
                    key="max_retries"
                )
                retry_delay = st.slider(
                    "Retry Delay", 
                    0.1, 5.0, 1.0,
                    help="Delay between retry attempts in seconds",
                    key="retry_delay"
                )
                
            with col2:
                rate_limit_rpm = st.number_input(
                    "Rate Limit (RPM)", 
                    0, 100, 0,
                    help="Rate limit in requests per minute (0 for no limit)",
                    key="rate_limit"
                )
                max_execution_time = st.number_input(
                    "Max Execution Time", 
                    0, 300, 0,
                    help="Maximum execution time in seconds (0 for no limit)",
                    key="max_execution_time"
                )
                context_window_size = st.number_input(
                    "Context Window Size", 
                    0, 32768, 4096,
                    help="Maximum context window size in tokens",
                    key="context_window"
                )
                
            # Additional settings
            debug = st.checkbox(
                "Debug Mode", 
                value=False,
                help="Enable debug logging",
                key="debug"
            )
            stream = st.checkbox(
                "Stream Response", 
                value=False,
                help="Enable streaming responses",
                key="stream"
            )
            track_token_usage = st.checkbox(
                "Track Token Usage", 
                value=True,
                help="Track token usage statistics",
                key="track_tokens"
            )

    # Display framework information only once
    if not st.session_state.intro_shown:
        st.markdown("""
        This assistant helps you understand and develop code for the MonkAI framework.
        You can ask questions about:
        - Framework components and their relationships
        - Class and method documentation
        - Code generation following framework patterns
        - Integration examples
        - Best practices and conventions
        
        Example questions:
        - "How do I create a new agent type?"
        - "What parameters does AgentManager.get_chat_completion accept?"
        - "Show me how to implement a custom agent creator"
        - "Explain the relationship between AgentManager and MonkaiAgentCreator"
        """)
        st.session_state.intro_shown = True

    # Chat input and processing
    if prompt := st.chat_input("Ask about MonkAI framework development..."):
        if not api_key:
            st.error("Please enter your API key in the sidebar")
            return
            
        # Add user message to chat
        messages.append({"role": "user", "content": prompt})
        display_chat_message({"role": "user", "content": prompt})
        
        try:
            # Create appropriate provider based on selection
            llm_provider = (OpenAIProvider(api_key=api_key) if provider == "openai" 
                          else GroqProvider(api_key=api_key))
            
            with st.spinner("Thinking..."):
                # Initialize AgentManager with provider instance
                if provider == "openai":
                    assistant_message = await openai_response(messages, model, temperature, max_tokens, max_retries, retry_delay, rate_limit_rpm, max_execution_time, context_window_size, debug, stream, track_token_usage, prompt, llm_provider)
                else:
                    pass
                display_chat_message(assistant_message)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

    # Chat management buttons
    col1, col2 = st.columns(2)
    if col1.button("Clear Chat"):
        st.session_state.messages = []
        st.experimental_rerun()
    
    if col2.button("Save Chat"):
        chat_data = {
            "provider": provider,
            "model": model,
            "messages": messages
        }
        filename = f"framework_dev_chat_{provider}_{model}_{len(messages)}.json"
        with open(filename, "w") as f:
            json.dump(chat_data, f, indent=2)
        st.success(f"Chat history saved to {filename}")

async def openai_response(messages, model, temperature, max_tokens, max_retries, retry_delay, rate_limit_rpm, max_execution_time, context_window_size, debug, stream, track_token_usage, prompt, llm_provider):
    manager = AgentManager(
                        agents_creators=[],
                        provider=llm_provider,  # Pass the provider instance
                        stream=stream,
                        debug=debug,
                        model=model,
                        max_retries=max_retries,
                        retry_delay=retry_delay,
                        rate_limit_rpm=rate_limit_rpm if rate_limit_rpm > 0 else None,
                        max_execution_time=max_execution_time if max_execution_time > 0 else None,
                        context_window_size=context_window_size,
                        track_token_usage=track_token_usage,
                        temperature=temperature
                    )

    current_agent = AgentArchitectCreator()
                    
                    # Call run with simplified parameters since provider handles model
    response = await manager.run(
                        user_message=prompt,
                        user_history=messages,
                        agent=current_agent.get_agent(),
                        max_tokens=max_tokens,
                        max_turn=30
                    )
                    
                    # Add assistant response to chat
    assistant_message = {
                        "role": "assistant",
                        "content": response.messages[-1]["content"]
                    }
    messages.append(assistant_message)
    return assistant_message

if __name__ == "__main__":
    main()