from monkai_agent.base import AgentManager
import asyncio
from monkai_agent.repl import run_demo_loop
from openai import AzureOpenAI
import config


if __name__ == '__main__': 
    """
    Run the demo loop for different agent builders.

    Import and instantiate specific agent builders for different roles, 
    such as Python developer, information researcher, journalist, 
    and secure calculator. Add these builders to a list for later use in 
    the demo loop, as many agents you created in the system can be added to this loop.

    """

    from examples.triage.python_developer_agent_creator import PythonDeveloperAgentCreator
    from examples.information_researcher.researcher_agent_criator import ResearcherAgentCriator
    from examples.triage.jornalist_agent_creator import JornalistAgentCreator
    from examples.triage.calculator_agents_creator import CalculatorAgentCriator
    
    agents_creators = []
    agents_creators.append(PythonDeveloperAgentCreator(user="valid_user"))
    agents_creators.append(ResearcherAgentCriator())
    agents_creators.append(JornalistAgentCreator())
    agents_creators.append(CalculatorAgentCriator("invalid_user"))
    client=AzureOpenAI(
            api_key=config.OPENAI_API_KEY_BRASILSOUTH,
            api_version=config.GPT4o_OPENAI_API_VERSION_BRASILSOUTH,
            azure_endpoint=config.OPENAI_AZURE_ENDPOINT_BRASILSOUTH,
        )
    agent_manager = AgentManager(client=client, agents_creators=agents_creators)
    asyncio.run(run_demo_loop(agent_manager, model=config.GPT4o_OPENAI_GPT_MODEL_BRASILSOUTH,stream=True, debug=True))

   