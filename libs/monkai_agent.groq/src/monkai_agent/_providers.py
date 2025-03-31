"""
LLM providers module for MonkAI framework.
Supports multiple LLM providers including OpenAI and Groq.
"""

from typing import Optional, Any
from groq import Groq
import os
from monkai_agent.providers import LLMProvider


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
        return client.chat.completions.create(messages=messages, **kwargs)


