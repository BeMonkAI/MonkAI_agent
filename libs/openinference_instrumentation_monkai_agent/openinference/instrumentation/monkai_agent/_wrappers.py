from functools import partial
from typing import Any, Callable, Dict, Optional

from openinference.instrumentation import OITracer
from wrapt import ObjectProxy

class _BaseProviderWrapper:
    """Base wrapper for MonkAI agent LLM providers."""

    def __init__(self, tracer: OITracer):
        self._tracer = tracer

    def __call__(
        self,
        wrapped: Callable,
        instance: ObjectProxy,
        args: tuple,
        kwargs: Dict[str, Any],
    ) -> Any:
        with self._tracer.start_span(
            name=f"{instance.__class__.__name__}.get_completion",
            attributes={
                "ai.model": kwargs.get("model", "unknown"),
                "ai.temperature": kwargs.get("temperature"),
                "ai.max_tokens": kwargs.get("max_tokens"),
                "ai.top_p": kwargs.get("top_p"),
                "ai.frequency_penalty": kwargs.get("frequency_penalty"),
                "ai.presence_penalty": kwargs.get("presence_penalty"),
            },
        ) as span:
            # Record input messages
            messages = args[0] if args else kwargs.get("messages", [])
            for i, msg in enumerate(messages):
                span.set_attribute(f"ai.request.messages.{i}.role", msg.get("role", ""))
                span.set_attribute(f"ai.request.messages.{i}.content", msg.get("content", ""))

            response = wrapped(*args, **kwargs)

            # Record response
            completion = response.choices[0].message
            span.set_attribute("ai.response.role", completion.role)
            span.set_attribute("ai.response.content", completion.content)
            if completion.tool_calls:
                span.set_attribute("ai.response.tool_calls", str(completion.tool_calls))

            # Record usage statistics if available
            if hasattr(response, "usage"):
                span.set_attribute("ai.token_count.prompt", response.usage.prompt_tokens)
                span.set_attribute("ai.token_count.completion", response.usage.completion_tokens)
                span.set_attribute("ai.token_count.total", response.usage.total_tokens)

            return response

class _OpenAIProviderWrapper(_BaseProviderWrapper):
    """Wrapper for OpenAI provider."""
    def __call__(self, wrapped, instance, args, kwargs):
        # Add OpenAI-specific instrumentation attributes
        with self._tracer.start_span(
            name="OpenAIProvider.get_completion",
            attributes={"ai.provider": "openai"}
        ) as span:
            return super().__call__(wrapped, instance, args, kwargs)

class _AzureProviderWrapper(_BaseProviderWrapper):
    """Wrapper for Azure OpenAI provider."""
    def __call__(self, wrapped, instance, args, kwargs):
        # Add Azure-specific instrumentation attributes
        with self._tracer.start_span(
            name="AzureProvider.get_completion",
            attributes={
                "ai.provider": "azure",
                "ai.azure.endpoint": instance.endpoint,
                "ai.azure.api_version": instance.api_version
            }
        ) as span:
            return super().__call__(wrapped, instance, args, kwargs)