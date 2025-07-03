# 🧮 Calculator MCP Agent Example

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-green.svg)](https://modelcontextprotocol.io)
[![Calculator](https://img.shields.io/badge/Calculator-Mathematics-yellow.svg)]()

> **Demonstrate how to create AI agents with mathematical capabilities using the Model Context Protocol**

This example demonstrates how to create an `MCPAgent` that connects to a Calculator MCP server to access mathematical calculation tools, allowing your AI agent to perform reliable and accurate mathematical operations.

## 🚀 What You Can Do

- ➕ **Basic operations** - Addition, subtraction, multiplication, and division
- 🛡️ **Safe calculations** - Protection against division by zero and other errors
- 📊 **Calculation history** - Access to the history of performed operations
- 🔧 **Simple integration** - Easy integration with MonkAI agents
- 🎯 **Guaranteed precision** - Reliable mathematical results
- 🤖 **Natural interface** - Perform calculations using natural language

## 📁 File Structure

- `calculator_mcp_server.py` - MCP server that provides basic calculator tools
- `calculator_agent_creator.py` - Creator that returns an MCPAgent configured to connect to the Calculator server
- `demo.py` - Practical usage example of the Calculator Agent
- `README.md` - This complete documentation

## ⚡ Features

The Calculator Agent provides access to the following tools through the MCP server:

### 🔧 Available Tools
- `add(a, b)` - Adds two numbers
- `subtract(a, b)` - Subtracts two numbers
- `multiply(a, b)` - Multiplies two numbers
- `divide(a, b)` - Divides two numbers (with protection against division by zero)

### 📚 Available Resources
- `calculation://history` - Access to the complete history of performed calculations

## 📋 How to Use

### 1. Import the CalculatorAgentCreator

```python
from calculator_agent_creator import CalculatorAgentCreator
```

### 2. Create the Agent Creator

```python
creator = CalculatorAgentCreator(model="gpt-4")
```

### 3. Initialize the Agent

```python
agent = await creator.initialize_agent()
```

### 4. Use the Calculation Tools

```python
# Perform mathematical operations
result = await agent.call_mcp_tool("add", {"a": 5, "b": 3})
print(f"5 + 3 = {result}")

result = await agent.call_mcp_tool("multiply", {"a": 4, "b": 7})
print(f"4 × 7 = {result}")
```

## 🎮 Complete Example

```python
import asyncio
from calculator_agent_creator import CalculatorAgentCreator

async def main():
    # Create the agent creator
    creator = CalculatorAgentCreator(model="gpt-4")
    
    # Initialize the agent and connect to the MCP server
    agent = await creator.initialize_agent()
    
    # Check connection status
    status = agent.get_connection_status()
    print(f"Connection status: {status}")
    
    # List available tools
    tools = agent.list_available_tools()
    print(f"Available tools: {[tool.name for tool in tools]}")
    
    # Perform calculations
    result = await agent.call_mcp_tool("add", {"a": 10, "b": 20})
    print(f"10 + 20 = {result}")
    
    # Cleanup
    await agent.disconnect_all_clients()

# Run the example
asyncio.run(main())
```

## 🚀 Running the Example

To run the complete example:

```bash
# Activate the Python virtual environment
source .venv/bin/activate

# Run the example
python demo.py
```

## 🔧 CalculatorAgentCreator Characteristics

### Initialization Parameters

- `model` (str): Language model to be used (default: "gpt-4")
- `server_script_path` (str, optional): Path to the server script. If None, uses the default path
- `python_executable` (str): Python executable to run the server (default: "python")

### Main Methods

- `get_agent()` - Returns the configured MCPAgent
- `get_agent_briefing()` - Returns a description of the agent's capabilities
- `initialize_agent()` - Initializes the agent and establishes MCP connections
- `agent_name` - Property that returns the agent's name

## 🏗️ Architecture

```
CalculatorAgentCreator
    ↓
MCPAgent (Calculator Agent)
    ↓
MCP Client Connection (stdio)
    ↓
Calculator MCP Server
    ↓
Tools: add, subtract, multiply, divide
Resources: calculation://history
```

## 🛡️ Error Handling

The agent has robust error handling:

- **Division by zero**: The Calculator server detects and throws an appropriate error
- **MCP connection**: Connection failures are captured and reported
- **Tools not found**: Clear error messages when tools don't exist

## 🎯 Usage Example with AgentManager

```python
from monkai_agent import AgentManager
from calculator_agent_creator import CalculatorAgentCreator

async def example_with_manager():
    # Create the agent
    creator = CalculatorAgentCreator()
    agent = await creator.initialize_agent()
    
    # Use with AgentManager
    manager = AgentManager()
    
    # Execute conversation
    response = await manager.run(
        agent=agent,
        messages=[{"role": "user", "content": "Calculate 25 + 17 and then multiply by 3"}],
        debug=True
    )
    
    print(response.messages[-1]["content"])
    
    # Cleanup
    await agent.disconnect_all_clients()
```

## 📦 Requirements

- Python 3.8+
- MonkAI Agent Framework
- MCP (Model Context Protocol) package
- OpenAI or other configured LLM provider

## ⚠️ Important Notes

1. **Virtual Environment**: Make sure to activate the virtual environment before running
2. **MCP Server**: The Calculator server is automatically started by the agent
3. **Connections**: Always disconnect MCP clients when finished for proper cleanup
4. **Debugging**: Use `debug=True` in AgentManager to see detailed logs of MCP operations
