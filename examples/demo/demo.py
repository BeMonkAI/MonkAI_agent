import asyncio
from openai import AzureOpenAI
from monkai_agent import OpenAIProvider, AzureProvider, AgentManager
from monkai_agent.repl import run_demo_loop
from monkai_agent.groq import GroqProvider, GROQ_MODELS
from groq import Groq
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor


if __name__ == '__main__': 
    """
    Run the demo loop for different agent builders.

    Import and instantiate specific agent builders for different roles, 
    such as Python developer, information researcher, journalist, 
    and secure calculator. Add these builders to a list for later use in 
    the demo loop, as many agents you created in the system can be added to this loop.
    """
    
    from examples.triage.python_developer_agent_creator import PythonDeveloperAgentCreator
    from examples.triage.jornalist_agent_creator import JornalistAgentCreator
    from examples.triage.calculator_agents_creator import CalculatorAgentCriator
    
    agents_creators = []
    agents_creators.append(PythonDeveloperAgentCreator(user="valid_user"))
    agents_creators.append(JornalistAgentCreator())
    agents_creators.append(CalculatorAgentCriator("valid_user"))

    # Initialize the provider - using Groq for this demo
    provider = GroqProvider("my-api-key")
    #provider = OpenAIProvider("my-api-key")
    agent_manager = AgentManager(provider=provider, agents_creators=agents_creators, model="llama-3.3-70b-versatile", temperature=0.3)
    asyncio.run(run_demo_loop(agent_manager, debug=True))

