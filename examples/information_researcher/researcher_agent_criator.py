from core.monkai_agent_creator import MonkaiAgentCreator, TransferTriageAgentCreator
from core.types import Agent
import core.security as security
import os
import requests

class ResearcherAgentCriator(TransferTriageAgentCreator):
    def __init__(self):
        super().__init__()
        self.__researcher_agent = Agent(name="Researcher Agent",
           instructions="""You are an agent responsible for searching the internet for information regarding a user's request and returning valid references. 
                           Answer the user's question correctly and send valid references. 
                           Always remember to check the references used one by one.
                        """,
            functions=[  
                        self.check_reference,
                      ])
        
    def check_reference(self, reference:str):
        """
        Check if the reference is valid.
        """
        if not reference:
            return f"Reference {reference} invalid."
        if requests.get(reference).status_code != 200:
            return f"Reference {reference} invalid"
        return f"Reference {reference} valid"
    
    def get_agent(self) -> Agent:
        """
        Returns the Researcher Agent.
        """
        return self.__researcher_agent
    
    def get_agent_briefing(self):
        return "You are an agent responsible for searching the internet for information regarding a user's request and returning valid references."