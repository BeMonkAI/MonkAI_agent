"""
LLM providers module for MonkAI framework.
Supports multiple LLM providers including OpenAI and Groq.
"""

import copy
from typing import Optional, Any
from groq import Groq
import os
import json
from monkai_agent import LLMProvider


 # Available Groq models
GROQ_MODELS = [
    'llama-3.3-70b-versatile',
    'deepseek-r1-distill-qwen-32b',
    'gemma2-9b-it',
    'mistral-saba-24b',
    'qwen-2.5-coder-32b'
]       

class GroqProvider(LLMProvider):
    """Groq LLM provider"""
    
    def __init__(self, api_key: str):
        """
        Initialize GroqProvider with API key.
        Args:
            api_key (str): Groq API key.
        """
        super().__init__()
        self.api_key = api_key
    
    def get_client(self):
        """Get Groq client instance."""
        return Groq(api_key=self.api_key)
    
    def _clean_messages(self, messages: list) -> list:
        """
        Clean messages to ensure compatibility with Groq API.
        Args:
            messages (list): List of messages to clean.
        """
        cleaned_messages = []
        for msg in messages:
            # Create base message with required fields
            cleaned_msg = {
                "role": msg["role"],
                "content": msg.get("content", "") if msg.get("content") is not None else ""
            }
            
            # Handle tool messages  
            if msg["role"] == "tool":
                if "tool_call_id" not in msg:
                    continue  # Skip tool messages without tool_call_id
                cleaned_msg["tool_call_id"] = msg["tool_call_id"]

            # Handle assistant messages
            elif msg["role"] == "assistant":
                # Remove unsupported fields
                if "reasoning" in msg:
                    del msg["reasoning"]
                
                # Handle tool_calls and function_call
                if "tool_calls" in msg and msg["tool_calls"] and len(msg["tool_calls"]) > 0:
                    first_tool = msg["tool_calls"][0]
                    cleaned_msg["function_call"] = {
                        "name": first_tool["function"]["name"],
                        "arguments": first_tool["function"]["arguments"]
                    }
                elif "function_call" in msg and msg["function_call"]:
                    cleaned_msg["function_call"] = msg["function_call"]
                # If no valid tool_calls or function_call, don't include function_call field
            
            cleaned_messages.append(cleaned_msg)
        return cleaned_messages
    
    def get_completion(self, messages: list, **kwargs):
        """
        Get completion from Groq API.
        Args:
            messages (list): List of messages to send to the API.
              
          model: ID of the model to use. For details on which models are compatible with the Chat
              API, see available [models](/docs/models)

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text so far, decreasing the model's likelihood to
              repeat the same line verbatim.

          function_call: Deprecated in favor of `tool_choice`.

              Controls which (if any) function is called by the model. `none` means the model
              will not call a function and instead generates a message. `auto` means the model
              can pick between generating a message or calling a function. Specifying a
              particular function via `{"name": "my_function"}` forces the model to call that
              function.

              `none` is the default when no functions are present. `auto` is the default if
              functions are present.

          functions: Deprecated in favor of `tools`.

              A list of functions the model may generate JSON inputs for.

          logit_bias: This is not yet supported by any of our models. Modify the likelihood of
              specified tokens appearing in the completion.

          logprobs: This is not yet supported by any of our models. Whether to return log
              probabilities of the output tokens or not. If true, returns the log
              probabilities of each output token returned in the `content` of `message`.

          max_completion_tokens: The maximum number of tokens that can be generated in the chat completion. The
              total length of input tokens and generated tokens is limited by the model's
              context length.

          max_tokens: Deprecated in favor of `max_completion_tokens`. The maximum number of tokens
              that can be generated in the chat completion. The total length of input tokens
              and generated tokens is limited by the model's context length.

          n: How many chat completion choices to generate for each input message. Note that
              the current moment, only n=1 is supported. Other values will result in a 400
              response.

          parallel_tool_calls: Whether to enable parallel function calling during tool use.

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on
              whether they appear in the text so far, increasing the model's likelihood to
              talk about new topics.

          reasoning_format: Specifies how to output reasoning tokens

          response_format: An object specifying the format that the model must output.

              Setting to `{ "type": "json_object" }` enables JSON mode, which guarantees the
              message the model generates is valid JSON.

              **Important:** when using JSON mode, you **must** also instruct the model to
              produce JSON yourself via a system or user message.

          seed: If specified, our system will make a best effort to sample deterministically,
              such that repeated requests with the same `seed` and parameters should return
              the same result. Determinism is not guaranteed, and you should refer to the
              `system_fingerprint` response parameter to monitor changes in the backend.

          service_tier: The service tier to use for the request. Defaults to `on_demand`.

              - `auto` will automatically select the highest tier available within the rate
                limits of your organization.
              - `flex` uses the flex tier, which will succeed or fail quickly.

          stop: Up to 4 sequences where the API will stop generating further tokens. The
              returned text will not contain the stop sequence.

          stream: If set, partial message deltas will be sent. Tokens will be sent as data-only
              [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format)
              as they become available, with the stream terminated by a `data: [DONE]`
              message. [Example code](/docs/text-chat#streaming-a-chat-completion).

          temperature: What sampling temperature to use, between 0 and 2. Higher values like 0.8 will
              make the output more random, while lower values like 0.2 will make it more
              focused and deterministic. We generally recommend altering this or top_p but not
              both

          tool_choice: Controls which (if any) tool is called by the model. `none` means the model will
              not call any tool and instead generates a message. `auto` means the model can
              pick between generating a message or calling one or more tools. `required` means
              the model must call one or more tools. Specifying a particular tool via
              `{"type": "function", "function": {"name": "my_function"}}` forces the model to
              call that tool.

              `none` is the default when no tools are present. `auto` is the default if tools
              are present.

          tools: A list of tools the model may call. Currently, only functions are supported as a
              tool. Use this to provide a list of functions the model may generate JSON inputs
              for. A max of 128 functions are supported.

          top_logprobs: This is not yet supported by any of our models. An integer between 0 and 20
              specifying the number of most likely tokens to return at each token position,
              each with an associated log probability. `logprobs` must be set to `true` if
              this parameter is used.

          top_p: An alternative to sampling with temperature, called nucleus sampling, where the
              model considers the results of the tokens with top_p probability mass. So 0.1
              means only the tokens comprising the top 10% probability mass are considered. We
              generally recommend altering this or temperature but not both.

          user: A unique identifier representing your end-user, which can help us monitor and
              detect abuse.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        Returns:
            ChatCompletion| Stream[ChatCompletionChunk]: Groq API response.
        """
        client = self.get_client()
        if 'agent' in kwargs:
            kwargs.pop('agent')
        # Clean and format messages
        formatted_messages = self._clean_messages(messages)
        # Check if this is a follow-up after tool execution
        # TODO: prove is this is helpful for any possible case
        last_messages = formatted_messages[-2:] if len(formatted_messages) >= 2 else formatted_messages
        has_tool_response = any(msg.get("role") == "tool" for msg in last_messages)
        
        # If we received a tool response, encourage completion
        if has_tool_response:
            formatted_messages.append({
                "role": "system",
                "content": "If all required tools have been executed and results are sufficient, please provide a final response without calling additional tools."
            })
            
        if "tool_choice" not in kwargs or kwargs["tool_choice"] not in ["none", "auto", "required"]:
            kwargs["tool_choice"] = "auto" if "tools" in kwargs and kwargs["tools"] else "none"
            
        response = client.chat.completions.create(
            messages=formatted_messages,
            **kwargs
        )
        return response


