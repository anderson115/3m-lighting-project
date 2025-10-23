"""
OrchestratorAgent - NEW AGENTIC SYSTEM (Not Yet Active)

🔄 MIGRATION STATUS: This is the NEW AI-guided orchestrator
   - Status: Built and ready (Stages 1-2 complete)
   - Usage: Not yet active (will replace core/orchestrator.py)
   - Activation: Stage 8 of migration (see AGENTIC_ARCHITECTURE.md)

   See core/orchestrator.py for the LEGACY system currently in use.
   See AGENTIC_ARCHITECTURE.md for full migration roadmap.

Master Coordinator for Category Intelligence System

This agent coordinates all data collection and validation activities,
making ACCEPT/REJECT/REFINE decisions on submissions, and ensuring
100% of data is traceable to real sources (zero fabrication tolerance).

Decision Framework:
- ACCEPT: Validation score >= 0.9, all sources valid
- REFINE: Validation score 0.7-0.9, improvable data
- REJECT: Validation score < 0.7, untraceable sources, or fabrication detected
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio

from .base import (
    Agent,
    AgentMessage,
    DataSubmission,
    ValidationResult,
    OrchestratorDecision,
    TaskAssignment,
    Gap,
    ProgressReport,
    MessageType,
    Decision,
    Priority,
)

from .validators import (
    QualityValidationAgent,
    SourceValidationAgent,
    RelevanceValidationAgent,
    GapIdentificationAgent,
)


class OrchestratorAgent(Agent):
    """
    Master coordinator that orchestrates data collection and validation.

    Responsibilities:
    1. Assign collection tasks to specialized agents
    2. Receive and track data submissions
    3. Coordinate validation across 4 validation agents
    4. Make ACCEPT/REJECT/REFINE decisions
    5. Track progress toward completeness (95% threshold)
    6. Identify gaps and assign gap-filling tasks
    7. Enforce zero fabrication at every step

    Attributes:
        category (str): Target category (e.g., "garage storage")
        requirements (Dict): Data requirements (brands count, market data, etc.)
        submissions (Dict): All received submissions by ID
        accepted_data (Dict): Accepted submissions by data_type
        refinement_attempts (Dict): Track refinement iterations per submission
        completeness (float): Current progress (0.0-1.0)
    """

    def __init__(self, category: str, requirements: Dict[str, Any]):
        """
        Initialize orchestrator with category and data requirements.

        Args:
            category: Category name (e.g., "garage storage")
            requirements: Data requirements dict with structure:
                {
                    "brands": {"min_count": 50, "tier_distribution": {...}},
                    "market_size": {"required": True, "recency": "2023-2025"},
                    "pricing": {"min_products": 120, "min_retailers": 4},
                    "resources": {"min_count": 30},
                    "historical_data": {"required": True, "years": 5}
                }
        """
        super().__init__(agent_id="orchestrator")
        self.category = category
        self.requirements = requirements

        # Data tracking
        self.submissions: Dict[str, DataSubmission] = {}
        self.accepted_data: Dict[str, List[DataSubmission]] = {}
        self.rejected_data: Dict[str, DataSubmission] = {}
        self.refining_data: Dict[str, DataSubmission] = {}
        self.refinement_attempts: Dict[str, int] = {}

        # Validation agents
        self.quality_validator = QualityValidationAgent("quality_validator")
        self.source_validator = SourceValidationAgent("source_validator")
        self.relevance_validator = RelevanceValidationAgent("relevance_validator", category)
        self.gap_analyzer = GapIdentificationAgent("gap_analyzer")

        # Progress tracking
        self.completeness = 0.0
        self.gaps: List[Gap] = []

        self.log_action("initialized", {
            "category": category,
            "requirements": requirements
        })

    async def assign_task(
        self,
        collector_agent: Agent,
        task_type: str,
        parameters: Dict[str, Any] = {},
        priority: Priority = Priority.MEDIUM,
        context: Optional[str] = None
    ) -> TaskAssignment:
        """
        Assign data collection task to a collector agent.

        Args:
            collector_agent: The agent to assign task to
            task_type: Type of data to collect (e.g., "market_size", "brand_data")
            parameters: Task-specific parameters
            priority: Task priority (LOW, MEDIUM, HIGH, CRITICAL)
            context: Additional context for the task

        Returns:
            TaskAssignment message
        """
        task = TaskAssignment(
            sender_agent=self.agent_id,
            recipient_agent=collector_agent.agent_id,
            task_type=task_type,
            parameters=parameters,
            priority=priority,
            context=context or f"Collect {task_type} for {self.category} category"
        )

        self.send_message(task)
        collector_agent.receive_message(task)

        self.log_action("task_assigned", {
            "task_id": task.message_id,
            "recipient": collector_agent.agent_id,
            "task_type": task_type,
            "priority": priority.value
        })

        return task

    async def receive_submission(self, submission: DataSubmission) -> OrchestratorDecision:
        """
        Receive data submission from collector agent and coordinate validation.

        Args:
            submission: Data submission from collector agent

        Returns:
            OrchestratorDecision (ACCEPT, REJECT, or REFINE)
        """
        self.receive_message(submission)
        self.submissions[submission.message_id] = submission

        self.log_action("submission_received", {
            "submission_id": submission.message_id,
            "sender": submission.sender_agent,
            "data_type": submission.data_type,
            "confidence": submission.confidence
        })

        # Coordinate validation
        validation_results = await self.coordinate_validation(submission)

        # Make decision
        decision = await self.make_decision(submission, validation_results)

        # Update tracking based on decision
        if decision.decision == Decision.ACCEPT:
            if submission.data_type not in self.accepted_data:
                self.accepted_data[submission.data_type] = []
            self.accepted_data[submission.data_type].append(submission)

            # Remove from refining if it was there
            if submission.message_id in self.refining_data:
                del self.refining_data[submission.message_id]

        elif decision.decision == Decision.REJECT:
            self.rejected_data[submission.message_id] = submission

            # Remove from refining if it was there
            if submission.message_id in self.refining_data:
                del self.refining_data[submission.message_id]

        elif decision.decision == Decision.REFINE:
            self.refining_data[submission.message_id] = submission

            # Track refinement attempts
            if submission.message_id not in self.refinement_attempts:
                self.refinement_attempts[submission.message_id] = 0
            self.refinement_attempts[submission.message_id] += 1

            # If too many refinement attempts, reject
            if self.refinement_attempts[submission.message_id] >= 3:
                self.log_action("max_refinements_reached", {
                    "submission_id": submission.message_id
                })
                decision.decision = Decision.REJECT
                decision.reasoning += " [Max refinement attempts (3) reached]"
                self.rejected_data[submission.message_id] = submission
                del self.refining_data[submission.message_id]

        # Update progress
        await self.update_progress()

        return decision

    async def coordinate_validation(self, submission: DataSubmission) -> Dict[str, ValidationResult]:
        """
        Coordinate validation across all 4 validation agents.

        Args:
            submission: Data submission to validate

        Returns:
            Dict mapping validator name to ValidationResult
        """
        self.log_action("validation_started", {
            "submission_id": submission.message_id
        })

        # Run all validators concurrently
        quality_result, source_result, relevance_result = await asyncio.gather(
            self.quality_validator.validate(submission),
            self.source_validator.validate(submission),
            self.relevance_validator.validate(submission)
        )

        validation_results = {
            "quality": quality_result,
            "source": source_result,
            "relevance": relevance_result
        }

        self.log_action("validation_completed", {
            "submission_id": submission.message_id,
            "quality_score": quality_result.score,
            "source_score": source_result.score,
            "relevance_score": relevance_result.score,
            "all_passed": all(r.passed for r in validation_results.values())
        })

        return validation_results

    async def make_decision(
        self,
        submission: DataSubmission,
        validation_results: Dict[str, ValidationResult]
    ) -> OrchestratorDecision:
        """
        Make ACCEPT/REJECT/REFINE decision based on validation results.

        Decision Logic:
        1. If source validation fails (score < 1.0) → REJECT (zero fabrication)
        2. If any validation score < 0.7 → REJECT
        3. If all validations pass (>= 0.9) → ACCEPT
        4. If scores 0.7-0.9 and improvable → REFINE

        Args:
            submission: Data submission
            validation_results: Results from all validators

        Returns:
            OrchestratorDecision
        """
        quality_result = validation_results["quality"]
        source_result = validation_results["source"]
        relevance_result = validation_results["relevance"]

        # Calculate overall quality score (weighted)
        quality_score = (
            quality_result.score * 0.35 +
            source_result.score * 0.45 +  # Source validation weighted highest
            relevance_result.score * 0.20
        )

        # Decision logic
        decision = None
        reasoning = []
        feedback = None

        # Rule 1: Source validation MUST pass (zero fabrication enforcement)
        if not source_result.passed or source_result.score < 1.0:
            decision = Decision.REJECT
            reasoning.append(f"Source validation failed (score: {source_result.score:.2f})")
            reasoning.extend(source_result.issues)
            reasoning.append("ZERO FABRICATION POLICY: All data must have valid sources")

        # Rule 2: Any validation score < 0.7 → REJECT
        elif any(r.score < 0.7 for r in validation_results.values()):
            decision = Decision.REJECT
            reasoning.append(f"Low validation score detected (overall: {quality_score:.2f})")
            for name, result in validation_results.items():
                if result.score < 0.7:
                    reasoning.append(f"- {name}: {result.score:.2f} (threshold: 0.7)")
                    reasoning.extend(result.issues[:3])  # First 3 issues

        # Rule 3: All validations pass → ACCEPT
        elif all(r.passed for r in validation_results.values()):
            decision = Decision.ACCEPT
            reasoning.append(f"All validations passed (overall score: {quality_score:.2f})")
            reasoning.append(f"- Quality: {quality_result.score:.2f}")
            reasoning.append(f"- Source: {source_result.score:.2f}")
            reasoning.append(f"- Relevance: {relevance_result.score:.2f}")

        # Rule 4: Scores 0.7-0.9 → REFINE
        else:
            decision = Decision.REFINE
            reasoning.append(f"Data improvable (overall score: {quality_score:.2f})")

            # Collect refinement suggestions
            refinement_suggestions = []
            for name, result in validation_results.items():
                if not result.passed:
                    refinement_suggestions.append(f"{name.capitalize()}: {result.reasoning}")
                    refinement_suggestions.extend(result.recommendations[:2])

            feedback = "\n".join(refinement_suggestions)
            reasoning.append("Refinement requested - see feedback for improvements")

        # Create decision message
        decision_message = OrchestratorDecision(
            sender_agent=self.agent_id,
            recipient_agent=submission.sender_agent,
            submission_id=submission.message_id,
            decision=decision,
            reasoning="\n".join(reasoning),
            feedback=feedback,
            quality_score=quality_score
        )

        self.log_action("decision_made", {
            "submission_id": submission.message_id,
            "decision": decision.value,
            "quality_score": quality_score
        })

        return decision_message

    async def update_progress(self):
        """
        Update progress tracking and identify gaps.

        Calculates completeness percentage based on requirements:
        - Brands: 50 required
        - Market size: required
        - Pricing: 120 products required
        - Resources: 30 required
        - Historical data: required
        """
        # Count accepted data
        brands_count = sum(
            len(sub.data.get("brands", []))
            for sub in self.accepted_data.get("brand_data", [])
        )

        has_market_size = "market_size" in self.accepted_data

        pricing_count = sum(
            len(sub.data.get("products", []))
            for sub in self.accepted_data.get("pricing", [])
        )

        resources_count = sum(
            len(sub.data.get("resources", []))
            for sub in self.accepted_data.get("resources", [])
        )

        has_historical = "historical_data" in self.accepted_data

        # Calculate completeness
        brands_completeness = min(brands_count / self.requirements.get("brands", {}).get("min_count", 50), 1.0)
        market_completeness = 1.0 if has_market_size else 0.0
        pricing_completeness = min(pricing_count / self.requirements.get("pricing", {}).get("min_products", 120), 1.0)
        resources_completeness = min(resources_count / self.requirements.get("resources", {}).get("min_count", 30), 1.0)
        historical_completeness = 1.0 if has_historical else 0.0

        # Weighted average
        self.completeness = (
            brands_completeness * 0.30 +
            market_completeness * 0.20 +
            pricing_completeness * 0.25 +
            resources_completeness * 0.15 +
            historical_completeness * 0.10
        )

        # Identify gaps
        collected_data = {
            "brands": brands_count,
            "market_size": has_market_size,
            "pricing": pricing_count,
            "resources": resources_count,
            "historical_data": has_historical
        }

        self.gaps = await self.gap_analyzer.analyze_gaps(collected_data, self.requirements)

        self.log_action("progress_updated", {
            "completeness": self.completeness,
            "gaps_count": len(self.gaps)
        })

    def get_progress_report(self) -> ProgressReport:
        """
        Generate progress report with completeness, gaps, and quality distribution.

        Returns:
            ProgressReport message
        """
        quality_distribution = {
            "accepted": len(self.accepted_data),
            "refining": len(self.refining_data),
            "rejected": len(self.rejected_data)
        }

        report = ProgressReport(
            sender_agent=self.agent_id,
            recipient_agent="user",
            completeness=self.completeness,
            gaps=self.gaps,
            quality_distribution=quality_distribution,
            estimated_completion=None  # TODO: Implement time estimation
        )

        return report

    async def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """
        Process incoming message from other agents.

        Args:
            message: Incoming message

        Returns:
            Response message (if applicable)
        """
        if message.message_type == MessageType.SUBMISSION:
            submission = DataSubmission(**message.dict())
            decision = await self.receive_submission(submission)
            return decision

        return None

    async def execute_task(self, task: TaskAssignment) -> DataSubmission:
        """
        Orchestrator doesn't execute collection tasks.
        """
        raise NotImplementedError("Orchestrator doesn't collect data - it coordinates other agents")

    def get_execution_summary(self) -> Dict[str, Any]:
        """
        Get detailed execution summary with progress metrics.

        Returns:
            Dict with summary statistics
        """
        base_summary = super().get_execution_summary()

        base_summary.update({
            "category": self.category,
            "completeness": self.completeness,
            "accepted_submissions": sum(len(subs) for subs in self.accepted_data.values()),
            "refining_submissions": len(self.refining_data),
            "rejected_submissions": len(self.rejected_data),
            "gaps_identified": len(self.gaps),
            "ready_for_report": self.completeness >= 0.95 and self.completeness <= 1.0
        })

        return base_summary
