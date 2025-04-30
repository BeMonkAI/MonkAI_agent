from monkai_agent import TransferTriageAgentCreator, Agent
import os
import requests

class JornalistAgentCreator(TransferTriageAgentCreator):

    def __init__(self):
        super().__init__()
        self.__jornalist_agent = Agent(name="Jornalist Agent",
           instructions=""" You are an agent in charge of summarizing the day's news read in specific newspapers.
                 If you cannot provide an answer, trigger the transfer_to_triage function to escalate the request to the triage agent.
                 """,
            functions=[  
                        self.read_news,
                        self.transfer_to_triage
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
        try:
            news = requests.get("https://g1.globo.com/").text
            return f"The news to summarize are: {news[:120000]}"
        except requests.exceptions.ConnectionError as e:
            return f"Failed to retrieve news: {str(e)}"