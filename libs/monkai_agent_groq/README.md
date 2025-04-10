# OpenInference Instrumentation for MonkAI Agent

This package provides OpenInference instrumentation for the MonkAI Agent framework. It tracks the interactions between your application and various LLM providers (OpenAI, Azure OpenAI, etc.) through the MonkAI Agent framework.

## Installation

```bash
pip install openinference-instrumentation-monkai-agent
```

## Usage

The instrumentation will automatically track calls to all MonkAI Agent LLM providers (OpenAI, Azure OpenAI, etc.) and collect telemetry data including:

- Model usage details (model name, temperature, tokens, etc.)
- Request/response content
- Provider-specific attributes
- Performance metrics
- Tool usage

### Basic Usage

```python
from openinference.instrumentation.monkai_agent import MonkaiAgentInstrumentor

# Enable instrumentation
MonkaiAgentInstrumentor().instrument()

# Your MonkAI Agent code here...
```

### Configuration

You can configure the instrumentation with custom tracers:

```python
from opentelemetry import trace
from openinference.instrumentation import TraceConfig
from openinference.instrumentation.monkai_agent import MonkaiAgentInstrumentor

# Configure custom tracer
tracer_provider = trace.TracerProvider()
trace.set_tracer_provider(tracer_provider)

# Configure and enable instrumentation
MonkaiAgentInstrumentor().instrument(
    tracer_provider=tracer_provider,
    config=TraceConfig(
        # Add your config options here
    )
)
```

## Collected Telemetry

The instrumentation collects the following telemetry:

### Common Attributes
- Model name
- Temperature
- Max tokens
- Top P
- Frequency penalty
- Presence penalty
- Request messages
- Response messages
- Token usage statistics

### Provider-Specific Attributes
- OpenAI: Provider name
- Azure: Provider name, endpoint, API version

### Spans
- One span per LLM completion request
- Nested spans for provider operations

## License

MIT License - See LICENSE file for details