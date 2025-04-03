import asyncio
from openai import AzureOpenAI
import config
from monkai_agent import OpenAIProvider, AgentManager
from monkai_agent.src.repl import run_demo_loop
from monkai_agent.groq.__providers import GroqProvider 

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
    #provider = OpenAIProvider(config.OPENAI_API_KEY_ARTHUR)
    provider = GroqProvider(config.GROQ_API_KEY)
    agent_manager = AgentManager(provider=provider, agents_creators=agents_creators, model= "llama-3.3-70b-versatile")
    #asyncio.run(run_demo_loop(agent_manager, model= config.GPT4o_OPENAI_GPT_MODEL_BRASILSOUTH,stream=True, debug=True))
    asyncio.run(run_demo_loop(agent_manager, model= "llama-3.3-70b-versatile"))

