# 🔍 DuckDuckGo Search MCP Integration

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-green.svg)](https://modelcontextprotocol.io)
[![DuckDuckGo](https://img.shields.io/badge/DuckDuckGo-Search%20Engine-orange.svg)](https://duckduckgo.com)

> **Empower your AI agents with real-time web search capabilities through DuckDuckGo's privacy-focused search engine**

This example demonstrates how to integrate your MonkAI agents with DuckDuckGo's search engine using a Model Context Protocol server: https://smithery.ai/server/@nickclyde/duckduckgo-mcp-server , enabling your AI to access up-to-date information from the web while respecting user privacy.

## 🚀 What You Can Do

- 🌐 **Real-time web search** - Access current information from across the internet
- 🔒 **Privacy-focused** - Use DuckDuckGo's privacy-respecting search engine
- 📰 **Latest news and updates** - Get the most recent information on any topic
- 🎯 **Targeted searches** - Find specific information with intelligent query processing
- 📊 **Multiple result formats** - Access web pages, news, images, and more
- 🤖 **Natural language queries** - Ask questions in plain English and get relevant results

## 🛠️ Prerequisites

Before you start, make sure you have:

1. **MonkAI Agent Library** - Installed in your environment
2. **Python 3.10+** - For async/await support
3. **Internet connection** - For accessing the DuckDuckGo search API
4. **OpenAI API Key** - For the underlying language model

## 📋 Quick Setup

### 1. Install Dependencies

```bash
pip install monkai-agent
```

### 2. Configure Your API Key

Create a `config.py` file:

```python
# config.py
api_key = "your-openai-api-key"  # Your OpenAI API key
```

### 3. Run the Example

```bash
cd examples/mcp_example/mcp-duckduckgo
python ddg_mcp_agent.py
```

## 💡 How It Works

### Search Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   MonkAI Agent  │───▶│   MCP Server    │───▶│  DuckDuckGo API │
│  Search-Enabled │    │  (Smithery.ai)  │    │   Web Search    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                                              │
        │           🌐 Search Results                  │
        └──────────────────────────────────────────────┘
```

The integration provides three layers of search functionality:

1. **MonkAI Agent** - Your AI assistant with web search capabilities
2. **MCP Server** - Protocol bridge that handles search requests
3. **DuckDuckGo API** - Privacy-focused search engine with real-time results

### Code Breakdown

#### 1. Search-Enabled Agent Creation

```python
# Create an agent with web search capabilities
duckduckagent = MCPAgent(
    name="DuckDuckGo Search Agent",
    instructions="""You are a DuckDuckGo search Agent that can search the web 
    for information when a user asks a question. You will use the DuckDuckGo 
    MCP server to perform web searches and return relevant information to the user.""",
    model="gpt-4o",
    auto_discover_capabilities=True  # Automatically discover search tools
)
```

#### 2. MCP Search Server Connection

```python
async def initialize_agent() -> MCPAgent:
    # Configure search server connection
    mcp_config = create_http_mcp_config(
        name="DuckDuckGo_MCP_Server",
        url=duckduckgo_server_url,
    )
    
    # Connect to DuckDuckGo via MCP
    await duckduckagent.add_mcp_client(mcp_config)
    connection_results = await duckduckagent.connect_all_clients()
    
    return duckduckagent
```

#### 3. Natural Language Search Queries

```python
# Ask questions and get real-time web results
result = await manager.run(
    "What's the weather like in New York?", 
    agent=agent
)
```

## 🎮 Example Usage

### Basic Web Search

```python
import asyncio
from ddg_mcp_agent import initialize_agent
from monkai_agent import AgentManager

async def search_demo():
    # Initialize search-enabled agent
    agent = await initialize_agent()
    manager = AgentManager(api_key="your-openai-key")
    
    # Perform a web search
    result = await manager.run(
        "What are the latest developments in artificial intelligence?",
        agent=agent
    )
    
    print(result.messages[-1].content)
    await agent.disconnect_all_clients()

# Run the demo
asyncio.run(search_demo())
```

### Advanced Search Scenarios

```python
# Current events and news
await manager.run(
    "What's happening in the stock market today?",
    agent=agent
)

# Technical information
await manager.run(
    "Explain the latest Python 3.12 features and improvements",
    agent=agent
)

# Real-time data
await manager.run(
    "What's the current Bitcoin price and recent trends?",
    agent=agent
)

# Comparative research
await manager.run(
    "Compare the features of the latest iPhone vs Samsung Galaxy models",
    agent=agent
)

# Location-specific queries
await manager.run(
    "Find the best restaurants in Tokyo that are open right now",
    agent=agent
)
```

### Multi-Query Research

```python
# Comprehensive research on a topic
research_topics = [
    "What is quantum computing?",
    "Latest quantum computing breakthroughs 2024",
    "Companies leading in quantum computing research",
    "Quantum computing applications in finance"
]

for topic in research_topics:
    result = await manager.run(topic, agent=agent)
    print(f"\n--- {topic} ---")
    print(result.messages[-1].content)
```

## 🔧 Configuration Options

### Environment Variables

Create a `config.py` file:

```python
# config.py
api_key = "your-openai-api-key"  # Your OpenAI API key

# Optional: Configure search parameters
search_config = {
    "max_results": 10,          # Maximum search results to process
    "safe_search": "moderate",  # Safe search level: strict, moderate, off
    "region": "us-en",         # Search region and language
}
```

### Custom Search Parameters

```python
# Initialize agent with custom search behavior
duckduckagent = MCPAgent(
    name="Custom Search Agent",
    instructions="""You are a specialized search agent. When searching:
    1. Focus on recent information (last 6 months)
    2. Prioritize authoritative sources
    3. Provide source URLs for verification
    4. Summarize key findings clearly""",
    model="gpt-4o",
    auto_discover_capabilities=True
)
```

### Custom MCP Server

If you're running your own MCP server:

```python
# Point to your custom search server
url = "http://localhost:3000/mcp/duckduckgo"
```

## 🔍 Available Search Operations

The DuckDuckGo MCP server typically supports these operations:

| Operation | Description | Example Query |
|-----------|-------------|---------------|
| `search` | General web search | "Latest news about electric vehicles" |
| `fetch_content` | Get specific page content | "Get details from this news article URL" |
| `news_search` | Search for news articles | "Recent developments in renewable energy" |
| `image_search` | Find relevant images | "Photos of the Aurora Borealis" |
| `instant_answer` | Get quick facts | "What's the capital of Australia?" |

## 🎯 Search Best Practices

### 1. Effective Query Formulation
```python
# Good: Specific and clear
"Python web scraping libraries comparison 2024"

# Better: Include context
"Compare BeautifulSoup vs Scrapy for web scraping in Python, focusing on performance and ease of use"

# Best: Specify information type needed
"Find recent benchmarks comparing Python web scraping libraries, including performance metrics and learning curve"
```

### 2. Source Verification
```python
# Always ask for sources
await manager.run(
    "Find information about climate change effects on polar ice caps, and provide the sources for verification",
    agent=agent
)
```

### 3. Time-Sensitive Queries
```python
# Specify timeframe for current information
await manager.run(
    "What are the latest tech layoffs in 2024? Focus on information from the last 3 months",
    agent=agent
)
```

## 🌟 Advanced Features

### Smart Query Enhancement

The agent automatically enhances your queries for better search results:

```python
# Your query: "weather New York"
# Enhanced query: "current weather conditions New York City today forecast"

# Your query: "best restaurants"
# Enhanced query: "best restaurants near me highly rated 2024 reviews"
```

### Multi-Source Validation

```python
# Cross-reference information from multiple sources
await manager.run(
    "Research the safety of autonomous vehicles, cross-referencing multiple recent studies and reports",
    agent=agent
)
```

### Contextual Follow-up

```python
# The agent maintains context for follow-up questions
await manager.run("Tell me about machine learning", agent=agent)
await manager.run("What are the latest developments in this field?", agent=agent)  # Continues ML context
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Connection Failed
```
RuntimeError: Failed to connect to MCP server
```
**Solution**: Check your internet connection and verify the MCP server URL is accessible.

#### 2. No Search Results
```
Agent returns: "No results found for your query"
```
**Solution**: Try rephrasing your query or using different keywords. DuckDuckGo may have detected bot-like behavior.

#### 3. Rate Limiting
```
Search request failed due to rate limiting
```
**Solution**: Wait a few minutes between requests or implement request throttling.

#### 4. Blocked Searches
```
Search blocked by DuckDuckGo's bot detection
```
**Solution**: Vary your search patterns and avoid rapid successive searches on the same topic.

### Debug Mode

Enable verbose logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable MCP debug output
import os
os.environ["MCP_DEBUG"] = "1"
```

### Search Verification

```python
# Test search functionality
async def test_search():
    agent = await initialize_agent()
    manager = AgentManager(api_key=config.api_key)
    
    # Test with a simple query
    result = await manager.run("What is the current date?", agent=agent)
    
    if "2024" in result.messages[-1].content or "2025" in result.messages[-1].content:
        print("✅ Search system working correctly")
    else:
        print("❌ Search functionality may be impaired")
```

## 🔒 Privacy and Ethics

- **Privacy-First**: DuckDuckGo doesn't track users or store personal information
- **No Filter Bubble**: Results aren't personalized based on search history
- **Unbiased Results**: Search results aren't influenced by commercial interests
- **Respect for Content**: Always respect website terms of service and robots.txt

## 🚀 Performance Tips

### 1. Query Optimization
```python
# Combine related queries to reduce API calls
await manager.run(
    "Research electric vehicle market trends, including Tesla stock performance, charging infrastructure development, and government incentives",
    agent=agent
)
```

### 2. Caching Results
```python
# Store frequently accessed information
search_cache = {}

async def cached_search(query, agent):
    if query in search_cache:
        return search_cache[query]
    
    result = await manager.run(query, agent=agent)
    search_cache[query] = result
    return result
```

### 3. Batch Processing
```python
# Process multiple searches efficiently
async def batch_search(queries, agent):
    results = []
    for query in queries:
        result = await manager.run(query, agent=agent)
        results.append(result)
        await asyncio.sleep(1)  # Respectful rate limiting
    return results
```
