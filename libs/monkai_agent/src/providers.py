from openai import OpenAI, AzureOpenAI


class LLMProvider:
    """Base class for LLM providers"""
    
    
    def get_client(self):
        """Get the LLM client"""
        raise NotImplementedError
    
    def get_completion(self, messages: list, **kwargs):
        """Get chat completion from the LLM"""
        raise NotImplementedError

class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider"""
    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
    
    def get_client(self):
        return OpenAI(api_key=self.api_key)
    
    def get_completion(self, messages: list, **kwargs):
        client = self.get_client()
        return client.chat.completions.create(
            messages=messages,
            **kwargs
        )
    

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
