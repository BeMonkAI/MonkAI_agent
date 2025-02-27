from monkai_agent.types import Agent
import os
from openai import AzureOpenAI
from monkai_agent.security import validate
from examples.python_developer.python_developer_agent_creator import PythonDeveloperAgentCreator
from monkai_agent.base import AgentManager
from monkai_agent.repl import run_demo_loop
import config
import asyncio

agents_creators = []
agents_creators.append(PythonDeveloperAgentCreator(user ='no_valid_user'))
client=AzureOpenAI(
            api_key=config.OPENAI_API_KEY_BRASILSOUTH,
            api_version=config.GPT4o_OPENAI_API_VERSION_BRASILSOUTH,
            azure_endpoint=config.OPENAI_AZURE_ENDPOINT_BRASILSOUTH,
        )
agent_manager = AgentManager(client=client, agents_creators=agents_creators)
asyncio.run(run_demo_loop(agent_manager, model=config.GPT4o_OPENAI_GPT_MODEL_BRASILSOUTH))