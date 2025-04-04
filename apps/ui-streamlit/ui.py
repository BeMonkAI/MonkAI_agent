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
from monkai_agent.groq import GROQ_MODELS
from openai import OpenAI
from mokai_ui_agent import MonkaiUIAgent

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

Agent monkai framework example 1:
 
   
            "from monkai_agent import  TransferTriageAgentCreator
            from monkai_agent import Agent
            import monkai_agent.src.security as security
            import os

            class PythonDeveloperAgentCreator(TransferTriageAgentCreator):
                def __init__(self, user):
                    super().__init__()
                    self.user = user
                    self.agent = Agent(
                        name="Python Developer Agent",
                    instructions'''You are a Python developer and you have to create Python code from text provided by the user.


                            1. Interpret the user's text to understand the requirements of the Python code to be generated.
                            2. Generate the Python code, defining classes as necessary and following good object-oriented practices. Ensure that the generated code is properly documented.
                            3. Check if there is an address provided by the user in the message. If no address is provided, use the current folder.
                            4. Create a .py file in the specified folder.
                            5. Define a class in the created file with the functionality that meets the conditions specified by the user.
                            6. If you cannot provide an answer, trigger the transfer_to_triage function to escalate the request to the triage agent.
                        ''',
                        functions=[  
                                    self.verify_address,    
                                    self.create_python_file,
                                    self.write_code_in_file,
                                    self.transfer_to_triage
                                ])
                    
                def is_user_valid(self):
                    if self.user=="valid_user":
                        return True
                    else:
                        return False
                
                
                def verify_address(self, address):
                    if not address:
                        return os.getcwd()
                    if not os.path.isdir(address):
                        return f"Endereço {address} não é valido."
                    return address

                @security.validate(is_user_valid)
                def create_python_file(self, path, file_name):
                    complete_path = os.path.join(path, file_name)
                    with open(complete_path, 'w') as f:
                        f.write('')
                
                
                @security.validate(is_user_valid)
                def write_code_in_file(self,path, file_name, code):
                '''
                    Write the code in the file.
                ''' 
                    complete_path = os.path.join(path, file_name)
                    with open(complete_path, 'w') as f:
                        f.write(code)

                def replace_code_in_file(self, path, file_name, code):
                '''
                    Replace the code in the file.
                    '''
                    complete_path = os.path.join(path, file_name)
                    with open(complete_path, 'w') as f:
                        f.write(code)

                def get_agent(self) -> Agent:
                '''
                    Returns the Python Developer Agent.

                    Args:
                        None
                    Returns:
                        Agent: The Python Developer Agent instance.
                    '''
                    return self.agent
                
                def get_agent_briefing(self) -> str:
                    return "You are a Python developer and you have to create Python code from text provided by the user."
                
Agent monkai framework example 2:

    from monkai_agent import TransferTriageAgentCreator, Agent
    import os
    import requests

    class JornalistAgentCreator(TransferTriageAgentCreator):

        def __init__(self):
            super().__init__()
            self.__jornalist_agent = Agent(name="Jornalist Agent",
            instructions='''You are an agent in charge of summarizing the day's news read in specific newspapers.
                    If you cannot provide an answer, trigger the transfer_to_triage function to escalate the request to the triage agent.
                    ''',
                functions=[  
                            self.read_news,
                            self.transfer_to_triage
                        ])
            
        def get_agent(self):
            '''
            Returns the Jornalist Agent.
            '''
            return self.__jornalist_agent
        
        def get_agent_briefing(self):
            return "You are an agent in charge of summarizing the day's news read in specific newspapers."
        
        def read_news(self):
            '''
            Read the news.
            '''
            try:
                news = requests.get("https://g1.globo.com/").text
                return f"The news to summarize are: {news[:120000]}"
            except requests.exceptions.ConnectionError as e:
                return f"Failed to retrieve news: {str(e)}"
        
        
"""



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
            api_key = st.session_state.api_key
            os.environ[f"{provider.upper()}_API_KEY"] = api_key
            agent_creator = MonkaiUIAgent(
                        base_prompt=FRAMEWORK_DEVELOPER_PROMPT,
                        model=model,
                        provider=provider,
                        api_key=api_key,
                       
                    )

            with st.spinner("Thinking..."):
                # Add system message with instructions
                full_messages = [
                    {"role": "system", "content": FRAMEWORK_DEVELOPER_PROMPT}
                ] + messages
                
                response = agent_creator.get_chat_completion(
                    messages=full_messages,
                    max_tokens=max_tokens
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