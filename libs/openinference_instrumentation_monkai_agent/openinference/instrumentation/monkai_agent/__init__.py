import logging
from importlib import import_module
from typing import Any, Collection

from opentelemetry import trace as trace_api
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor  # type: ignore
from wrapt import wrap_function_wrapper

from monkai_agent.src.providers import OpenAIProvider, AzureProvider, LLMProvider
from openinference.instrumentation import OITracer, TraceConfig
from openinference.instrumentation.monkai_agent._wrappers import (
    _OpenAIProviderWrapper,
    _AzureProviderWrapper,
    _BaseProviderWrapper
)
from openinference.instrumentation.monkai_agent.version import __version__

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

_instruments = ("monkai_agent >= 0.0.33",)

class MonkaiAgentInstrumentor(BaseInstrumentor):  # type: ignore[misc]
    """An instrumentor for the MonkAI agent framework."""

    __slots__ = ("_original_openai_get_completion", "_original_azure_get_completion", "_tracer")

    def instrumentation_dependencies(self) -> Collection[str]:
        return _instruments

    def _instrument(self, **kwargs: Any) -> None:
        if not (tracer_provider := kwargs.get("tracer_provider")):
            tracer_provider = trace_api.get_tracer_provider()
        if not (config := kwargs.get("config")):
            config = TraceConfig()
        else:
            assert isinstance(config, TraceConfig)
        self._tracer = OITracer(
            trace_api.get_tracer(__name__, __version__, tracer_provider),
            config=config,
        )

        # Wrap OpenAI provider
        self._original_openai_get_completion = OpenAIProvider.get_completion
        wrap_function_wrapper(
            module="monkai_agent.src.providers",
            name="OpenAIProvider.get_completion",
            wrapper=_OpenAIProviderWrapper(tracer=self._tracer),
        )

        # Wrap Azure provider
        self._original_azure_get_completion = AzureProvider.get_completion
        wrap_function_wrapper(
            module="monkai_agent.src.providers",
            name="AzureProvider.get_completion",
            wrapper=_AzureProviderWrapper(tracer=self._tracer),
        )

        # Wrap base LLM provider for any custom implementations
        wrap_function_wrapper(
            module="monkai_agent.src.providers",
            name="LLMProvider.get_completion",
            wrapper=_BaseProviderWrapper(tracer=self._tracer),
        )

    def _uninstrument(self, **kwargs: Any) -> None:
        monkai_module = import_module("monkai_agent.src.providers")
        if self._original_openai_get_completion is not None:
            monkai_module.OpenAIProvider.get_completion = self._original_openai_get_completion
        if self._original_azure_get_completion is not None:
            monkai_module.AzureProvider.get_completion = self._original_azure_get_completion