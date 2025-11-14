# Presentation Generation Module - Technical Specification

**Date:** November 13, 2025
**Version:** 1.0
**Status:** Ready for Development

---

## System Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION GENERATION PIPELINE         │
└─────────────────────────────────────────────────────────────┘

INPUT LAYER
├── Raw Data (CSV, JSON, Database)
├── Project Config (YAML)
└── Insight Specifications (Markdown)
       ↓
DATA PROCESSING LAYER
├── Data Validator
├── Data Transformer (Pandas)
└── Data Aggregator
       ↓
INTELLIGENCE LAYER
├── Claude API (Insight Generation)
├── Data Analyzer (Statistical)
└── Citation Tracker
       ↓
VISUALIZATION LAYER
├── Plotly (Chart Generation)
├── Image Processor
└── Asset Manager
       ↓
PRESENTATION LAYER
├── Slide Builder (python-pptx)
├── Template Engine (Jinja2)
└── Layout Manager
       ↓
OUTPUT LAYER
├── PowerPoint Generator (PPTX)
├── PDF Converter
├── Google Slides Publisher
└── Quality Validator
       ↓
DELIVERABLES
├── presentation.pptx
├── presentation.pdf
└── Google Slides URL
```

---

## Module 1: Data Processing Layer

### 1.1 DataValidator

**Purpose:** Ensure input data meets schema requirements

```python
# modules/presentation-generation/02-processing/validators.py

from dataclasses import dataclass
from typing import List, Dict
import json

@dataclass
class DataValidationError(Exception):
    field: str
    message: str
    severity: str  # "error" or "warning"

class DataValidator:
    """Validates input data against schema"""

    def __init__(self, schema_path: str):
        with open(schema_path) as f:
            self.schema = json.load(f)

    def validate(self, data: Dict) -> List[DataValidationError]:
        """Returns list of validation errors"""
        errors = []

        # Check required fields
        for field in self.schema.get("required", []):
            if field not in data:
                errors.append(DataValidationError(
                    field=field,
                    message=f"Missing required field: {field}",
                    severity="error"
                ))

        # Validate field types
        for field, spec in self.schema.get("properties", {}).items():
            if field in data:
                if not self._validate_type(data[field], spec.get("type")):
                    errors.append(DataValidationError(
                        field=field,
                        message=f"Invalid type for {field}",
                        severity="error"
                    ))

        return errors

    def _validate_type(self, value, expected_type):
        """Type checking logic"""
        type_map = {
            "string": str,
            "number": (int, float),
            "integer": int,
            "array": list,
            "object": dict
        }
        return isinstance(value, type_map.get(expected_type, object))
```

### 1.2 DataProcessor

**Purpose:** Clean, aggregate, and transform data

```python
# modules/presentation-generation/02-processing/data-processor.py

import pandas as pd
from typing import Dict, List

class DataProcessor:
    """Processes raw data for presentation generation"""

    def __init__(self, validator: DataValidator):
        self.validator = validator
        self.data = None

    def load_and_validate(self, data_path: str) -> bool:
        """Load CSV/JSON and validate against schema"""
        # Load data
        if data_path.endswith('.csv'):
            self.data = pd.read_csv(data_path)
        elif data_path.endswith('.json'):
            self.data = pd.read_json(data_path)

        # Validate
        errors = self.validator.validate(self.data.to_dict())
        if [e for e in errors if e.severity == "error"]:
            raise ValueError(f"Data validation failed: {errors}")

        return True

    def aggregate(self, groupby: List[str], agg_functions: Dict) -> pd.DataFrame:
        """Aggregate data by specified columns"""
        return self.data.groupby(groupby).agg(agg_functions).reset_index()

    def calculate_percentages(self, column: str, total_column: str) -> pd.DataFrame:
        """Add percentage calculations"""
        self.data[f'{column}_pct'] = (
            self.data[column] / self.data[total_column] * 100
        ).round(1)
        return self.data

    def get_top_n(self, column: str, n: int = 10) -> pd.DataFrame:
        """Get top N rows by specified column"""
        return self.data.nlargest(n, column)

    def to_dict(self) -> Dict:
        """Export processed data as dictionary"""
        return self.data.to_dict(orient='records')
```

### Input Schema Example

```json
{
  "name": "GarageOrganizer",
  "version": "1.0",
  "required": [
    "project_name",
    "client_name",
    "data_sources",
    "insights"
  ],
  "properties": {
    "project_name": {"type": "string"},
    "client_name": {"type": "string"},
    "data_sources": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "type": {"type": "string", "enum": ["reddit", "youtube", "instagram"]},
          "count": {"type": "integer"},
          "percentage": {"type": "number"}
        }
      }
    },
    "insights": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "title": {"type": "string"},
          "description": {"type": "string"},
          "data_points": {"type": "array"},
          "verbatims": {"type": "array"}
        }
      }
    }
  }
}
```

---

## Module 2: Intelligence Layer

### 2.1 InsightGenerator (Claude API Integration)

**Purpose:** Generate compelling slide content from raw data

```python
# modules/presentation-generation/02-processing/insight-generator.py

import anthropic
from typing import Dict, List

class InsightGenerator:
    """Generates insights using Claude API"""

    def __init__(self, model: str = "claude-opus-4"):
        self.client = anthropic.Anthropic()
        self.model = model

    def generate_slide_titles(self, data: Dict, num_slides: int = 5) -> List[str]:
        """Generate compelling slide titles"""
        prompt = f"""
        Based on this research data:
        {data}

        Generate {num_slides} compelling, data-driven slide titles for a
        professional market research presentation.

        Requirements:
        - Each title should be 5-10 words
        - Must be data-grounded (not speculative)
        - Should tell a story across the sequence
        - Use active voice

        Return only the titles, one per line.
        """

        response = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text.strip().split('\n')

    def generate_slide_description(self, title: str, data: Dict) -> str:
        """Generate detailed description for a slide"""
        prompt = f"""
        Create a compelling slide description for a professional presentation.

        Slide Title: {title}
        Supporting Data: {data}

        Requirements:
        - 2-3 paragraphs maximum
        - Data-grounded (cite percentages)
        - Professional tone
        - Include key implications
        - Format as Markdown

        Return only the description.
        """

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text.strip()

    def generate_design_brief(self, slide_data: Dict) -> str:
        """Generate design brief for a complex data slide (like Garage Organizer Slide 9)"""
        prompt = f"""
        Create a detailed design brief for a data visualization slide.

        Data to visualize:
        {slide_data}

        Requirements for the brief:
        - Specify slide structure (zones, sections)
        - Include all required data elements
        - Describe visualization approach
        - Note typography, colors, spacing
        - Include "creative freedom" section
        - Format as Markdown matching the GenSpark style

        This brief will be used to generate the actual slide design.
        """

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text.strip()

    def cite_sources(self, claim: str, data: Dict) -> str:
        """Find data sources for a specific claim"""
        prompt = f"""
        Given this claim: "{claim}"
        And this data: {data}

        Return a properly formatted citation that includes:
        - Source name (Reddit, YouTube, etc.)
        - Number of records analyzed
        - Relevant percentages
        - Confidence level assessment

        Format as a single line for footer use.
        """

        response = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text.strip()
```

---

## Module 3: Visualization Layer

### 3.1 ChartGenerator (Plotly Integration)

**Purpose:** Create professional charts from data

```python
# modules/presentation-generation/03-generation/chart-generator.py

import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List
import os

class ChartGenerator:
    """Generates charts using Plotly"""

    def __init__(self, output_dir: str = "charts/", theme: str = "plotly_white"):
        self.output_dir = output_dir
        self.theme = theme
        os.makedirs(output_dir, exist_ok=True)

    def bar_chart(self, data: Dict, x_col: str, y_col: str,
                  title: str = "", filename: str = "chart.png") -> str:
        """Create horizontal/vertical bar chart"""
        fig = go.Figure(data=[
            go.Bar(x=data[x_col], y=data[y_col], marker_color='#16A085')
        ])

        fig.update_layout(
            title=title,
            xaxis_title=x_col,
            yaxis_title=y_col,
            template=self.theme,
            height=600,
            width=1000
        )

        output_path = os.path.join(self.output_dir, filename)
        fig.write_image(output_path, width=1280, height=720)
        return output_path

    def comparison_chart(self, segment1: Dict, segment2: Dict,
                        categories: List[str]) -> str:
        """Create side-by-side comparison (like Garage Organizer Slide 9)"""
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=categories,
            y=segment1['values'],
            name=segment1['name'],
            marker_color='#16A085'
        ))

        fig.add_trace(go.Bar(
            x=categories,
            y=segment2['values'],
            name=segment2['name'],
            marker_color='#111827'
        ))

        fig.update_layout(
            barmode='group',
            title='Segment Comparison',
            template=self.theme,
            height=600,
            width=1200,
            xaxis_title='Pain Points',
            yaxis_title='Percentage (%)'
        )

        output_path = os.path.join(self.output_dir, 'comparison.png')
        fig.write_image(output_path, width=1280, height=720)
        return output_path

    def heatmap(self, data: Dict, title: str = "") -> str:
        """Create heatmap for correlation/pattern data"""
        fig = go.Figure(data=go.Heatmap(z=data['z'], x=data['x'], y=data['y']))
        fig.update_layout(title=title, template=self.theme)

        output_path = os.path.join(self.output_dir, 'heatmap.png')
        fig.write_image(output_path, width=1000, height=800)
        return output_path

    def number_highlight(self, value: float, label: str,
                        context: str = "") -> str:
        """Create large number highlight graphic"""
        fig = go.Figure()
        fig.add_annotation(
            text=f"<b>{value}%</b><br>{label}<br><sub>{context}</sub>",
            showarrow=False,
            font=dict(size=72, color="#16A085")
        )

        fig.update_layout(
            template="plotly_white",
            height=400,
            width=600,
            margin=dict(l=0, r=0, t=0, b=0)
        )

        output_path = os.path.join(self.output_dir, f'{label.replace(" ", "_")}.png')
        fig.write_image(output_path)
        return output_path
```

---

## Module 4: Presentation Layer

### 4.1 SlideBuilder (python-pptx Integration)

**Purpose:** Assemble slides from components

```python
# modules/presentation-generation/03-generation/slide-builder.py

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from typing import Dict, List
import os

class SlideBuilder:
    """Builds slides using python-pptx"""

    # Color scheme
    COLORS = {
        'charcoal': RGBColor(17, 24, 39),      # #111827
        'teal': RGBColor(22, 160, 133),        # #16A085
        'white': RGBColor(255, 255, 255),
        'light_gray': RGBColor(243, 244, 246)
    }

    def __init__(self, template_path: str = None):
        """Initialize with optional template PPTX"""
        if template_path and os.path.exists(template_path):
            self.prs = Presentation(template_path)
        else:
            self.prs = Presentation()
            self.prs.slide_width = Inches(10)
            self.prs.slide_height = Inches(5.625)  # 16:9

    def add_title_slide(self, title: str, subtitle: str = "",
                       author: str = "") -> None:
        """Add title slide"""
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])  # Blank

        # Background
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = self.COLORS['white']

        # Title
        title_box = slide.shapes.add_textbox(
            Inches(0.5), Inches(1.5), Inches(9), Inches(1.5)
        )
        title_frame = title_box.text_frame
        title_frame.word_wrap = True
        p = title_frame.paragraphs[0]
        p.text = title
        p.font.size = Pt(54)
        p.font.bold = True
        p.font.color.rgb = self.COLORS['charcoal']

        # Subtitle
        if subtitle:
            subtitle_box = slide.shapes.add_textbox(
                Inches(0.5), Inches(3.2), Inches(9), Inches(1)
            )
            subtitle_frame = subtitle_box.text_frame
            p = subtitle_frame.paragraphs[0]
            p.text = subtitle
            p.font.size = Pt(32)
            p.font.color.rgb = self.COLORS['teal']

    def add_content_slide(self, title: str, content: Dict) -> None:
        """Add content slide with title and body"""
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])

        # Title with teal underline
        title_box = slide.shapes.add_textbox(
            Inches(0.5), Inches(0.3), Inches(9), Inches(0.6)
        )
        title_frame = title_box.text_frame
        p = title_frame.paragraphs[0]
        p.text = title
        p.font.size = Pt(44)
        p.font.bold = True
        p.font.color.rgb = self.COLORS['charcoal']

        # Teal underline
        slide.shapes.add_shape(
            1,  # Line
            Inches(0.5), Inches(1.0), Inches(2), Inches(0)
        ).line.color.rgb = self.COLORS['teal']

        # Body content
        if 'text' in content:
            text_box = slide.shapes.add_textbox(
                Inches(0.5), Inches(1.3), Inches(9), Inches(3.8)
            )
            text_frame = text_box.text_frame
            text_frame.word_wrap = True
            p = text_frame.paragraphs[0]
            p.text = content['text']
            p.font.size = Pt(18)
            p.font.color.rgb = self.COLORS['charcoal']

    def add_data_slide(self, title: str, chart_path: str = None,
                      table_data: List[List] = None) -> None:
        """Add slide with chart/data visualization"""
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])

        # Title
        title_box = slide.shapes.add_textbox(
            Inches(0.5), Inches(0.3), Inches(9), Inches(0.6)
        )
        p = title_box.text_frame.paragraphs[0]
        p.text = title
        p.font.size = Pt(44)
        p.font.bold = True
        p.font.color.rgb = self.COLORS['charcoal']

        # Chart image
        if chart_path:
            slide.shapes.add_picture(
                chart_path,
                Inches(0.5), Inches(1.2),
                width=Inches(9), height=Inches(3.8)
            )

        # Table (if provided)
        if table_data:
            rows, cols = len(table_data), len(table_data[0])
            table_shape = slide.shapes.add_table(rows, cols,
                                                 Inches(0.5), Inches(4.2),
                                                 Inches(9), Inches(1.2))
            table = table_shape.table

            for i, row in enumerate(table_data):
                for j, cell_text in enumerate(row):
                    cell = table.cell(i, j)
                    cell.text = str(cell_text)

    def save(self, output_path: str) -> str:
        """Save presentation to file"""
        self.prs.save(output_path)
        return output_path

    def get_slide_count(self) -> int:
        """Return number of slides"""
        return len(self.prs.slides)
```

---

## Module 5: Template System

### 5.1 Template Configuration

```yaml
# modules/presentation-generation/00-config/theme-config.yaml

name: "Professional Market Research"
version: "1.0"

# Color palette
colors:
  primary: "#16A085"      # Teal
  secondary: "#111827"    # Charcoal
  accent: "#F3F4F6"      # Light gray
  text: "#111827"
  background: "#FFFFFF"

# Typography
fonts:
  headline:
    family: "Inter"
    weight: "bold"
    sizes:
      title: 54
      section: 44
      subsection: 32

  body:
    family: "Inter"
    weight: "regular"
    sizes:
      primary: 18
      secondary: 14
      footer: 10

# Layout defaults
layout:
  slide_ratio: "16:9"
  margins:
    top: 0.5
    right: 0.5
    bottom: 0.5
    left: 0.5

  spacing:
    section_gap: 0.3
    content_gap: 0.2
    footer_gap: 0.1

# Slide templates
templates:
  title_slide:
    layout: "full_width"
    background: "colored"
    content: ["title", "subtitle", "author"]

  content_slide:
    layout: "title_body"
    background: "white"
    content: ["title", "body_text"]

  data_slide:
    layout: "title_chart"
    background: "white"
    content: ["title", "chart", "footnote"]

  comparison_slide:
    layout: "two_column"
    background: "white"
    content: ["title", "left_content", "right_content"]
```

---

## Module 6: Orchestration

### 6.1 Main Workflow Script

```bash
#!/bin/bash
# modules/presentation-generation/workflows/generate-presentation.sh

set -e

PROJECT_NAME="${1:-}"
DATA_FILE="${2:-}"

if [ -z "$PROJECT_NAME" ] || [ -z "$DATA_FILE" ]; then
    echo "Usage: ./generate-presentation.sh <project_name> <data_file>"
    exit 1
fi

WORK_DIR="projects/$PROJECT_NAME"
OUTPUT_DIR="$WORK_DIR/05-final-mile"

mkdir -p "$OUTPUT_DIR"

echo "========================================="
echo "Generating Presentation: $PROJECT_NAME"
echo "========================================="

# Step 1: Validate data
echo "[1/5] Validating input data..."
python3 -c "
from modules.presentation_generation.validators import DataValidator
validator = DataValidator('schema.json')
with open('$DATA_FILE') as f:
    import json
    data = json.load(f)
    errors = validator.validate(data)
    if errors:
        raise ValueError(f'Validation failed: {errors}')
" || exit 1

# Step 2: Process data
echo "[2/5] Processing data..."
python3 << EOF
from modules.presentation_generation.data_processor import DataProcessor, DataValidator
processor = DataProcessor(DataValidator('schema.json'))
processor.load_and_validate('$DATA_FILE')
data = processor.to_dict()
EOF

# Step 3: Generate insights
echo "[3/5] Generating insights..."
python3 << EOF
from modules.presentation_generation.insight_generator import InsightGenerator
generator = InsightGenerator()
# Generate slide content, titles, design briefs
EOF

# Step 4: Create visualizations
echo "[4/5] Creating visualizations..."
python3 << EOF
from modules.presentation_generation.chart_generator import ChartGenerator
chart_gen = ChartGenerator()
# Generate all charts
EOF

# Step 5: Build presentation
echo "[5/5] Building presentation..."
python3 << EOF
from modules.presentation_generation.slide_builder import SlideBuilder
builder = SlideBuilder('template.pptx')
# Add all slides
builder.save('$OUTPUT_DIR/presentation.pptx')
EOF

echo ""
echo "========================================="
echo "✓ Presentation created successfully!"
echo "========================================="
echo "Output: $OUTPUT_DIR/presentation.pptx"
```

---

## Dependencies & Installation

```
# requirements.txt
python-pptx==0.6.21
plotly==5.17.0
pandas==2.1.0
anthropic==0.7.6
pyyaml==6.0.1
python-dotenv==1.0.0
```

```bash
# Installation
pip install -r requirements.txt

# Google Slides support (optional)
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

---

## Performance Targets

| Operation | Target Time | Notes |
|-----------|------------|-------|
| Data validation | <10 sec | Local file parsing |
| Data processing | <30 sec | Pandas aggregation |
| Insight generation | <60 sec | Claude API call (batched) |
| Chart generation | <45 sec | Plotly exports (parallel) |
| Slide assembly | <30 sec | python-pptx rendering |
| **Total per deck** | **<5 min** | After setup complete |

---

## Testing Strategy

```python
# tests/test_end_to_end.py

def test_full_pipeline():
    """End-to-end test with sample data"""
    # 1. Load sample garage-organizer data
    # 2. Run through entire pipeline
    # 3. Compare output slides with reference deck
    # 4. Verify slide count, text, chart presence

def test_data_integrity():
    """Verify data accuracy through pipeline"""
    # 1. Check percentages round correctly
    # 2. Verify citations are accurate
    # 3. Confirm no data loss

def test_design_consistency():
    """Verify design matches template"""
    # 1. Check color usage
    # 2. Verify typography
    # 3. Validate spacing/layout
```

---

## Development Timeline

**Week 1 (Days 1-5): Setup & Foundation**
- [ ] Create module structure
- [ ] Set up python-pptx template system
- [ ] Implement DataValidator & DataProcessor
- [ ] Build test suite infrastructure

**Week 2 (Days 6-10): Intelligence & Visualization**
- [ ] Integrate Claude API (InsightGenerator)
- [ ] Build ChartGenerator (Plotly)
- [ ] Create theme/template configuration system
- [ ] Test on sample data

**Week 3 (Days 11-15): Assembly & Integration**
- [ ] Build SlideBuilder (python-pptx)
- [ ] Integrate all components
- [ ] Create orchestration script
- [ ] End-to-end testing on garage-organizer rebuild

**Week 4 (Days 16-20): Refinement & Deployment**
- [ ] Quality assurance & comparison
- [ ] Documentation & examples
- [ ] Performance optimization
- [ ] Production deployment

---

**Status:** READY FOR DEVELOPMENT
**Estimated Effort:** 80-120 hours
**Team:** 1 Python developer (full-time) + code review support
