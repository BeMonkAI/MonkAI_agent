
from .monkai_agent_creator import MonkaiAgentCreator, TransferTriageAgentCreator
from .types import Agent

class TriageAgentCreator(MonkaiAgentCreator):
    """
    Class for creating triage agents.

    This class inherits from MonkaiAgentCreator and is responsible for creating
    triage agents that decide which agent should handle the user's request. It
    provides methods to create the triage agent and to provide a description of
    its capabilities.

    """
    def __init__(self, agents_creator:list[MonkaiAgentCreator]):
       self.agents_creator = agents_creator
       self.__build_agent()
       for creator in self.agents_creator:
           if isinstance(creator, TransferTriageAgentCreator):
               creator.triage_agent = self.triage_agent
       
    def __create_transfer_function(self, agent_creator:MonkaiAgentCreator):
        """
        Creates a transfer function for the given agent creator.

        Args:
            agent_creator (MonkaiAgentCreator): The agent creator for which to create the transfer function.

        Returns:
            Callable: A function that transfers the conversation to the specified agent.
        """
        def transfer_function():
            return agent_creator.get_agent()
        transfer_function.__name__ = f"transfer_to_{agent_creator.get_agent().name.replace(' ', '_')}"
        return transfer_function
 
    def __build_agent(self):
        """
        Builds the triage agent by aggregating instructions and functions from all agent creators.

        This method constructs the triage agent with specific instructions on when to transfer
        the conversation to each specific agent based on the user's query.
        """
        instructions = ""
        functions = []
        print("Building triage agent")
        print(self.agents_creator)
        for agent_creator in self.agents_creator:

            functions.append(self.__create_transfer_function(agent_creator))
            agent = agent_creator.get_agent()
            print(agent.name)
            print(agent_creator.get_agent_briefing())
            instructions += f"- **Transfer to `{agent.name}`** if the user's query is about: {agent_creator.get_agent_briefing()}\n\n"
        self.triage_agent = Agent(
            name="Triage Agent",
            instructions=f"""
            Determine which agent is best suited to handle the user's request and transfer the conversation to that agent. 
            Briefing:
 
                {instructions}
            Guardrails:
                - Do not respond to questions that are outside the established context.    
            """,
            functions=functions
        )

    def get_agent(self)->Agent:
        """
        Creates and returns an instance of a triage agent.
        """
        return self.triage_agent

    def get_agent_briefing(self)->str:
        """
        Returns a brief description of the triage agent's capabilities.
        """
        return "Review the user's query and transfer the conversation to the appropriate agent."