"""
This module is responsible for processing and printing streaming responses from an agent, formatting the output with colors for easier viewing on the terminal. 

The term "repl" is widely recognized in the development community and reflects the classic Read-Eval-Print Loop pattern commonly used in interactive environments. 

This choice reinforces familiarity and facilitates understanding of its purpose within the framework.

"""


import json
from .base import AgentManager, Agent



def process_and_print_streaming_response(response):
    """
    Processes and prints the streaming response.

    Args:
        response (dict): The streaming response to be processed and printed.
    """
    content = ""
    last_sender = ""

    for chunk in response:
        if "sender" in chunk:
            last_sender = chunk["sender"]

        if "content" in chunk and chunk["content"] is not None:
            if not content and last_sender:
                print(f"\033[94m{last_sender}:\033[0m", end=" ", flush=True)
                last_sender = ""
            print(chunk["content"], end="", flush=True)
            content += chunk["content"]

        if "tool_calls" in chunk and chunk["tool_calls"] is not None:
            for tool_call in chunk["tool_calls"]:
                f = tool_call["function"]
                name = f["name"]
                if not name:
                    continue
                print(f"\033[94m{last_sender}: \033[95m{name}\033[0m()")

        if "delim" in chunk and chunk["delim"] == "end" and content:
            print()  # End of response message
            content = ""

        if "response" in chunk:
            return chunk["response"]
  
def pretty_print_messages(messages) -> None:
    """
    Pretty prints the messages with specific formatting.

    Args:
        messages (list): List of messages to be printed.
    """
    for message in messages:
        if message["role"] != "assistant":
            continue

        # print agent name in blue
        print(f"\033[94m{message['sender']}\033[0m:", end=" ")

        # print response, if any
        if message["content"]:
            print(message["content"])

        # print tool calls in purple, if any
        tool_calls = message.get("tool_calls") or []
        if len(tool_calls) > 1:
            print()
        for tool_call in tool_calls:
            f = tool_call["function"]
            name, args = f["name"], f["arguments"]
            arg_str = json.dumps(json.loads(args)).replace(":", "=")
            print(f"\033[95m{name}\033[0m({arg_str[1:-1]})")


async def __run_demo_loop(manager:AgentManager,  agent=None, context_variables={}, model="gpt-4o",stream=False, debug=False) -> None:
    """
    Runs the demo loop for interacting with the MonkAI Agent.

    Args:
        manager (AgentManager): The manager instance to run the agent.
        context_variables (dict, optional): Context variables for the agent. Defaults to {}.
        model (str, optional): The model to use for the agent. Defaults to "gpt-4o".
        stream (bool, optional): Flag to enable streaming response. Defaults to False.
        debug (bool, optional): Flag to enable debugging. Defaults to False.
    """
    print("Starting MonkAI Agent ✨")

    messages = []

    while True:
        user_input = input("\033[38;2;167;112;69mUser\033[0m: ")
        if user_input.lower() == "exit":
            print("Exiting MonkAI Agent 🚀")
            break
        
        response = await manager.run(
            agent=agent,
            user_message=user_input,
            user_history=messages
        )

        if stream:
            response = process_and_print_streaming_response(response)
        else:
            pretty_print_messages(response.messages)

        messages.extend(response.messages)
        agent = response.agent

async def run_simples_demo_loop(agent:Agent,  client, context_variables={}, model="gpt-4o",stream=False, debug=False) -> None:
    manager = AgentManager(client=client, agents_creators=[])
    await __run_demo_loop(manager, agent=agent, context_variables=context_variables, model=model, stream=stream, debug=debug)
    

async def run_demo_loop(manager:AgentManager,  context_variables={}, model="gpt-4o",stream=False, debug=False) -> None:
    """
    Runs the demo loop for interacting with the MonkAI Agent.

    Args:
        manager (AgentManager): The manager instance to run the agent.
        context_variables (dict, optional): Context variables for the agent. Defaults to {}.
        model (str, optional): The model to use for the agent. Defaults to "gpt-4o".
        stream (bool, optional): Flag to enable streaming response. Defaults to False.
        debug (bool, optional): Flag to enable debugging. Defaults to False.
    """
    await __run_demo_loop(manager, context_variables=context_variables, model=model, stream=stream, debug=debug)
