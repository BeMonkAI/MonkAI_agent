"""
This module establishes the main structure for creating agent instances within the MonkAI framework. 

It provides an abstract class, 'MonkaiAgentCreator', which serves as a blueprint for developing various types of agents, ensuring that all subclasses implement the essential methods for agent creation and description. Additionally, it includes concrete classes for different types of agents, including a prompt testing and optimization agent.

"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Tuple
import time
import threading
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from openai import OpenAI
import tiktoken
from .types import Agent
from .agent import BaseAgent
from .llm_providers import get_llm_provider
import os
from .rate_limiter import RateLimiter
from typing import Callable

# Default token limits for different models
DEFAULT_TOKEN_LIMITS = {
    "gpt-4": 8192,
    "gpt-4o": 8192,
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-16k": 16384,
    "claude-2": 100000,
    "mixtral-8x7b": 32768
}

class TokenUsage:
    """Class to track token usage for input and output."""
    
    def __init__(self, input_tokens: int = 0, output_tokens: int = 0):
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        
    def __str__(self) -> str:
        return f"Input tokens: {self.input_tokens}, Output tokens: {self.output_tokens}"

class MonkaiAgentCreator(ABC):
    """
    Abstract class for creating agent instances.

    This class provides a blueprint for creating different types of agents
    based on the system's needs. It includes methods to create an agent
    instance and to provide a brief description of the agent's capabilities.

    """
    def __init__(self):
        self._predecessor_agent = None

    @abstractmethod
    def get_agent(self)->Agent:
        """
        Creates and returns an instance of an agent.

        """
        pass

    @abstractmethod
    def get_agent_briefing(self)->str:
        """
        Returns a brief description of the agent's capabilities.

        """
        pass

    @property
    def agent_name(self) -> str:
        agent = self.get_agent()
        if agent is None:
            return None
        return agent.name

    @property
    def predecessor_agent(self) -> Agent:
        return self._predecessor_agent

    @predecessor_agent.setter
    def predecessor_agent(self, agent: Agent):
        self._predecessor_agent = agent


class TransferTriageAgentCreator(MonkaiAgentCreator):
    """
    A class to create and manage a triage agent.

    """

    triage_agent = None
    """
    The triage agent instance.
    
    """
    def __init__(self):
        super().__init__()

   # @property.setter
    def set_triage_agent(self, triage_agent: Agent):
        """
        Sets the triage agent.

        Args:
            triage_agent (Agent): The triage agent to be set.
        """
        self.triage_agent = triage_agent

    def transfer_to_triage(self):
        """
        Transfers the conversation to the  triage agent.

        Args:
            agent (Agent): The agent to transfer the conversation to.
        """
        return self.triage_agent


class PromptTestingAgentCreator(MonkaiAgentCreator):
    """
    A class to create and manage agents for prompt testing and optimization.
    Supports multiple system prompts and AI-enhanced prompt generation.
    """
    def __init__(self, 
                 client: OpenAI,
                 base_prompt: str,
                 additional_prompts: Optional[Dict[str, str]] = None,
                 enable_ai_prompt_generation: bool = False,
                 model: str = "gpt-4"):
        """
        Initialize the PromptTestingAgentCreator.

        Args:
            client (OpenAI): The OpenAI client instance
            base_prompt (str): The default system prompt
            additional_prompts (Dict[str, str], optional): Additional prompts to test
            enable_ai_prompt_generation (bool): Whether to enable AI prompt generation
            model (str): The model to use for the agent
        """
        super().__init__()
        self.client = client
        self.base_prompt = base_prompt
        self.additional_prompts = additional_prompts or {}
        self.enable_ai_prompt_generation = enable_ai_prompt_generation
        self.model = model
        self._current_prompt_name = "Base Prompt"
        self._current_prompt = base_prompt
        self._ai_enhanced_prompt = None

    async def generate_enhanced_prompt(self) -> str:
        """
        Generate an AI-enhanced prompt by analyzing existing prompts.
        
        Returns:
            str: The generated enhanced prompt
        """
        all_prompts = {"Base Prompt": self.base_prompt, **self.additional_prompts}
        prompt_analysis = "\n".join([
            f"Prompt {i+1}:\n{prompt}\n"
            for i, prompt in enumerate(all_prompts.values())
        ])
        
        messages = [
            {"role": "system", "content": "You are an expert in prompt engineering and optimization."},
            {"role": "user", "content": f"""Analyze these prompts and create an enhanced version that combines their strengths:
            
{prompt_analysis}

Create a new prompt that:
1. Synthesizes the best aspects of all prompts
2. Adds improvements and optimizations
3. Maintains clarity and structure
4. Is more comprehensive and effective

Format the response as a complete system prompt."""}
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content

    def set_current_prompt(self, prompt_name: str):
        """
        Set the current prompt to use for the agent.

        Args:
            prompt_name (str): Name of the prompt to use
        """
        if prompt_name == "Base Prompt":
            self._current_prompt = self.base_prompt
        elif prompt_name == "AI-Enhanced Expert" and self._ai_enhanced_prompt:
            self._current_prompt = self._ai_enhanced_prompt
        elif prompt_name in self.additional_prompts:
            self._current_prompt = self.additional_prompts[prompt_name]
        else:
            raise ValueError(f"Unknown prompt name: {prompt_name}")
        
        self._current_prompt_name = prompt_name

    def get_agent(self) -> Agent:
        """
        Creates and returns an agent instance with the current prompt.

        Returns:
            Agent: The created agent instance
        """
        return Agent(
            name=f"TestAgent_{self._current_prompt_name}",
            instructions=self._current_prompt,
            model=self.model
        )

    def get_agent_briefing(self) -> str:
        """
        Returns a brief description of the agent's capabilities.

        Returns:
            str: Description of the agent's capabilities
        """
        return f"Agent using {self._current_prompt_name} for prompt testing and optimization"

    async def initialize(self):
        """
        Initialize the agent creator, including AI prompt generation if enabled.
        """
        if self.enable_ai_prompt_generation:
            print("\nGenerating AI-enhanced prompt...")
            self._ai_enhanced_prompt = await self.generate_enhanced_prompt()
            print("AI-enhanced prompt generated successfully!")

    @property
    def available_prompts(self) -> List[str]:
        """
        Get list of available prompt names.

        Returns:
            List[str]: List of available prompt names
        """
        prompts = ["Base Prompt"] + list(self.additional_prompts.keys())
        if self.enable_ai_prompt_generation and self._ai_enhanced_prompt:
            prompts.append("AI-Enhanced Expert")
        return prompts

class MonkaiAgentCreator:
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
        self.provider = provider
        self.max_execution_time = max_execution_time
        self.context_window_size = context_window_size
        self.freeze_context_window_size = freeze_context_window_size
        self.api_key = api_key or os.getenv(f"{provider.upper()}_API_KEY")
        self.track_token_usage = track_token_usage
        self.last_token_usage = None
        
        # Set up rate limiting if specified
        self._rate_limiter = None
        if rate_limit_rpm:
            self._rate_limiter = RateLimiter(max_calls=rate_limit_rpm, time_window=60)
            
        # Initialize the client and tokenizer
        self._setup_client()
        if self.track_token_usage:
            self._setup_tokenizer()
            
    def _setup_client(self):
        """Set up the API client based on the provider."""
        from .llm_providers import get_llm_provider
        self._client = get_llm_provider(
            provider=self.provider,
            api_key=self.api_key,
            model=self.model
        ).get_client()
            
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
                summary_response = self._client.chat.completions.create(
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
                
            # Get the provider instance
            from .llm_providers import get_llm_provider
            provider = get_llm_provider(
                provider=self.provider,
                api_key=self.api_key,
                model=self.model
            )
                
            # Handle timeout
            if self.max_execution_time:
                response = self._run_with_timeout(
                    lambda: provider.get_chat_completion(**completion_params),
                    self.max_execution_time
                )
            else:
                response = provider.get_chat_completion(**completion_params)
                
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