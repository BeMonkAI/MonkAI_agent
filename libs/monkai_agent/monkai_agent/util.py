"""
This module is responsible for providing utility functions that aid in the operation of the MonkAI agent. 

These functions include printing debug messages with timestamps, merging dictionary fields, and handling chunked responses. 

These utilities are essential for the maintenance and efficient operation of the agent, providing supporting functionality that is reused across multiple parts of the code.
"""

import inspect
from datetime import datetime
from functools import wraps
from .types import AgentStatus, Agent
from .monkai_agent_creator import MonkaiAgentCreator


def completion_task(func):
    """
    A decorator that manages the agent's status during task execution.
    Sets the agent's status to COMPLETED if the task completes successfully,
    or ERROR if an exception occurs. Supports both synchronous and asynchronous functions.

    Args:
        func: The function to be decorated

    Returns:
        callable: The wrapped function that manages the agent's status
    """
    if inspect.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                if not (len(args) > 0 and isinstance(args[0], MonkaiAgentCreator)):
                    return await func(*args, **kwargs)
                agent = args[0].get_agent()
                result = await func(*args, **kwargs)
                agent.status = AgentStatus.COMPLETED
                return result
            except Exception as e:
                if len(args) > 0 and isinstance(args[0], MonkaiAgentCreator):
                    agent = args[0].get_agent()
                    agent.status = AgentStatus.ERROR
                raise e
        return async_wrapper
    else:
        @wraps(func)
        def sync_wrapper(*args, **kwargs): 
            try:
                if not (len(args) > 0 and isinstance(args[0], MonkaiAgentCreator)):
                    return func(*args, **kwargs)
                agent = args[0].get_agent()
                result = func(*args, **kwargs)
                agent.status = AgentStatus.COMPLETED
                return result
            except Exception as e:
                if len(args) > 0 and isinstance(args[0], MonkaiAgentCreator):
                    agent = args[0].get_agent()
                    agent.status = AgentStatus.ERROR
                raise e
        return sync_wrapper


def debug_print(debug: bool, *args: str) -> None:
    """
    Prints debug messages with a timestamp if debugging is enabled.

    Args:
        debug (bool): Flag indicating whether debugging is enabled.
        *args (str): Variable length argument list of messages to print.
    """
    if not debug:
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = " ".join(map(str, args))
    print(f"\033[97m[\033[90m{timestamp}\033[97m]\033[90m {message}\033[0m")


def merge_fields(target, source):
    """
    Merges fields from the source dictionary into the target dictionary.

    Args:
        target (dict): The target dictionary to merge fields into.
        source (dict): The source dictionary to merge fields from.
    """
    for key, value in source.items():
        if isinstance(value, str):
            target[key] += value
        elif value is not None and isinstance(value, dict):
            merge_fields(target[key], value)


def merge_chunk(final_response: dict, delta: dict) -> None:
    """
    Merges a chunk of data (delta) into the final response dictionary.

    Args:
        final_response (dict): The final response dictionary to merge data into.
        delta (dict): The chunk of data to merge into the final response.
    """
    delta.pop("role", None)
    merge_fields(final_response, delta)

    tool_calls = delta.get("tool_calls")
    if tool_calls and len(tool_calls) > 0:
        index = tool_calls[0].pop("index")
        merge_fields(final_response["tool_calls"][index], tool_calls[0])


def function_to_json(func) -> dict:
    """
    Converts a Python function into a JSON-serializable dictionary
    that describes the function's signature, including its name,
    description, and parameters.

    Args:
        func: The function to be converted.

    Returns:
        A dictionary representing the function's signature in JSON format.
    """
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
        type(None): "null",
    }

    try:
        signature = inspect.signature(func)
    except ValueError as e:
        raise ValueError(
            f"Failed to get signature for function {func.__name__}: {str(e)}"
        )

    parameters = {}
    for param in signature.parameters.values():
        try:
            param_type = type_map.get(param.annotation, "string")
        except KeyError as e:
            raise KeyError(
                f"Unknown type annotation {param.annotation} for parameter {param.name}: {str(e)}"
            )
        parameters[param.name] = {"type": param_type}

    required = [
        param.name
        for param in signature.parameters.values()
        if param.default == inspect._empty
    ]

    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": func.__doc__ or "",
            "parameters": {
                "type": "object",
                "properties": parameters,
                "required": required,
            },
        },
    }


