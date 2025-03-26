"""
LLM providers module for MonkAI framework.
Supports multiple LLM providers including OpenAI and Groq.
"""
'''
from typing import Optional, Dict, Any
from openai import OpenAI
from groq import Groq
import os

class LLMProvider:
    """Base class for LLM providers"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def get_client(self):
        """Get the LLM client"""
        raise NotImplementedError
    
    def get_chat_completion(self, messages: list, **kwargs):
        """Get chat completion from the LLM"""
        raise NotImplementedError

class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider"""
    
    def get_client(self):
        return OpenAI(api_key=self.api_key)
    
    def get_chat_completion(self, messages: list, **kwargs):
        client = self.get_client()
        return client.chat.completions.create(
            messages=messages,
            **kwargs
        )

class GroqProvider(LLMProvider):
    """Groq LLM provider"""
    
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        super().__init__(api_key)
        self.model = model
    
    def get_client(self):
        return Groq(api_key=self.api_key)
    
    def get_chat_completion(self, messages: list, **kwargs):
        client = self.get_client()
        # Map OpenAI parameters to Groq parameters
        groq_params = {
            "messages": messages,
            "model": self.model,
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 2000),
            "top_p": kwargs.get("top_p", 1.0),
            "frequency_penalty": kwargs.get("frequency_penalty", 0.0),
            "presence_penalty": kwargs.get("presence_penalty", 0.0),
            "stream": kwargs.get("stream", False)
        }
        return client.chat.completions.create(**groq_params)

# Available Groq models
GROQ_MODELS = [
    'llama-3.3-70b-versatile',
    'deepseek-r1-distill-qwen-32b',
    'gemma2-9b-it',
    'mistral-saba-24b',
    'qwen-2.5-coder-32b'
]

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
        raise ValueError(f"Unknown provider: {provider}") '
        ''''