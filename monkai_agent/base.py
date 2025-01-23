"""
This module is responsible for providing the core functionality and type definitions for the MonkAI agent. 

It sets up the necessary environment, including logging configuration, importing essential modules, and defining constants and global variables. 

In addition, it imports and uses utility functions and specific types that are essential for the efficient operation of the agent.
"""

import logging
from .types import Response
from .monkai_agent_creator import MonkaiAgentCreator
from .triage_agent_creator import TriageAgentCreator 
from .types import Response
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import copy
import json
from collections import defaultdict
from typing import List
from openai import OpenAI

__DOCUMENT_GUARDRAIL_TEXT__ = "RESPONDER SÓ USANDO A INFORMAÇÃO DOS DOCUMENTOS: "

# Local imports
from .util import function_to_json, debug_print, merge_chunk
from .types import (
    Agent,
    AgentFunction,
    ChatCompletionMessage,
    ChatCompletionMessageToolCall,
    Function,
    Response,
    Result,
)

__CTX_VARS_NAME__ = "context_variables"

class AgentManager:
    """
    Manages the interaction with AI agents.

    This class is responsible for managing the lifecycle of AI agents, handling
    user interactions, processing tool calls, and managing context variables.

    """

    def __init__(self, client, agents_creators: list[MonkaiAgentCreator], context_variables=None, stream=False, debug=False):    
        """
        Initializes the AgentManager with the provided client, agent creators, and optional parameters.
        """
        
        self.client = OpenAI() if not client else client
        """
        The client instance to use for the agent.
        """
        self.agents_creators = agents_creators
        """
        A list of agent creators to initialize the triage agent.
        """
        self.triage_agent_criator = TriageAgentCreator(agents_creators)
        """
        The creator for the triage agent.
        """
        self.context_variables = context_variables or {}
        """
        Context variables for the agent.
        """
        self.stream = stream
        """
        Flag to enable streaming response.
        """
        self.debug = debug
        """
        Flag to enable debugging.
        """
        self.agent = self.triage_agent_criator.get_agent()
        """
        The current agent instance.
        """

    def get_chat_completion(
        self,
        agent: Agent,
        history: List,
        context_variables: dict,
        model_override: str,
        stream: bool,
        debug: bool,
    ) -> ChatCompletionMessage:
        """

        Generates a chat completion based on the user message and conversation history.

        Returns:
            Completion: The generated chat completion.

        """
        
        context_variables = defaultdict(str, context_variables)
        instructions = (
            agent.instructions(context_variables)
            if callable(agent.instructions)
            else agent.instructions
        )
        messages = [{"role": "system", "content": instructions}] + history
        debug_print(debug, "Getting chat completion for...:", messages)

        tools = [function_to_json(f) for f in agent.functions]
        # hide context_variables from model
        for tool in tools:
            params = tool["function"]["parameters"]
            params["properties"].pop(__CTX_VARS_NAME__, None)
            if __CTX_VARS_NAME__ in params["required"]:
                params["required"].remove(__CTX_VARS_NAME__)

        create_params = {
            "model": model_override or agent.model,
            "messages": messages,
            "tools": tools or None,
            "tool_choice": agent.tool_choice,
            "stream": stream,
        }

        if tools:
            create_params["parallel_tool_calls"] = agent.parallel_tool_calls

        return self.client.chat.completions.create(**create_params)

    def handle_function_result(self, result, debug) -> Result:
        """

        Handles the result of a function call, updating context variables and processing the result.

        Returns:
            PartialResponse: The response after handling the function result.

        """
        
        match result:
            case Result() as result:
                return result

            case Agent() as agent:
                return Result(
                    value=json.dumps({"assistant": agent.name}),
                    agent=agent,
                )
            case _:
                try:
                    return Result(value=str(result))
                except Exception as e:
                    error_message = f"Failed to cast response to string: {result}. Make sure agent functions return a string or Result object. Error: {str(e)}"
                    debug_print(debug, error_message)
                    raise TypeError(error_message)

    def handle_tool_calls(
        self,
        tool_calls: List[ChatCompletionMessageToolCall],
        functions: List[AgentFunction],
        context_variables: dict,
        debug: bool,
    ) -> Response:
        """
        Handles tool calls by executing the corresponding functions.

        Args:
            tool_calls (list): List of tool calls to handle.
            functions (list): List of functions that the agent can perform.
            context_variables (dict): Context variables for the agent.
            debug (bool): Flag to enable debugging.

        Returns:
            Response: The response after handling the tool calls.
        """
        
        function_map = {f.__name__: f for f in functions}
        partial_response = Response(
            messages=[], agent=None, context_variables={})

        for tool_call in tool_calls:
            name = tool_call.function.name
            # handle missing tool case, skip to next tool
            if name not in function_map:
                debug_print(debug, f"Tool {name} not found in function map.")
                partial_response.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "tool_name": name,
                        "content": f"Error: Tool {name} not found.",
                    }
                )
                continue
            args = json.loads(tool_call.function.arguments)
            debug_print(
                debug, f"Processing tool call: {name} with arguments {args}")

            func = function_map[name]
            # pass context_variables to agent functions
            if __CTX_VARS_NAME__ in func.__code__.co_varnames:
                args[__CTX_VARS_NAME__] = context_variables
            raw_result = function_map[name](**args)

            result: Result = self.handle_function_result(raw_result, debug)
            partial_response.messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "tool_name": name,
                    "content": result.value,
                }
            )
            partial_response.context_variables.update(result.context_variables)
            if result.agent:
                partial_response.agent = result.agent

        return partial_response

    def __run_and_stream(
        self,
        agent: Agent,
        messages: List,
        context_variables: dict = {},
        model_override: str = None,
        debug: bool = False,
        max_turns: int = float("inf"),
        execute_tools: bool = True,
    ):
        active_agent = agent
        context_variables = copy.deepcopy(context_variables)
        history = copy.deepcopy(messages)
        init_len = len(messages)

        while len(history) - init_len < max_turns:

            message = {
                "content": "",
                "sender": agent.name,
                "role": "assistant",
                "function_call": None,
                "tool_calls": defaultdict(
                    lambda: {
                        "function": {"arguments": "", "name": ""},
                        "id": "",
                        "type": "",
                    }
                ),
            }

            # get completion with current history, agent
            completion = self.get_chat_completion(
                agent=active_agent,
                history=history,
                context_variables=context_variables,
                model_override=model_override,
                stream=True,
                debug=debug,
            )

            yield {"delim": "start"}
            for chunk in completion:
                delta = json.loads(chunk.choices[0].delta.json())
                if delta["role"] == "assistant":
                    delta["sender"] = active_agent.name
                yield delta
                delta.pop("role", None)
                delta.pop("sender", None)
                merge_chunk(message, delta)
            yield {"delim": "end"}

            message["tool_calls"] = list(
                message.get("tool_calls", {}).values())
            if not message["tool_calls"]:
                message["tool_calls"] = None
            debug_print(debug, "Received completion:", message)
            history.append(message)

            if not message["tool_calls"] or not execute_tools:
                debug_print(debug, "Ending turn.")
                break

            # convert tool_calls to objects
            tool_calls = []
            for tool_call in message["tool_calls"]:
                function = Function(
                    arguments=tool_call["function"]["arguments"],
                    name=tool_call["function"]["name"],
                )
                tool_call_object = ChatCompletionMessageToolCall(
                    id=tool_call["id"], function=function, type=tool_call["type"]
                )
                tool_calls.append(tool_call_object)

            # handle function calls, updating context_variables, and switching agents
            partial_response = self.handle_tool_calls(
                tool_calls, active_agent.functions, context_variables, debug
            )
            history.extend(partial_response.messages)
            context_variables.update(partial_response.context_variables)
            if partial_response.agent:
                active_agent = partial_response.agent

        yield {
            "response": Response(
                messages=history[init_len:],
                agent=active_agent,
                context_variables=context_variables,
            )
        }

    async def __run(
        self,
        agent: Agent,
        messages: List,
        context_variables: dict = {},
        model_override: str = None,
        stream: bool = False,
        debug: bool = False,
        max_turns: int = float("inf"),
        execute_tools: bool = True,
    ) -> Response:
        if stream:
            return self.__run_and_stream(
                agent=agent,
                messages=messages,
                context_variables=context_variables,
                model_override=model_override,
                debug=debug,
                max_turns=max_turns,
                execute_tools=execute_tools,
            )
        active_agent = agent
        context_variables = copy.deepcopy(context_variables)
        history = copy.deepcopy(messages)
        init_len = len(messages)

        while len(history) - init_len < max_turns and active_agent:
            if active_agent.external_content:
                history[-1]["content"] = __DOCUMENT_GUARDRAIL_TEXT__ +  history[-1]["content"]
            # get completion with current history, agentr
            completion = self.get_chat_completion(
                agent=active_agent,
                history=history,
                context_variables=context_variables,
                model_override=model_override,
                stream=stream,
                debug=debug,
            )
            message = completion.choices[0].message
            debug_print(debug, "Received completion:", message)
            message.sender = active_agent.name
            history.append(
                json.loads(message.model_dump_json())
            )  # to avoid OpenAI types (?)

            if not message.tool_calls or not execute_tools:
                debug_print(debug, "Ending turn.")
                break

            # handle function calls, updating context_variables, and switching agents
            partial_response = self.handle_tool_calls(
                message.tool_calls, active_agent.functions, context_variables, debug
            )
            history.extend(partial_response.messages)
            context_variables.update(partial_response.context_variables)
            if partial_response.agent is not None:
                active_agent = partial_response.agent


        return Response(
            messages=history[init_len:],
            agent=active_agent,
            context_variables=context_variables,
        )

    def get_triage_agent(self):
        """
        Returns the triage agent.

        Returns:
            Agent: The triage agent instance.
        """
        return self.triage_agent_criator.get_agent()

    async def run(self,user_message:str, user_history:list = None, agent=None, model_override="gpt-4o")->Response:

        """
        Executes the main workflow:
            - Handles the conversation with the user.
            - Manages the interaction with the agent.
            - Processes tool calls and updates context variables.

        Returns:
            Response: The response from the agent after processing the user message.
        """
        # Append user's message
        messages=user_history if user_history is not  None else []
        messages.append({"role": "user", "content": user_message})

        #Determined the agent to use
        agent_to_use = agent if agent is not None else self.agent

        # Run the conversation asynchronously
        response:Response = await self.__run(
            agent=agent_to_use,
            model_override=model_override,
            messages= messages,
            context_variables=self.context_variables,
            stream=self.stream,
            debug=self.debug,
        )
        assert(response is not None)
        return response