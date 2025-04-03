"""
LLM providers module for MonkAI framework.
Supports multiple LLM providers including OpenAI and Groq.
"""

from typing import Optional, Any
from groq import Groq
import os
import json
from monkai_agent import LLMProvider


 # Available Groq models
GROQ_MODELS = [
    'llama-3.3-70b-versatile',
    'deepseek-r1-distill-qwen-32b',
    'gemma2-9b-it',
    'mistral-saba-24b',
    'qwen-2.5-coder-32b'
]       

class GroqProvider(LLMProvider):
    """Groq LLM provider"""
    
    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
    
    def get_client(self):
        return Groq(api_key=self.api_key)
    
    def _format_tools_for_prompt(self, tools):
        """Format tools into a readable prompt format"""
        if not tools:
            return ""
            
        tools_desc = "\nAvailable tools:\n"
        for tool in tools:
            func = tool["function"]
            tools_desc += f"\n- {func['name']}: {func['description']}"
            if "parameters" in func:
                params = func["parameters"].get("properties", {})
                if params:
                    tools_desc += "\n  Parameters:"
                    for param_name, param_info in params.items():
                        tools_desc += f"\n    - {param_name}: {param_info.get('description', 'No description')}"
        
        tools_desc += "\n\nTo use a tool, respond in the following JSON format:\n"
        tools_desc += """
{
    "tool_calls": [
        {
            "type": "function",
            "function": {
                "name": "tool_name",
                "arguments": {
                    "param1": "value1",
                    "param2": "value2"
                }
            }
        }
    ]
}
"""
        return tools_desc
    
    def get_completion(self, messages: list, **kwargs):
        client = self.get_client()
        tools = kwargs.get('tools', None)
        
        # Filter out unsupported parameters
        groq_kwargs = {k: v for k, v in kwargs.items() if k not in [
            'tools', 
            'tool_choice',
            'parallel_tool_calls'
        ]}
        
        # Clean up messages and handle tool messages
        cleaned_messages = []
        for idx, msg in enumerate(messages):
            if idx == 0 and msg['role'] == 'system':
                # Add tools information to system message
                tools_desc = self._format_tools_for_prompt(tools)
                msg['content'] = msg['content'] + "\n" + tools_desc
                
            if msg['role'] == 'tool':
                # Convert tool messages to assistant messages with proper formatting
                cleaned_msg = {
                    'role': 'assistant',
                    'content': f"Tool '{msg.get('tool_name', msg.get('name', 'unknown'))}' response: {msg['content']}"
                }
            else:
                # Handle regular messages
                cleaned_msg = {
                    'role': msg['role'],
                    'content': msg['content']
                }
            cleaned_messages.append(cleaned_msg)
        
        # If there are tools available, append a reminder to use tools format
        if tools and cleaned_messages[-1]['role'] == 'user':
            cleaned_messages[-1]['content'] += "\n\nRemember to use tools when necessary by responding in the specified JSON format."
            
        response = client.chat.completions.create(
            messages=cleaned_messages,
            **groq_kwargs
        )
        
        # Try to parse the response content as JSON if it looks like a tool call
        content = response.choices[0].message.content
        if content.strip().startswith('{') and 'tool_calls' in content:
            try:
                tool_data = json.loads(content)
                if 'tool_calls' in tool_data:
                    response.choices[0].message.tool_calls = tool_data['tool_calls']
                    response.choices[0].message.content = ""
            except json.JSONDecodeError:
                pass
                
        return response


