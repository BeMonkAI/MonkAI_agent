# Agent Definition Examples

This folder contains practical examples of how to define and implement agents using the MonkAI Agent framework. The examples demonstrate different types of agents and their functionalities.

## 📋 Content

- [Agent Definition (Jupyter Notebook)](#agent-definition-jupyter-notebook)
- [Business Analyst](#business-analyst)
- [How to Execute](#how-to-execute)
- [Prerequisites](#prerequisites)

## 📊 Agent Definition (Jupyter Notebook)

**File:** `agent_definition.ipynb`

This notebook demonstrates the creation of a **Calculator Agent** - an agent specialized in complex mathematical operations.

### Calculator Agent Features

The agent has three main mathematical functions:

1. **`my_function(a: float, b: float)`**
   - Performs multiple mathematical operations in a single expression
   - Returns: (division, multiplication, number sequence, maximum value)
   - Example: `my_function(10, 2)` → `(5.0, 20, [10, 11, ...], calculated_value)`

2. **`fibonacci(num1: str)`**
   - Calculates the Fibonacci sequence
   - Parameter: number of elements in the sequence
   - Returns: list with the Fibonacci sequence

3. **`bernoulli(n: int)`**
   - Calculates the first n Bernoulli numbers
   - Parameter: quantity of Bernoulli numbers to calculate
   - Returns: list with the Bernoulli numbers

### Usage Example

```python
from monkai_agent.types import Agent

calculator_agent = Agent(
    name="Calculator Agent",
    instructions="""You are an agent responsible for performing mathematical calculations.
                You have access to mathematical functions for complex calculations.""",
    functions=[my_function, fibonacci, bernoulli]
)

# Run in interactive mode
await run_simples_demo_loop(calculator_agent, api_key="your_api_key")
```

## 💼 Business Analyst

**File:** `analista_negocio_agente_monkai.py`

This example demonstrates the creation of an agent specialized in business analysis and financial insights.

### Agent Characteristics

- **Name:** "Business Analyst Agent"
- **Specialization:** Market trend interpretation and financial analysis
- **Features:**
  - Summarize financial and market reports
  - Highlight relevant financial indicators (KPIs)
  - Suggest strategic decisions based on data
  - Identify risks, opportunities and emerging trends

### Usage Example

```python
from monkai_agent import Agent, AgentManager

# Configure the manager
manager = AgentManager(api_key="your_api_key")

# Create the agent
agent = Agent(
    name="Business Analyst Agent",
    instructions="""You are an experienced Business Analyst..."""
)

# Execute query
result = asyncio.run(manager.run(
    "Summarize the main financial insights from this week's economic reports.",
    agent=agent
))
```

### Response Style

The agent was configured to:
- ✅ Use bullet points whenever possible
- ✅ Avoid technical jargon
- ✅ Be direct and clear
- ✅ Focus on practical recommendations

## 🚀 How to Execute

### Notebook (agent_definition.ipynb)

1. Open Jupyter Notebook
2. Execute cells sequentially
3. In the last cell, replace `"api_key"` with your real API key
4. Run the interactive loop to test the agent

### Python Script (analista_negocio_agente_monkai.py)

1. Replace the `api_key` in the code with your real key
2. Execute the script:
   ```bash
   python analista_negocio_agente_monkai.py
   ```

## 📋 Prerequisites

### Installation

```bash
pip install monkai_agent
```

### Dependencies

- Python 3.8+
- monkai_agent
- asyncio (included in standard Python)

### Configuration

1. **API Key:** Both examples require a valid API key
2. **Environment:** It's recommended to use a Python virtual environment

```bash
# Activate virtual environment (if using .venv)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 📝 Agent Structure

Both examples follow the standard MonkAI Agent structure:

```python
Agent(
    name="Agent Name",               # Identifier name
    instructions="Instructions...",  # Agent prompt/context
    functions=[func1, func2]         # Available functions (optional)
)
```

## 🔧 Customization

You can modify these examples to:

- Add new functions to agents
- Change instructions for different specialties
- Integrate with different LLM providers
- Implement custom functionalities

## 📚 Next Steps

After executing these examples, explore:

- `../triage/` - Examples of agents in triage system
- `../mcp_example/` - Integration with Model Context Protocol
- `../creators_and_manager/` - Advanced agent creation

---

*For more information, consult the main MonkAI Agent documentation.*
