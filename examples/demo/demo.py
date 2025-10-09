import asyncio
import os
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

    # Initialize the provider - using Azure for this demo
    # Make sure to set your API keys as environment variables:
    # export AZURE_API_KEY="your-azure-api-key"
    # export GROQ_API_KEY="your-groq-api-key" 
    # export OPENAI_API_KEY="your-openai-api-key"
    
    #provider = GroqProvider(os.getenv("GROQ_API_KEY"))
    #provider = OpenAIProvider(os.getenv("OPENAI_API_KEY"))
    azure_api_key = os.getenv("AZURE_API_KEY")
    if not azure_api_key:
        raise ValueError("AZURE_API_KEY environment variable is required")
    
    provider = AzureProvider(
        api_key=azure_api_key,
        endpoint="https://monkai-foundry.cognitiveservices.azure.com/",
        api_version="2025-01-01-preview",
    )
    agent_manager = AgentManager(provider=provider, agents_creators=agents_creators, model="gpt-4.1", temperature=0.3)
    asyncio.run(run_demo_loop(agent_manager, debug=True))

