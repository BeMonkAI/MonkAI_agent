import mcp
from mcp.client.streamable_http import streamablehttp_client
import json
import base64

import asyncio
from monkai_agent import MCPAgent, create_http_mcp_config

config = {
  "notionApiKey": "ntn_G58331265171w7qi1FgInrsHUnFkLTDBadzD8fItVYZg4H"
}
# Encode config in base64
config_b64 = base64.b64encode(json.dumps(config).encode()).decode()
smithery_api_key = "55b454e4-186b-403d-a356-b2c86014428b"

# Create server URL
url = f"https://server.smithery.ai/@smithery/notion/mcp?config={config_b64}&api_key={smithery_api_key}"



notion_agent=MCPAgent(
    name="Notion manager Agent",
    instructions="""You are an Agent that is connected to the users Notion server, when requested
    you can query and list the databases in the users Notion account as well as perform operations 
    such as creating new databases. 
    """,
    model="gpt-4o"
)

async def initialize_agent() -> MCPAgent:

    mcp_config = create_http_mcp_config(
        name="Notion MCP Server",
        url=url,
    )
    
    # Add the MCP client to the agent
    await notion_agent.add_mcp_client(mcp_config)
    
    # Connect to all MCP servers
    connection_results = await notion_agent.connect_all_clients()

    if not connection_results.get("Notion MCP Server", False):
        raise RuntimeError("Failed to connect to MCP server")

    return notion_agent


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

            #list notion databases
            result = await agent.call_mcp_tool("list-databases",
                server_name="Notion MCP Server")
            
            # Print the result
            print(f"Result: {result[0].text}")

            await agent.disconnect_all_clients()
            
        except Exception as e:
            print(f"❌ Error during demo: {e}")
    
    # Run the demo
    asyncio.run(demo())
