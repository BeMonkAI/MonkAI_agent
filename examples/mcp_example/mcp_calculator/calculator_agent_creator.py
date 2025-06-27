"""
Calculator Agent Creator

This module creates an MCPAgent that connects to the Calculator MCP server to access
calculator tools like add, subtract, multiply, and divide operations.
"""

import sys
import os
import asyncio
from pathlib import Path
from typing import Optional

# Add the parent directories to the path to import monkai_agent modules
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
libs_path = project_root / "libs" / "monkai_agent"
# Also add the project root to access config.py
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(libs_path))

from monkai_agent import MCPAgent, MCPClientConfig, create_stdio_mcp_config
from monkai_agent.monkai_agent_creator import MonkaiAgentCreator


class CalculatorAgentCreator(MonkaiAgentCreator):
    """
    Creator for Calculator MCP Agent.
    
    This class creates and configures an MCPAgent that connects to the Calculator
    MCP server, providing access to mathematical calculation tools.
    """
    
    def __init__(self, 
                 model: str = "gpt-4",
                 server_script_path: Optional[str] = None,
                 python_executable: Optional[str] = None):
        """
        Initialize the Calculator Agent Creator.
        
        Args:
            model (str): The language model to use for the agent
            server_script_path (str, optional): Path to the calculator server script.
                                               If None, uses the default path relative to this file.
            python_executable (str, optional): Python executable to use for running the server.
                                              If None, auto-detects the current Python executable.
        """
        super().__init__()
        self.model = model
        
        # Auto-detect the current Python executable if not provided
        if python_executable is None:
            self.python_executable = sys.executable
        else:
            self.python_executable = python_executable
        
        # Default to the calculator server in the same directory
        if server_script_path is None:
            self.server_script_path = str(current_dir / "calculator_mcp_server.py")
        else:
            self.server_script_path = server_script_path
            
        self._agent = None
        
    @property
    def agent_name(self) -> str:
        """Return the name of this agent type."""
        return "Calculator Agent"
    
    def get_agent_briefing(self) -> str:
        """
        Get a brief description of the Calculator Agent's capabilities.
        
        Returns:
            str: Description of the agent's mathematical capabilities
        """
        return """
        Calculator Agent - Mathematical Operations Expert
        
        This agent provides access to basic mathematical operations through an MCP server:
        
        Available Tools:
        • add(a, b) - Add two numbers
        • subtract(a, b) - Subtract two numbers  
        • multiply(a, b) - Multiply two numbers
        • divide(a, b) - Divide two numbers (with zero division protection)
        
        Available Resources:
        • calculation://history - Access to calculation history
        
        The agent can perform mathematical calculations and maintain a history
        of operations performed. It's ideal for tasks requiring mathematical
        computation and calculation tracking.
        """
    
    def get_agent(self) -> MCPAgent:
        """
        Create and return the Calculator MCPAgent.
        
        Returns:
            MCPAgent: Configured agent with Calculator MCP server connection
        """
        return self._agent
    
    
    def _get_calculator_instructions(self,prompt_name,prompt_arguments) -> str:
        """
        Get the system instructions for the Calculator Agent.
        
        Returns:
            str: System instructions for mathematical operations
        """
        
        
        return """
        You are a Calculator Agent with access to mathematical operation tools through an MCP server.

        Your capabilities include:
        
        1. MATHEMATICAL OPERATIONS:
           - Addition: Use Calculator_add(a, b) to add two numbers
           - Subtraction: Use Calculator_subtract(a, b) to subtract two numbers
           - Multiplication: Use Calculator_multiply(a, b) to multiply two numbers
           - Division: Use Calculator_divide(a, b) to divide two numbers
        
        2. CALCULATION HISTORY:
           - Access calculation history through the calculation://history resource
           - Keep track of operations performed
        
        3. BEST PRACTICES:
           - Always use the MCP tools for calculations rather than doing math manually
           - Handle division by zero gracefully by checking inputs
           - Provide clear explanations of the calculations performed
           - Show step-by-step work for complex calculations
           
        4. ERROR HANDLING:
           - If a calculation fails, explain what went wrong
           - Suggest alternative approaches when appropriate
           - Validate inputs before performing operations
           
        When users ask for calculations, break down complex problems into simple operations
        and use the available tools to perform each step. Always show your work and 
        provide clear, accurate results.
        """
    
    async def initialize_agent(self) -> MCPAgent:
        """
        Initialize the agent and establish MCP server connections.
        
        Returns:
            MCPAgent: The initialized agent with active connections
        """
        self._agent = MCPAgent(
            name="Calculator Agent",
            model=self.model,
            mcp_clients=[],  # Will be added after creation
            auto_discover_capabilities=True
        )

       
        # Create and add the calculator MCP client configuration
        calculator_config = create_stdio_mcp_config(
            name="Calculator",
            command=self.python_executable,
            args=[self.server_script_path],
            env=None,
            cwd=str(current_dir)
        )
        
        # Add the MCP client to the agent
        await self._agent.add_mcp_client(calculator_config, prompt_name="calculator_prompt", arguments={})

       
        
        # Connect to all MCP servers
        connection_results = await self._agent.connect_all_clients()

        await self._agent.get_mcp_prompt(prompt_name="calculator_prompt",arguments={})

        
        if not connection_results.get("Calculator", False):
            raise RuntimeError("Failed to connect to Calculator MCP server")
            
        return self._agent


# Convenience function for creating a calculator agent
def create_calculator_agent(model: str = "gpt-4", 
                          server_script_path: Optional[str] = None,
                          python_executable: Optional[str] = None) -> CalculatorAgentCreator:
    """
    Convenience function to create a Calculator Agent Creator.
    
    Args:
        model (str): The language model to use
        server_script_path (str, optional): Path to the calculator server script
        python_executable (str, optional): Python executable to use for running the server
        
    Returns:
        CalculatorAgentCreator: The configured creator instance
    """
    return CalculatorAgentCreator(model=model, server_script_path=server_script_path, python_executable=python_executable)


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def demo():
        """Demonstrate the Calculator Agent."""
        try:
            # Create the calculator agent creator
            creator = create_calculator_agent()
            
            print("Creating Calculator Agent...")
            print(creator.get_agent_briefing())
            
            # Initialize the agent with MCP connections
            agent = await creator.initialize_agent()
            
            print(f"✅ {creator.agent_name} created successfully!")
            print(f"Connected MCP servers: {list(agent.get_connection_status().keys())}")
            
            # List available tools
            tools = agent.list_available_tools()
            print(f"Available tools: {[tool.name for tool in tools]}")
            
            # Example calculation using MCP tools
            print("\n🧮 Testing calculator functionality...")
            result = await agent.call_mcp_tool("add", {"a": 5, "b": 3})
            print(f"5 + 3 = {result}")
            
            result = await agent.call_mcp_tool("multiply", {"a": 4, "b": 7})
            print(f"4 × 7 = {result}")
            
            # Cleanup
            await agent.disconnect_all_clients()
            print("✅ Demo completed successfully!")
            
        except Exception as e:
            print(f"❌ Error during demo: {e}")
            import traceback
            traceback.print_exc()
    
    # Run the demo
    asyncio.run(demo())
