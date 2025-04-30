import os
from typing import Any, Callable, Dict, List, Optional

import tiktoken

from monkai_agent.base import DEFAULT_TOKEN_LIMITS
from monkai_agent.rate_limiter import RateLimiter
from monkai_agent.base import TokenUsage


class MonkaiUIAgent:
    """Base class for creating different types of agents."""
    
    def __init__(
        self,
        base_prompt: str,
        model: str = "gpt-3.5-turbo",
        provider: str = "openai",
        rate_limit_rpm: Optional[int] = None,
        max_execution_time: Optional[int] = 30,
        context_window_size: Optional[int] = None,
        freeze_context_window_size: bool = True,
        api_key: Optional[str] = None,
        track_token_usage: bool = True
    ):
        """
        Initialize the MonkaiAgentCreator.
        
        Args:
            base_prompt: The base prompt for the agent
            model: The model to use (default: gpt-3.5-turbo)
            provider: The provider to use (default: openai)
            rate_limit_rpm: Rate limit in requests per minute (optional)
            max_execution_time: Maximum execution time in seconds (optional)
            context_window_size: Maximum context window size in tokens (optional)
            freeze_context_window_size: Whether to freeze context window size (default: True)
            api_key: API key for the provider (optional)
            track_token_usage: Whether to track token usage (default: True)
        """
        self.base_prompt = base_prompt
        self.model = model
        self.max_execution_time = max_execution_time
        self.context_window_size = context_window_size
        self.freeze_context_window_size = freeze_context_window_size
        self.api_key = api_key or os.getenv(f"{provider.upper()}_API_KEY")
        self.track_token_usage = track_token_usage
        self.last_token_usage = None
        self.__setup_client(provider)
        # Set up rate limiting  if specified
        self._rate_limiter = None
        if rate_limit_rpm:
            self._rate_limiter = RateLimiter(max_calls=rate_limit_rpm, time_window=60)
            
        # Initialize the client and tokenizer
        if self.track_token_usage:
            self._setup_tokenizer()
            
    def __setup_client(self, provider: str):
        """Set up the API client based on the provider."""
        if provider == "openai":
            from monkai_agent.providers import OpenAIProvider
            self.__provider = OpenAIProvider(api_key=self.api_key)
        elif provider == "groq" :
            from monkai_agent.groq import GroqProvider
            self.__provider = GroqProvider(api_key=self.api_key)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
            
            
    def _setup_tokenizer(self):
        """Set up the tokenizer for token counting."""
        try:
            self._tokenizer = tiktoken.encoding_for_model(self.model)
        except KeyError:
            # Fallback to cl100k_base for unknown models
            self._tokenizer = tiktoken.get_encoding("cl100k_base")
            
    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in a text string."""
        if not self.track_token_usage:
            return 0
        return len(self._tokenizer.encode(text))
        
    def count_message_tokens(self, messages: List[Dict[str, str]]) -> int:
        """Count the total number of tokens in a list of messages."""
        if not self.track_token_usage:
            return 0
            
        total_tokens = 0
        for message in messages:
            # Add tokens for message format
            total_tokens += 4  # Every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                total_tokens += self.count_tokens(value)
                if key == "name":  # If there's a name, the role is omitted
                    total_tokens -= 1  # Role is omitted
        total_tokens += 2  # Every reply is primed with <im_start>assistant
        return total_tokens
        
    def _summarize_messages(self, messages: List[Dict[str, str]], max_tokens: int) -> List[Dict[str, str]]:
        """
        Summarize conversation history to fit within context window.
        
        Args:
            messages: List of conversation messages
            max_tokens: Maximum number of tokens to target
            
        Returns:
            List of summarized messages
        """
        if not messages:
            return messages
            
        # Keep system message as is
        system_message = next((m for m in messages if m["role"] == "system"), None)
        if system_message:
            messages = [m for m in messages if m["role"] != "system"]
        
        # If we have too many messages, summarize the older ones
        if len(messages) > 4:  # Keep last 2 exchanges (4 messages) as is
            summary_request = [
                {"role": "system", "content": "You are a conversation summarizer. Create a concise summary of the conversation while preserving key information."},
                {"role": "user", "content": f"Summarize this conversation, preserving key details:\n\n" + "\n".join([f"{m['role']}: {m['content']}" for m in messages[:-4]])}
            ]
            
            try:
                summary_response = self.__provider.get_completion(
                    messages=summary_request,
                    model=self.model,
                    max_tokens=max_tokens // 4  # Use at most 1/4 of max tokens for summary
                )
                summary = summary_response.choices[0].message.content
                
                # Replace old messages with summary
                summarized_messages = [{"role": "system", "content": f"Previous conversation summary: {summary}"}]
                summarized_messages.extend(messages[-4:])  # Add last 4 messages
                
                if system_message:
                    summarized_messages.insert(0, system_message)
                    
                return summarized_messages
                
            except Exception as e:
                print(f"Warning: Failed to summarize messages: {str(e)}")
                return messages  # Return original messages if summarization fails
                
        return messages if not system_message else [system_message] + messages
        
    def get_chat_completion(self, messages: List[Dict[str, str]], max_tokens: Optional[int] = None, stream: bool = False) -> Any:
        """
        Get a chat completion from the model.
        
        Args:
            messages: List of conversation messages
            max_tokens: Maximum number of tokens to generate
            stream: Whether to stream the response
            
        Returns:
            Chat completion response
            
        The token usage information can be accessed through the last_token_usage property
        after the completion is received.
        """
        if self.freeze_context_window_size and self.context_window_size:
            # Get default token limit for model
            model_token_limit = DEFAULT_TOKEN_LIMITS.get(self.model, 4096)
            max_context_tokens = min(self.context_window_size, model_token_limit)
            
            # Summarize messages if needed
            messages = self._summarize_messages(messages, max_context_tokens)
        
        # Count input tokens
        input_tokens = self.count_message_tokens(messages) if self.track_token_usage else 0
        
        # Apply rate limiting if configured
        if self._rate_limiter:
            self._rate_limiter.acquire()
            
        try:
            # Set up completion parameters
            completion_params = {
                "messages": messages,
                "model": self.model,
                "stream": stream
            }
            if max_tokens:
                completion_params["max_tokens"] = max_tokens
                
        
            # Handle timeout
            if self.max_execution_time:
                response = self._run_with_timeout(
                    lambda: self.__provider.get_completion(**completion_params),
                    self.max_execution_time
                )
            else:
                response = self.__provider.get_completion(**completion_params)
                
            # Track token usage
            if self.track_token_usage and hasattr(response, 'usage'):
                self.last_token_usage = TokenUsage(
                    input_tokens=response.usage.prompt_tokens,
                    output_tokens=response.usage.completion_tokens
                )
            elif self.track_token_usage:
                # If response doesn't have usage info, estimate output tokens
                output_tokens = self.count_tokens(response.choices[0].message.content)
                self.last_token_usage = TokenUsage(input_tokens=input_tokens, output_tokens=output_tokens)
                
            return response
                
        finally:
            # Release rate limit token
            if self._rate_limiter:
                self._rate_limiter.release()
                
    def get_token_usage(self) -> Optional[TokenUsage]:
        """Get the token usage from the last request."""
        return self.last_token_usage

    def _run_with_timeout(self, func: Callable, timeout: int) -> Any:
        """
        Run a function with a timeout.
        
        Args:
            func: Function to run
            timeout: Timeout in seconds
            
        Returns:
            Function result
            
        Raises:
            TimeoutError: If the function execution exceeds the timeout
        """
        import threading
        import queue
        
        result_queue = queue.Queue()
        
        def worker():
            try:
                result = func()
                result_queue.put(("success", result))
            except Exception as e:
                result_queue.put(("error", e))
                
        thread = threading.Thread(target=worker)
        thread.daemon = True
        thread.start()
        
        try:
            status, result = result_queue.get(timeout=timeout)
            if status == "error":
                raise result
            return result
        except queue.Empty:
            raise TimeoutError(f"Task execution exceeded maximum allowed time of {timeout} seconds")