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
- `initialize_agents()`: Initializes the agents using the provided creators.
- `get_agent(name: str) -> Agent`: Retrieves an agent by name.
- `set_current_agent(agent: Agent)`: Sets the currently active agent.
- `run_agent(agent: Agent, user_input: str) -> str`: Runs the specified agent with the given user input.

### Agent
A class representing an AI agent with specific instructions and functions.

#### Constructor Parameters
- `name` (str): The name of the agent.
- `instructions` (str): Instructions for the agent.
- `functions` (list[callable]): List of functions the agent can call.

#### Key Methods
- `get_name() -> str`: Returns the name of the agent.
- `get_instructions() -> str`: Returns the instructions for the agent.
- `get_functions() -> list[callable]`: Returns the list of functions the agent can call.

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
from monkai_agent import AgentManager, Agent

# Create an agent
agent = Agent(name="Example Agent", instructions="You are a helpful assistant.", functions=[])

# Create an agent manager
manager = AgentManager(agents_creators=[agent])

# Run the agent
response = manager.run_agent(agent, "Hello, how can you help me?")
print(response)
```

## Best Practices

1. Always initialize the AgentManager with appropriate agent creators for your use case
2. Maintain conversation history using the Memory class for better context management
3. Use context variables to share state between different parts of the conversation
4. Enable debug mode during development for better visibility into the system's operation
5. Configure model parameters (temperature, max_tokens, etc.) based on your specific needs

## Test Files

### Test Files Overview
The MonkAI framework includes several test files to ensure the functionality of key features:

- **`test_timeout.py`**: Verifies the timeout functionality by testing long and short requests with different timeout settings.
- **`test_context_window.py`**: Tests the context window management by checking message and token counts and ensuring valid responses after summarization.
- **`test_rate_limit.py`**: Ensures the rate limiting feature is working by making multiple requests and measuring the time intervals between them.

### Running Tests
To run the tests, navigate to the `tests` directory and execute the test files using Python:

```bash
cd tests
python test_timeout.py
python test_context_window.py
python test_rate_limit.py
```

Each test will output results to the console, indicating whether the test passed or failed and providing details on the execution.

## Error Handling

The framework includes robust error handling for:
- Missing tools/functions
- Invalid function results
- Context variable management
- Agent switching
- Tool call execution

### Error Handling Examples
- **Missing Tools**: If a tool is not found, the framework logs an error and continues execution without crashing.
- **Invalid Results**: The framework attempts to cast results to strings or raises a `TypeError` if this fails, providing detailed error messages.
- **Context Management**: Errors in context variable updates are logged, and the framework ensures that context remains consistent.

## Additional Classes and Parameters

### TokenUsage
- **input_tokens**: int
- **output_tokens**: int

### MonkaiAgentCreator (Abstract Class)
- **Methods**:
  - `get_agent() -> Agent`
  - `get_agent_briefing() -> str`
- **Properties**:
  - `agent_name`: str
  - `predecessor_agent`: Agent

### TransferTriageAgentCreator (Subclass of MonkaiAgentCreator)
- **Methods**:
  - `set_triage_agent(triage_agent: Agent)`
  - `transfer_to_triage()`

### PromptTestingAgentCreator (Subclass of MonkaiAgentCreator)
- **Constructor Parameters**:
  - `client`: OpenAI
  - `base_prompt`: str
  - `additional_prompts`: Optional[Dict[str, str]]
  - `enable_ai_prompt_generation`: bool
  - `model`: str

### RateLimiter
- **Constructor Parameters**:
  - `max_calls`: int
  - `time_window`: float
- **Methods**:
  - `acquire(block: bool = True) -> bool`
  - `release()`

### BaseAgent
- **Properties**:
  - `name`: str
  - `instructions`: str
  - `model`: str
  - `functions`: List[AgentFunction]
  - `tool_choice`: str
  - `parallel_tool_calls`: bool

### LLMProvider
- **Constructor Parameters**:
  - `api_key`: str
- **Methods**:
  - `get_client()`
  - `get_chat_completion(messages: list, **kwargs)`

### OpenAIProvider (Subclass of LLMProvider)
- **Methods**:
  - `get_client()`
  - `get_chat_completion(messages: list, **kwargs)`

### GroqProvider (Subclass of LLMProvider)
- **Constructor Parameters**:
  - `api_key`: str
  - `model`: str
- **Methods**:
  - `get_client()`
  - `get_chat_completion(messages: list, **kwargs)`

This documentation provides a high-level overview of the MonkAI framework's core components and functionality. For specific implementation details, refer to the source code and inline documentation.

## Additional Information

For more details, please refer to the [README](README.md) file. 