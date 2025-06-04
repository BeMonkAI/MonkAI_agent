"""
Integration example showing MCPAgent with MonkAI AgentManager

This example demonstrates how to use MCPAgent within the existing
MonkAI agent framework, including integration with AgentManager.
"""

import asyncio
import logging
from typing import Dict, Any

from monkai_agent import (
    MCPAgent, 
    AgentManager, 
    create_stdio_mcp_config,
    Response,
    Result
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPAgentManager(AgentManager):
    """
    Extended AgentManager that can handle MCPAgent instances.
    
    This manager ensures that MCP connections are properly managed
    throughout the agent lifecycle.
    """
    
    async def prepare_mcp_agent(self, agent: MCPAgent) -> None:
        """Prepare an MCPAgent by connecting to all its MCP servers."""
        if isinstance(agent, MCPAgent):
            logger.info(f"Connecting MCP clients for agent: {agent.name}")
            results = await agent.connect_all_clients()
            
            for server_name, success in results.items():
                if success:
                    logger.info(f"✓ Connected to MCP server: {server_name}")
                else:
                    logger.warning(f"✗ Failed to connect to MCP server: {server_name}")
    
    async def cleanup_mcp_agent(self, agent: MCPAgent) -> None:
        """Clean up MCP connections for an MCPAgent."""
        if isinstance(agent, MCPAgent):
            logger.info(f"Disconnecting MCP clients for agent: {agent.name}")
            await agent.disconnect_all_clients()
    
    async def run_with_mcp_support(
        self, 
        agent: MCPAgent, 
        messages: list, 
        context_variables: Dict[str, Any] = None
    ) -> Response:
        """
        Run an MCPAgent with proper MCP connection management.
        
        This method ensures MCP connections are established before running
        and cleaned up afterwards.
        """
        try:
            # Prepare MCP connections
            await self.prepare_mcp_agent(agent)
            
            # Run the agent (you would integrate this with your existing run method)
            # This is a simplified version - integrate with your actual AgentManager.run()
            response = await self._run_agent_with_mcp(agent, messages, context_variables or {})
            
            return response
            
        finally:
            # Clean up MCP connections
            await self.cleanup_mcp_agent(agent)
    
    async def _run_agent_with_mcp(
        self, 
        agent: MCPAgent, 
        messages: list, 
        context_variables: Dict[str, Any]
    ) -> Response:
        """
        Internal method to run the agent with MCP capabilities.
        
        This would integrate with your existing agent execution logic,
        but now the agent can call MCP tools, access resources, etc.
        """
        # This is where you'd integrate with your existing agent execution
        # For now, this is a placeholder showing the concept
        
        # The agent can now use MCP tools in its execution
        available_tools = agent.list_available_tools()
        available_resources = agent.list_available_resources()
        
        logger.info(f"Agent has access to {len(available_tools)} MCP tools")
        logger.info(f"Agent has access to {len(available_resources)} MCP resources")
        
        # Your existing agent execution logic would go here
        # The key difference is that the agent can now call:
        # - await agent.call_mcp_tool(tool_name, arguments)
        # - await agent.get_mcp_resource(resource_uri)
        # - await agent.get_mcp_prompt(prompt_name, arguments)
        
        return Response(
            messages=messages,
            agent=agent,
            context_variables=context_variables
        )


async def example_research_agent_with_mcp():
    """
    Example of a research agent that uses MCP servers for data access.
    """
    
    # Create an MCPAgent configured as a research assistant
    research_agent = MCPAgent(
        name="Research Assistant",
        model="gpt-4",
        instructions="""You are a research assistant with access to various data sources through MCP servers.
        
        You can:
        1. Search databases and knowledge bases
        2. Access document repositories
        3. Use analysis tools
        4. Generate reports
        
        Always cite your sources and explain how you obtained information.""",
        auto_discover_capabilities=True
    )
    
    # Configure MCP servers for different data sources
    mcp_configs = [
        # Database search server
        create_stdio_mcp_config(
            name="database_search",
            command="python",
            args=["database_mcp_server.py"]
        ),
        
        # Document repository server
        create_stdio_mcp_config(
            name="document_repo",
            command="python", 
            args=["documents_mcp_server.py"]
        ),
        
        # Analysis tools server
        create_stdio_mcp_config(
            name="analysis_tools",
            command="python",
            args=["analysis_mcp_server.py"]
        )
    ]
    
    # Add MCP clients to the agent
    for config in mcp_configs:
        await research_agent.add_mcp_client(config)
    
    # Create the MCP-aware agent manager
    manager = MCPAgentManager()
    
    # Example research query
    messages = [
        {"role": "user", "content": "Research the latest trends in AI development and create a summary report."}
    ]
    
    try:
        # Run the agent with MCP support
        response = await manager.run_with_mcp_support(
            research_agent, 
            messages,
            context_variables={"research_depth": "comprehensive", "output_format": "report"}
        )
        
        logger.info("Research completed successfully")
        return response
        
    except Exception as e:
        logger.error(f"Research failed: {e}")
        raise


async def example_multi_agent_mcp_workflow():
    """
    Example showing multiple agents using different MCP servers in a workflow.
    """
    
    # Data collection agent
    data_collector = MCPAgent(
        name="Data Collector",
        model="gpt-4",
        instructions="Collect and validate data from various sources.",
        auto_discover_capabilities=True
    )
    
    # Add data source MCP server
    await data_collector.add_mcp_client(create_stdio_mcp_config(
        name="data_sources",
        command="python",
        args=["data_collection_server.py"]
    ))
    
    # Analysis agent  
    analyst = MCPAgent(
        name="Data Analyst",
        model="gpt-4",
        instructions="Analyze data and generate insights.",
        auto_discover_capabilities=True
    )
    
    # Add analysis tools MCP server
    await analyst.add_mcp_client(create_stdio_mcp_config(
        name="analysis_tools",
        command="python",
        args=["analysis_tools_server.py"]
    ))
    
    # Report generator agent
    reporter = MCPAgent(
        name="Report Generator", 
        model="gpt-4",
        instructions="Generate comprehensive reports from analysis results.",
        auto_discover_capabilities=True
    )
    
    # Add reporting tools MCP server
    await reporter.add_mcp_client(create_stdio_mcp_config(
        name="reporting_tools",
        command="python",
        args=["reporting_server.py"]
    ))
    
    manager = MCPAgentManager()
    
    try:
        # Step 1: Data collection
        logger.info("Step 1: Collecting data...")
        collection_response = await manager.run_with_mcp_support(
            data_collector,
            [{"role": "user", "content": "Collect sales data for Q4 2024"}]
        )
        
        # Step 2: Data analysis
        logger.info("Step 2: Analyzing data...")
        analysis_response = await manager.run_with_mcp_support(
            analyst,
            [{"role": "user", "content": "Analyze the collected sales data for trends and patterns"}],
            context_variables={"input_data": "sales_data_q4_2024"}
        )
        
        # Step 3: Report generation
        logger.info("Step 3: Generating report...")
        report_response = await manager.run_with_mcp_support(
            reporter,
            [{"role": "user", "content": "Generate a comprehensive Q4 sales report"}],
            context_variables={"analysis_results": "q4_trends_analysis"}
        )
        
        logger.info("Multi-agent workflow completed successfully")
        return report_response
        
    except Exception as e:
        logger.error(f"Workflow failed: {e}")
        raise


async def example_mcp_agent_function_integration():
    """
    Example showing how MCP capabilities can be wrapped as agent functions.
    """
    
    # Create an MCPAgent
    agent = MCPAgent(
        name="Tool Integration Agent",
        model="gpt-4", 
        instructions="You have access to both local and remote tools.",
        auto_discover_capabilities=True
    )
    
    # Add MCP server
    await agent.add_mcp_client(create_stdio_mcp_config(
        name="external_tools",
        command="python",
        args=["external_tools_server.py"]
    ))
    
    # Connect to MCP servers
    await agent.connect_all_clients()
    
    # Define wrapper functions that use MCP capabilities
    async def search_database(query: str) -> Result:
        """Search the external database using MCP tools."""
        try:
            result = await agent.call_mcp_tool("database_search", {"query": query})
            return Result(
                value=f"Search results: {result}",
                context_variables={"last_search": query}
            )
        except Exception as e:
            return Result(
                value=f"Search failed: {e}",
                context_variables={"error": str(e)}
            )
    
    async def get_document(doc_id: str) -> Result:
        """Retrieve a document using MCP resources."""
        try:
            content = await agent.get_mcp_resource(f"document://{doc_id}")
            return Result(
                value=f"Document content: {content}",
                context_variables={"retrieved_doc": doc_id}
            )
        except Exception as e:
            return Result(
                value=f"Document retrieval failed: {e}",
                context_variables={"error": str(e)}
            )
    
    async def generate_analysis_prompt(topic: str) -> Result:
        """Generate an analysis prompt using MCP prompts."""
        try:
            prompt = await agent.get_mcp_prompt("analysis_template", {"topic": topic})
            return Result(
                value=f"Generated prompt: {prompt}",
                context_variables={"prompt_topic": topic}
            )
        except Exception as e:
            return Result(
                value=f"Prompt generation failed: {e}",
                context_variables={"error": str(e)}
            )
    
    # Add these MCP-wrapper functions to the agent
    agent.functions.extend([search_database, get_document, generate_analysis_prompt])
    
    logger.info("Agent now has access to MCP capabilities through wrapped functions")
    logger.info(f"Total functions available: {len(agent.functions)}")
    
    # Clean up
    await agent.disconnect_all_clients()


if __name__ == "__main__":
    # Example usage
    print("MCP Agent Integration Examples")
    print("="*50)
    
    # Uncomment to run specific examples:
    # asyncio.run(example_research_agent_with_mcp())
    # asyncio.run(example_multi_agent_mcp_workflow())
    # asyncio.run(example_mcp_agent_function_integration())
    
    print("Examples are ready. Uncomment the desired example to run.")
