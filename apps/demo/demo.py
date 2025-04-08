import asyncio
from openai import AzureOpenAI
import config
from monkai_agent import OpenAIProvider, AgentManager
from monkai_agent.src.repl import run_demo_loop
from monkai_agent.groq.__providers import GroqProvider 
from monkai_agent.src.providers import AzureProvider
from groq import Groq
from openinference.instrumentation.groq import GroqInstrumentor
from openinference.instrumentation.openai import OpenAIInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.trace.export import  ConsoleSpanExporter, SimpleSpanProcessor

endpoint = "http://127.0.0.1:6006/v1/traces"
tracer_provider = trace_sdk.TracerProvider()
tracer_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(endpoint)))

GroqInstrumentor().instrument(tracer_provider=tracer_provider)
OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)


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
    provider = AzureProvider(api_key=config.OPENAI_API_KEY_BRASILSOUTH, endpoint=config.OPENAI_AZURE_ENDPOINT_BRASILSOUTH,api_version=config.GPT4o_OPENAI_API_VERSION_BRASILSOUTH)
    #provider = GroqProvider(config.GROQ_API_KEY)
    #agent_manager = AgentManager(provider=provider, agents_creators=agents_creators, model='llama3-70b-8192')
    agent_manager = AgentManager(provider=provider, agents_creators=agents_creators,model=config.GPT4o_OPENAI_GPT_MODEL_BRASILSOUTH)
    
    #asyncio.run(run_demo_loop(agent_manager, model= ))
    asyncio.run(run_demo_loop(agent_manager, debug =True))

