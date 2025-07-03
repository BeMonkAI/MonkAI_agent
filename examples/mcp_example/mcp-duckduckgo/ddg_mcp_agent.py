import json
import base64
import sys
import os
import asyncio


from monkai_agent import AgentManager,MCPAgent, create_http_mcp_config
from monkai_agent.repl import pretty_print_messages


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
        name="DuckDuckGo_MCP_Server", #Remember to name your mcp client without spaces
        url=url,
    )
    
    # Add the MCP client to the agent
    await duckduckagent.add_mcp_client(mcp_config)
    
    # Connect to all MCP servers
    connection_results = await duckduckagent.connect_all_clients()

    if not connection_results.get("DuckDuckGo_MCP_Server", False):
        raise RuntimeError("Failed to connect to MCP server")

    return duckduckagent


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def demo():
        try:
            # Initialize the agent
            agent = await initialize_agent()
            manager = AgentManager(api_key="YOUR OPENAI API KEY")
            result = await manager.run("Whats the weather like in new york?", agent=agent)
            pretty_print_messages(result.messages)
            await agent.disconnect_all_clients()
            
        except Exception as e:
            print(f"❌ Error during demo: {e}")
    
    # Run the demo
    asyncio.run(demo())
