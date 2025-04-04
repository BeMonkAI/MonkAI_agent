from monkai_agent import TransferTriageAgentCreator, Agent
from monkai_agent.src.security import validate
import os
import requests

   
class CalculatorAgentCriator(TransferTriageAgentCreator):
    def __init__(self, user:str):
        super().__init__()
        self.user = user
        self.calculator_agent = Agent(name="Calculator Agent",
        instructions="""You are an agent responsible for performing mathematical calculations.
                    You have access to the following functions:
                    - my_function(a: float, b: float) -> tuple: Performs multiple mathematical operations in a single expression.
                    - fibonacci(num1: str) -> list: Calculate the Fibonacci sequence.
                    - bernoulli(num1: str) -> list: Calculate the Bernoulli numbers.                           
            """,
            functions=[ 
                        self.my_function,
                        self.fibonacci,
                        self.bernoulli,
                        self.transfer_to_triage
                      ])

   
    # Example usage
    def is_user_valid(self):
        if self.user=="valid_user":
            return True
        else:
            return False
        
    @validate(is_user_valid)
    def my_function(self, a: float, b: float):
        """
        Performs multiple mathematical operations in a single expression:
        - Division: a / b
        - Multiplication: a * b
        - Generates a sequence of 10 numbers: [1..10]
        - Finds the maximum value in the sequence
    
        Returns:
            tuple: (division_result, multiplication_result, number_sequence, max_value)
        
        Example:
            result = single_equation(10, 2)
            print(result)  # Output: (5.0, 20, [1, 2, ..., 10], 10)
        """
        return (a / b, a * b, list(range(1, 11)), max(range(1, 11)))

    def fibonacci(self, num1):
        """Calculate the Fibonacci sequence.
        
        Parameters:
            num1 (str): The number of elements of the Fibonacci sequence.

        Returns:
            list: The Fibonacci sequence.
        """
        num1 = int(num1)
        fib = [0, 1]
        for i in range(2, num1):
            fib.append(fib[i-1] + fib[i-2])
        return fib

    def bernoulli(self, n:int):
        """
        Calculate the first n Bernoulli numbers.

        Parameters:
        n (int): The number of Bernoulli numbers to calculate.

        Returns:
        list: A list of the first n Bernoulli numbers.
        """
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for m in range(n + 1):
            A[m][0] = 1 / (m + 1)
            for j in range(1, m + 1):
                A[m][j] = (A[m][j - 1] * (m - j + 1)) / (j + 1)
        B = [A[m][m] for m in range(n + 1)]
        return B
        
    def get_agent(self):
        """
        Returns the Calculator Agent.
        """
        return self.calculator_agent
    
    def get_agent_briefing(self):
        return "You are an agent responsible for performing mathematical calculations."