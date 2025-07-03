# 🧠 Mem0 Memory MCP Integration

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-green.svg)](https://modelcontextprotocol.io)
[![Mem0](https://img.shields.io/badge/Mem0-Memory%20Platform-purple.svg)](https://mem0.ai)

> **Give your AI agents persistent memory with Mem0's advanced memory management through MCP**

This example demonstrates how to integrate your MonkAI agents with Mem0's memory platform using a Model Context Protocol server: https://smithery.ai/server/@mem0ai/mem0-memory-mcp , enabling your AI to remember user interactions, preferences, and context across conversations.

## 🚀 What You Can Do

- 🧠 **Store user memories** - Automatically capture and store important user information
- 🔍 **Retrieve past context** - Access previous conversations and user preferences
- 👤 **User-specific memory** - Maintain separate memory collections for different users
- 🔄 **Contextual continuity** - Build ongoing relationships with consistent personality
- 📈 **Memory analytics** - Track and analyze memory patterns over time
- 🗑️ **Memory management** - Update, delete, and organize stored memories

## 🛠️ Prerequisites

Before you start, make sure you have:

1. **Mem0 API Key** - Get yours from [Mem0.ai](https://mem0.ai)
2. **MonkAI Agent Library** - Installed in your environment
3. **Python 3.10+** - For async/await support

## 📋 Quick Setup

### 1. Get Your Mem0 API Key

1. Sign up at [Mem0.ai](https://mem0.ai)
2. Navigate to your dashboard
3. Generate a new API key
4. Copy your **API Key**

### 2. Configure Your Agent

```python
# Replace with your actual Mem0 API key
config = {
  "mem0ApiKey": "m0-YOUR_ACTUAL_MEM0_API_KEY_HERE"
}
```

### 3. Run the Example

```bash
cd examples/mcp_example/mcp-memory
python mem0_mcp_agent.py
```

## 💡 How It Works

### Memory Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   MonkAI Agent  │───▶│   MCP Server    │───▶│   Mem0 Platform │
│   with Memory   │    │  (Smithery.ai)  │    │  Memory Store   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                                              │
        │              🧠 Memory Flow                  │
        └──────────────────────────────────────────────┘
```

The integration provides three layers of memory management:

1. **MonkAI Agent** - Your AI assistant with memory-aware capabilities
2. **MCP Server** - Protocol bridge that handles memory operations
3. **Mem0 Platform** - Advanced memory storage and retrieval system

### Code Breakdown

#### 1. Memory-Enabled Agent Creation

```python
# Create an agent with memory capabilities
memory_agent = MCPAgent(
    name="Memory Manager Agent",
    instructions="""You are a memory manager Agent that stores and retrieves 
    user-specific memories to maintain context and make informed decisions 
    based on past interactions.""",
    model="gpt-4o"
)
```

#### 2. MCP Memory Server Connection

```python
async def initialize_agent() -> MCPAgent:
    # Configure memory server connection
    mcp_config = create_http_mcp_config(
        name="Memory_MCP_Server",
        url=mem0_server_url,
    )
    
    # Connect to Mem0 via MCP
    await memory_agent.add_mcp_client(mcp_config)
    connection_results = await memory_agent.connect_all_clients()
    
    return memory_agent
```

#### 3. Memory-Aware Conversations

```python
# The agent automatically stores and retrieves memories
result = await manager.run(
    "What memories are stored for user123?", 
    agent=agent
)
```

## 🎮 Example Usage

### Basic Memory Operations

```python
import asyncio
from mem0_mcp_agent import initialize_agent
from monkai_agent import AgentManager

async def memory_demo():
    # Initialize memory-enabled agent
    agent = await initialize_agent()
    manager = AgentManager(api_key="your-openai-key")
    
    # Store a new memory
    await manager.run(
        "Remember that John prefers coffee over tea and works in marketing",
        agent=agent
    )
    
    # Retrieve user memories
    result = await manager.run(
        "What do you remember about John?",
        agent=agent
    )
    
    print(result.messages[-1].content)
    await agent.disconnect_all_clients()

# Run the demo
asyncio.run(memory_demo())
```

### Advanced Memory Management

```python
# User-specific memory storage
await manager.run(
    "Store for user456: Loves hiking, vegetarian, lives in San Francisco, has 2 cats named Whiskers and Mittens",
    agent=agent
)

# Contextual memory retrieval
await manager.run(
    "Based on what you remember about user456, suggest a good restaurant for them",
    agent=agent
)

# Memory search and filtering
await manager.run(
    "Show me all memories related to food preferences across all users",
    agent=agent
)

# Memory updates
await manager.run(
    "Update user456's profile: they moved to Portland and adopted a third cat named Shadow",
    agent=agent
)
```

### Multi-User Memory Management

```python
# Handle multiple users with separate memory contexts
users = ["alice", "bob", "charlie"]

for user in users:
    result = await manager.run(
        f"What personal preferences do you remember about {user}?",
        agent=agent
    )
    print(f"\n--- Memories for {user} ---")
    print(result.messages[-1].content)
```

## 🔧 Configuration Options

### Environment Variables

Create a `config.py` file:

```python
# config.py
api_key = "your-openai-api-key"  # Your OpenAI API key
mem0_api_key = "m0-your-mem0-key"  # Your Mem0 API key
```

### Custom Memory Configuration

```python
# Advanced memory configuration
config = {
    "mem0ApiKey": "your-mem0-key",
    "organizationId": "your-org-id",  # Optional: for team accounts
    "projectId": "your-project-id",   # Optional: for project-specific memories
}
```

### Custom MCP Server

If you're running your own MCP server:

```python
# Point to your custom memory server
url = "http://localhost:3000/mcp/memory"
```

## 🔍 Available Memory Operations

The Mem0 MCP server typically supports these operations:

| Operation | Description | Example Query |
|-----------|-------------|---------------|
| `store_memory` | Save new memories for users | "Remember that Alice likes chocolate" |
| `get_memories` | Retrieve memories for a user | "What do you remember about Bob?" |
| `search_memories` | Find specific memories | "Show me all food-related memories" |
| `update_memory` | Modify existing memories | "Update: Alice now prefers dark chocolate" |
| `delete_memory` | Remove specific memories | "Forget about Bob's old address" |
| `list_users` | Get all users with memories | "Which users have stored memories?" |

## 🧠 Memory Best Practices

### 1. Structured Memory Storage
```python
# Good: Structured information
"Remember for user789: Name is Sarah, age 28, works as a data scientist at TechCorp, prefers morning meetings, allergic to peanuts"

# Better: Use clear categories
"Store user preferences for sarah_tech: Work schedule - prefers 9am meetings, Dietary restrictions - peanut allergy, Role - Senior Data Scientist"
```

### 2. User Identification
```python
# Always specify user context
await manager.run(
    "For user_id_12345: Remember they prefer email over phone calls",
    agent=agent
)
```

### 3. Memory Hygiene
```python
# Regularly clean up outdated information
await manager.run(
    "Update user456's location from San Francisco to Portland, and remove the old address",
    agent=agent
)
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Connection Failed
```
RuntimeError: Failed to connect to MCP server
```
**Solution**: Verify your Mem0 API key is correct and active.

#### 2. Memory Not Found
```
No memories found for user
```
**Solution**: Ensure you're using consistent user identifiers and that memories have been stored.

#### 3. API Rate Limits
```
Rate limit exceeded
```
**Solution**: Implement exponential backoff or upgrade your Mem0 plan.

#### 4. Memory Retrieval Empty
```
Agent returns: "I don't have any memories stored"
```
**Solution**: Check that memories were successfully stored and use exact user IDs.

### Debug Mode

Enable verbose logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Also enable MCP debug
import os
os.environ["MCP_DEBUG"] = "1"
```

### Memory Verification

```python
# Test memory storage and retrieval
async def test_memory():
    agent = await initialize_agent()
    manager = AgentManager(api_key=config.api_key)
    
    # Store test memory
    await manager.run("Remember that test_user likes pizza", agent=agent)
    
    # Verify storage
    result = await manager.run("What do you remember about test_user?", agent=agent)
    
    if "pizza" in result.messages[-1].content.lower():
        print("✅ Memory system working correctly")
    else:
        print("❌ Memory storage/retrieval failed")
```

## 🔒 Privacy and Security

- **User Isolation**: Memories are stored per user and are not shared across users
- **Data Encryption**: Mem0 encrypts all stored memories
- **Access Control**: Only your API key can access your organization's memories
- **Compliance**: Mem0 follows GDPR and other privacy regulations

## 🚀 Advanced Features

### Memory Analytics

```python
# Analyze memory patterns
await manager.run(
    "Give me statistics about stored memories: how many users, most common preferences, memory categories",
    agent=agent
)
```

### Semantic Memory Search

```python
# Find related memories using semantic search
await manager.run(
    "Find all memories related to 'outdoor activities' even if they don't explicitly mention those words",
    agent=agent
)
```

### Memory Relationships

```python
# Understand connections between memories
await manager.run(
    "Show me how different users' preferences relate to each other",
    agent=agent
)
```

