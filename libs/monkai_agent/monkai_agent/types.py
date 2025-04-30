"""
This module defines the data types and models used by the MonkAI agent. It includes class and type definitions that represent the agent's functions, processable messages, instructions, and associated models. 

These definitions play a crucial role in ensuring data consistency and validation, facilitating maintenance and seamless scalability of the codebase. 

"""

from openai.types.chat import ChatCompletionMessage
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
    Function,
)
from typing import Any, List, Callable, Union, Optional
from enum import Enum
# Third-party imports
from pydantic import BaseModel

AgentFunction = Callable[[], Union[str, "Agent", dict]]

class AgentStatus(int, Enum):
    """
    Enum representing the status of an agent.
    
    """
    IDLE = 0
    """
    The agent is idle and not processing any tasks.
    
    """
    PROCESSING = 1
    """
    The agent is currently processing a task.
    
    """
    COMPLETED = 2
    """
    The agent has completed its task.
    
    """
    ERROR = 3
    """
    The agent encountered an error during processing.
    
    """
class Agent(BaseModel):
    """
    Represents a function that an agent can perform.

    """
    name: str = "Agent"
    """
    Name of Agent   
    
    """
    model: str = None
    """
    The model used by the agent.
    
    """
    instructions: Union[str, Callable[[], str]] = "You are a helpful agent."
    """
    Instructions for the agent.

    """
    functions: List[AgentFunction] = []
    """
    List of functions the agent can perform. 
    
    """
    tool_choice: str = None
    """
    The tool choice for the agent.
    
    """
    parallel_tool_calls: bool = True
    """
    Whether the agent can make parallel tool calls. 

    """
    external_content: bool = False
    """
    Whether the agent can use external content.

    """
    context_variables: dict = {}
    """
    Default context variables for the agent.
    """
    predecessor_agent: Optional["Agent"] = None

    """
    The agent's predecessor.
    """
    sucessors_agent: Optional[List["Agent"]] = None
    """
    The agent's successors.
    """
    status: AgentStatus = AgentStatus.IDLE
    

class Response(BaseModel):
    """
    Represents a response from an agent.
 
    """
    messages: List = []
    """
    List of messages in the response.

    """
    agent: Optional[Agent] = None
    """
    The agent that generated the response.

    """
    context_variables: dict = {}
    """
    Context variables associated with the response.

    """  


class Result(BaseModel):
    """
    Encapsulates the possible return values for an agent function.
    
    """

    value: str = ""
    """
    The result value as a string.
    """
    agent: Optional[Agent] = None
    """
    The agent instance, if applicable.
    """
    context_variables: dict = {}
    """
    A dictionary of context variables.
    """

class PromptTest(BaseModel):
    """
    Represents a test case for a prompt.
    """
    name: str
    """
    Name of the test case
    """
    input_text: str
    """
    Input text to test the prompt with
    """
    memory: Optional[Any] = None
    """
    Input text to test the prompt with
    """
    expected_output: str
    """
    Expected output for the test case
    """
    actual_output: Optional[str] = None
    """
    Actual output from the test
    """
    success: Optional[bool] = None
    """
    Whether the test passed
    """
    metadata: dict = {}
    """
    Additional metadata about the test
    """

class PromptOptimizer(BaseModel):
    """
    Represents a prompt optimization configuration.
    """
    name: str = "PromptOptimizer"
    """
    Name of the optimizer
    """
    model: str = "gpt-4o"
    """
    The model used for optimization
    """
    instructions: str = """You are a prompt optimization expert. Your task is to analyze existing prompts and suggest improvements based on:
    1. Clarity and specificity
    2. Task alignment
    3. Context preservation
    4. Output format consistency
    5. Edge case handling
    
    Provide detailed explanations for your suggestions and include example improvements."""
    """
    Instructions for the optimizer
    """
    optimization_criteria: List[str] = [
        "clarity",
        "specificity",
        "task_alignment",
        "context_preservation",
        "output_format",
        "edge_cases"
    ]
    """
    Criteria for prompt optimization
    """
    test_cases: List[PromptTest] = []
    """
    Test cases to validate prompt improvements
    """