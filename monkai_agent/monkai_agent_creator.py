"""
This module establishes the main structure for creating agent instances within the MonkAI framework. 

It provides an abstract class, 'MonkaiAgentCreator', which serves as a blueprint for developing various types of agents, ensuring that all subclasses implement the essential methods for agent creation and description. Additionally, it includes a concrete class, 'TransferTriageAgentCreator', which extends 'MonkaiAgentCreator' and implements specific logic for creating and managing a triage agent.

"""

from abc import ABC, abstractmethod
from .types import Agent

class MonkaiAgentCreator(ABC):
    """
    Abstract class for creating agent instances.

    This class provides a blueprint for creating different types of agents
    based on the system's needs. It includes methods to create an agent
    instance and to provide a brief description of the agent's capabilities.

    """
    def __init__(self):
        self._predecessor_agent = None

    @abstractmethod
    def get_agent(self)->Agent:
        """
        Creates and returns an instance of an agent.

        """
        pass

    @abstractmethod
    def get_agent_briefing(self)->str:
        """
        Returns a brief description of the agent's capabilities.

        """
        pass

    @property
    def agent_name(self) -> str:
        agent = self.get_agent()
        if agent is None or not  isinstance(agent, Agent):
            return None
        return agent.name

    @property
    def predecessor_agent(self) -> Agent:
        return self._predecessor_agent

    @predecessor_agent.setter
    def predecessor_agent(self, agent: Agent):
        self._predecessor_agent = agent


class TransferTriageAgentCreator(MonkaiAgentCreator):
    """
    A class to create and manage a triage agent.

    """

    triage_agent = None
    """
    The triage agent instance.
    
    """
    def __init__(self):
        super().__init__()

   # @property.setter
    def set_triage_agent(self, triage_agent: Agent):
        """
        Sets the triage agent.

        Args:
            triage_agent (Agent): The triage agent to be set.
        """
        self.triage_agent = triage_agent

    def transfer_to_triage(self):
        """
        Transfers the conversation to the  triage agent.

        Args:
            agent (Agent): The agent to transfer the conversation to.
        """
        return self.triage_agent