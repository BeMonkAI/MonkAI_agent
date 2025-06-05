"""
MCP Agent - Model Context Protocol Agent

This module implements the MCPAgent class which extends the base Agent class
to integrate with MCP (Model Context Protocol) clients. It allows agents to
access tools, resources, and prompts from MCP servers.

The MCPAgent can connect to multiple MCP servers simultaneously and provides
a unified interface for accessing their capabilities.
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional, Union, AsyncGenerator
from pathlib import Path

from pydantic import BaseModel, Field
from httpx import Auth
# MCP imports
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.streamable_http import streamablehttp_client
from mcp.client.session import ClientSession
from mcp.types import (
    Resource,
    Tool,
    Prompt,
    CallToolRequest,
    GetPromptRequest,
    CallToolResult
)

from .types import Agent

logger = logging.getLogger(__name__)


class MCPClientConfig(BaseModel):
    """Configuration for an MCP client connection."""
    
    model_config = {"arbitrary_types_allowed": True}
    
    name: str
    """Name identifier for this MCP client connection."""
    
    connection_type: str = Field(default="stdio", pattern="^(stdio|sse|http)$")
    """Type of connection: 'stdio', 'sse', or 'http'."""
    
    # Stdio-specific configuration
    command: Optional[str] = None
    """Command to execute for stdio connections."""
    
    args: List[str] = Field(default_factory=list)
    """Arguments for the stdio command."""
    
    env: Optional[Dict[str, str]] = None
    """Environment variables for stdio connections."""
    
    cwd: Optional[Union[str, Path]] = None
    """Working directory for stdio connections."""
    
    # SSE/HTTP-specific configuration
    url: Optional[str] = None
    """URL for SSE or HTTP connections."""
    
    headers: Optional[Dict[str, Any]] = None
    """Headers for SSE or HTTP connections."""
    
    timeout: float = 30.0
    """Connection timeout in seconds."""

    auth: Optional[Auth] = None


class MCPClientConnection(BaseModel):
    """Represents an active MCP client connection."""
    
    model_config = {"arbitrary_types_allowed": True}
    
    config: MCPClientConfig
    """Configuration used for this connection."""
    
    session: Optional[ClientSession] = None
    """Active client session."""
    
    # Store the context managers to keep connections alive
    _stdio_streams: Optional[Any] = None
    _sse_streams: Optional[Any] = None
    _http_streams: Optional[Any] = None
    
    is_connected: bool = False
    """Whether the connection is currently active."""
    
    available_tools: List[Tool] = Field(default_factory=list)
    """Tools available from this MCP server."""
    
    available_resources: List[Resource] = Field(default_factory=list)
    """Resources available from this MCP server."""

    available_prompts: List[Prompt] = Field(default_factory=list)
    """Prompts available from this MCP server."""
    

class MCPAgent(Agent):
    """
    MCP-enabled Agent that can connect to and interact with MCP servers.
    
    This agent extends the base Agent class with the ability to connect to
    multiple MCP servers and access their tools, resources, and prompts.
    """
    
    mcp_clients: List[MCPClientConnection] = Field(default_factory=list)
    """List of MCP client connections."""
    
    auto_discover_capabilities: bool = True
    """Whether to automatically discover server capabilities on connection."""
    
    
    async def add_mcp_client(self, config: MCPClientConfig) -> MCPClientConnection:
        """
        Add a new MCP client connection.
        
        Args:
            config: Configuration for the MCP client
            
        Returns:
            MCPClientConnection: The created connection object
        """
        connection = MCPClientConnection(config=config)
        self.mcp_clients.append(connection)
        
        if self.auto_discover_capabilities:
            await self._connect_client(connection)
            
        return connection
    
    async def _connect_client(self, connection: MCPClientConnection) -> bool:
        """
        Establish connection to an MCP server.
        
        Args:
            connection: The client connection to establish
            
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            config = connection.config
            
            if config.connection_type == "stdio":
                if not config.command:
                    raise ValueError(f"Command required for stdio connection: {config.name}")
                    
                server_params = StdioServerParameters(
                    command=config.command,
                    args=config.args or [],
                    env=config.env,
                    cwd=config.cwd
                )
                
                # Keep the context manager alive by storing it
                connection._stdio_streams = stdio_client(server_params)
                streams = await connection._stdio_streams.__aenter__()
                read_stream, write_stream = streams
                
                # Create and store session
                connection.session = ClientSession(read_stream, write_stream)
                await connection.session.__aenter__()
                connection.is_connected = True
                
                # Initialize the session
                init_result = await connection.session.initialize()
                logger.info(f"Connected to MCP server '{config.name}': {init_result}")
                
                # Discover capabilities
                if self.auto_discover_capabilities:
                    await self._discover_capabilities(connection)
                    
                return True
                        
            elif config.connection_type == "sse":
                if not config.url:
                    raise ValueError(f"URL required for SSE connection: {config.name}")
                    
                connection._sse_streams = sse_client(
                    url=config.url,
                    headers=config.headers,
                    timeout=config.timeout
                )
                streams = await connection._sse_streams.__aenter__()
                read_stream, write_stream = streams
                
                connection.session = ClientSession(read_stream, write_stream)
                await connection.session.__aenter__()
                connection.is_connected = True
                
                # Initialize the session
                init_result = await connection.session.initialize()
                logger.info(f"Connected to MCP server '{config.name}': {init_result}")
                
                # Discover capabilities
                if self.auto_discover_capabilities:
                    await self._discover_capabilities(connection)
                    
                return True
            
            elif config.connection_type == "http":
                if not config.url:
                    raise ValueError(f"URL required for HTTP connection: {config.name}")
                    
                connection._http_streams = streamablehttp_client(
                    url=config.url,
                    headers=config.headers, 
                    auth=config.auth, 
                    timeout=config.timeout
                )
                streams = await connection._http_streams.__aenter__()
                read_stream, write_stream, _ = streams  
                
                connection.session = ClientSession(read_stream, write_stream)
                await connection.session.__aenter__()
                connection.is_connected = True              
                
                # Initialize the session
                init_result = await connection.session.initialize()
                logger.info(f"Connected to MCP server '{config.name}': {init_result}")
                
                # Discover capabilities
                if self.auto_discover_capabilities:
                    await self._discover_capabilities(connection)
                    
                return True
            else:
                raise ValueError(f"Unsupported connection type: {config.connection_type}")
                
        except Exception as e:
            logger.error(f"Failed to connect to MCP server '{config.name}': {e}")
            connection.is_connected = False
            return False
    
    async def _discover_capabilities(self, connection: MCPClientConnection) -> None:
        """
        Discover available tools, resources, and prompts from an MCP server.
        
        Args:
            connection: The client connection to query
        """
        if not connection.session or not connection.is_connected:
            return
            
        try:
            # List available tools
            tools_response = await connection.session.list_tools()
            connection.available_tools = tools_response.tools
            logger.debug(f"Discovered {len(connection.available_tools)} tools from '{connection.config.name}'")
            
            # List available resources
            resources_response = await connection.session.list_resources()
            connection.available_resources = resources_response.resources
            logger.debug(f"Discovered {len(connection.available_resources)} resources from '{connection.config.name}'")
            
            # List available prompts
            prompts_response = await connection.session.list_prompts()
            connection.available_prompts = prompts_response.prompts
            logger.debug(f"Discovered {len(connection.available_prompts)} prompts from '{connection.config.name}'")
            
        except Exception as e:
            logger.error(f"Failed to discover capabilities from '{connection.config.name}': {e}")
    
    @staticmethod
    def extract_tool_result_content(result_content) -> str:
        """
        Extract the content from a CallToolResult content object and return it as a string.
        
        Args:
            result: The CallToolResult content object to extract content from
            
        Returns:
            str: The extracted content as a string
        """
        if not result_content:
            return ""
        
        content_parts = []
        
        for content_item in result_content:
            if hasattr(content_item, 'type'):
                if content_item.type == "text":
                    content_parts.append(content_item.text)
                elif content_item.type == "image":
                    # For images, include a description with the mime type
                    content_parts.append(f"[Image: {content_item.mimeType}]")
                elif content_item.type == "resource":
                    # Handle embedded resources
                    if hasattr(content_item.resource, 'text'):
                        content_parts.append(content_item.resource.text)
                    elif hasattr(content_item.resource, 'blob'):
                        content_parts.append(f"[Binary Resource: {content_item.resource.mimeType or 'unknown'}]")
            else:
                # Fallback: convert to string if type not recognized
                content_parts.append(str(content_item))
        
        return "\n".join(content_parts)

    async def call_mcp_tool(self, tool_name: str, arguments: Dict[str, Any], server_name: Optional[str] = None) -> Any:
        """
        Call a tool from an MCP server.
        
        Args:
            tool_name: Name of the tool to call
            arguments: Arguments to pass to the tool
            server_name: Optional server name to target. If None, searches all servers.
            
        Returns:
            The result from the tool call
            
        Raises:
            ValueError: If tool not found or server not connected
        """
        target_connection = None
        
        if server_name:
            # Look for specific server
            target_connection = next(
                (conn for conn in self.mcp_clients if conn.config.name == server_name),
                None
            )
            if not target_connection:
                raise ValueError(f"MCP server '{server_name}' not found")
        else:
            # Search all connected servers for the tool
            for connection in self.mcp_clients:
                if connection.is_connected:
                    tool_exists = any(tool.name == tool_name for tool in connection.available_tools)
                    if tool_exists:
                        target_connection = connection
                        break
        
        if not target_connection or not target_connection.is_connected:
            raise ValueError(f"Tool '{tool_name}' not found in any connected MCP server")
        
        # Add connection health check
        if not target_connection.session:
            logger.warning(f"Session is None for server '{target_connection.config.name}', attempting to reconnect")
            success = await self._connect_client(target_connection)
            if not success:
                raise ValueError(f"Failed to reconnect to MCP server '{target_connection.config.name}'")
        
        try:
            # Check if session is still valid before calling
            if hasattr(target_connection.session, '_closed') and target_connection.session._closed:
                logger.warning(f"Session is closed for server '{target_connection.config.name}', attempting to reconnect")
                success = await self._connect_client(target_connection)
                if not success:
                    raise ValueError(f"Failed to reconnect to MCP server '{target_connection.config.name}'")
            
            result = await target_connection.session.call_tool(name=tool_name, arguments=arguments)
            return result.content
        except Exception as e:
            logger.error(f"Failed to call tool '{tool_name}': {e}")
            # Mark connection as closed and attempt to reconnect      
            raise e
        
    async def get_mcp_resource(self, resource_uri: str, server_name: Optional[str] = None) -> Any:
        """
        Get a resource from an MCP server.
        
        Args:
            resource_uri: URI of the resource to retrieve
            server_name: Optional server name to target. If None, searches all servers.
            
        Returns:
            The resource content
            
        Raises:
            ValueError: If resource not found or server not connected
        """
        target_connection = None
        
        if server_name:
            # Look for specific server
            target_connection = next(
                (conn for conn in self.mcp_clients if conn.config.name == server_name),
                None
            )
            if not target_connection:
                raise ValueError(f"MCP server '{server_name}' not found")
        else:
            # Search all connected servers for the resource
            for connection in self.mcp_clients:
                if connection.is_connected:
                    resource_exists = any(resource.uri == resource_uri for resource in connection.available_resources)
                    if resource_exists:
                        target_connection = connection
                        break
        
        if not target_connection or not target_connection.is_connected:
            raise ValueError(f"Resource '{resource_uri}' not found in any connected MCP server")
        
        try:
            #request = GetResourceRequest(uri=resource_uri)
            result = await target_connection.session.read_resource(resource_uri)
            return ""
        except Exception as e:
            logger.error(f"Failed to get resource '{resource_uri}': {e}")
            raise
    
    async def get_mcp_prompt(self, prompt_name: str, arguments: Optional[Dict[str, Any]] = None, server_name: Optional[str] = None) -> Any:
        """
        Get a prompt from an MCP server.
        
        Args:
            prompt_name: Name of the prompt to retrieve
            arguments: Optional arguments for the prompt
            server_name: Optional server name to target. If None, searches all servers.
            
        Returns:
            The prompt content
            
        Raises:
            ValueError: If prompt not found or server not connected
        """
        target_connection = None
        
        if server_name:
            # Look for specific server
            target_connection = next(
                (conn for conn in self.mcp_clients if conn.config.name == server_name),
                None
            )
            if not target_connection:
                raise ValueError(f"MCP server '{server_name}' not found")
        else:
            # Search all connected servers for the prompt
            for connection in self.mcp_clients:
                if connection.is_connected:
                    prompt_exists = any(prompt.name == prompt_name for prompt in connection.available_prompts)
                    if prompt_exists:
                        target_connection = connection
                        break
        
        if not target_connection or not target_connection.is_connected:
            raise ValueError(f"Prompt '{prompt_name}' not found in any connected MCP server")
        
        try:
            request = GetPromptRequest(name=prompt_name, arguments=arguments or {})
            result = await target_connection.session.get_prompt(request)
            return result.messages
        except Exception as e:
            logger.error(f"Failed to get prompt '{prompt_name}': {e}")
            raise
    
    def list_available_tools(self, server_name: Optional[str] = None) -> List[Tool]:
        """
        List all available tools from connected MCP servers.
        
        Args:
            server_name: Optional server name to filter by
            
        Returns:
            List of available tools
        """
        tools = []
        for connection in self.mcp_clients:
            if server_name and connection.config.name != server_name:
                continue
            if connection.is_connected:
                tools.extend(connection.available_tools)
        return tools
    
    def list_available_resources(self, server_name: Optional[str] = None) -> List[Resource]:
        """
        List all available resources from connected MCP servers.
        
        Args:
            server_name: Optional server name to filter by
            
        Returns:
            List of available resources
        """
        resources = []
        for connection in self.mcp_clients:
            if server_name and connection.config.name != server_name:
                continue
            if connection.is_connected:
                resources.extend(connection.available_resources)
        return resources
    
    def list_available_prompts(self, server_name: Optional[str] = None) -> List[Prompt]:
        """
        List all available prompts from connected MCP servers.
        
        Args:
            server_name: Optional server name to filter by
            
        Returns:
            List of available prompts
        """
        prompts = []
        for connection in self.mcp_clients:
            if server_name and connection.config.name != server_name:
                continue
            if connection.is_connected:
                prompts.extend(connection.available_prompts)
        return prompts
    
    async def connect_all_clients(self) -> Dict[str, bool]:
        """
        Connect to all configured MCP servers.
        
        Returns:
            Dict mapping server names to connection success status
        """
        results = {}
        for connection in self.mcp_clients:
            if not connection.is_connected:
                success = await self._connect_client(connection)
                results[connection.config.name] = success
            else:
                results[connection.config.name] = True
        return results
    
    async def disconnect_all_clients(self) -> None:
        """Disconnect from all MCP servers."""
        for connection in self.mcp_clients:
            if connection.is_connected:
                try:
                    # Close the session first
                    if connection.session:
                        await connection.session.__aexit__(None, None, None)
                        connection.session = None
                    
                    # Close the stream context managers
                    if connection._stdio_streams:
                        await connection._stdio_streams.__aexit__(None, None, None)
                        connection._stdio_streams = None
                    
                    if connection._sse_streams:
                        await connection._sse_streams.__aexit__(None, None, None)
                        connection._sse_streams = None
                        
                    if connection._http_streams:
                        await connection._http_streams.__aexit__(None, None, None)
                        connection._http_streams = None
                    
                    connection.is_connected = False
                    logger.info(f"Disconnected from MCP server '{connection.config.name}'")
                    
                except Exception as e:
                    logger.error(f"Error disconnecting from '{connection.config.name}': {e}")
                    connection.is_connected = False
    
    def get_connection_status(self) -> Dict[str, Dict[str, Any]]:
        """
        Get the status of all MCP client connections.
        
        Returns:
            Dict with connection status information
        """
        status = {}
        for connection in self.mcp_clients:
            status[connection.config.name] = {
                "connected": connection.is_connected,
                "connection_type": connection.config.connection_type,
                "tools_count": len(connection.available_tools),
                "resources_count": len(connection.available_resources),
                "prompts_count": len(connection.available_prompts)
            }
        return status


# Convenience functions for creating MCP agent configurations

def create_stdio_mcp_config(name: str, command: str, args: List[str] = None, **kwargs) -> MCPClientConfig:
    """
    Create an MCP client configuration for stdio connections.
    
    Args:
        name: Name for the client connection
        command: Command to execute
        args: Optional command arguments
        **kwargs: Additional configuration options
        
    Returns:
        MCPClientConfig: Configuration object
    """
    return MCPClientConfig(
        name=name,
        connection_type="stdio",
        command=command,
        args=args or [],
        **kwargs
    )


def create_sse_mcp_config(name: str, url: str, headers: Dict[str, Any] = None, **kwargs) -> MCPClientConfig:
    """
    Create an MCP client configuration for SSE connections.
    
    Args:
        name: Name for the client connection
        url: SSE endpoint URL
        headers: Optional headers
        **kwargs: Additional configuration options
        
    Returns:
        MCPClientConfig: Configuration object
    """
    return MCPClientConfig(
        name=name,
        connection_type="sse",
        url=url,
        headers=headers or {},
        **kwargs
    )
