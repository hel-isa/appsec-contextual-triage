"""
Shared deterministic triage logic for AppSec Contextual Triage.

Single source of truth for the reachability check used by both
Phase 1 (deterministic gate) and Phase 2 (local-LLM audit layer).

The check is intentionally string-based for this proof of concept;
see the README roadmap for the planned AST-aware version.
"""
from __future__ import annotations

# Demo scenario: pandas==1.5.3 RCE in pd.read_pickle
CRITICAL_FUNCTION = "read_pickle"


def is_sink_used(source_code: str, sink: str = CRITICAL_FUNCTION) -> bool:
    """Return True if the risky sink appears in the given source code."""
    return sink in source_code


def get_verdict(source_code: str, sink: str = CRITICAL_FUNCTION) -> str:
    """Map the reachability check to a pipeline verdict ('BLOCK' or 'ALLOW')."""
    return "BLOCK" if is_sink_used(source_code, sink) else "ALLOW"
