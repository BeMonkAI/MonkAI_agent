from openai import OpenAI


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