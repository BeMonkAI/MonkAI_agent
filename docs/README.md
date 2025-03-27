# MonkAI Framework

MonkAI is a powerful framework designed to facilitate the creation and management of AI agents. It provides tools for prompt testing, agent management, and more.

## Features

- **Prompt Testing**: Test and optimize prompts with ease.
- **Agent Management**: Manage multiple AI agents efficiently.
- **AI Prompt Generation**: Enable AI-enhanced prompt generation.

## Installation

To install MonkAI, use the following command:

```bash
pip install monkai
```

## Getting Started

Here's a quick example to get you started with MonkAI:

```python
import asyncio
from monkai_agent import AgentManager
from monkai_agent.monkai_agent_creator import PromptTestingAgentCreator

async def main():
    # Your code here

if __name__ == "__main__":
    asyncio.run(main())
```

## Quick Start

```python
from monkai_agent import MonkaiAgentCreator

# Create an agent with default settings
agent = MonkaiAgentCreator(
    base_prompt="You are a helpful AI assistant.",
    model="gpt-3.5-turbo",
    provider="openai"
)

# Send a message and get response
messages = [{"role": "user", "content": "Hello!"}]
response = agent.get_chat_completion(messages=messages, max_tokens=50)
print(response.choices[0].message.content)
```

## Features

### 1. Token Usage Tracking
Monitor and manage token usage in real-time:
```python
agent = MonkaiAgentCreator(
    base_prompt="Your prompt",
    track_token_usage=True
)

# Get token count before sending
messages = [{"role": "user", "content": "Your message"}]
token_count = agent.count_message_tokens(messages)
print(f"This request will use {token_count} input tokens")

# Get token usage after request
response = agent.get_chat_completion(messages=messages, max_tokens=50)
token_usage = agent.get_token_usage()
print(f"Input tokens: {token_usage.input_tokens}")
print(f"Output tokens: {token_usage.output_tokens}")
```

### 2. Rate Limiting
Control request frequency to stay within API limits:
```python
agent = MonkaiAgentCreator(
    base_prompt="Your prompt",
    rate_limit_rpm=60  # 60 requests per minute
)
```

### 3. Request Timeout
Prevent long-running requests:
```python
agent = MonkaiAgentCreator(
    base_prompt="Your prompt",
    max_execution_time=30  # 30 seconds timeout
)
```

### 4. Context Window Management
Automatically manage conversation history:
```python
agent = MonkaiAgentCreator(
    base_prompt="Your prompt",
    context_window_size=4096,
    freeze_context_window_size=True
)
```

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `GROQ_API_KEY`: Your Groq API key (if using Groq provider)

### Available Models
- OpenAI:
  - gpt-4
  - gpt-4o
  - gpt-3.5-turbo
  - gpt-3.5-turbo-16k
- Groq:
  - mixtral-8x7b
  - claude-2

## Running Tests

To ensure the framework is functioning correctly, run the included test files:

```bash
cd tests
python test_timeout.py
python test_context_window.py
python test_rate_limit.py
```

Each test will output results to the console, indicating whether the test passed or failed and providing details on the execution.

## Advanced Usage

For detailed documentation, refer to the `api_reference.md` file. 