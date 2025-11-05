"""
Agentic Category Intelligence System

This package implements an AI-guided data collection and validation system
with ZERO fabrication tolerance.

Architecture:
- OrchestratorAgent: Coordinates all agents, makes accept/reject/refine decisions
- Collection Agents: Acquire data from real sources
- Validation Agents: Verify quality, relevance, and source traceability
- Communication Protocol: Structured message passing between agents

Core Principle: Every data point must be traceable to a real source.
"""

from .base import (
    Agent,
    AgentMessage,
    DataSubmission,
    ValidationResult,
    OrchestratorDecision,
    TaskAssignment,
    MessageType,
    Decision,
    Priority,
)

from .orchestrator import OrchestratorAgent
from .collectors import (
    MarketDataAgent,
    BrandDiscoveryAgent,
    PricingScraperAgent,
    ResourceCuratorAgent,
)
from .validators import (
    QualityValidationAgent,
    RelevanceValidationAgent,
    SourceValidationAgent,
    GapIdentificationAgent,
)

__all__ = [
    # Base
    "Agent",
    "AgentMessage",
    "DataSubmission",
    "ValidationResult",
    "OrchestratorDecision",
    "TaskAssignment",
    "MessageType",
    "Decision",
    "Priority",
    # Orchestrator
    "OrchestratorAgent",
    # Collectors
    "MarketDataAgent",
    "BrandDiscoveryAgent",
    "PricingScraperAgent",
    "ResourceCuratorAgent",
    # Validators
    "QualityValidationAgent",
    "RelevanceValidationAgent",
    "SourceValidationAgent",
    "GapIdentificationAgent",
]
