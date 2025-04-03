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
    
    def _clean_messages(self, messages: list) -> list:
        """Clean messages to ensure compatibility with Groq API."""
        cleaned_messages = []
        for msg in messages:
            cleaned_msg = {
                "role": msg["role"],
                "content": msg.get("content", "")
            }
            
            # Handle tool messages  
            if msg["role"] == "tool":
                if "tool_call_id" not in msg:
                    continue  # Skip tool messages without tool_call_id
                cleaned_msg["tool_call_id"] = msg["tool_call_id"]
            
            # Handle function calls for assistant messages
            elif msg["role"] == "assistant" and "function_call" in msg and msg["function_call"]:
                cleaned_msg["function_call"] = msg["function_call"]
            
            cleaned_messages.append(cleaned_msg)
        return cleaned_messages
    
    def get_completion(self, messages: list, **kwargs):
        client = self.get_client()
        
        # Clean and format messages
        formatted_messages = self._clean_messages(messages)
            
        if "tool_choice" not in kwargs or kwargs["tool_choice"] not in ["none", "auto", "required"]:
            kwargs["tool_choice"] = "auto" if "tools" in kwargs and kwargs["tools"] else "none"
            
        response = client.chat.completions.create(
            messages=formatted_messages,
            **kwargs
        )
        return response


