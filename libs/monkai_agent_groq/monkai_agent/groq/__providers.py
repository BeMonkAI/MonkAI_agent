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
    
    def _clean_messages(self, messages: list) -> list:
        """Clean messages to ensure compatibility with Groq API."""
        cleaned_messages = []
        for msg in messages:
            # Only keep supported fields
            cleaned_msg = {
                "role": msg["role"],
                "content": msg.get("content", "")
            }
            # Handle function calls only for assistant messages
            if msg["role"] == "assistant" and "function_call" in msg and msg["function_call"]:
                cleaned_msg["function_call"] = msg["function_call"]
            cleaned_messages.append(cleaned_msg)
        return cleaned_messages
    
    def get_completion(self, messages: list, **kwargs):
        client = self.get_client()
        
        # Clean and format messages
        formatted_messages = self._clean_messages(messages)
            
        if "tool_choice" not in kwargs or kwargs["tool_choice"] not in ["none", "auto", "required"]:
            kwargs["tool_choice"] = "required" if "tools" in kwargs and kwargs["tools"] else "none"
            
        response = client.chat.completions.create(
            messages=formatted_messages,
            **kwargs
        )
        return response


