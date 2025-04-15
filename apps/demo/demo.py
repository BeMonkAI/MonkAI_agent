import asyncio
from openai import AzureOpenAI
import config
from monkai_agent import OpenAIProvider, AzureProvider, AgentManager
from monkai_agent.repl import run_demo_loop
from monkai_agent.groq import GroqProvider, GROQ_MODELS
from groq import Groq
from openinference.instrumentation.groq import GroqInstrumentor
from openinference.instrumentation.openai import OpenAIInstrumentor
from openinference.instrumentation.monkai_agent import MonkaiAgentInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

# Set up OpenTelemetry tracing
endpoint = "http://127.0.0.1:6006/v1/traces"
tracer_provider = trace_sdk.TracerProvider()
tracer_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(endpoint)))
tracer_provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))  # Also print to console for debugging

# Enable instrumentation for all providers
#GroqInstrumentor().instrument(tracer_provider=tracer_provider)
#OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)
MonkaiAgentInstrumentor().instrument(tracer_provider=tracer_provider)

if __name__ == '__main__': 
    """
    Run the demo loop for different agent builders.

    Import and instantiate specific agent builders for different roles, 
    such as Python developer, information researcher, journalist, 
    and secure calculator. Add these builders to a list for later use in 
    the demo loop, as many agents you created in the system can be added to this loop.
    """
    
    from apps.examples.triage.python_developer_agent_creator import PythonDeveloperAgentCreator
    from apps.examples.triage.jornalist_agent_creator import JornalistAgentCreator
    from apps.examples.triage.calculator_agents_creator import CalculatorAgentCriator
    
    agents_creators = []
    agents_creators.append(PythonDeveloperAgentCreator(user="valid_user"))
    agents_creators.append(JornalistAgentCreator())
    agents_creators.append(CalculatorAgentCriator("invalid_user"))

    # Initialize the provider - using Groq for this demo
    provider = GroqProvider(config.GROQ_API_KEY)
    agent_manager = AgentManager(provider=provider, agents_creators=agents_creators, model='llama3-70b-8192')
  
    asyncio.run(run_demo_loop(agent_manager, debug=True))

