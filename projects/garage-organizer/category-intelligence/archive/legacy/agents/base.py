"""
Base Agent Classes and Communication Protocol

Defines the foundation for the agentic category intelligence system.
All agents inherit from Agent base class and communicate via structured messages.
"""

import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, HttpUrl, Field


class MessageType(str, Enum):
    """Types of messages agents can send"""
    SUBMISSION = "submission"
    VALIDATION = "validation"
    DECISION = "decision"
    TASK = "task"
    FEEDBACK = "feedback"
    PROGRESS = "progress"


class Decision(str, Enum):
    """Orchestrator decisions on data submissions"""
    ACCEPT = "accept"
    REJECT = "reject"
    REFINE = "refine"


class Priority(str, Enum):
    """Task/message priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Source(BaseModel):
    """Data source with full traceability"""
    url: HttpUrl
    publisher: str
    date_published: Optional[str] = None
    excerpt: Optional[str] = None
    access_date: datetime = Field(default_factory=datetime.now)
    confidence: str = Field(default="medium", description="Source reliability: high, medium, low")

    def validate_accessible(self) -> bool:
        """Check if source URL is accessible (to be implemented)"""
        # TODO: Implement URL accessibility check
        return True


class AgentMessage(BaseModel):
    """Base class for all agent communications"""
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)
    sender_agent: str
    recipient_agent: str
    message_type: MessageType
    priority: Priority = Priority.MEDIUM

    class Config:
        use_enum_values = True


class DataSubmission(AgentMessage):
    """Collection agent submits data to orchestrator"""
    message_type: MessageType = MessageType.SUBMISSION
    data_type: str  # "market_size", "brand_data", "pricing", etc.
    data: Dict[str, Any]
    sources: List[Source]
    confidence: float = Field(ge=0.0, le=1.0, description="Agent's confidence in data quality")
    quality_self_assessment: float = Field(ge=0.0, le=1.0)
    reasoning: Optional[str] = None

    def validate_no_fabrication(self) -> List[str]:
        """Check for fabrication markers"""
        issues = []

        # Check for placeholder patterns
        fabrication_markers = [
            "placeholder", "example.com", "TODO", "TBD",
            "FIXME", "xxx", "test", "sample"
        ]

        data_str = str(self.data).lower()
        for marker in fabrication_markers:
            if marker in data_str:
                issues.append(f"Fabrication marker detected: '{marker}'")

        # Check for missing sources
        if not self.sources:
            issues.append("No sources provided - all data must have sources")

        # Check for unrealistic perfect scores (suspicious)
        if self.confidence == 1.0 and self.quality_self_assessment == 1.0:
            issues.append("Perfect scores suspicious - likely fabricated")

        return issues


class ValidationResult(AgentMessage):
    """Validation agent reports on data quality"""
    message_type: MessageType = MessageType.VALIDATION
    submission_id: str
    validation_type: str  # "quality", "relevance", "source", "gap"
    passed: bool
    score: float = Field(ge=0.0, le=1.0)
    issues: List[str] = []
    recommendations: List[str] = []
    reasoning: str

    class Config:
        use_enum_values = True


class OrchestratorDecision(AgentMessage):
    """Orchestrator makes accept/reject/refine decision"""
    message_type: MessageType = MessageType.DECISION
    submission_id: str
    decision: Decision
    reasoning: str
    feedback: Optional[str] = None  # If REFINE, what to improve
    quality_score: float = Field(ge=0.0, le=1.0)

    class Config:
        use_enum_values = True


class TaskAssignment(AgentMessage):
    """Orchestrator assigns collection task to agent"""
    message_type: MessageType = MessageType.TASK
    task_type: str
    parameters: Dict[str, Any] = {}
    deadline: Optional[datetime] = None
    context: Optional[str] = None  # Additional context for task


class Gap(BaseModel):
    """Identified data gap that needs filling"""
    gap_type: str  # "missing_data", "insufficient_count", "low_quality"
    description: str
    current_value: Any
    required_value: Any
    priority: Priority
    suggested_action: str


class ProgressReport(AgentMessage):
    """Orchestrator reports current progress"""
    message_type: MessageType = MessageType.PROGRESS
    completeness: float = Field(ge=0.0, le=1.0)
    gaps: List[Gap] = []
    quality_distribution: Dict[str, int] = {}  # {"accepted": 45, "refining": 5, "rejected": 2}
    estimated_completion: Optional[datetime] = None


class Agent(ABC):
    """Base class for all agents in the system"""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.message_queue: List[AgentMessage] = []
        self.sent_messages: List[AgentMessage] = []
        self.execution_log: List[Dict[str, Any]] = []

    @abstractmethod
    async def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Process incoming message and optionally return response"""
        pass

    def send_message(self, message: AgentMessage):
        """Send message to another agent"""
        self.sent_messages.append(message)
        self.log_action("sent_message", {
            "message_id": message.message_id,
            "recipient": message.recipient_agent,
            "type": message.message_type
        })

    def receive_message(self, message: AgentMessage):
        """Receive message from another agent"""
        self.message_queue.append(message)
        self.log_action("received_message", {
            "message_id": message.message_id,
            "sender": message.sender_agent,
            "type": message.message_type
        })

    def log_action(self, action: str, details: Dict[str, Any]):
        """Log agent action for audit trail"""
        self.execution_log.append({
            "timestamp": datetime.now().isoformat(),
            "agent_id": self.agent_id,
            "action": action,
            "details": details
        })

    @abstractmethod
    async def execute_task(self, task: TaskAssignment) -> DataSubmission:
        """Execute assigned task and return data submission"""
        pass

    def get_execution_summary(self) -> Dict[str, Any]:
        """Get summary of agent's execution"""
        return {
            "agent_id": self.agent_id,
            "messages_sent": len(self.sent_messages),
            "messages_received": len(self.message_queue),
            "actions_logged": len(self.execution_log),
            "last_activity": self.execution_log[-1]["timestamp"] if self.execution_log else None
        }


class CollectionAgent(Agent):
    """Base class for data collection agents"""

    def __init__(self, agent_id: str, data_type: str):
        super().__init__(agent_id)
        self.data_type = data_type
        self.collected_data: List[DataSubmission] = []

    async def collect_data(self, **kwargs) -> Dict[str, Any]:
        """Collect data from sources (to be implemented by subclasses)"""
        raise NotImplementedError("Subclasses must implement collect_data()")

    def validate_sources(self, sources: List[Source]) -> bool:
        """Validate that all sources are properly formatted"""
        if not sources:
            return False

        for source in sources:
            # Check for placeholder URLs
            url_str = str(source.url).lower()
            if any(marker in url_str for marker in ["example", "placeholder", "test"]):
                return False

            # Check required fields
            if not source.publisher:
                return False

        return True

    async def execute_task(self, task: TaskAssignment) -> DataSubmission:
        """Execute collection task"""
        self.log_action("task_started", {"task_type": task.task_type})

        # Collect data using real sources
        data = await self.collect_data(**task.parameters)

        # Validate no fabrication
        sources = data.get("sources", [])
        if not self.validate_sources(sources):
            raise ValueError("Sources validation failed - no fabricated sources allowed")

        # Create submission
        submission = DataSubmission(
            sender_agent=self.agent_id,
            recipient_agent=task.sender_agent,  # Send back to orchestrator
            data_type=self.data_type,
            data=data,
            sources=sources,
            confidence=data.get("confidence", 0.8),
            quality_self_assessment=data.get("quality_score", 0.8),
            reasoning=data.get("reasoning", "")
        )

        # Validate no fabrication markers
        fabrication_issues = submission.validate_no_fabrication()
        if fabrication_issues:
            raise ValueError(f"Fabrication detected: {', '.join(fabrication_issues)}")

        self.collected_data.append(submission)
        self.log_action("task_completed", {"submission_id": submission.message_id})

        return submission


class ValidationAgent(Agent):
    """Base class for validation agents"""

    def __init__(self, agent_id: str, validation_type: str):
        super().__init__(agent_id)
        self.validation_type = validation_type
        self.validation_history: List[ValidationResult] = []

    @abstractmethod
    async def validate(self, submission: DataSubmission) -> ValidationResult:
        """Validate data submission (to be implemented by subclasses)"""
        pass

    async def process_message(self, message: AgentMessage) -> Optional[ValidationResult]:
        """Process validation request"""
        if message.message_type == MessageType.SUBMISSION:
            submission = DataSubmission(**message.dict())
            result = await self.validate(submission)
            self.validation_history.append(result)
            return result

        return None

    async def execute_task(self, task: TaskAssignment) -> DataSubmission:
        """Validation agents don't execute collection tasks"""
        raise NotImplementedError("Validation agents don't collect data")
