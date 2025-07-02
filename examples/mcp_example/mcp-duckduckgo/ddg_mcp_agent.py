import json
import base64
import sys
import os
import asyncio


from monkai_agent import MCPAgent, create_http_mcp_config


smithery_api_key = "55b454e4-186b-403d-a356-b2c86014428b"
url = f"https://server.smithery.ai/@nickclyde/duckduckgo-mcp-server/mcp?api_key={smithery_api_key}"


duckduckagent=MCPAgent(
    name="DuckDuckGo Search Agent",
    instructions="""You are a DuckDuckGo search Agent that can search the web for information when a user asks a question.
    You will use the DuckDuckGo MCP server to perform web searches and return relevant information to the user.
    """,
    model="gpt-4o",
    auto_discover_capabilities=True
)

async def initialize_agent() -> MCPAgent:

    mcp_config = create_http_mcp_config(
        name="DuckDuckGo MCP Server",
        url=url,
    )
    
    # Add the MCP client to the agent
    await duckduckagent.add_mcp_client(mcp_config)
    
    # Connect to all MCP servers
    connection_results = await duckduckagent.connect_all_clients()

    if not connection_results.get("DuckDuckGo MCP Server", False):
        raise RuntimeError("Failed to connect to MCP server")

    return duckduckagent


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def demo():
        try:
            # Initialize the agent
            agent = await initialize_agent()

            # List available tools
            tools = agent.list_available_tools()
            print(f"Available tools: {[tool.name for tool in tools]}")
            
            # Run a sample query
            query = "What is the weather like in New York City today?"

            result = await agent.call_mcp_tool("search",arguments={
                "query": query,},
                server_name="DuckDuckGo MCP Server")
            
            # Print the result
            print(f"Result: {result[0].text}")

            await agent.disconnect_all_clients()
            
        except Exception as e:
            print(f"❌ Error during demo: {e}")
    
    # Run the demo
    asyncio.run(demo())
