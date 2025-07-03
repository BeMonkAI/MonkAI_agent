import mcp
from mcp.client.streamable_http import streamablehttp_client
import json
import base64


import asyncio
from monkai_agent import AgentManager,MCPAgent, create_http_mcp_config
from monkai_agent.repl import pretty_print_messages

config = {
  "mem0ApiKey": "YOUR MEM0_API_KEY",  # Replace with your actual MEM0 API key
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
        name="Memory_MCP_Server", #Remember to name your mcp client without spaces
        url=url,
    )
    
    # Add the MCP client to the agent
    await memory_agent.add_mcp_client(mcp_config)

    # Connect to all MCP servers
    connection_results = await memory_agent.connect_all_clients()

    if not connection_results.get("Memory_MCP_Server", False):
        raise RuntimeError("Failed to connect to MCP server")

    return memory_agent


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def demo():
        try:
            # Initialize the agent
            agent = await initialize_agent()
            manager = AgentManager(api_key="YOUR OPENAI API KEY")
            result = await manager.run("Quais memórias estão armazenadas? para o user123", agent=agent)
            pretty_print_messages(result.messages)
            await agent.disconnect_all_clients()
            
        except Exception as e:
            print(f"❌ Error during demo: {e}")
    
    # Run the demo
    asyncio.run(demo())