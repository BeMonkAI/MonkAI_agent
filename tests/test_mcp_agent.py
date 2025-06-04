"""
Basic test for MCPAgent functionality

This test verifies that the MCPAgent can be imported and basic functionality works.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../libs/monkai_agent'))

import asyncio
from monkai_agent import MCPAgent, create_stdio_mcp_config, create_sse_mcp_config, MCPClientConfig


def test_mcp_agent_creation():
    """Test that MCPAgent can be created successfully."""
    agent = MCPAgent(
        name="Test Agent",
        model="gpt-4",
        instructions="Test instructions"
    )
    
    assert agent.name == "Test Agent"
    assert agent.model == "gpt-4"
    assert agent.instructions == "Test instructions"
    assert agent.mcp_clients == []
    assert agent.auto_discover_capabilities == True


def test_mcp_client_config_creation():
    """Test MCP client configuration creation."""
    
    # Test stdio config
    stdio_config = create_stdio_mcp_config(
        name="test_stdio",
        command="python",
        args=["server.py"]
    )
    
    assert stdio_config.name == "test_stdio"
    assert stdio_config.connection_type == "stdio"
    assert stdio_config.command == "python"
    assert stdio_config.args == ["server.py"]
    
    # Test SSE config
    sse_config = create_sse_mcp_config(
        name="test_sse",
        url="https://example.com/mcp"
    )
    
    assert sse_config.name == "test_sse"
    assert sse_config.connection_type == "sse"
    assert sse_config.url == "https://example.com/mcp"


async def test_mcp_agent_client_management():
    """Test adding MCP clients to an agent."""
    agent = MCPAgent(
        name="Test Agent",
        model="gpt-4",
        auto_discover_capabilities=False  # Disable auto-discovery for testing
    )
    
    # Create a test config
    config = MCPClientConfig(
        name="test_client",
        connection_type="stdio",
        command="echo",
        args=["hello"]
    )
    
    # Add client (without connecting)
    connection = await agent.add_mcp_client(config)
    
    assert len(agent.mcp_clients) == 1
    assert connection.config.name == "test_client"
    assert connection.is_connected == False
    
    # Test connection status
    status = agent.get_connection_status()
    assert "test_client" in status
    assert status["test_client"]["connected"] == False
    assert status["test_client"]["connection_type"] == "stdio"


def test_mcp_agent_inheritance():
    """Test that MCPAgent properly inherits from Agent."""
    agent = MCPAgent(
        name="Inheritance Test",
        model="gpt-4",
        instructions="Test inheritance",
        parallel_tool_calls=False,
        external_content=True
    )
    
    # Test inherited properties
    assert agent.name == "Inheritance Test"
    assert agent.model == "gpt-4" 
    assert agent.instructions == "Test inheritance"
    assert agent.parallel_tool_calls == False
    assert agent.external_content == True
    
    # Test MCP-specific properties
    assert hasattr(agent, 'mcp_clients')
    assert hasattr(agent, 'auto_discover_capabilities')


def test_capability_listing():
    """Test listing capabilities from MCP clients."""
    agent = MCPAgent(name="Test Agent", model="gpt-4")
    
    # Initially should be empty
    assert agent.list_available_tools() == []
    assert agent.list_available_resources() == []
    assert agent.list_available_prompts() == []
    
    # Test with server name filter
    assert agent.list_available_tools(server_name="nonexistent") == []


async def test_mcp_config_validation():
    """Test MCP configuration validation."""
    
    # Valid stdio config
    valid_stdio = MCPClientConfig(
        name="valid_stdio",
        connection_type="stdio",
        command="python"
    )
    assert valid_stdio.connection_type == "stdio"
    
    # Valid SSE config  
    valid_sse = MCPClientConfig(
        name="valid_sse",
        connection_type="sse",
        url="https://example.com"
    )
    assert valid_sse.connection_type == "sse"
    
    # Test invalid connection type should raise validation error
    try:
        invalid_config = MCPClientConfig(
            name="invalid",
            connection_type="invalid_type"
        )
        assert False, "Should have raised validation error"
    except ValueError:
        pass  # Expected


def run_tests():
    """Run all tests."""
    print("Running MCPAgent tests...")
    
    # Run synchronous tests
    test_mcp_agent_creation()
    print("✓ MCPAgent creation test passed")
    
    test_mcp_client_config_creation()
    print("✓ MCP client config creation test passed")
    
    test_mcp_agent_inheritance()
    print("✓ MCPAgent inheritance test passed")
    
    test_capability_listing()
    print("✓ Capability listing test passed")
    
    # Run async tests
    asyncio.run(test_mcp_agent_client_management())
    print("✓ MCP client management test passed")
    
    asyncio.run(test_mcp_config_validation())
    print("✓ MCP config validation test passed")
    
    print("\nAll tests passed! ✓")


if __name__ == "__main__":
    run_tests()
