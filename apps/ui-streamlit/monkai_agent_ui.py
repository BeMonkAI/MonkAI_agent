"""
A Streamlit UI for the MonkAI Framework Developer Agent.
This interface allows users to:
1. Choose the LLM provider (OpenAI or Groq)
2. Input their API key
3. Select the model they want to use
4. Interact with the specialized Framework Developer agent
5. Save and review conversation history
"""

import os
import json
import streamlit as st
from typing import Dict, List, Optional
from monkai_agent import AgentManager, MonkaiAgentCreator
from openai import OpenAI

from monkai_agent.groq import GROQ_MODELS
from monkai_agent import LLMProvider

# Available Groq models

def get_llm_provider(provider: str = "openai", api_key: Optional[str] = None, **kwargs) -> LLMProvider:
    """
    Get an LLM provider instance.
    
    Args:
        provider: The LLM provider to use ("openai" or "groq")
        api_key: The API key for the provider
        **kwargs: Additional arguments for the provider
        
    Returns:
        An instance of LLMProvider
    """
    if api_key is None:
        if provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
        elif provider == "groq":
            api_key = os.getenv("GROQ_API_KEY")
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    if provider == "openai":
        return OpenAIProvider(api_key)
    elif provider == "groq":
        model = kwargs.get("model", GROQ_MODELS[0])
        return GroqProvider(api_key, model)
    else:
        raise ValueError(f"Unknown provider: {provider}") 
        


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

def create_framework_developer_agent(provider: str, model: str, api_key: str) -> MonkaiAgentCreator:
    """
    Create a specialized Framework Developer agent.
    
    Args:
        provider: The LLM provider (openai or groq)
        model: The model to use
        api_key: The API key for the provider
        
    Returns:
        MonkaiAgentCreator instance configured for framework development
    """
    return MonkaiAgentCreator(
        base_prompt=FRAMEWORK_DEVELOPER_PROMPT,
        model=model,
        provider=provider,
        api_key=api_key
    )

def initialize_chat_history() -> List[Dict]:
    """Initialize an empty chat history"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
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
    st.set_page_config(
        page_title="MonkAI Framework Developer",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("MonkAI Framework Developer Assistant")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Provider selection
        provider = st.selectbox(
            "Select Provider",
            ["openai", "groq"],
            help="Choose between OpenAI and Groq"
        )
        
        # API key section
        st.subheader("API Key Configuration")
        
        # API key input with Enter button
        api_key_col1, api_key_col2 = st.columns([3, 1])
        with api_key_col1:
            api_key = st.text_input(
                f"Enter {provider.upper()} API Key",
                type="password",
                help=f"Enter your {provider.upper()} API key",
                key="api_key_input"
            )
        with api_key_col2:
            if st.button("Enter"):
                if api_key:
                    st.success("API Key set! ✅")
                    st.session_state.api_key = api_key
                else:
                    st.error("Please enter an API key")
        
        # Model selection based on provider
        available_models = OPENAI_MODELS if provider == "openai" else GROQ_MODELS
        model = st.selectbox(
            "Select Model",
            available_models,
            help="Choose the model to use"
        )
        
        # Advanced settings
        with st.expander("Advanced Settings"):
            temperature = st.slider("Temperature", 0.0, 2.0, 0.7)
            max_tokens = st.number_input("Max Tokens", 1, 4096, 2048)
            top_p = st.slider("Top P", 0.0, 1.0, 0.9)
            frequency_penalty = st.slider("Frequency Penalty", -2.0, 2.0, 0.0)
            presence_penalty = st.slider("Presence Penalty", -2.0, 2.0, 0.0)
    
    # Display framework information
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
    
    # Initialize chat history
    messages = initialize_chat_history()
    
    # Display chat history
    for message in messages:
        display_chat_message(message)
    
    # Chat input
    if prompt := st.chat_input("Ask about MonkAI framework development..."):
        # Check if API key is set in session state
        if not getattr(st.session_state, 'api_key', None):
            st.error("Please enter your API key and click 'Enter' in the sidebar")
            return
            
        # Add user message to chat
        messages.append({"role": "user", "content": prompt})
        display_chat_message({"role": "user", "content": prompt})
        
        # Create agent and get response
        try:
            #api_key = st.session_state.api_key
            #os.environ[f"{provider.upper()}_API_KEY"] = api_key
            client = OpenAI(api_key=st.session_state.api_key)
            agent_manager = AgentManager(client, model, api_key)
            
            with st.spinner("Thinking..."):
                # Add system message with instructions
                full_messages = [
                    {"role": "system", "content": FRAMEWORK_DEVELOPER_PROMPT}
                ] + messages
                
                response = agent_manager.get_chat_completion(
                    messages=full_messages,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty
                )
            
            # Add assistant response to chat
            assistant_message = {
                "role": "assistant",
                "content": response.choices[0].message.content
            }
            messages.append(assistant_message)
            display_chat_message(assistant_message)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # Add buttons for chat management
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

if __name__ == "__main__":
    main() 