# 🔌 Model Context Protocol (MCP) Examples

This directory contains comprehensive examples demonstrating how to integrate MonkAI agents with various external services using the Model Context Protocol (MCP). MCP provides a standardized way for AI agents to connect to external tools, databases, and services, greatly expanding their capabilities.

## 🌟 What is Model Context Protocol (MCP)?

The Model Context Protocol is an open standard that enables secure connections between AI applications and external data sources and tools. It allows your MonkAI agents to:

- **Access external data** in real-time
- **Perform specialized operations** through external services
- **Maintain context** across different tools and systems
- **Scale capabilities** without rebuilding core agent logic

## 📁 Available Examples

### 🧮 [Calculator MCP](./mcp_calculator/)
**Integrate mathematical computation capabilities with your agents**

- **What it demonstrates**: Basic MCP server creation and mathematical operations
- **Key features**:
  - Addition, subtraction, multiplication, division
  - Safe calculation with error handling
  - Calculation history tracking
  - Natural language mathematical queries
- **Files**: `calculator_mcp_server.py`, `calculator_agent_creator.py`, `demo.py`
- **Difficulty**: ⭐ Beginner - Perfect introduction to MCP concepts

### 🔍 [DuckDuckGo Search](./mcp-duckduckgo/)
**Enable real-time web search capabilities for your agents**

- **What it demonstrates**: Integration with external APIs and real-time data access
- **Key features**:
  - Privacy-focused web search
  - Real-time information retrieval
  - Multiple result formats (web, news, images)
  - Natural language search queries
- **Files**: `ddg_mcp_agent.py`, configuration files
- **Difficulty**: ⭐⭐ Intermediate - External service integration
- **Requirements**: Internet connection, DuckDuckGo MCP server

### 💾 [Memory System](./mcp-memory/)
**Add persistent memory capabilities using Mem0 platform**

- **What it demonstrates**: Persistent context storage and advanced memory management
- **Key features**:
  - User-specific memory collections
  - Automatic memory capture and retrieval
  - Contextual continuity across conversations
  - Memory analytics and management
- **Files**: `mem0_mcp_agent.py`, configuration files
- **Difficulty**: ⭐⭐⭐ Advanced - Persistent state management
- **Requirements**: Mem0 API key, internet connection

### 📝 [Notion Integration](./mcp-notion/)
**Connect agents to Notion databases for data management**

- **What it demonstrates**: Database integration and document management
- **Key features**:
  - Query and search Notion databases
  - Create and manage pages
  - Database operations via natural language
  - Real-time workspace interaction
- **Files**: `notion_mcp_agent.py`, configuration files
- **Difficulty**: ⭐⭐⭐ Advanced - Database and API integration
- **Requirements**: Notion API key, configured Notion workspace

## 🎯 Learning Progression

### 1. **Start with Calculator** 🧮
Begin with the calculator example to understand:
- Basic MCP server setup
- Agent-to-MCP communication
- Function calling through MCP
- Error handling patterns

### 2. **Progress to DuckDuckGo** 🔍
Learn about external service integration:
- API-based MCP servers
- Real-time data fetching
- Handling dynamic responses
- Service reliability patterns

### 3. **Explore Memory System** 💾
Understand persistent state management:
- Context storage and retrieval
- User session management
- Long-term memory patterns
- Analytics and insights

### 4. **Master Notion Integration** 📝
Apply advanced concepts:
- Complex database operations
- Multi-step workflows
- Document and data management
- Production-ready integrations

## 🛠️ General Prerequisites

### Required for All Examples
```bash
# Activate virtual environment
source .venv/bin/activate

# Install MonkAI Agent
pip install monkai-agent

# Install MCP support (if not included)
pip install mcp
```

### API Keys Required
Different examples require different API keys:

- **Calculator**: No external APIs required
- **DuckDuckGo**: No API key required (uses public search)
- **Memory (Mem0)**: Mem0 API key required
- **Notion**: Notion API key and workspace access required

## 🚀 Quick Start Guide

### 1. Choose Your Example
Pick an example based on your learning goals and complexity preference.

### 2. Read the Specific README
Each example has detailed documentation in its subdirectory.

### 3. Set Up Prerequisites
Install required dependencies and configure API keys as needed.

### 4. Run the Demo
Each example includes a demo script to test functionality.

### 5. Customize and Experiment
Modify the examples to fit your specific use cases.

## 🏗️ Architecture Overview

All MCP examples follow a similar architectural pattern:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   MonkAI Agent  │    │   MCP Server    │    │ External Service│
│                 │    │                 │    │                 │
│  - Instructions │◄──►│ - Protocol      │◄──►│ - API/Database  │
│  - Functions    │    │ - Tools/Resources│    │ - Data Source   │
│  - Context      │    │ - Security      │    │ - Computation   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Key Components:
- **MonkAI Agent**: Your AI agent with specific instructions
- **MCP Server**: Standardized interface to external services
- **External Service**: The actual tool, API, or data source

## 🔧 Common Patterns

### Agent Creation Pattern
```python
from monkai_agent.mcp_agent import MCPAgent

# Create MCP-enabled agent
agent = MCPAgent(
    name="Your Agent Name",
    instructions="Agent behavior instructions",
    mcp_servers=["path/to/mcp/server"]
)
```

### Error Handling Pattern
```python
try:
    result = await agent.run("Your query")
    print(result)
except MCPConnectionError:
    print("MCP server connection failed")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 🐛 Troubleshooting

### Common Issues and Solutions

#### MCP Server Not Starting
```bash
# Check MCP server installation
pip list | grep mcp

# Restart with verbose logging
python your_mcp_server.py --verbose
```

#### Connection Timeouts
- Verify internet connection for external services
- Check API key validity and permissions
- Ensure MCP server ports are not blocked

#### Authentication Errors
- Verify API keys are correctly configured
- Check service-specific permission settings
- Ensure workspace access for database integrations

## 📚 Additional Resources

### MCP Protocol Documentation
- **Official MCP Specification**: [Model Context Protocol](https://modelcontextprotocol.io)
- **MCP Server Registry**: [Smithery.ai](https://smithery.ai)

### MonkAI Agent Documentation
- **Main Documentation**: `../../DOCUMENTATION.md`
- **Basic Examples**: `../agent_definition/`
- **Advanced Patterns**: `../creators_and_manager/`

### Community Resources
- **GitHub Issues**: Report bugs and request features
- **Example Contributions**: Submit your own MCP examples
- **Best Practices**: Share successful integration patterns

---

**💡 Pro Tip**: Start with the calculator example to understand MCP fundamentals, then gradually progress to more complex integrations. Each example builds upon concepts from previous ones, creating a comprehensive learning path for MCP mastery!
