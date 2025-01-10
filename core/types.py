from openai.types.chat import ChatCompletionMessage
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
    Function,
)
from typing import List, Callable, Union, Optional

# Third-party imports
from pydantic import BaseModel

AgentFunction = Callable[[], Union[str, "Agent", dict]]


class Agent(BaseModel):
    """
    Represents a function that an agent can perform.

    """
    name: str = "Agent"
    """
    Name of Agent   
    
    """
    model: str = "gpt-4o"
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