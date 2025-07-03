# MonkAI Agent Demo with Tracer

This demo is an extension of the basic MonkAI Agent demo, but with the addition of **observability and tracing** using Arize Phoenix. It allows monitoring and tracking all agent interactions in real-time through an intuitive web interface.

## 🔍 What is this Demo?

This demo contains **exactly the same agents** as the basic demo:
- **Journalist Agent** - Specialized in news summarization
- **Python Developer Agent** - Focused on Python development  
- **Calculator Agent** - Secure agent for mathematical calculations

**The main difference**: Adds complete observability and tracing capabilities to monitor agent behavior.

## 🆚 Differences from Basic Demo

### Basic Demo vs Tracer Demo

| Aspect | Basic Demo | Tracer Demo |
|---------|-------------|-------------|
| **Agents** | ✅ Same 3 agents | ✅ Same 3 agents |
| **Functionality** | ✅ Multi-agent interaction | ✅ Multi-agent interaction |
| **Observability** | ❌ Only terminal logs | ✅ Complete web interface |
| **Tracing** | ❌ Not available | ✅ Complete tracking |
| **Analysis** | ❌ Limited | ✅ Metrics and visualizations |
| **Debugging** | ❌ Basic | ✅ Advanced with Phoenix |

## 🔧 Prerequisites

### Required Package Installation

It is **mandatory** to install the following packages:

```bash
# Basic MonkAI Agent packages
pip install monkai-agent
pip install monkai-agent-groq

# Package for observability and tracing
pip install arize-phoenix

# Specific instrumentation for MonkAI Agent
pip install openinference-instrumentation-monkai-agent
```

### API Key Configuration

Configure your OpenAI API key in the `config.py` file:

```python
OPENAI_API_KEY_ARTHUR = "your-openai-key-here"
```

## 🚀 How to Execute

### Step 1: Activate Virtual Environment
```bash
source .venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install arize-phoenix
pip install openinference-instrumentation-monkai-agent
```

### Step 3: Start Phoenix Server (Terminal 1)
```bash
.venv/bin/python -m phoenix.server.main serve
```

This will start the Phoenix server on the default port (6006). You will see a message like:
```
🚀 Phoenix UI available at http://localhost:6006
```

### Step 4: Run the Demo (Terminal 2)
In a **new terminal**, execute:
```bash
# Activate environment
source .venv/bin/activate

# Run demo
cd examples/demo_tracer
python demo.py
```

### Step 5: Access Phoenix Interface
Open your browser and go to: **http://localhost:6006**

## 📊 Tracing Features

### What you can monitor:

1. **Conversation Flow**
   - Agent transfers
   - Response time for each agent
   - Function call sequence

2. **Performance Metrics**
   - API call latency
   - Tokens used
   - Cost per interaction

3. **Advanced Debugging**
   - Structured logs
   - Error stack traces
   - Prompt and response analysis

4. **Interactive Visualizations**
   - Interaction timeline
   - Dependency graphs
   - Metrics dashboards

## 🎯 Phoenix Interface

### Main Sections:

1. **Traces**: Visualizes each complete interaction
2. **Sessions**: Groups related conversations  
3. **Evaluations**: Response quality analysis
4. **Datasets**: Historical data for analysis

### Usage Example:

1. Execute a question in the demo: *"Calculate 15% of 250"*
2. In Phoenix, you will see:
   - How triage directed to Calculator Agent
   - Time spent in each step
   - Tokens consumed
   - Complete structured response

## 🔧 Tracing Configuration

### Tracing Endpoint
```python
endpoint = "http://127.0.0.1:6006/v1/traces"
```

### Enabled Instrumentation
```python
# Instruments all MonkAI Agent calls
MonkaiAgentInstrumentor().instrument(tracer_provider=tracer_provider)
```

### Span Processors
- **OTLP Exporter**: Sends data to Phoenix
- **Console Exporter**: Terminal logs (debug)

## 🛠️ Troubleshooting

### Phoenix is not starting
```bash
# Check if it's installed
pip list | grep phoenix

# Reinstall if necessary
pip install --upgrade arize-phoenix
```

### Cannot access http://localhost:6006
1. Check if Phoenix server is running
2. Confirm there's no port conflict
3. Try accessing: http://127.0.0.1:6006

### Traces don't appear in Phoenix
1. Check if endpoint is correct
2. Confirm that `MonkaiAgentInstrumentor` is instrumented
3. Run the demo and ask some questions

### Instrumentation Error
```bash
# Reinstall instrumentation
pip install --upgrade openinference-instrumentation-monkai-agent
```

## 📈 Tracing Benefits

### For Development:
- **Visual debugging** of agent flow
- **Performance bottleneck identification**
- **Response quality analysis**

### For Production:
- **Real-time monitoring**
- **Automatic alerts** for failures
- **Detailed cost analysis**
- **Data-driven optimization**

## 🎓 Advanced Use Cases

### Performance Analysis
```python
# Phoenix automatically collects:
# - Response time per agent
# - Token usage
# - Transfer frequency
# - Success rate
```

### Agent Debugging
```python
# Visualize:
# - Why an agent transferred to another
# - What prompt was used internally
# - How functions were called
# - Where errors occurred
```

## 📚 Additional Resources

- **Phoenix Documentation**: [docs.arize.com](https://docs.arize.com)
- **OpenInference**: [github.com/Arize-ai/openinference](https://github.com/Arize-ai/openinference)
- **Basic Demo**: `../demo/` (version without tracing)

## 🔄 Comparison with Basic Demo

If you want to test **without tracing**, use the basic demo:
```bash
cd ../demo
python demo.py
```

The tracer demo offers the **same functionality** + complete observability!

---

**💡 Tip**: Use this demo to understand how your agents behave in production and optimize their performance!
