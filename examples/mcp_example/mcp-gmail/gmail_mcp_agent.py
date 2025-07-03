import mcp
from mcp.client.streamable_http import streamablehttp_client
import json
import base64


import asyncio
from monkai_agent import AgentManager,MCPAgent, create_http_mcp_config
from monkai_agent.repl import pretty_print_messages

config = {
  "CLIENT_ID": "Your client ID here",
  "CLIENT_SECRET": "Your client secret here",
  "REFRESH_TOKEN": "Your refresh tioken here"
}
# Encode config in base64
config_b64 = base64.b64encode(json.dumps(config).encode()).decode()
smithery_api_key = "55b454e4-186b-403d-a356-b2c86014428b"

# Create server URL
url = f"https://server.smithery.ai/@shinzo-labs/gmail-mcp/mcp?config={config_b64}&api_key={smithery_api_key}"


gmail_agent=MCPAgent(
    name="Gmail Manager Agent",
    instructions=""" You are a Gmail manager Agent that can read and write emails when requested by the user.
    You can also search for emails based on the user's queries.
    """,
    model="gpt-4o"
)

async def initialize_agent() -> MCPAgent:

    mcp_config = create_http_mcp_config(
        name="Gmail_MCP_Server", #Remember to name your mcp client without spaces
        url=url,
    )
    
    # Add the MCP client to the agent
    await gmail_agent.add_mcp_client(mcp_config)

    # Connect to all MCP servers
    connection_results = await gmail_agent.connect_all_clients()

    if not connection_results.get("Gmail_MCP_Server", False):
        raise RuntimeError("Failed to connect to MCP server")

    return gmail_agent


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def demo():
        try:
            # Initialize the agent
            agent = await initialize_agent()
            '''tools= agent.list_available_tools()
            print(f"Available tools: {tools}")'''
            manager = AgentManager(api_key="Your openai API key here")
            result = await manager.run("Send any drafts I have", agent=agent)
            pretty_print_messages(result.messages)
            await agent.disconnect_all_clients()
            
        except Exception as e:
            print(f"❌ Error during demo: {e}")
    
    # Run the demo
    asyncio.run(demo())