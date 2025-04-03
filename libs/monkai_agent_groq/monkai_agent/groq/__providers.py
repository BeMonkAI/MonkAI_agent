"""
LLM providers module for MonkAI framework.
Supports multiple LLM providers including OpenAI and Groq.
"""

from typing import Optional, Any
from groq import Groq
import os
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
    
    def get_completion(self, messages: list, **kwargs):
        client = self.get_client()
        
        # Filter out unsupported parameters
        groq_kwargs = {k: v for k, v in kwargs.items() if k not in [
            'tools', 
            'tool_choice',
            'parallel_tool_calls'
        ]}
        
        # Clean up messages and handle tool messages
        cleaned_messages = []
        for msg in messages:
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
            
        return client.chat.completions.create(
            messages=cleaned_messages,
            **groq_kwargs
        )


