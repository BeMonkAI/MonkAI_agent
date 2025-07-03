# 🎯 Notion MCP Integration

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-green.svg)](https://modelcontextprotocol.io)
[![Notion](https://img.shields.io/badge/Notion-API-black.svg)](https://developers.notion.com)

> **Seamlessly connect your AI agents to Notion databases with the Model Context Protocol (MCP)**

This example demonstrates how to integrate your MonkAI agents with Notion databases using a Model Context Protocol server: https://smithery.ai/server/@smithery/notion , enabling your AI to interact with your Notion workspace in real-time.

## 🚀 What You Can Do

- 📊 **Query Notion databases** - List and explore your existing databases
- 🔍 **Search database content** - Find specific pages and records
- ✨ **Create new databases** - Programmatically set up new data structures
- 📝 **Manage pages** - Create, read, update, and delete pages
- 🤖 **Natural language interface** - Ask questions about your Notion data in plain language

## 🛠️ Prerequisites

Before you start, make sure you have:

1. **Notion API Key** - Get yours from [Notion Developers](https://developers.notion.com)
2. **MonkAI Agent Library** - Installed in your environment
3. **Python 3.10+** - For async/await support

## 📋 Quick Setup

### 1. Get Your Notion API Key

1. Go to [Notion Developers](https://developers.notion.com)
2. Create a new integration
3. Copy your **Internal Integration Token**
4. Share your databases with the integration

### 2. Configure Your Agent

```python
# Replace with your actual Notion API key
_config = {
  "notionApiKey": "secret_YOUR_NOTION_API_KEY_HERE"
}
```

### 3. Run the Example

```bash
cd examples/mcp_example/mcp-notion
python notion_mcp_agent.py
```

## 💡 How It Works

### Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   MonkAI Agent  │───▶│   MCP Server    │───▶│  Notion API     │
│                 │    │  (Smithery.ai)  │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

The integration uses three key components:

1. **MonkAI Agent** - Your AI assistant with natural language understanding
2. **MCP Server** - Protocol bridge that translates between AI and Notion
3. **Notion API** - Direct access to your Notion workspace

### Code Breakdown

#### 1. Agent Initialization

```python
# Create the Notion-enabled agent
notion_agent = MCPAgent(
    name="Notion manager Agent",
    instructions="""You are an Agent that is connected to the users Notion server, 
    when requested you can query and list the databases in the users Notion account 
    as well as perform operations such as creating new databases.""",
    model="gpt-4o"
)
```

#### 2. MCP Server Connection

```python
async def initialize_agent() -> MCPAgent:
    # Configure the MCP connection
    mcp_config = create_http_mcp_config(
        name="Notion_MCP_Server",
        url=notion_server_url,
    )
    
    # Connect to Notion via MCP
    await notion_agent.add_mcp_client(mcp_config)
    connection_results = await notion_agent.connect_all_clients()
    
    return notion_agent
```

#### 3. Natural Language Queries

```python
# Ask questions in natural language
result = await manager.run(
    "What databases do I have in Notion?", 
    agent=agent
)
```

## 🎮 Example Usage

### Basic Database Query

```python
import asyncio
from notion_mcp_agent import initialize_agent
from monkai_agent import AgentManager

async def demo():
    # Initialize the Notion-connected agent
    agent = await initialize_agent()
    manager = AgentManager(api_key="your-openai-key")
    
    # Query your databases
    result = await manager.run(
        "List all my Notion databases and their properties", 
        agent=agent
    )
    
    print(result.messages[-1].content)
    await agent.disconnect_all_clients()

# Run the demo
asyncio.run(demo())
```

### Advanced Operations

```python
# Create a new database
await manager.run(
    "Create a new database called 'Project Tasks' with columns for Name, Status, Due Date, and Priority",
    agent=agent
)

# Search for specific content
await manager.run(
    "Find all pages in my databases that mention 'machine learning'",
    agent=agent
)

# Analyze database structure
await manager.run(
    "What's the structure of my 'Projects' database? Show me all properties and their types",
    agent=agent
)
```

## 🔧 Configuration Options

### Environment Variables

Create a `config.py` file:

```python
# config.py
api_key = "your-openai-api-key"  # Your OpenAI API key
notion_api_key = "secret_your_notion_key"  # Your Notion integration token
```

### Custom MCP Server

If you're running your own MCP server:

```python
# Point to your custom server
url = "http://localhost:3000/mcp/notion"
```

## 🔍 Available Operations

The Notion MCP server typically supports these operations:

| Operation | Description | Example Query |
|-----------|-------------|---------------|
| `list_databases` | Get all accessible databases | "What databases do I have?" |
| `query_database` | Search within a specific database | "Show me all tasks due this week" |
| `create_database` | Create a new database | "Create a reading list database" |
| `get_page` | Retrieve a specific page | "Get the details of the project plan page" |
| `create_page` | Add a new page | "Add a new task: Review documentation" |
| `update_page` | Modify existing content | "Mark the task as completed" |

## 🐛 Troubleshooting

### Common Issues

#### 1. Connection Failed
```
RuntimeError: Failed to connect to MCP server
```
**Solution**: Check your Notion API key and make sure the integration has access to your databases.

#### 2. Authentication Error
```
401 Unauthorized
```
**Solution**: Verify your Notion API key is correct and hasn't expired.

#### 3. Database Not Found
```
Database not accessible
```
**Solution**: Share the specific database with your Notion integration.

### Debug Mode

Enable verbose logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

