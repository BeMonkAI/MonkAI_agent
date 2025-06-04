# MCP Agent Examples

This directory contains examples and documentation for using the MCPAgent (Model Context Protocol Agent) within the MonkAI agent framework.

## Overview

The MCPAgent extends the base Agent class to provide integration with MCP (Model Context Protocol) servers. This allows agents to access external tools, resources, and prompts through standardized MCP connections.

## Key Features

- **Multiple Connection Types**: Support for stdio, SSE, and HTTP connections to MCP servers
- **Auto-discovery**: Automatically discover tools, resources, and prompts from connected servers
- **Multi-server Support**: Connect to multiple MCP servers simultaneously
- **Unified Interface**: Access all MCP capabilities through a consistent API
- **Integration**: Seamless integration with existing MonkAI agent framework

## Files in this Directory

### Core Examples

- **`mcp_agent_example.py`** - Basic usage examples showing how to create and use MCPAgent with different connection types
- **`mcp_integration_example.py`** - Advanced examples showing integration with AgentManager and multi-agent workflows
- **`test_mcp_agent.py`** - Basic tests to verify MCPAgent functionality

### MCP Server Examples

You can create simple MCP servers for testing. Here's a basic calculator server:

```python
# calculator_mcp_server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Calculator")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    return a - b

@mcp.resource("calculation://history")
def get_calculation_history() -> str:
    """Get calculation history"""
    return "Recent calculations: 5+3=8, 10-2=8"

if __name__ == "__main__":
    mcp.run()
```

## Quick Start

### 1. Basic MCPAgent Usage

```python
from monkai_agent import MCPAgent, create_stdio_mcp_config

# Create an MCPAgent
agent = MCPAgent(
    name="My MCP Agent",
    model="gpt-4",
    instructions="You can access external tools and resources.",
    auto_discover_capabilities=True
)

# Add an MCP server connection
config = create_stdio_mcp_config(
    name="calculator",
    command="python",
    args=["calculator_mcp_server.py"]
)

await agent.add_mcp_client(config)
await agent.connect_all_clients()

# Use MCP capabilities
tools = agent.list_available_tools()
result = await agent.call_mcp_tool("add", {"a": 5, "b": 3})
```

### 2. Multiple MCP Servers

```python
# Connect to multiple servers
configs = [
    create_stdio_mcp_config("calculator", "python", ["calc_server.py"]),
    create_sse_mcp_config("web_service", "https://api.example.com/mcp"),
]

for config in configs:
    await agent.add_mcp_client(config)

await agent.connect_all_clients()

# Access capabilities from all servers
all_tools = agent.list_available_tools()
all_resources = agent.list_available_resources()
```

### 3. Integration with AgentManager

```python
from monkai_agent import AgentManager

class MCPAgentManager(AgentManager):
    async def run_with_mcp_support(self, agent, messages, context_variables=None):
        try:
            # Connect MCP clients
            await agent.connect_all_clients()
            
            # Run agent with MCP capabilities
            response = await self.run(agent, messages, context_variables)
            return response
        finally:
            # Clean up connections
            await agent.disconnect_all_clients()
```

## MCP Connection Types

### 1. Stdio Connections

Best for local MCP servers and command-line tools:

```python
config = create_stdio_mcp_config(
    name="local_tools",
    command="python",
    args=["my_mcp_server.py"],
    cwd="/path/to/server",
    env={"API_KEY": "your-key"}
)
```

### 2. SSE (Server-Sent Events) Connections

Best for web-based MCP services:

```python
config = create_sse_mcp_config(
    name="web_service",
    url="https://api.example.com/mcp/stream",
    headers={"Authorization": "Bearer token"},
    timeout=60.0
)
```

## Available Methods

### Connection Management

- `add_mcp_client(config)` - Add a new MCP client
- `connect_all_clients()` - Connect to all configured servers
- `disconnect_all_clients()` - Disconnect from all servers
- `get_connection_status()` - Get status of all connections

### Capability Discovery

- `list_available_tools(server_name=None)` - List available tools
- `list_available_resources(server_name=None)` - List available resources
- `list_available_prompts(server_name=None)` - List available prompts

### MCP Operations

- `call_mcp_tool(tool_name, arguments, server_name=None)` - Call an MCP tool
- `get_mcp_resource(resource_uri, server_name=None)` - Get an MCP resource
- `get_mcp_prompt(prompt_name, arguments=None, server_name=None)` - Get an MCP prompt

## Running the Examples

1. **Install dependencies**:
   ```bash
   pip install "mcp[cli]"
   ```

2. **Create a simple MCP server** (optional):
   ```python
   # Run this in mcp_agent_example.py to create calculator_mcp_server.py
   create_simple_calculator_server()
   ```

3. **Run the tests**:
   ```bash
   python test_mcp_agent.py
   ```

4. **Try the examples**:
   ```bash
   python mcp_agent_example.py
   python mcp_integration_example.py
   ```

## Best Practices

1. **Connection Management**: Always use proper connection management with try/finally blocks or context managers
2. **Error Handling**: Handle MCP connection failures gracefully
3. **Server Discovery**: Use auto-discovery for development, but cache capabilities for production
4. **Resource Cleanup**: Always disconnect from MCP servers when done
5. **Server-Specific Calls**: Use server_name parameter when you need specific server capabilities

## Integration Patterns

### 1. Wrapper Functions

Wrap MCP capabilities as regular agent functions:

```python
async def search_database(query: str) -> Result:
    result = await agent.call_mcp_tool("search", {"query": query})
    return Result(value=result)

agent.functions.append(search_database)
```

### 2. Multi-Agent Workflows

Use different MCP servers for different agent roles:

```python
# Data collector with data source MCP server
collector = MCPAgent(name="Collector")
await collector.add_mcp_client(data_source_config)

# Analyst with analysis tools MCP server  
analyst = MCPAgent(name="Analyst")
await analyst.add_mcp_client(analysis_tools_config)
```

### 3. Dynamic Capability Loading

Load MCP capabilities based on context:

```python
if context_variables.get("need_database"):
    await agent.add_mcp_client(database_config)
    
if context_variables.get("need_analysis"):
    await agent.add_mcp_client(analysis_config)
```

## Troubleshooting

### Common Issues

1. **Connection Failures**: Check that MCP server is running and accessible
2. **Tool Not Found**: Verify tool name and ensure server is connected
3. **Permission Errors**: Check file permissions for stdio servers
4. **Import Errors**: Ensure `mcp[cli]` is installed

### Debug Mode

Enable debug logging to see MCP operations:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Further Reading

- [MCP Specification](https://spec.modelcontextprotocol.io)
- [MCP Python SDK Documentation](https://modelcontextprotocol.io)
- [Creating MCP Servers](https://modelcontextprotocol.io/docs/building-servers)
