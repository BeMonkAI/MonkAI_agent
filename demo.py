from core.base import AgentManager
import asyncio
from core.triage_agent_creator import TriageAgentCreator
from core.repl import run_demo_loop
from bson import ObjectId
import config 
import openai
#from openai import AzureOpenAI



if __name__ == '__main__': 
    """
    Run the demo loop for different agent builders.

    Import and instantiate specific agent builders for different roles, 
    such as Python developer, information researcher, journalist, 
    and secure calculator. Add these builders to a list for later use in 
    the demo loop, as many agents you created in the system can be added to this loop.

    """

    from examples.python_developer.python_developer_agent_creator import PythonDeveloperAgentCreator
    from examples.information_researcher.researcher_agent_criator import ResearcherAgentCriator
    from examples.jornalist.jornalist_agent_creator import JornalistAgentCreator
    from examples.secure_calculator.calculator_agents_creator import CalculatorAgentCriator
    
    agents_creators = []
    agents_creators.append(PythonDeveloperAgentCreator())
    agents_creators.append(ResearcherAgentCriator())
    agents_creators.append(JornalistAgentCreator())
    agents_creators.append(CalculatorAgentCriator("invalid_user"))
    client=openai.Client(api_key='api_key')
    #client=openai.Client(api_key=config.API_KEY)    
    #client=AzureOpenAI(api_key=config.API_KEY)
    agent_manager = AgentManager(client=client, agents_creators=agents_creators)
    asyncio.run(run_demo_loop(agent_manager, model='gpt-4o'))  

