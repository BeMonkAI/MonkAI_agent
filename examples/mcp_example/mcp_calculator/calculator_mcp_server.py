
"""
Simple Calculator MCP Server

This is a basic MCP server that provides calculator tools.
"""

from mcp.server import FastMCP

# Create an MCP server
mcp = FastMCP("Calculator")

import mcp.types as types

# Define available prompts

@mcp.prompt()
def calculator_prompt() -> types.Prompt:
    """Prompt for the Calculator Agent"""
    return types.Prompt(
        name="calculator",
        description="""
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
        """,
    )



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
