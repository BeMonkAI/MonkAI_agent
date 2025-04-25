"""
This module is a standout feature of the MonkAI framework, setting it apart by enabling the seamless creation and management of triage agents. These agents play a pivotal role in ensuring efficient user interaction by determining the most appropriate agent to handle each user's request.

The TriageAgentCreator class, a key component of this module, extends the abstract MonkaiAgentCreator and incorporates advanced logic for triage management. Its functionality includes the creation of dynamic transfer functions, which allow conversations to be redirected to the right agent based on the context and user needs.

Key Features:
- Centralized Decision-Making: Streamlines the process of determining agent responsibilities, reducing complexity in multi-agent systems.
- Enhanced User Experience: Ensures users are directed to the correct agent promptly, minimizing delays and miscommunication.
- Customizable and Scalable: The triage logic is flexible and can adapt to various application scenarios, making it suitable for projects of any scale.
This module exemplifies the innovation and practicality at the core of MonkAI, delivering a robust solution for efficient agent orchestration.

"""


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
       super().__init__()
       self.agents_creator = agents_creator
       self.__build_agent()
       for creator in self.agents_creator:
           if creator.predecessor_agent is None:
                creator.predecessor_agent = self.triage_agent
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
            agent = agent_creator.get_agent()
            if not  isinstance(agent, Agent):
                continue
            functions.append(self.__create_transfer_function(agent_creator))
            print(agent.name)
            print(agent_creator.get_agent_briefing())
            instructions += f"- **Transfer to `{agent.name}`** if the user's query is about: {agent_creator.get_agent_briefing()}\n\n"
        self.triage_agent = Agent(
            name="Triage Agent",
            instructions=f"""
            You are a triage agent who, given an initial conversation with the user, determines which agent is the most suitable to handle the user's request and transfers the conversation to that agent.
            Do not share your reasoning process with the user! Do not make irrational assumptions on behalf of the user. Do not share the agent transfer process with the user. 
            
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