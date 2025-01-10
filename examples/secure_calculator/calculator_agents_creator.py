from core.monkai_agent_creator import MonkaiAgentCreator, TransferTriageAgentCreator
from core.types import Agent
from core.security import validate
import os
import requests

   
class CalculatorAgentCriator(TransferTriageAgentCreator):
    def __init__(self, user:str):
        self.user = user
        self.calculator_agent = Agent(name="Calculator Agent",
           instructions="""You are an agent responsible for performing mathematical calculations.
            """,
            functions=[  
                        self.sum,
                        self.substract,
                        self.multiply,
                        self.divide
                      ])

   
    # Example usage
    def is_user_valid(self):
        if self.user=="valid_user":
            return True
        else:
            return False
        
    @validate(is_user_valid)
    def sum(num1, num2):
        """Sum two numbers."""
        return num1+num2
    
    @validate(is_user_valid)
    def substract(num1, num2):
        """Substract two numbers."""
        return num1-num2
    
    @validate(is_user_valid)
    def multiply(num1, num2):
        """Multiply two numbers."""
        return num1*num2
    
    @validate(is_user_valid)
    def divide(num1, num2):
        """"Divide two numbers."""
        return num1/num2
    
    def get_agent(self):
        """
        Returns the Calculator Agent.
        """
        return self.calculator_agent
    
    def get_agent_briefing(self):
        return "You are an agent responsible for performing mathematical calculations."