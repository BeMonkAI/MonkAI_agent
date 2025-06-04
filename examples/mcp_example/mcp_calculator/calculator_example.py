"""
Calculator Agent Example

This example demonstrates how to use the CalculatorAgentCreator to create
an MCPAgent that connects to the Calculator MCP server and performs calculations.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the path to access the calculator agent creator
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from calculator_agent_creator import CalculatorAgentCreator


async def main():
    """Main example function demonstrating Calculator Agent usage."""
    
    print("🧮 Calculator Agent Example")
    print("=" * 50)
    
    try:
        # Create the calculator agent creator
        print("1. Creating Calculator Agent Creator...")
        creator = CalculatorAgentCreator(model="gpt-4")
        
        print(f"   Agent Name: {creator.agent_name}")
        print("\n2. Agent Briefing:")
        print(creator.get_agent_briefing())
        
        # Initialize the agent and connect to MCP server
        print("\n3. Initializing agent and connecting to Calculator MCP server...")
        agent = await creator.initialize_agent()
        
        # Check connection status
        connection_status = agent.get_connection_status()
        print(f"   Connection Status: {connection_status}")
        
        # List available tools
        tools = agent.list_available_tools()
        print(f"   Available Tools: {[tool.name for tool in tools]}")
        
        # List available resources
        resources = agent.list_available_resources()
        print(f"   Available Resources: {[resource.uri for resource in resources]}")
        
        print("\n4. Testing Calculator Tools:")
        print("-" * 30)
        
        # Test addition
        result = await agent.call_mcp_tool("add", {"a": 15, "b": 27})
        print(f"   15 + 27 = {result}")
        
        # Test subtraction
        result = await agent.call_mcp_tool("subtract", {"a": 50, "b": 18})
        print(f"   50 - 18 = {result}")
        
        # Test multiplication
        result = await agent.call_mcp_tool("multiply", {"a": 8, "b": 9})
        print(f"   8 × 9 = {result}")
        
        # Test division
        result = await agent.call_mcp_tool("divide", {"a": 84, "b": 4})
        print(f"   84 ÷ 4 = {result}")
        
        # Test division with decimal result
        result = await agent.call_mcp_tool("divide", {"a": 10, "b": 3})
        print(f"   10 ÷ 3 = {result}")
        
        # Test error handling (division by zero)
        print("\n5. Testing Error Handling:")
        print("-" * 30)
        try:
            result = await agent.call_mcp_tool("divide", {"a": 10, "b": 0})
            print(f"   10 ÷ 0 = {result}")
        except Exception as e:
            print(f"   ✅ Division by zero properly handled: {e}")
        
        # Get calculation history resource
        print("\n6. Accessing Calculation History:")
        print("-" * 30)
        try:
            history = await agent.get_mcp_resource("calculation://history")
            print(f"   History: {history}")
        except Exception as e:
            print(f"   History access: {e}")
        
        # Cleanup
        print("\n7. Cleaning up connections...")
        await agent.disconnect_all_clients()
        
        print("\n✅ Calculator Agent Example completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during example: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Run the example
    asyncio.run(main())
