# MonkAI Framework Documentation

## Overview

MonkAI is a powerful framework for creating and managing AI agents with advanced features like rate limiting, token tracking, context window management, and timeout handling. This framework is designed to be flexible, efficient, and easy to use while providing robust control over AI interactions.

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
response = agent.get_chat_completion(messages=messages)
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
response = agent.get_chat_completion(messages=messages)
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

## Installation

```bash
pip install monkai-agent
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

## Advanced Usage

See the following sections for detailed documentation:
- [Token Management](./token_management.md)
- [Rate Limiting](./rate_limiting.md)
- [Context Window](./context_window.md)
- [Timeout Handling](./timeout.md)
- [LLM Providers](./llm_providers.md) 