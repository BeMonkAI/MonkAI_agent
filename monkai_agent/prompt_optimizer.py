"""
This module provides functionality for testing and optimizing prompts used in the MonkAI agent.
It includes tools for running prompt tests, analyzing results, and generating improved prompts.
"""

from typing import List, Optional, Dict
from .types import PromptTest, PromptOptimizer, Agent
from openai import OpenAI

class PromptOptimizerManager:
    """
    Manages the process of testing and optimizing prompts.
    """
    
    def __init__(self, client: Optional[OpenAI] = None, model: str = "gpt-4o") -> None:
        """
        Initialize the PromptOptimizerManager.
        
        Args:
            client (OpenAI, optional): OpenAI client instance. If None, creates a new one.
        """
        self.client = client or OpenAI()
        self.model = model
        
    def analyze_prompt(self, prompt: str, context: Optional[Dict] = None) -> str:
        """
        Analyze a prompt and suggest improvements.
        
        Args:
            prompt (str): The prompt to analyze
            context (Dict, optional): Additional context for the analysis
            
        Returns:
            str: Analysis and improvement suggestions
        """
        optimizer = PromptOptimizer()
        optimizer.model = self.model
        messages = [
            {"role": "system", "content": optimizer.instructions},
            {"role": "user", "content": f"Please analyze this prompt and suggest improvements:\n\n{prompt}"}
        ]
        
        if context:
            messages.append({"role": "user", "content": f"Additional context:\n{context}"})
            
        response = self.client.chat.completions.create(
            model=optimizer.model,
            messages=messages,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    async def run_prompt_test(self, agent: Agent, test_case: PromptTest) -> PromptTest:
        """
        Run a single test case with the given agent.
        
        Args:
            agent (Agent): The agent to test
            test_case (PromptTest): The test case to run
            
        Returns:
            PromptTest: Updated test case with results
        """
        # Run the test using the agent
        response = await agent.run(test_case.input_text)
        test_case.actual_output = response.messages[-1].content if response.messages else None
        
        # Compare actual vs expected output
        test_case.success = test_case.actual_output == test_case.expected_output
        
        return test_case
    
    async def run_prompt_tests(self, agent: Agent, test_cases: List[PromptTest]) -> List[PromptTest]:
        """
        Run multiple test cases with the given agent.
        
        Args:
            agent (Agent): The agent to test
            test_cases (List[PromptTest]): List of test cases to run
            
        Returns:
            List[PromptTest]: Updated test cases with results
        """
        results = []
        for test_case in test_cases:
            result = await self.run_prompt_test(agent, test_case)
            results.append(result)
        return results
    
    def generate_test_report(self, test_cases: List[PromptTest]) -> str:
        """
        Generate a report from test results.
        
        Args:
            test_cases (List[PromptTest]): List of test cases with results
            
        Returns:
            str: Formatted test report
        """
        total_tests = len(test_cases)
        passed_tests = sum(1 for test in test_cases if test.success)
        failed_tests = total_tests - passed_tests
        
        report = f"Prompt Test Report\n{'='*50}\n\n"
        report += f"Total Tests: {total_tests}\n"
        report += f"Passed: {passed_tests}\n"
        report += f"Failed: {failed_tests}\n\n"
        
        for test in test_cases:
            report += f"Test: {test.name}\n"
            report += f"Status: {'✓ PASSED' if test.success else '✗ FAILED'}\n"
            if not test.success:
                report += f"Expected: {test.expected_output}\n"
                report += f"Actual: {test.actual_output}\n"
            report += "\n"
            
        return report 