# 🎨 Creator Intelligence Dashboard

Real-time visual monitoring system for Creator Intelligence Module tests.

## 🎯 **Features**

### ✅ **Visual Design**
- **ADHD-Optimized**: High contrast, clear hierarchy, animation cues
- **Dyslexia-Friendly**: Monospace fonts, generous spacing, color-coded status
- **Non-Cookie-Cutter**: Custom gradient design, unique visual elements
- **Animated Progress**: Shimmer effects, pulse animations for active states

### ✅ **Real-Time Updates**
- WebSocket-based live data streaming (2-second refresh)
- Automatic reconnection on disconnect
- Connection status indicator

### ✅ **Comprehensive Metrics**
- **Progress Bar**: Visual 0-100% completion
- **Live Stats**: Success count, failure count, elapsed time, API quota
- **Step Checklist**: Real-time pipeline progress tracking
- **Current Step**: Highlighted active operation

## 🚀 **Quick Start**

### **1. Start Dashboard Server**
```bash
cd modules/creator-intelligence
source ../../venv/bin/activate
python dashboard/server.py
```

### **2. Open in Browser**
```
http://localhost:10350
```

### **3. Run a Test** (in separate terminal)
```bash
python test_50_creators_with_metrics.py
```

Dashboard will automatically detect and monitor the test in real-time.

## 📊 **Architecture**

```
dashboard/
├── server.py          # FastAPI backend with WebSocket
├── index.html         # ADHD-optimized frontend
└── README.md          # This file
```

### **Backend (server.py)**
- FastAPI server on port **10350**
- WebSocket endpoint: `ws://localhost:10350/ws`
- REST endpoint: `http://localhost:10350/api/status`
- Monitors: `test_50_creators_system_test.log`

### **Frontend (index.html)**
- Pure HTML/CSS/JavaScript (no frameworks)
- WebSocket client for live updates
- Gradient backgrounds, animated progress bars
- Responsive design (mobile-friendly)

## 🎨 **Visual Elements**

### **Color System**
- **Purple Gradient**: Primary hero/active elements (`#667eea` → `#764ba2`)
- **Success Green**: Completed items (`#48bb78`)
- **Failure Red**: Error states (`#f56565`)
- **Neutral Blue**: Status info (`#667eea`)
- **Dark Background**: Reduces eye strain (`#0a0f1e` → `#1a1f3a`)

### **Typography**
- **Font**: Monospace (SF Mono, Monaco, Inconsolata)
- **Sizes**: Large, clear, high contrast
- **Letter Spacing**: Enhanced for readability

### **Animations**
- **Pulse**: Running status, connection indicator
- **Shimmer**: Progress bar fill
- **Hover**: Interactive stat boxes
- **Transition**: Smooth state changes

## 📱 **Responsive Breakpoints**

- **Desktop**: Full layout with stats grid
- **Tablet**: 2-column stats grid
- **Mobile**: Single column, scaled text

## 🔧 **Configuration**

### **Port Assignment**
Assigned port: **10350** (from 10300-10399 range)

To change port, edit `server.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=10350)
```

### **Update Frequency**
WebSocket updates every 2 seconds. To change, edit `server.py`:
```python
await asyncio.sleep(2)  # Adjust frequency here
```

## 🔍 **Troubleshooting**

### **Dashboard Won't Start**
```bash
# Install dependencies
pip install fastapi uvicorn websockets

# Check port availability
lsof -i :10350

# View logs
python dashboard/server.py  # Run in foreground to see errors
```

### **No Live Updates**
1. Check WebSocket connection (connection status indicator in top-right)
2. Verify log file exists: `test_50_creators_system_test.log`
3. Check browser console for JavaScript errors

### **Test Not Detected**
Dashboard monitors `test_50_creators_system_test.log`. Ensure your test writes to this file:
```python
python test_50_creators_with_metrics.py 2>&1 | tee test_50_creators_system_test.log
```

## 🎯 **Usage Tips**

### **For ADHD Users**
- Dashboard uses **high-contrast colors** for easy focus
- **Animated elements** draw attention to active operations
- **Progress bar** provides clear visual checkpoint
- **Step checklist** breaks down complex process into chunks

### **For Dyslexic Users**
- **Monospace fonts** improve character differentiation
- **Generous spacing** reduces visual crowding
- **Color coding** provides non-textual cues
- **Large text sizes** reduce reading strain

### **For General Use**
- Leave dashboard open during long tests
- Connection indicator shows real-time status
- Stats update live (no refresh needed)
- Completion summary appears automatically

## 🔗 **Integration**

### **With Module Tests**
Dashboard automatically monitors any test that writes to `test_50_creators_system_test.log`.

### **With Website**
To embed in website:
1. Serve `index.html` from your web server
2. Update WebSocket URL to match server location
3. Add authentication if needed
4. Consider HTTPS for production

### **Multiple Modules**
To monitor multiple modules:
1. Create separate dashboard instances on different ports
2. Update log file paths in `server.py`
3. Create master dashboard page linking to all modules

## 📈 **Performance**

- **Memory**: ~50MB (FastAPI + WebSocket)
- **CPU**: Minimal (log parsing only)
- **Network**: ~1KB/s per client (WebSocket)
- **Scalability**: Supports multiple concurrent clients

## 🛡️ **Security**

### **Current Setup** (Development)
- No authentication
- Listens on all interfaces (`0.0.0.0`)
- Suitable for local/trusted networks only

### **Production Recommendations**
- Add JWT authentication
- Use HTTPS/WSS
- Restrict to `127.0.0.1` or use firewall
- Implement rate limiting

## 📝 **Future Enhancements**

- [ ] Historical test comparison
- [ ] Export metrics to CSV/JSON
- [ ] Multiple test monitoring (tabbed interface)
- [ ] Dark/light mode toggle
- [ ] Custom alert thresholds
- [ ] PM2 ecosystem integration

## 🤝 **Contributing**

When modifying dashboard:
1. Maintain ADHD/dyslexia optimizations
2. Test on mobile devices
3. Verify WebSocket reconnection
4. Update this README

## 📄 **License**

Part of 3M Lighting Project - Creator Intelligence Module
