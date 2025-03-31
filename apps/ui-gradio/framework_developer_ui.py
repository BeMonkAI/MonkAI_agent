"""
Gradio UI for the MonkAI Framework Developer Agent.
This interface helps users understand and develop code for the MonkAI framework.
"""

import gradio as gr
import os
from openai import AzureOpenAI, OpenAI
from monkai_agent import AgentManager
from monkai_agent.monkai_agent_creator import PromptTestingAgentCreator
import json
from typing import List, Tuple
import config

# Initialize OpenAI client
client = client=AzureOpenAI(
            api_key=config.OPENAI_API_KEY_BRASILSOUTH,
            api_version=config.GPT4o_OPENAI_API_VERSION_BRASILSOUTH,
            azure_endpoint=config.OPENAI_AZURE_ENDPOINT_BRASILSOUTH,
        )

# Define the framework developer prompt with MonkAI-specific knowledge
framework_developer_prompt = """You are a specialized AI framework developer for the MonkAI framework.
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

# Create the agent creator
agent_creator = PromptTestingAgentCreator(
    client=client,
    base_prompt=framework_developer_prompt,
    model="gpt-4"
)

# Create agent manager
agent_manager = AgentManager(client=client, agents_creators=[agent_creator], model = config.GPT4o_OPENAI_GPT_MODEL_BRASILSOUTH)

def format_response(result: str) -> str:
    """Format the response with proper markdown."""
    try:
        # Try to parse as JSON for code generation
        result_dict = json.loads(result)
        return f"""
### Generated Code
```python
{result_dict['code']}
```

### Dependencies
```bash
pip install {' '.join(result_dict['dependencies'])}
```

### Usage Example
```python
{result_dict['usage_example']}
```

### Notes
{result_dict['notes']}
"""
    except json.JSONDecodeError:
        # If not JSON, format as regular documentation
        return f"""
### Response
{result}
"""

async def chat(message: str, history: List[Tuple[str, str]]) -> Tuple[str, List[Tuple[str, str]]]:
    """
    Handle chat messages and generate responses.
    
    Args:
        message: The user's message
        history: The chat history
        
    Returns:
        Tuple of (response, updated history)
    """
    try:
        # Get the agent
        agent = agent_creator.get_agent()
        agent_manager.agent = agent
        
        # Run the query
        messages = [{"role": "user", "content": message}]
        response = agent_manager.get_chat_completion(
            agent=agent,
            history=messages,
            context_variables={},
            model_override=None,
            temperature=0.7,
            max_tokens=2000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stream=False,
            debug=False
        )
        
        # Format the response
        result = response.choices[0].message.content
        formatted_response = format_response(result)
        
        # Update history
        history.append((message, formatted_response))
        
        return "", history
        
    except Exception as e:
        error_message = f"Error: {str(e)}"
        history.append((message, error_message))
        return "", history

# Create the Gradio interface
with gr.Blocks(css="""
    .contain { display: flex; flex-direction: column; }
    .message { padding: 10px; margin: 5px; border-radius: 10px; }
    .user { background-color: #A77045; color: white; margin-left: 20%; }
    .assistant { background-color: #f5f5f5; margin-right: 20%; }
    .code-block { background-color: #f8f9fa; padding: 10px; border-radius: 5px; }
    .markdown { font-family: monospace; }
    .header { display: flex; justify-content: center; align-items: center; padding: 10px; }
    .title { color: #A77045; }
    .send-button { background-color: rgb(167, 112, 69) !important; color: white !important; }
    .send-button:hover { background-color: rgb(147, 92, 49) !important; }
""") as demo:
    with gr.Row(elem_classes="header"):
        gr.Markdown("""
        # MonkAI Framework Developer Assistant
        """, elem_classes="title")
    
    gr.Markdown("""
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
    
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        bubble_full_width=False,
        avatar_images=(None, "https://api.dicebear.com/7.x/bottts/svg?seed=monkai"),
        height=600,
        show_label=False
    )
    
    with gr.Row():
        txt = gr.Textbox(
            show_label=False,
            placeholder="Ask about MonkAI framework development...",
            container=False
        )
        submit_btn = gr.Button("Send", elem_classes="send-button")
    
    # Handle user input
    txt.submit(chat, [txt, chatbot], [txt, chatbot])
    submit_btn.click(chat, [txt, chatbot], [txt, chatbot])
    
    # Add clear button
    clear_btn = gr.Button("Clear Chat")
    clear_btn.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch() 