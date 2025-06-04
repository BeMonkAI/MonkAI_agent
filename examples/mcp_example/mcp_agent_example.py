"""
Example usage of MCPAgent with MCP servers

This example demonstrates how to create and use an MCPAgent that connects
to MCP servers and utilizes their tools, resources, and prompts.
"""

import asyncio
import logging
from pathlib import Path

from monkai_agent import MCPAgent, create_stdio_mcp_config, create_sse_mcp_config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def example_stdio_mcp_agent():
    """Example using stdio connection to an MCP server."""
    
    # Create an MCPAgent
    agent = MCPAgent(
        name="MCP Demo Agent",
        model="gpt-4o",
        instructions="You are an assistant that can access tools and resources through MCP servers.",
        auto_discover_capabilities=True
    )
    
    # Create a configuration for a stdio-based MCP server
    # This example assumes you have a simple calculator MCP server script
    stdio_config = create_stdio_mcp_config(
        name="calculator_server",
        command="python",
        args=["calculator_mcp_server.py"],  # Your MCP server script
        cwd=Path.cwd()
    )
    
    try:
        # Add the MCP client to the agent
        connection = await agent.add_mcp_client(stdio_config)
        logger.info(f"Added MCP client: {connection.config.name}")
        
        # Connect to all MCP servers
        results = await agent.connect_all_clients()
        logger.info(f"Connection results: {results}")
        
        # Check connection status
        status = agent.get_connection_status()
        logger.info(f"Connection status: {status}")
        
        # List available tools
        tools = agent.list_available_tools()
        logger.info(f"Available tools: {[tool.name for tool in tools]}")
        
        # Example: Call a tool (assuming the calculator server has an 'add' tool)
        if any(tool.name == "add" for tool in tools):
            result = await agent.call_mcp_tool("add", {"a": 5, "b": 3})
            logger.info(f"Tool call result: {result}")
        
        # List available resources
        resources = agent.list_available_resources()
        logger.info(f"Available resources: {[resource.uri for resource in resources]}")
        
        # List available prompts
        prompts = agent.list_available_prompts()
        logger.info(f"Available prompts: {[prompt.name for prompt in prompts]}")
        
    except Exception as e:
        logger.error(f"Error in MCP agent example: {e}")
    finally:
        # Clean up connections
        await agent.disconnect_all_clients()


async def example_multiple_mcp_servers():
    """Example using multiple MCP servers with different connection types."""
    
    # Create an MCPAgent
    agent = MCPAgent(
        name="Multi-Server MCP Agent",
        model="gpt-4",
        instructions="You are an assistant with access to multiple MCP servers providing various capabilities.",
        auto_discover_capabilities=True
    )
    
    # Configuration for different types of MCP servers
    configs = [
        # Stdio-based server (e.g., local tool server)
        create_stdio_mcp_config(
            name="calculator_server",
            command="python",
            args=["calculator_mcp_server.py"],
        ),
        
        # SSE-based server (e.g., web service)
        create_sse_mcp_config(
            name="web_service",
            url="https://example.com/mcp/stream",
            headers={"Authorization": "Bearer your-token-here"}
        )
    ]
    
    try:
        # Add all MCP clients
        for config in configs:
            await agent.add_mcp_client(config)
        
        # Connect to all servers
        results = await agent.connect_all_clients()
        logger.info(f"Connection results: {results}")
        
        # Get overview of all capabilities
        all_tools = agent.list_available_tools()
        all_resources = agent.list_available_resources()
        all_prompts = agent.list_available_prompts()
        
        logger.info(f"Total tools available: {len(all_tools)}")
        logger.info(f"Total resources available: {len(all_resources)}")
        logger.info(f"Total prompts available: {len(all_prompts)}")
        
        # Show capabilities by server
        status = agent.get_connection_status()
        for server_name, server_status in status.items():
            logger.info(f"Server '{server_name}': {server_status}")
        
        # Example: Call a tool from a specific server
        try:
            result = await agent.call_mcp_tool(
                "some_tool", 
                {"param": "value"}, 
                server_name="local_tools"
            )
            logger.info(f"Tool result from specific server: {result}")
        except ValueError as e:
            logger.warning(f"Tool call failed: {e}")
        
        # Example: Get a resource
        try:
            if all_resources:
                resource_content = await agent.get_mcp_resource(all_resources[0].uri)
                logger.info(f"Resource content: {resource_content}")
        except Exception as e:
            logger.warning(f"Resource retrieval failed: {e}")
        
        # Example: Get a prompt
        try:
            if all_prompts:
                prompt_content = await agent.get_mcp_prompt(all_prompts[0].name)
                logger.info(f"Prompt content: {prompt_content}")
        except Exception as e:
            logger.warning(f"Prompt retrieval failed: {e}")
            
    except Exception as e:
        logger.error(f"Error in multi-server example: {e}")
    finally:
        await agent.disconnect_all_clients()


async def example_mcp_agent_with_functions():
    """Example showing how to combine MCPAgent with regular agent functions."""
    
    def local_calculator(a: int, b: int) -> str:
        """Local function that can be called by the agent."""
        return f"Local calculation: {a} + {b} = {a + b}"
    
    # Create an MCPAgent with both MCP capabilities and local functions
    agent = MCPAgent(
        name="Hybrid Agent",
        model="gpt-4o",
        instructions="You can use both local functions and MCP server tools.",
        functions=[local_calculator],  # Regular agent functions
        auto_discover_capabilities=True
    )
    
    # Add MCP server
    stdio_config = create_stdio_mcp_config(
        name="external_tools",
        command="python",
        args=["external_tools_server.py"]
    )
    
    try:
        await agent.add_mcp_client(stdio_config)
        await agent.connect_all_clients()
        
        # The agent now has access to both:
        # 1. Local functions (like local_calculator)
        # 2. MCP server tools, resources, and prompts
        
        logger.info("Agent has both local functions and MCP capabilities")
        logger.info(f"Local functions: {len(agent.functions)}")
        logger.info(f"MCP tools: {len(agent.list_available_tools())}")
        
    except Exception as e:
        logger.error(f"Error in hybrid agent example: {e}")
    finally:
        await agent.disconnect_all_clients()


# Simple MCP server example (for testing)
def create_simple_calculator_server():
    """
    Example of a simple MCP server that could be used with the MCPAgent.
    
    Save this as 'calculator_mcp_server.py' to use with the examples above.
    """
    server_code = '''
"""
Simple Calculator MCP Server

This is a basic MCP server that provides calculator tools.
"""

from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Calculator")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    return a - b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@mcp.tool()
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

@mcp.resource("calculation://history")
def get_calculation_history() -> str:
    """Get calculation history"""
    return "Recent calculations: 5+3=8, 10-2=8, 4*3=12"

if __name__ == "__main__":
    mcp.run()
'''
    
    with open("calculator_mcp_server.py", "w") as f:
        f.write(server_code)
    
    logger.info("Created calculator_mcp_server.py - you can now run the examples!")


if __name__ == "__main__":
    # Uncomment the example you want to run:
    
    # Create the simple server file first
    create_simple_calculator_server()
    
    # Run the examples
    #asyncio.run(example_stdio_mcp_agent())
    #asyncio.run(example_multiple_mcp_servers())
    asyncio.run(example_mcp_agent_with_functions())
    
    print("Examples are ready to run. Uncomment the desired example in __main__ section.")
