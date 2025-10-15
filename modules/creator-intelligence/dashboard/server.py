#!/usr/bin/env python3
"""
Real-time dashboard server for Creator Intelligence Module.
WebSocket-based live updates with ADHD-optimized visual interface.
"""

import asyncio
import json
import os
import time
from pathlib import Path
from typing import Dict, List
from datetime import datetime

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(title="Creator Intelligence Dashboard")

# Paths
MODULE_ROOT = Path(__file__).parent.parent
LOG_FILE = MODULE_ROOT / "test_50_creators_system_test.log"
METRICS_FILE = MODULE_ROOT / "test_metrics_50_creators.json"
DB_PATH = MODULE_ROOT / "data" / "database" / "creators.db"

# Active WebSocket connections
active_connections: List[WebSocket] = []


class DashboardMonitor:
    """Monitor test progress and send updates via WebSocket."""

    def __init__(self):
        self.last_log_position = 0
        self.current_metrics = {
            "status": "initializing",
            "progress_percent": 0,
            "current_creator": 0,
            "total_creators": 51,
            "successful": 0,
            "failed": 0,
            "start_time": None,
            "elapsed_seconds": 0,
            "steps_completed": [],
            "current_step": "Starting...",
            "api_quota_used": 0,
            "llm_tokens_used": 0
        }

    async def parse_log_updates(self) -> Dict:
        """Parse log file for new updates."""
        if not LOG_FILE.exists():
            return {"status": "waiting", "message": "Waiting for test to start..."}

        try:
            with open(LOG_FILE, 'r') as f:
                f.seek(self.last_log_position)
                new_lines = f.readlines()
                self.last_log_position = f.tell()

            # Parse new log lines
            for line in new_lines:
                self._parse_line(line)

            # Calculate derived metrics
            if self.current_metrics["current_creator"] > 0:
                self.current_metrics["progress_percent"] = int(
                    (self.current_metrics["current_creator"] / self.current_metrics["total_creators"]) * 100
                )

            # Check if test completed
            if "TEST COMPLETE" in "".join(new_lines):
                self.current_metrics["status"] = "completed"
                self._load_final_metrics()

            return self.current_metrics

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _parse_line(self, line: str):
        """Parse a single log line and update metrics."""

        # Start time
        if "Start Time:" in line and not self.current_metrics["start_time"]:
            self.current_metrics["start_time"] = time.time()
            self.current_metrics["status"] = "running"
            self.current_metrics["steps_completed"].append("✅ Test initialized")

        # Initialization
        if "CreatorIntelligenceOrchestrator initialized" in line:
            self.current_metrics["steps_completed"].append("✅ Orchestrator initialized")

        # Starting analysis
        if "Starting creator analysis" in line:
            self.current_metrics["current_step"] = "Searching for creators..."
            self.current_metrics["steps_completed"].append("✅ Analysis started")

        # Total creators found
        if "Total creators found:" in line:
            try:
                total = int(line.split("Total creators found:")[1].strip())
                self.current_metrics["total_creators"] = total
                self.current_metrics["steps_completed"].append(f"✅ Found {total} creators")
            except:
                pass

        # Processing creator
        if "Processing creator" in line:
            try:
                parts = line.split("Processing creator")[1].strip()
                current = int(parts.split("/")[0].strip())
                username = parts.split(":")[1].split("(")[0].strip()

                self.current_metrics["current_creator"] = current
                self.current_metrics["current_step"] = f"Processing {username}"
            except:
                pass

        # Successfully processed
        if "Successfully processed" in line:
            try:
                count = int(line.split("Successfully processed")[1].split("creators")[0].strip())
                self.current_metrics["successful"] = count
            except:
                pass

        # Failed processing
        if "Failed processing" in line:
            self.current_metrics["failed"] += 1

        # Scoring
        if "Scoring creators" in line:
            self.current_metrics["current_step"] = "Scoring creators..."
            self.current_metrics["steps_completed"].append("✅ Content classified")

        # Saving to database
        if "Saving to database" in line:
            self.current_metrics["current_step"] = "Saving to database..."
            self.current_metrics["steps_completed"].append("✅ Creators scored")

        # Update elapsed time
        if self.current_metrics["start_time"]:
            self.current_metrics["elapsed_seconds"] = int(time.time() - self.current_metrics["start_time"])

    def _load_final_metrics(self):
        """Load final metrics from JSON file."""
        if METRICS_FILE.exists():
            try:
                with open(METRICS_FILE, 'r') as f:
                    final_data = json.load(f)

                self.current_metrics.update({
                    "api_quota_used": final_data.get("api_usage", {}).get("youtube_quota_used", 0),
                    "llm_tokens_used": final_data.get("performance", {}).get("llm_tokens_used", 0),
                    "total_duration_minutes": final_data.get("total_duration_minutes", 0),
                    "success_rate": final_data.get("results", {}).get("success_rate", "0%")
                })

                self.current_metrics["steps_completed"].append("✅ Test completed successfully")
            except Exception as e:
                print(f"Error loading final metrics: {e}")


monitor = DashboardMonitor()


@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    """Serve the dashboard HTML."""
    html_path = Path(__file__).parent / "index.html"
    return HTMLResponse(content=html_path.read_text())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates."""
    await websocket.accept()
    active_connections.append(websocket)

    try:
        # Send initial state
        await websocket.send_json(monitor.current_metrics)

        # Keep connection alive and send updates
        while True:
            await asyncio.sleep(2)  # Update every 2 seconds

            # Get latest metrics
            metrics = await monitor.parse_log_updates()

            # Send to this client
            await websocket.send_json(metrics)

    except WebSocketDisconnect:
        active_connections.remove(websocket)


@app.get("/api/status")
async def get_status():
    """REST endpoint for current status."""
    return await monitor.parse_log_updates()


@app.get("/report.html")
async def get_report():
    """Serve the test report."""
    if METRICS_FILE.exists():
        return HTMLResponse(content=generate_report_html())
    else:
        return HTMLResponse(content="<h1>No report available yet</h1><p>Run a test first.</p>", status_code=404)


def generate_report_html():
    """Generate HTML report from metrics."""
    with open(METRICS_FILE, 'r') as f:
        data = json.load(f)

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Test Report - Creator Intelligence</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif; background: #0a0e1a; color: #e8eaf0; padding: 2rem; max-width: 900px; margin: 0 auto; }}
        h1 {{ color: #8b5cf6; }}
        .metric {{ background: rgba(255,255,255,0.05); padding: 1rem; margin: 1rem 0; border-radius: 8px; border-left: 3px solid #8b5cf6; }}
        .metric-label {{ font-size: 0.8rem; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.5px; }}
        .metric-value {{ font-size: 1.8rem; font-weight: 700; color: #10b981; margin-top: 0.3rem; }}
        pre {{ background: rgba(0,0,0,0.3); padding: 1rem; border-radius: 8px; overflow-x: auto; }}
    </style>
</head>
<body>
    <h1>Creator Intelligence Test Report</h1>

    <div class="metric">
        <div class="metric-label">Total Duration</div>
        <div class="metric-value">{data.get('total_duration_minutes', 0):.2f} minutes</div>
    </div>

    <div class="metric">
        <div class="metric-label">Creators Analyzed</div>
        <div class="metric-value">{data.get('results', {}).get('total_creators_analyzed', 0)}</div>
    </div>

    <div class="metric">
        <div class="metric-label">Success Rate</div>
        <div class="metric-value">{data.get('results', {}).get('success_rate', '0%')}</div>
    </div>

    <div class="metric">
        <div class="metric-label">API Quota Used</div>
        <div class="metric-value">{data.get('api_usage', {}).get('youtube_quota_used', 0)} / {data.get('api_usage', {}).get('youtube_quota_limit', 10000)}</div>
    </div>

    <div class="metric">
        <div class="metric-label">LLM Tokens</div>
        <div class="metric-value">{data.get('performance', {}).get('llm_tokens_used', 0):,}</div>
    </div>

    <h2>Full Metrics</h2>
    <pre>{json.dumps(data, indent=2)}</pre>

    <p><a href="/" style="color: #8b5cf6;">← Back to Dashboard</a></p>
</body>
</html>"""
    return html


if __name__ == "__main__":
    print("=" * 80)
    print("🎨 CREATOR INTELLIGENCE DASHBOARD")
    print("=" * 80)
    print(f"📊 Dashboard URL: http://localhost:10350")
    print(f"🔌 WebSocket: ws://localhost:10350/ws")
    print(f"📁 Monitoring: {LOG_FILE.name}")
    print("=" * 80)
    print("\n✅ Server starting...\n")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=10350,
        log_level="info"
    )
