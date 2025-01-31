from monkai_agent.monkai_agent_creator import TransferTriageAgentCreator
from monkai_agent.types import Agent
from monkai_agent.security import validate
import os
import requests

   
class CalculatorAgentCriator(TransferTriageAgentCreator):
    def __init__(self, user:str):
        self.user = user
        self.calculator_agent = Agent(name="Calculator Agent",
           instructions="""You are an agent responsible for performing mathematical calculations. 
            If you cannot provide an answer, trigger the transfer_to_triage function to escalate the request to the triage agent.
                            
            """,
            functions=[  
                        self.sum,
                        self.substract,
                        self.multiply,
                        self.divide,
                        self.transfer_to_triage
                      ])

   
    # Example usage
    def is_user_valid(self):
        if self.user=="valid_user":
            return True
        else:
            return False
        
    @validate(is_user_valid)
    def sum(self, num1, num2):
        """Sum two numbers.
        
        Parameters:
            num1 (obj): The first number.
            num2 (str): The second number.

        Returns:
            float: The result of the sum.
        """
        return float(num1)+float(num2)
    
    @validate(is_user_valid)
    def substract(self, num1, num2):
        """Substract two numbers.
        
        Parameters:
            num1 (str): The first number.
            num2 (str): The second number.

        Returns:
            float: The result of the substraction.
        """
        return float(num1)-float(num2)
    
    def multiply(self, num1, num2):
        """Multiply two numbers.
        
        Parameters:
            num1 (str): The first number.
            num2 (str): The second number.

        Returns:
            float: The result of the multiplication.
        """
        return float(num1)*float(num2)
    
    def divide(self, num1, num2):
        """"Divide two numbers.     
        
        Parameters:
            num1 (str): The first number.
            num2 (str): The second number.

        Returns:
            float: The result of the division."""
        return float(num1)/float(num2)
    
    def get_agent(self):
        """
        Returns the Calculator Agent.
        """
        return self.calculator_agent
    
    def get_agent_briefing(self):
        return "You are an agent responsible for performing mathematical calculations."