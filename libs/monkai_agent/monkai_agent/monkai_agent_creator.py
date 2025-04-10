"""
This module establishes the main structure for creating agent instances within the MonkAI framework. 

It provides an abstract class, 'MonkaiAgentCreator', which serves as a blueprint for developing various types of agents, ensuring that all subclasses implement the essential methods for agent creation and description. Additionally, it includes concrete classes for different types of agents, including a prompt testing and optimization agent.

"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from openai import OpenAI
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
        """
        Returns the name of the agent.
        """
        agent = self.get_agent()
        if agent is None or not  isinstance(agent, Agent):
            return None
        return agent.name

    @property
    def predecessor_agent(self) -> Agent:
        """
        Returns the predecessor agent of the current agent.
        """
        return self._predecessor_agent

    @predecessor_agent.setter
    def predecessor_agent(self, agent: Agent):
        """
        Sets the predecessor agent for the current agent.
        Args:
            agent (Agent): The predecessor agent to be set.
        """
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


class PromptTestingAgentCreator(MonkaiAgentCreator):
    """
    A class to create and manage agents for prompt testing and optimization.
    Supports multiple system prompts and AI-enhanced prompt generation.
    """
    def __init__(self, 
                 client: OpenAI,
                 base_prompt: str,
                 additional_prompts: Optional[Dict[str, str]] = None,
                 enable_ai_prompt_generation: bool = False,
                 model: str = "gpt-4"):
        """
        Initialize the PromptTestingAgentCreator.

        Args:
            client (OpenAI): The OpenAI client instance
            base_prompt (str): The default system prompt
            additional_prompts (Dict[str, str], optional): Additional prompts to test
            enable_ai_prompt_generation (bool): Whether to enable AI prompt generation
            model (str): The model to use for the agent
        """
        super().__init__()
        self.client = client
        self.base_prompt = base_prompt
        self.additional_prompts = additional_prompts or {}
        self.enable_ai_prompt_generation = enable_ai_prompt_generation
        self.model = model
        self._current_prompt_name = "Base Prompt"
        self._current_prompt = base_prompt
        self._ai_enhanced_prompt = None

    async def generate_enhanced_prompt(self) -> str:
        """
        Generate an AI-enhanced prompt by analyzing existing prompts.
        
        Returns:
            str: The generated enhanced prompt
        """
        all_prompts = {"Base Prompt": self.base_prompt, **self.additional_prompts}
        prompt_analysis = "\n".join([
            f"Prompt {i+1}:\n{prompt}\n"
            for i, prompt in enumerate(all_prompts.values())
        ])
        
        messages = [
            {"role": "system", "content": "You are an expert in prompt engineering and optimization."},
            {"role": "user", "content": f"""Analyze these prompts and create an enhanced version that combines their strengths:
            
{prompt_analysis}

Create a new prompt that:
1. Synthesizes the best aspects of all prompts
2. Adds improvements and optimizations
3. Maintains clarity and structure
4. Is more comprehensive and effective

Format the response as a complete system prompt."""}
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content

    def set_current_prompt(self, prompt_name: str):
        """
        Set the current prompt to use for the agent.

        Args:
            prompt_name (str): Name of the prompt to use
        """
        if prompt_name == "Base Prompt":
            self._current_prompt = self.base_prompt
        elif prompt_name == "AI-Enhanced Expert" and self._ai_enhanced_prompt:
            self._current_prompt = self._ai_enhanced_prompt
        elif prompt_name in self.additional_prompts:
            self._current_prompt = self.additional_prompts[prompt_name]
        else:
            raise ValueError(f"Unknown prompt name: {prompt_name}")
        
        self._current_prompt_name = prompt_name

    def get_agent(self) -> Agent:
        """
        Creates and returns an agent instance with the current prompt.

        Returns:
            Agent: The created agent instance
        """
        return Agent(
            name=f"TestAgent_{self._current_prompt_name}",
            instructions=self._current_prompt,
            model=self.model
        )

    def get_agent_briefing(self) -> str:
        """
        Returns a brief description of the agent's capabilities.

        Returns:
            str: Description of the agent's capabilities
        """
        return f"Agent using {self._current_prompt_name} for prompt testing and optimization"

    async def initialize(self):
        """
        Initialize the agent creator, including AI prompt generation if enabled.
        """
        if self.enable_ai_prompt_generation:
            print("\nGenerating AI-enhanced prompt...")
            self._ai_enhanced_prompt = await self.generate_enhanced_prompt()
            print("AI-enhanced prompt generated successfully!")

    @property
    def available_prompts(self) -> List[str]:
        """
        Get list of available prompt names.

        Returns:
            List[str]: List of available prompt names
        """
        prompts = ["Base Prompt"] + list(self.additional_prompts.keys())
        if self.enable_ai_prompt_generation and self._ai_enhanced_prompt:
            prompts.append("AI-Enhanced Expert")
        return prompts