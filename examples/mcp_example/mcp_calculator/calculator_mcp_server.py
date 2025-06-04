
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
