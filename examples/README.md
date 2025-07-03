# 📚 MonkAI Agent Examples

This folder contains a comprehensive collection of practical examples demonstrating the different functionalities and usage patterns of the MonkAI Agent framework. Each subdirectory presents a specific aspect of the framework, from basic concepts to advanced implementations.

## 📋 Examples Structure

### 🎯 [agent_definition/](./agent_definition/)
**Objective**: Demonstrate the fundamental concepts of agent creation and definition.

- **Main Content**: 
  - `agent_definition.ipynb` - Interactive notebook with Calculator Agent
  - `analista_negocio_agente_monkai.py` - Business analyst agent implementation
- **What you'll learn**:
  - How to define a basic agent
  - Implement custom functions for agents
  - Configure instructions and behaviors
  - Work with mathematical functions (Fibonacci, Bernoulli)

### 🏗️ [creators_and_manager/](./creators_and_manager/)
**Objective**: Demonstrate the Creator and Manager pattern for more complex architectures.

- **Main Content**: 
  - `agent_definition_class.ipynb` - Notebook about Creator Pattern
- **What you'll learn**:
  - Implement the Creator pattern for specialized agents
  - Manage multiple agents simultaneously
  - Implement security and validation layers
  - Integration with Azure OpenAI

### 🚀 [demo/](./demo/)
**Objective**: Practical example of multiple agents working together.

- **Main Content**: 
  - `demo.py` - Demo with 3 specialized agents
- **Included Agents**:
  - **Journalist Agent** - News summarization
  - **Python Developer Agent** - Python development
  - **Calculator Agent** - Secure mathematical calculations
- **What you'll learn**:
  - Coordination between multiple agents
  - Agent specialization by domain
  - Integration with Groq provider

### 🔍 [demo_tracer/](./demo_tracer/)
**Objective**: Demonstrate advanced observability and tracing with Arize Phoenix.

- **Main Content**: 
  - `demo.py` - Same basic demo + observability
- **Additional Features**:
  - Real-time monitoring web interface
  - Complete interaction tracing
  - Advanced metrics and visualizations
  - Enhanced debugging
- **What you'll learn**:
  - Implement observability in agents
  - Monitor performance and behavior
  - Use Arize Phoenix for analysis

### 🔌 [mcp_example/](./mcp_example/)
**Objective**: Demonstrate integration with Model Context Protocol (MCP) servers.

This section contains multiple sub-examples:

#### 🧮 [mcp_calculator/](./mcp_example/mcp_calculator/)
- **Functionality**: Agent with mathematical capabilities via MCP
- **Tools**: Basic operations, calculation history
- **Files**: MCP Server, Creator, Demo

#### 🔍 [mcp-duckduckgo/](./mcp_example/mcp-duckduckgo/)
- **Functionality**: Real-time web search via DuckDuckGo
- **Features**: Privacy respected, multiple result formats
- **Usage**: Up-to-date web information

#### 💾 [mcp-memory/](./mcp_example/mcp-memory/)
- **Functionality**: Persistent memory system
- **Features**: Context storage and retrieval

#### 📝 [mcp-notion/](./mcp_example/mcp-notion/)
- **Functionality**: Notion integration for data management
- **Features**: Access to Notion pages and databases

**What you'll learn with MCP**:
- Connect agents to external services
- Use standardized protocols for extensibility
- Implement specialized capabilities via MCP servers

### 🎯 [triage/](./triage/)
**Objective**: Demonstrate intelligent triage system with multiple specialized agents.

- **Main Content**: 
  - `triage_example.ipynb` - Triage example notebook
  - Specialized creators for different domains
- **Specialized Agents**:
  - `python_developer_agent_creator.py` - Python development
  - `jornalist_agent_creator.py` - Research and journalism
  - `calculator_agents_creator.py` - Secure calculations
- **What you'll learn**:
  - Implement automatic triage system
  - Route queries to specialized agents
  - Manage multi-agent workflows
  - Manager pattern for coordination

## 🎯 Recommended Learning Progression

To get the most out of the examples, we recommend following this sequence:

### 1. **Fundamentals** 📖
Start with `agent_definition/` to understand basic concepts.

### 2. **Basic Demo** 🚀
Run `demo/` to see agents working together.

### 3. **Advanced Architecture** 🏗️
Explore `creators_and_manager/` for organizational patterns.

### 4. **Observability** 🔍
Implement tracing with `demo_tracer/` for monitoring.

### 5. **External Integrations** 🔌
Try `mcp_example/` to expand capabilities.

### 6. **Complex System** 🎯
Finish with `triage/` for production architectures.

## 🛠️ General Prerequisites

Before running any example, make sure you have:

### Base Installation
```bash
# Activate virtual environment
source .venv/bin/activate

# Install main package
pip install monkai-agent

# For Groq examples
pip install monkai-agent-groq
```

### Required API Keys
- **OpenAI API Key** (for basic examples)
- **Azure OpenAI** (for Azure examples)
- **Groq API Key** (for Groq demos)

### Optional Dependencies
```bash
# For observability (demo_tracer)
pip install arize-phoenix

# For specific MCP integrations
pip install mcp  # or specific dependencies for each MCP server
```

## 📝 How to Use

1. **Choose the appropriate example** for your level and objective
2. **Read the specific README** of the chosen example
3. **Configure the necessary API keys**
4. **Run the specific prerequisites**
5. **Execute the code** following the instructions

## 🤝 Contributing

Want to add a new example? Follow this structure:
- Create a new folder with a descriptive name
- Include an explanatory README.md
- Add well-commented code
- Provide clear execution instructions
- Update this main README

## 📚 Additional Resources

- **Complete Documentation**: See `DOCUMENTATION.md` in the project root
- **API Reference**: Explore the `libs/` folder for implementation details
- **UI Examples**: Check `ui/` for graphical interfaces

---

**💡 Tip**: Each example is independent, but concepts learned in one can be applied to others. Experiment, modify, and adapt the examples to your specific needs!
