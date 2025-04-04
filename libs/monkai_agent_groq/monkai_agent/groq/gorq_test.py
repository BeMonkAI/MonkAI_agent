import json
from groq import Groq
import os
import config

# Initialize Groq client
client = Groq(api_key= config.GROQ_API_KEY)
model = "llama-3.3-70b-versatile"

# Define weather tools
def get_temperature(location: str):
    # This is a mock tool/function. In a real scenario, you would call a weather API.
    temperatures = {"New York": 22, "London": 18, "Tokyo": 26, "Sydney": 20}
    return temperatures.get(location, "Temperature data not available")

def get_weather_condition(location: str):
    # This is a mock tool/function. In a real scenario, you would call a weather API.
    conditions = {"New York": "Sunny", "London": "Rainy", "Tokyo": "Cloudy", "Sydney": "Clear"}
    return conditions.get(location, "Weather condition data not available")

# Define system messages and tools
messages = [
    {"role": "system", "content": "You are a helpful weather assistant."},
    {"role": "user", "content": "What's the weather like in New York and London?"},
]

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_temperature",
            "description": "Get the temperature for a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The name of the city",
                    }
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather_condition",
            "description": "Get the weather condition for a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The name of the city",
                    }
                },
                "required": ["location"],
            },
        },
    }
]

# Make the initial request
response = client.chat.completions.create(
    model=model, messages=messages, tools=tools, tool_choice="auto", max_completion_tokens=4096
)

response_message = response.choices[0].message
tool_calls = response_message.tool_calls

# Process tool calls
messages.append(response_message)

available_functions = {
    "get_temperature": get_temperature,
    "get_weather_condition": get_weather_condition,
}

for tool_call in tool_calls:
    function_name = tool_call.function.name
    function_to_call = available_functions[function_name]
    function_args = json.loads(tool_call.function.arguments)
    function_response = function_to_call(**function_args)

    messages.append(
        {
            "role": "tool",
            "content": str(function_response),
            "tool_call_id": tool_call.id,
        }
    )

# Make the final request with tool call results
final_response = client.chat.completions.create(
    model=model, messages=messages, tools=tools, tool_choice="auto", max_completion_tokens=4096
)

print(final_response.choices[0].message.content)