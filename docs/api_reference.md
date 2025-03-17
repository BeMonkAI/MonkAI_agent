# MonkAI Framework Documentation

## Overview
MonkAI is an AI agent framework that manages interactions between users and AI agents, handling conversations, tool calls, and context management. The framework is designed to be flexible and extensible, supporting multiple agents and complex interactions.

## Core Classes

### AgentManager
The main class responsible for managing AI agent interactions and lifecycle.

#### Constructor Parameters
- `client` (OpenAI, optional): OpenAI client instance. If not provided, creates a new one.
- `agents_creators` (list[MonkaiAgentCreator]): List of agent creators for initializing agents.
- `context_variables` (dict, optional): Variables to maintain context across interactions.
- `current_agent` (Agent, optional): The currently active agent instance.
- `stream` (bool, optional): Enable streaming responses. Defaults to False.
- `debug` (bool, optional): Enable debug mode. Defaults to False.

#### Key Methods

##### `run(user_message: str, user_history: Memory | List, agent=None, model_override="gpt-4o", temperature=None, max_tokens=None, top_p=None, frequency_penalty=None, presence_penalty=None, max_turn: int = float("inf")) -> Response`
Main method to execute the conversation workflow.

Parameters:
- `user_message`: The message from the user
- `user_history`: Conversation history (Memory object or List)
- `agent`: Specific agent to use (optional)
- `model_override`: Override default model
- `temperature`: Model temperature parameter
- `max_tokens`: Maximum tokens for response
- `top_p`: Top-p sampling parameter
- `frequency_penalty`: Frequency penalty parameter
- `presence_penalty`: Presence penalty parameter
- `max_turn`: Maximum number of conversation turns

##### `get_chat_completion(agent, history, context_variables, model_override, temperature, max_tokens, top_p, frequency_penalty, presence_penalty, stream, debug) -> ChatCompletionMessage`
Generates chat completions based on the conversation history.

##### `handle_tool_calls(tool_calls, functions, context_variables, debug) -> Response`
Processes tool calls and executes corresponding functions.

##### `handle_function_result(result, debug) -> Result`
Handles the results of function calls and updates context.

## Data Types

### Response
Represents the response from an agent interaction.

Properties:
- `messages`: List of conversation messages
- `agent`: The agent that generated the response
- `context_variables`: Updated context variables

### Result
Represents the result of a function call.

Properties:
- `value`: The result value
- `agent`: Associated agent (if any)
- `context_variables`: Updated context variables

### Agent
Base interface for AI agents.

Properties:
- `name`: Agent identifier
- `model`: AI model to use
- `instructions`: Agent instructions/prompt
- `functions`: Available functions
- `tool_choice`: Tool selection strategy
- `parallel_tool_calls`: Number of parallel tool calls allowed
- `external_content`: Flag for external content usage

### Memory
Manages conversation history and memory filtering.

Methods:
- `filter_memory()`: Filters conversation history based on agent
- `append()`: Adds new messages to history
- `extend()`: Extends history with multiple messages
- `get_last_message()`: Retrieves the most recent message

## Constants and Special Variables

- `__DOCUMENT_GUARDRAIL_TEXT__`: Prefix for document-based responses
- `__CTX_VARS_NAME__`: Name for context variables in function calls

## Creator Classes

### MonkaiAgentCreator
Base class for creating and configuring MonkAI agents. This class provides the foundation for creating different types of agents with customizable parameters and functionality.

#### Constructor Parameters
- `base_prompt` (str): The base prompt/instructions for the agent
- `model` (str, optional): The model to use. Defaults to "gpt-3.5-turbo"
- `provider` (str, optional): The LLM provider to use. Defaults to "openai"
- `rate_limit_rpm` (int, optional): Rate limit in requests per minute
- `max_execution_time` (int, optional): Maximum execution time in seconds. Defaults to 30
- `context_window_size` (int, optional): Maximum context window size in tokens
- `freeze_context_window_size` (bool, optional): Whether to freeze context window size. Defaults to True
- `api_key` (str, optional): API key for the provider
- `track_token_usage` (bool, optional): Whether to track token usage. Defaults to True

#### Key Methods

##### `get_chat_completion(messages: List[Dict[str, str]], max_tokens: Optional[int] = None, stream: bool = False) -> Any`
Get a chat completion from the model.

Parameters:
- `messages`: List of conversation messages
- `max_tokens`: Maximum number of tokens to generate
- `stream`: Whether to stream the response

##### `get_token_usage() -> Optional[TokenUsage]`
Get the token usage information from the last request.

#### Token Usage Tracking
The class includes built-in token usage tracking through the `TokenUsage` class:
- `input_tokens`: Number of tokens in the input
- `max_tokens`: Maximum number of tokens to generate
- `output_tokens`: Number of tokens in the generated output

#### Rate Limiting
Includes configurable rate limiting functionality:
- Set maximum requests per minute
- Automatic request throttling
- Built-in timeout handling

#### Context Window Management
Provides sophisticated context window management:
- Configurable context window size
- Automatic message summarization when context limit is reached
- Support for different model token limits

### PromptTestingAgentCreator
Specialized creator for testing and optimizing prompts.

#### Constructor Parameters
- `client` (OpenAI): The OpenAI client instance
- `base_prompt` (str): The default system prompt
- `additional_prompts` (Dict[str, str], optional): Additional prompts to test
- `enable_ai_prompt_generation` (bool): Whether to enable AI prompt generation
- `model` (str): The model to use for the agent. Defaults to "gpt-4"

### TriageAgentCreator
Specialized creator for triage agents that manage agent selection and routing.

#### Constructor Parameters
- `agents_creator` (list[MonkaiAgentCreator]): List of agent creators to manage

#### Features
- Centralized decision-making for agent selection
- Dynamic transfer functions for agent routing
- Automatic predecessor agent management
- Support for customizable triage logic

## Usage Example

```python
# Initialize the agent manager
agent_manager = AgentManager(
    client=OpenAI(),
    agents_creators=[CustomAgentCreator()],
    context_variables={"key": "value"},
    stream=True
)

# Run a conversation
response = await agent_manager.run(
    user_message="Hello!",
    user_history=[],
    temperature=0.7,
    max_tokens=1000
)
```

## Best Practices

1. Always initialize the AgentManager with appropriate agent creators for your use case
2. Maintain conversation history using the Memory class for better context management
3. Use context variables to share state between different parts of the conversation
4. Enable debug mode during development for better visibility into the system's operation
5. Configure model parameters (temperature, max_tokens, etc.) based on your specific needs

## Error Handling

The framework includes robust error handling for:
- Missing tools/functions
- Invalid function results
- Context variable management
- Agent switching
- Tool call execution

This documentation provides a high-level overview of the MonkAI framework's core components and functionality. For specific implementation details, refer to the source code and inline documentation. 