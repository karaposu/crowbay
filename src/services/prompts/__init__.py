# filepath: src/services/prompts/__init__.py

"""Clarifier prompt assets — the LLM-facing text, kept apart from the engine.

`services/clarifier.py` is the engine (routing/suppression/persistence, no
prompts). This package holds the prompts a real LLM backend uses. Prompt
strings + Pydantic output schemas are pure Python (importable keyless); only
the `check_*` functions touch LangChain, and they lazy-import it so CI and
the deterministic mock never need the dependency or an API key.
"""

from services.prompts.clarification_prompts import (
    ATTRIBUTE_CODE_MAP,
    SEMANTIC_ATTRIBUTE_CHECKER,
    AttributeReport,
    check_attributes,
    to_entry_results,
)
from services.prompts.consumer_prompts import (
    CHANNEL_COMPOSITION_CODE_MAP,
    FULL_CONSUMER_PROMPT,
    ConsumerReport,
    consume_submission,
    to_llm_output,
)

__all__ = [
    "ATTRIBUTE_CODE_MAP",
    "CHANNEL_COMPOSITION_CODE_MAP",
    "FULL_CONSUMER_PROMPT",
    "SEMANTIC_ATTRIBUTE_CHECKER",
    "AttributeReport",
    "ConsumerReport",
    "check_attributes",
    "consume_submission",
    "to_entry_results",
    "to_llm_output",
]
