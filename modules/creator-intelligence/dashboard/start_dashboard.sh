#!/usr/bin/env bash
#
# Quick launcher for Creator Intelligence Dashboard
# Starts server and opens browser
#

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo ""
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${PURPLE}   🎨 Creator Intelligence Dashboard${NC}"
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

echo -e "${BLUE}📁 Project Root:${NC} $PROJECT_ROOT"
echo -e "${BLUE}🔧 Activating venv...${NC}"

# Activate venv
cd "$PROJECT_ROOT"
source venv/bin/activate

# Check if FastAPI is installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo -e "${BLUE}📦 Installing dependencies...${NC}"
    pip install fastapi uvicorn websockets -q
fi

# Start server in background
echo -e "${BLUE}🚀 Starting dashboard server...${NC}"
python "$SCRIPT_DIR/server.py" &
SERVER_PID=$!

# Wait for server to start
sleep 3

# Check if server is running
if curl -s http://localhost:10350/ > /dev/null 2>&1; then
    echo ""
    echo -e "${GREEN}✅ Dashboard is running!${NC}"
    echo ""
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}   📊 Dashboard:${NC} http://localhost:10350"
    echo -e "${GREEN}   🔌 WebSocket:${NC} ws://localhost:10350/ws"
    echo -e "${GREEN}   🛑 Stop:${NC} kill $SERVER_PID"
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    # Open browser (macOS)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo -e "${BLUE}🌐 Opening browser...${NC}"
        open http://localhost:10350
    fi

    echo ""
    echo -e "${GREEN}💡 TIP:${NC} Run a test in another terminal:"
    echo -e "   ${BLUE}python modules/creator-intelligence/test_50_creators_with_metrics.py${NC}"
    echo ""

    # Keep script running
    echo -e "${BLUE}Press Ctrl+C to stop dashboard${NC}"
    wait $SERVER_PID
else
    echo ""
    echo -e "${RED}❌ Failed to start dashboard${NC}"
    kill $SERVER_PID 2>/dev/null || true
    exit 1
fi
