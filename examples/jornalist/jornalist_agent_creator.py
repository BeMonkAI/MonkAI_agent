from core.monkai_agent_creator import MonkaiAgentCreator, TransferTriageAgentCreator
from core.types import Agent
import core.security as security
import os
import requests

class JornalistAgentCreator(TransferTriageAgentCreator):

    def __init__(self):
        super().__init__()
        self.__jornalist_agent = Agent(name="Jornalist Agent",
           instructions=""" You are an agent in charge of summarizing the day's news read in specific newspapers.""",
            functions=[  
                        self.read_news,
                      ])
        
    def get_agent(self):
        """
        Returns the Jornalist Agent.
        """
        return self.__jornalist_agent
    
    def get_agent_briefing(self):
        return "You are an agent in charge of summarizing the day's news read in specific newspapers."
    
    def read_news(self):
        """
        Read the news.
        """
        news = requests.get("https://g1.globo.com/").text
        return f"As noticias a resumir são: {news[:120000]}"