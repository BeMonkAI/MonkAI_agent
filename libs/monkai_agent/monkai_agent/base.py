"""
This module is responsible for providing the core functionality and type definitions for the MonkAI agent. 

It sets up the necessary environment, including logging configuration, importing essential modules, and defining constants and global variables. 

In addition, it imports and uses utility functions and specific types that are essential for the efficient operation of the agent.
"""

import logging
from .types import AgentStatus, Response
from .monkai_agent_creator import MonkaiAgentCreator
from .triage_agent_creator import TriageAgentCreator 
from .memory import Memory
#logging.basicConfig(level=logging.INFO)
#ogger = logging.getLogger(__name__)
import copy
import json
from collections import defaultdict
from typing import List
from openai import OpenAI, APIError, OpenAIError
import time

from typing import Dict, List, Optional, Any, Tuple
import threading
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import tiktoken
from .types import Agent
#from .llm_providers import get_llm_provider
import os
from .rate_limiter import RateLimiter
from typing import Callable
import config
from .prompt_optimizer import PromptOptimizerManager
import asyncio
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


__DOCUMENT_GUARDRAIL_TEXT__ = "RESPONDER SÓ USANDO A INFORMAÇÃO DOS DOCUMENTOS: "

# Local imports
from .util import function_to_json, debug_print, merge_chunk
from .types import (
    Agent,
    AgentFunction,
    ChatCompletionMessage,
    ChatCompletionMessageToolCall,
    Function,
    Response,
    Result,
)

__CTX_VARS_NAME__ = "context_variables"

class ChatCompletionError(Exception):
    """Custom exception for chat completion errors."""
    def __init__(self, message, original_error=None):
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)

from .providers import OpenAIProvider, LLMProvider

class AgentManager:
    """
    Manages the interaction with AI agents.

    This class is responsible for managing the lifecycle of AI agents, handling
    user interactions, processing tool calls, and managing context variables.

    """

    def __init__(self, agents_creators: list[MonkaiAgentCreator]=None, context_variables=None, 
                 current_agent=None, stream=False, debug=False, max_retries: int = 3,  
                 retry_delay: float = 1.0, base_prompt: str=None, model: str = "gpt-3.5-turbo", 
                 provider: LLMProvider = None, rate_limit_rpm: Optional[int] = None, 
                 max_execution_time: Optional[int] = None, context_window_size: Optional[int] = None,
                 freeze_context_window_size: bool = True, api_key: Optional[str] = None, 
                 track_token_usage: bool = True, temperature = None):
        
        self.provider = provider or OpenAIProvider(api_key)
        self.agents_creators = agents_creators
        """
        A list of agent creators to initialize the triage agent.
        """
        self.triage_agent_criator = TriageAgentCreator(agents_creators)
        """
        The creator for the triage agent.
        """
        self.context_variables = context_variables or {}
        """
        Context variables for the agent.
        """
        self.stream = stream
        """
        Flag to enable streaming response.
        """
        self.debug = debug
        """
        Flag to enable debugging.
        """
        self.agent = self.triage_agent_criator.get_agent() if current_agent == None else current_agent
        """
        The current agent instance.
        """
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.temperature = temperature

        self.base_prompt = base_prompt
        self.model = model
        self.max_execution_time = max_execution_time
        self.context_window_size = context_window_size
        self.track_token_usage = track_token_usage
        self.last_token_usage = None
        
        # Set up rate limiting if specified
        self._rate_limiter = None
        if rate_limit_rpm:
            self._rate_limiter = RateLimiter(max_calls=rate_limit_rpm, time_window=60)
            
        if self.track_token_usage:
            self._setup_tokenizer()
            
    def _setup_tokenizer(self):
        """Set up the tokenizer for token counting."""
        try:
            self._tokenizer = tiktoken.encoding_for_model(self.model)
        except KeyError:
            # Fallback to cl100k_base for unknown models
            self._tokenizer = tiktoken.get_encoding("cl100k_base")
            
    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in a text string."""
        if not self.track_token_usage or text is None or isinstance(text, list):
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
                summary_response = self.provider.get_completion(
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

    def _handle_openai_error(self, error: OpenAIError, attempt: int, debug: bool) -> None:
        """
        Handle OpenAI API errors with specific error messages and retry logic.

        Args:
            error: The OpenAI error that occurred
            attempt: Current attempt number
            debug: Flag to enable debugging

        Raises:
            ChatCompletionError: With specific error message based on error type
        """
        error_handlers = {
            'invalid_request_error': "Invalid request: The request was malformed or missing parameters.",
            'invalid_api_key': "Authentication failed: Invalid or expired API key.",
            'authentication_error': "Authentication failed: Please check your credentials.",
            'rate_limit_exceeded': "Rate limit exceeded: Too many requests.",
            'quota_exceeded': "Quota exceeded: Account usage limit reached.",
            'content_filter': "Content filtered: Response blocked by content moderation policy.",
            'context_length_exceeded': "Context length exceeded: Request exceeds model's token limit.",
            'model_not_found': "Model not found: The requested model does not exist.",
            'unsupported_language': "Unsupported language: The model doesn't support the requested language.",
            'bad_request': "Bad request: The request was invalid.",
            'server_error': "Server error: A general server-side failure occurred.",
            'api_error': "API error: An unexpected API failure occurred.",
            'service_unavailable': "Service unavailable: The service is temporarily down."
        }

        error_code = getattr(error, 'code', 'api_error')
        error_msg = error_handlers.get(error_code, f"Unknown error: {str(error)}")
        
        # Determine if error is retryable
        non_retryable = {'invalid_request_error', 'invalid_api_key', 'model_not_found', 
                        'unsupported_language'}
        
        if error_code in non_retryable or attempt >= self.max_retries:
            raise ChatCompletionError(error_msg, error)
        
        debug_print(debug, f"Attempt {attempt} failed with {error_code}. Retrying in {self.retry_delay} seconds...")
        time.sleep(self.retry_delay)

    def get_chat_completion(
        self,
        agent: Agent,
        history: List,
        context_variables: dict,
        max_tokens: float,
        top_p: float,
        frequency_penalty: float,
        presence_penalty: float,        
        stream: bool,
        debug: bool,
    ) -> ChatCompletionMessage:
        """
        Generates a chat completion with retry logic and error handling.

        Args:
            agent (Agent): The agent instance to use for completion
            history (List): Conversation history
            context_variables (dict): Variables for context
            max_tokens (float): Maximum tokens to generate
            top_p (float): Nucleus sampling parameter
            frequency_penalty (float): Frequency penalty parameter
            presence_penalty (float): Presence penalty parameter
            stream (bool): Enable streaming responses
            debug (bool): Enable debug logging

        Returns:
            ChatCompletionMessage: The generated completion

        Raises:
            ChatCompletionError: If the request fails after all retries
        """
        # Merge agent's context variables with passed context variables
        # Agent's context variables are overridden by passed context variables
        merged_context = {**agent.context_variables, **context_variables}
        context_variables = defaultdict(str, merged_context)
        agent.status = AgentStatus.PROCESSING
        instructions = (
            agent.instructions(context_variables)
            if callable(agent.instructions)
            else agent.instructions
        )
        messages = [{"role": "system", "content": instructions}] + history
        debug_print(debug, "Getting chat completion for...:", messages)
        if self.context_window_size:
            # Get default token limit for model
            model_token_limit = DEFAULT_TOKEN_LIMITS.get(self.model, 4096)
            max_context_tokens = min(self.context_window_size, model_token_limit)
            
            # Summarize messages if needed
            messages = self._summarize_messages(messages, max_context_tokens)
        
        tools = [function_to_json(f) for f in agent.functions]
        # hide context_variables from model
        for tool in tools:
            params = tool["function"]["parameters"]
            params["properties"].pop(__CTX_VARS_NAME__, None)
            if __CTX_VARS_NAME__ in params["required"]:
                params["required"].remove(__CTX_VARS_NAME__)

        # Count input tokens
        input_tokens = self.count_message_tokens(messages) if self.track_token_usage else 0
        
        # Apply rate limiting if configured
        if self._rate_limiter:
            self._rate_limiter.acquire()
            
        try:
            # Set up completion parameters with agent info for instrumentation
            create_params = {
                "model": agent.model or self.model,
                "messages": messages,
                "tools": tools or None,
                "tool_choice": agent.tool_choice,
                "stream": stream,
                "agent": agent,  # This will be removed by the wrapper
            }
            if self.temperature:
                create_params["temperature"] = self.temperature
            if max_tokens: 
                create_params["max_tokens"] = max_tokens
            if top_p:
                create_params["top_p"] = top_p
            if frequency_penalty:
                create_params["frequency_penalty"] = frequency_penalty
            if presence_penalty:
                create_params["presence_penalty"] = presence_penalty
            if tools:
                create_params["parallel_tool_calls"] = agent.parallel_tool_calls
                
            # Handle timeout
            if self.max_execution_time:
                response = self._run_with_timeout(
                    lambda: self.provider.get_completion(**create_params),
                    self.max_execution_time
                )
            else:
                attempts = 0
                while True:
                    try:
                        response = self.provider.get_completion(**create_params)
                        break
                    except OpenAIError as e:
                        attempts += 1
                        error_code = getattr(e, 'code', 'api_error')
                        if error_code == "content_filter":
                            promp_otimizer = PromptOptimizerManager(self.client, self.model)
                            instructions = promp_otimizer.analyze_prompt(instructions,context_variables)
                            messages = [{"role": "system", "content": instructions}] + history
                            create_params["messages"] = messages
                        self._handle_openai_error(e, attempts, debug)
                    
                        
                            
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

    def handle_function_result(self, result, debug) -> Result:
        """

        Handles the result of a function call, updating context variables and processing the result.

        Returns:
            PartialResponse: The response after handling the function result.

        """
        
        match result:
            case Result() as result:
                return result

            case Agent() as agent:
                return Result(
                    value=json.dumps({"assistant": agent.name}),
                    agent=agent,
                )
            case _:
                try:
                    return Result(value=str(result))
                except Exception as e:
                    error_message = f"Failed to cast response to string: {result}. Make sure agent functions return a string or Result object. Error: {str(e)}"
                    debug_print(debug, error_message)
                    raise TypeError(error_message)

    def _validate_and_filter_arguments(self, func: Callable, args: dict, name: str, debug: bool) -> tuple[dict, Optional[str]]:
        """
        Validates function arguments and returns a filtered dict of valid arguments.
        
        Args:
            func: The function to validate arguments for
            args: Dictionary of arguments to validate
            name: Function name for error messages
            debug: Flag for debug printing
            
        Returns:
            tuple[dict, Optional[str]]: (filtered arguments dict, error message if any)
        """
        try:
            import inspect
            sig = inspect.signature(func)
            
            # Get required parameters (excluding context_variables)
            required_params = [
                param.name for param in sig.parameters.values()
                if param.default == param.empty 
                and param.name != __CTX_VARS_NAME__
            ]
            
            # Check for missing required arguments
            missing_args = [param for param in required_params if param not in args]
            if missing_args:
                error_msg = f"Missing required arguments for {name}: {', '.join(missing_args)}"
                debug_print(debug, error_msg)
                return {}, error_msg
                
            # Filter to only valid arguments
            valid_params = set(sig.parameters.keys())
            filtered_args = {
                k: v for k, v in args.items() 
                if k in valid_params
            }
            
            # Log unexpected arguments
            unexpected_args = [arg for arg in args if arg not in valid_params]
            if unexpected_args:
                debug_print(debug, f"Warning: Removing unexpected arguments for {name}: {', '.join(unexpected_args)}")
                
            return filtered_args, None
            
        except Exception as e:
            debug_print(debug, f"Failed to validate arguments: {str(e)}")
            return args, None  # Return original args on validation failure

    def handle_tool_calls(
        self,
        tool_calls: List[ChatCompletionMessageToolCall],
        functions: List[AgentFunction],
        context_variables: dict,
        debug: bool,
    ) -> Response:
        """
        Handles tool calls by executing the corresponding functions.

        Args:
            tool_calls (list): List of tool calls to handle.
            functions (list): List of functions that the agent can perform.
            context_variables (dict): Context variables for the agent.
            debug (bool): Flag to enable debugging.

        Returns:
            Response: The response after handling the tool calls.
        """
        
        function_map = {f.__name__: f for f in functions}
        partial_response = Response(
            messages=[], agent=None, context_variables={})

        for tool_call in tool_calls:
            name = tool_call.function.name
            # handle missing tool case, skip to next tool
            if name not in function_map:
                debug_print(debug, f"Tool {name} not found in function map.")
                partial_response.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "tool_name": name,
                        "content": f"Error: Tool {name} not found.",
                    }
                )
                continue
            args = json.loads(tool_call.function.arguments)
            debug_print(
                debug, f"Processing tool call: {name} with arguments {args}")

            func = function_map[name]
            
            # Validate and filter arguments
            filtered_args, error = self._validate_and_filter_arguments(func, args, name, debug)
            if error:
                partial_response.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "tool_name": name,
                    "content": f"Error: {error}"
                })
                continue

            # pass context_variables to agent functions
            if __CTX_VARS_NAME__ in func.__code__.co_varnames:
                filtered_args[__CTX_VARS_NAME__] = context_variables

            raw_result = func(**filtered_args)

            result: Result = self.handle_function_result(raw_result, debug)
            partial_response.messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "tool_name": name,
                    "content": result.value,
                }
            )
            partial_response.context_variables.update(result.context_variables)
            if result.agent:
                partial_response.agent = result.agent

        return partial_response

    def __run_and_stream(
        self,
        agent: Agent,
        messages: Memory | List,
        context_variables: dict = {},
        debug: bool = False,
        max_turns: int = float("inf"),
        execute_tools: bool = True,
        max_tokens: float = None,
        top_p: float = None,
        frequency_penalty: float = None,
        presence_penalty: float = None,
    ):
        active_agent = agent
        context_variables = copy.deepcopy(context_variables)
        
        filtered_messages = messages.filter_memory(agent)
        history = copy.deepcopy(filtered_messages)
        init_len = len(filtered_messages)

        while len(history) - init_len < max_turns and active_agent:

            if active_agent.status == AgentStatus.COMPLETED:
                active_agent.status = AgentStatus.IDLE
                break

            message = {
                "content": "",
                "sender": agent.name,
                "role": "assistant",
                "function_call": None,
                "tool_calls": defaultdict(
                    lambda: {
                        "function": {"arguments": "", "name": ""},
                        "id": "",
                        "type": "",
                    }
                ),
            }

            # get completion with current history, agent
            completion = self.get_chat_completion(
                agent=active_agent,
                history=history,
                context_variables=context_variables,
                stream=True,
                debug=debug,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
            )

            yield {"delim": "start"}
            for chunk in completion:
                delta = json.loads(chunk.choices[0].delta.json())
                if delta["role"] == "assistant":
                    delta["sender"] = active_agent.name
                yield delta
                delta.pop("role", None)
                delta.pop("sender", None)
                merge_chunk(message, delta)
            yield {"delim": "end"}

            message["tool_calls"] = list(
                message.get("tool_calls", {}).values())
            if not message["tool_calls"]:
                message["tool_calls"] = None
            debug_print(debug, "Received completion:", message)
            history.append(message)

            if not message["tool_calls"] or not execute_tools:
                debug_print(debug, "Ending turn.")
                break

            # convert tool_calls to objects
            tool_calls = []
            for tool_call in message["tool_calls"]:
                function = Function(
                    arguments=tool_call["function"]["arguments"],
                    name=tool_call["function"]["name"],
                )
                tool_call_object = ChatCompletionMessageToolCall(
                    id=tool_call["id"], function=function, type=tool_call["type"]
                )
                tool_calls.append(tool_call_object)

            # handle function calls, updating context_variables, and switching agents
            partial_response = self.handle_tool_calls(
                tool_calls, active_agent.functions, context_variables, debug
            )
            history.extend(partial_response.messages)
            context_variables.update(partial_response.context_variables)
            if partial_response.agent:
                active_agent = partial_response.agent

        yield {
            "response": Response(
                messages=history[init_len:],
                agent=active_agent,
                context_variables=context_variables,
            )
        }

    async def __run(
        self,
        agent: Agent,
        messages: Memory | List,
        context_variables: dict = {},
        max_tokens: float = None,
        top_p: float = None,
        frequency_penalty: float = None,
        presence_penalty: float = None,
        stream: bool = False,
        debug: bool = False,
        max_turns: int = float("inf"),
        execute_tools: bool = True,
    ) -> Response:
        if stream:
            return self.__run_and_stream(
                agent=agent,
                messages=messages,
                context_variables=context_variables,
                debug=debug,
                max_turns=max_turns,
                execute_tools=execute_tools,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
            )
        try:
            active_agent = agent
            context_variables = copy.deepcopy(context_variables)
            i = 0
            if isinstance(messages, Memory):
                last_message = messages.get_last_message()
            response_history = []

            while i < max_turns and active_agent:
                try:
                    if active_agent.status == AgentStatus.COMPLETED:
                        active_agent.status = AgentStatus.IDLE
                        break
                    i += 1
                    if isinstance(messages, Memory):
                        history = messages.filter_memory(active_agent)
                    else:
                        history = copy.deepcopy(messages)
                    
                    # Remove 'agent' field from each element in history if it exists
                    for elem in history:
                        if 'agent' in elem:
                            elem.pop('agent')
                            
                    if active_agent.external_content:
                        history[-1]["content"] = __DOCUMENT_GUARDRAIL_TEXT__ + history[-1]["content"]
                    
                    completion = self.get_chat_completion(
                        agent=active_agent,
                        history=history,
                        context_variables=context_variables,
                        max_tokens=max_tokens,
                        top_p=top_p,
                        frequency_penalty=frequency_penalty,
                        presence_penalty=presence_penalty,
                        stream=stream,
                        debug=debug,
                    )

                    message = completion.choices[0].message
                    debug_print(debug, "Received completion:", message)
                    message.sender = active_agent.name
                    messages.append(json.loads(message.model_dump_json()))
                    response_history.append(json.loads(message.model_dump_json()))
                    if not message.tool_calls or not execute_tools:
                        debug_print(debug, "Ending turn.")
                        break

                    partial_response = self.handle_tool_calls(
                        message.tool_calls, active_agent.functions, context_variables, debug
                    )
                    messages.extend(partial_response.messages)
                    response_history.extend(partial_response.messages)
                    context_variables.update(partial_response.context_variables)
                    if partial_response.agent is not None:
                        active_agent = partial_response.agent

                except ChatCompletionError as e:
                    error_message = {
                        "role": "assistant",
                        "content": f"I apologize, but I encountered an error while processing your request: {e.message}",
                        "sender": active_agent.name
                    }
                    messages.append(error_message)
                    response_history.append(error_message)
                    break

            if isinstance(messages, Memory):
                last_message['agent'] = active_agent.name

            return Response(
                messages=response_history,
                agent=active_agent,
                context_variables=context_variables,
            )

        except Exception as e:
            error_message = {
                "role": "assistant",
                "content": f"An unexpected error occurred: {str(e)}",
                "sender": agent.name
            }
            return Response(
                messages=[error_message],
                agent=agent,
                context_variables=context_variables,
            )

    def get_triage_agent(self):
        """
        Returns the triage agent.

        Returns:
            Agent: The triage agent instance.
        """
        return self.triage_agent_criator.get_agent()

    async def run(self,user_message:str, user_history:Memory = None | List, agent=None, 
                  max_tokens=None, top_p=None, frequency_penalty=None, presence_penalty=None,
                    max_turn: int = float("inf") )->Response:

        """
        Executes the main workflow:
            - Handles the conversation with the user.
            - Manages the interaction with the agent.
            - Processes tool calls and updates context variables.

        Returns:
            Response: The response from the agent after processing the user message.
        """
        # Append user's message
        messages=copy.deepcopy(user_history) if user_history is not  None else []
        messages.append({"role": "user", "content": user_message, "agent": None})
        
        #Determined the agent to use
        agent_to_use = agent if agent is not None else self.agent
        # Run the conversation asynchronously
        response:Response = await self.__run(
            agent=agent_to_use,
            messages= messages,
            context_variables=self.context_variables,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stream=self.stream,
            debug=self.debug,
            max_turns=max_turn,
        )
        assert(response is not None)
        return response