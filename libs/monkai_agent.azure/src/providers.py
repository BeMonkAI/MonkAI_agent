"""
LLM providers module for MonkAI framework.
Supports Azure OpenAI Service integration.
"""

from typing import Optional, Any
from openai import AzureOpenAI
import os
from monkai_agent.providers import LLMProvider

# Available Azure OpenAI models
AZURE_MODELS = [
    'gpt-4',
    'gpt-4-turbo',
    'gpt-35-turbo',
    'gpt-35-turbo-16k',
    'gpt-4o'
]

class AzureProvider(LLMProvider):
    """Azure OpenAI Service provider"""
    
    def __init__(self, api_key: str, endpoint: str, api_version: str = "2024-02-15-preview"):
        super().__init__()
        self.api_key = api_key
        self.endpoint = endpoint
        self.api_version = api_version
    
    def get_client(self):
        return AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.endpoint
        )
    
    def get_completion(self, messages: list, **kwargs):
        client = self.get_client()
        return client.chat.completions.create(messages=messages, **kwargs)
