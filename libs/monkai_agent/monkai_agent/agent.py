"""
This module defines the base agent class and related types.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from .types import AgentFunction

@dataclass
class BaseAgent:
    """Base class for all agents in the MonkAI framework."""
    
    name: str
    instructions: str
    model: str
    functions: List[AgentFunction] = None
    tool_choice: str = "auto"
    parallel_tool_calls: bool = False

    def __post_init__(self):
        if self.functions is None:
            self.functions = [] 