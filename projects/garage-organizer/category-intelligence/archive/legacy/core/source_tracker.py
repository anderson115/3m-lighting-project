"""
Source Tracker - Citation and audit management
Tracks all data sources with full metadata for auditability
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, HttpUrl, Field
import json


class DataSource(BaseModel):
    """Single data source with full metadata"""

    url: str
    title: str
    publisher: str
    access_date: str
    excerpt: Optional[str] = None
    archived_path: Optional[str] = None
    confidence: Literal["high", "medium", "low", "unverified"] = "medium"
    data_type: Literal["confirmed", "estimated", "inferred"] = "confirmed"
    notes: Optional[str] = None

    def to_citation(self, index: int) -> str:
        """Generate formatted citation"""
        return (
            f"[{index}] {self.publisher}: \"{self.title}\" "
            f"({self.access_date}) - {self.url}"
        )


class SourceTracker:
    """Manages all source citations and audit trail"""

    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.sources: List[DataSource] = []
        self.data_points: Dict[str, List[int]] = {}  # data_point -> source_indices

    def add_source(
        self,
        url: str,
        title: str,
        publisher: str,
        excerpt: Optional[str] = None,
        confidence: str = "medium",
        data_type: str = "confirmed",
        notes: Optional[str] = None,
    ) -> int:
        """
        Add new source and return its index

        Args:
            url: Source URL
            title: Page/article title
            publisher: Publisher/website name
            excerpt: Relevant excerpt from source
            confidence: high/medium/low/unverified
            data_type: confirmed/estimated/inferred
            notes: Additional notes

        Returns:
            Source index number
        """
        source = DataSource(
            url=url,
            title=title,
            publisher=publisher,
            access_date=datetime.now().strftime("%Y-%m-%d"),
            excerpt=excerpt,
            confidence=confidence,
            data_type=data_type,
            notes=notes,
        )

        self.sources.append(source)
        return len(self.sources) - 1

    def link_data_to_source(self, data_point: str, source_index: int):
        """Link a data point to its source(s)"""
        if data_point not in self.data_points:
            self.data_points[data_point] = []
        self.data_points[data_point].append(source_index)

    def get_sources_for_data(self, data_point: str) -> List[DataSource]:
        """Get all sources for a specific data point"""
        if data_point not in self.data_points:
            return []
        indices = self.data_points[data_point]
        return [self.sources[i] for i in indices]

    def get_citation(self, source_index: int) -> str:
        """Get formatted citation for source"""
        return self.sources[source_index].to_citation(source_index + 1)

    def export_audit_trail(self) -> Path:
        """Export complete audit trail to JSON"""
        audit_data = {
            "generated_at": datetime.now().isoformat(),
            "total_sources": len(self.sources),
            "sources": [s.dict() for s in self.sources],
            "data_point_mapping": self.data_points,
        }

        audit_path = self.output_dir / "audit" / "source_audit.json"
        audit_path.parent.mkdir(exist_ok=True, parents=True)

        with open(audit_path, "w") as f:
            json.dump(audit_data, f, indent=2)

        return audit_path

    def export_citation_list(self) -> Path:
        """Export formatted citation list"""
        citations = []
        for i, source in enumerate(self.sources):
            citations.append({
                "index": i + 1,
                "citation": source.to_citation(i + 1),
                "confidence": source.confidence,
                "data_type": source.data_type,
            })

        cite_path = self.output_dir / "audit" / "citations.json"
        with open(cite_path, "w") as f:
            json.dump(citations, f, indent=2)

        return cite_path

    def validate_sources(self) -> Dict[str, any]:
        """Validate all sources and return report"""
        validation_report = {
            "total_sources": len(self.sources),
            "by_confidence": {
                "high": 0,
                "medium": 0,
                "low": 0,
                "unverified": 0,
            },
            "by_data_type": {
                "confirmed": 0,
                "estimated": 0,
                "inferred": 0,
            },
            "missing_excerpts": 0,
            "missing_archives": 0,
        }

        for source in self.sources:
            validation_report["by_confidence"][source.confidence] += 1
            validation_report["by_data_type"][source.data_type] += 1

            if not source.excerpt:
                validation_report["missing_excerpts"] += 1
            if not source.archived_path:
                validation_report["missing_archives"] += 1

        return validation_report

    def __len__(self) -> int:
        return len(self.sources)

    def __repr__(self) -> str:
        return f"<SourceTracker sources={len(self.sources)} data_points={len(self.data_points)}>"
