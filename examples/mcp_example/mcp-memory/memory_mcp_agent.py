import mcp
from mcp.client.streamable_http import streamablehttp_client
import json
import base64


import asyncio
from monkai_agent import MCPAgent, create_http_mcp_config

config = {
  "mem0ApiKey": "m0-vN1o2nqZHuCClMD11aeI9z98EK4Kwm70vod9PCbi"
}
# Encode config in base64
config_b64 = base64.b64encode(json.dumps(config).encode()).decode()
smithery_api_key = "55b454e4-186b-403d-a356-b2c86014428b"

# Create server URL
url = f"https://server.smithery.ai/@mem0ai/mem0-memory-mcp/mcp?config={config_b64}&api_key={smithery_api_key}"

memory_agent=MCPAgent(
    name="Memory Manager Agent",
    instructions=""" You are a memory manager Agent that stores and retrieves user-specific memories to 
    maintain context and make informed decisions based on past interactions.
    """,
    model="gpt-4o"
)

async def initialize_agent() -> MCPAgent:

    mcp_config = create_http_mcp_config(
        name="Memory MCP Server",
        url=url,
    )
    
    # Add the MCP client to the agent
    await memory_agent.add_mcp_client(mcp_config)

    # Connect to all MCP servers
    connection_results = await memory_agent.connect_all_clients()

    if not connection_results.get("Memory MCP Server", False):
        raise RuntimeError("Failed to connect to MCP server")

    return memory_agent


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

            #insert a user memory 
            result = await agent.call_mcp_tool("add-memory",
                arguments={
                    "content": "I love to play football and I am a big fan of Manchester United.",
                    "userId": "user123"
                },
                server_name="Memory MCP Server")
            
            #Query users memory 
            result2 = await agent.call_mcp_tool("search-memories",
                arguments={
                    "query": "What team is the user a fan of?",
                    "userId": "user123"
                },
                server_name="Memory MCP Server")
            
            # Print the result
            print(f"Result: {result[0].text}")
            print(f"Memory Search Result: {result2[0].text}")

            await agent.disconnect_all_clients()
            
        except Exception as e:
            print(f"❌ Error during demo: {e}")
    
    # Run the demo
    asyncio.run(demo())