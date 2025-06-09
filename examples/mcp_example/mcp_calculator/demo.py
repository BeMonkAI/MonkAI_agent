import asyncio
from pathlib import Path
from openai import AzureOpenAI
import sys
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
import mcp
# Set up OpenTelemetry tracing
endpoint = "http://127.0.0.1:6006/v1/traces"
tracer_provider = trace_sdk.TracerProvider()
tracer_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(endpoint)))
tracer_provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))  # Also print to console for debugging

# Enable instrumentation for all providers
#GroqInstrumentor().instrument(tracer_provider=tracer_provider)
#OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)
MonkaiAgentInstrumentor().instrument(tracer_provider=tracer_provider)
import sys



async def main():
    """
    Run the demo loop for different agent builders.

    Import and instantiate specific agent builders for different roles, 
    such as Python developer, information researcher, journalist, 
    and secure calculator. Add these builders to a list for later use in 
    the demo loop, as many agents you created in the system can be added to this loop.
    """
    # Add the path to access the calculator agent creator
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))
    from calculator_agent_creator import CalculatorAgentCreator
    
    agents_creators = []
 
    creator = CalculatorAgentCreator(model="gpt-4o", python_executable=sys.executable)
    res = await creator.initialize_agent()  # Ensure the agent is initialized
    if not res:
        print("Failed to initialize the Calculator Agent. Please check the server script path and Python executable.")
        exit(1)
    agents_creators.append(creator)  # Adjust path as needed


    # Initialize the provider - using Groq for this demo
    #provider = GroqProvider(config.GROQ_API_KEY)
    provider = AzureProvider(
            api_key=config.OPENAI_API_KEY_BRASILSOUTH,
            api_version=config.OPENAI_API_VERSION,
            endpoint=config.OPENAI_AZURE_ENDPOINT_BRASILSOUTH,
    )
    agent_manager = AgentManager(provider=provider, agents_creators=agents_creators, model="gpt-4o", temperature=0.3)
    return await run_demo_loop(agent_manager, debug=True)

if __name__ == '__main__': 
     asyncio.run(main(), debug=True)

