# Day 001: Environment Setup & FastAPI Hello World

> **Time**: 1.5-2 hours | **Difficulty**: ⭐⭐ Easy

---

## 🎯 What You'll Build Today

- ✅ Python virtual environment
- ✅ FastAPI server running on port 8000
- ✅ `/health` endpoint returning JSON
- ✅ API documentation at `/docs`
- ✅ Your first curl test!

---

## 📦 Dependencies (Day 1 Only)

```bash
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.4.0
python-multipart>=0.0.6
python-dotenv>=1.0.0
```

---

## 📂 Files to Create

```
defi-analytics-platform/
├── src/
│   ├── __init__.py          ← CREATE
│   └── api/
│       ├── __init__.py      ← CREATE
│       └── main.py          ← CREATE (main file)
├── .env                     ← CREATE
├── .gitignore               ← UPDATE
└── requirements-day001.txt  ← CREATE
```

---

## 🚀 Step-by-Step Implementation

### **Step 1: Setup Virtual Environment** (10 min)

```bash
# Navigate to project root
cd /home/user/defi-analytics-platform

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# You should see (venv) in your prompt
# (venv) user@host:~/defi-analytics-platform$

# Upgrade pip
pip install --upgrade pip
```

**✅ Checkpoint**: Your prompt should show `(venv)`

---

### **Step 2: Create Requirements File** (5 min)

```bash
cat > requirements-day001.txt << 'EOF'
# Day 001 Dependencies - FastAPI Basics

# Core API Framework
fastapi>=0.104.0          # Modern Python web framework
uvicorn>=0.24.0           # ASGI server
pydantic>=2.4.0           # Data validation
python-multipart>=0.0.6   # Form data support
python-dotenv>=1.0.0      # Environment variables
EOF
```

```bash
# Install dependencies
pip install -r requirements-day001.txt

# Verify installation
pip list | grep -E 'fastapi|uvicorn|pydantic'
```

**Expected output:**
```
fastapi          0.104.1
pydantic         2.4.2
uvicorn          0.24.0
```

**✅ Checkpoint**: All packages installed without errors

---

### **Step 3: Create Project Structure** (5 min)

```bash
# Create directories
mkdir -p src/api

# Create __init__.py files
touch src/__init__.py
touch src/api/__init__.py

# Create environment file
cat > .env << 'EOF'
# DeFi Analytics Platform - Environment Variables

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
ENVIRONMENT=development

# Future: Database (Day 28+)
# DATABASE_URL=postgresql://user:pass@localhost/defi_analytics

# Future: Web3 (Day 25+)
# WEB3_PROVIDER_URL=https://mainnet.infura.io/v3/YOUR_KEY
# THE_GRAPH_API_KEY=your_key_here
EOF
```

```bash
# Update .gitignore
cat >> .gitignore << 'EOF'

# Virtual environment
venv/
env/

# Environment variables
.env
.env.local

# Python cache
__pycache__/
*.py[cod]
*$py.class
*.so

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF
```

**✅ Checkpoint**: Run `ls -la src/api/` and verify files exist

---

### **Step 4: Create FastAPI Application** (30 min)

Create `src/api/main.py`:

```python
"""
=============================================================================
DeFi ANALYTICS PLATFORM - FastAPI Backend
=============================================================================

DAY 001: Basic Setup

PURPOSE:
- Initialize FastAPI application
- Create health check endpoint
- Set up CORS middleware
- Enable API documentation

LEARNING GOALS:
- Understand FastAPI app initialization
- Learn about middleware
- Create your first endpoint
- Test with curl

AUTHOR: Built for DeFi Analytics Tutorial
DAY: 001/030
=============================================================================
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# ====================================================================================
# INITIALIZE FastAPI APP
# ====================================================================================

app = FastAPI(
    title="DeFi Analytics Platform API",
    description="""
    ## 🚀 DeFi Analytics & Risk Management Platform

    Comprehensive API for DeFi portfolio management, yield optimization,
    and risk assessment.

    ### Features (Building over 30 days)

    * **Day 1-5**: Foundation (You are here! ✨)
    * **Day 6-12**: Liquidity Analysis
    * **Day 13-18**: Risk Assessment
    * **Day 19-24**: Yield Optimization
    * **Day 25-28**: Blockchain Integration
    * **Day 29-30**: Production Polish

    ### Current Progress

    ✅ FastAPI server initialized
    ✅ Health check endpoint
    🔨 More endpoints coming soon...

    Built for Economics & Finance MSc students.
    """,
    version="0.1.0-day001",
    contact={
        "name": "DeFi Analytics Team",
        "email": "contact@defi-analytics.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    docs_url="/docs",      # Swagger UI
    redoc_url="/redoc"     # ReDoc alternative
)


# ====================================================================================
# MIDDLEWARE CONFIGURATION
# ====================================================================================

# CORS - Allow all origins for development
# In production, you'd restrict this to specific domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Allow all origins (development only!)
    allow_credentials=True,
    allow_methods=["*"],           # Allow all HTTP methods
    allow_headers=["*"],           # Allow all headers
)


# ====================================================================================
# ENDPOINTS
# ====================================================================================

@app.get(
    "/",
    tags=["General"],
    summary="Root endpoint",
    response_description="API information and available endpoints"
)
async def root() -> Dict[str, Any]:
    """
    # Root Endpoint

    Returns basic information about the DeFi Analytics Platform API.

    ## What This Returns

    - API name and version
    - Documentation links
    - Current status
    - Available endpoint categories

    ## Example Usage

    ```bash
    curl http://localhost:8000/
    ```

    ## Response

    ```json
    {
      "message": "DeFi Analytics Platform API",
      "version": "0.1.0-day001",
      "status": "operational"
    }
    ```
    """
    return {
        "message": "DeFi Analytics Platform API",
        "version": "0.1.0-day001",
        "day": "001/030",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "status": "operational",
        "endpoints": {
            "general": [
                "GET /",
                "GET /health"
            ],
            "liquidity": "Coming Day 6-12",
            "risk": "Coming Day 13-18",
            "yield": "Coming Day 19-24",
            "portfolio": "Coming Day 22-24"
        },
        "environment": os.getenv("ENVIRONMENT", "development")
    }


@app.get(
    "/health",
    tags=["General"],
    summary="Health check endpoint",
    response_description="Health status of API and services"
)
async def health_check() -> Dict[str, Any]:
    """
    # Health Check Endpoint

    Monitor the health status of the API and its dependent services.

    ## What This Checks

    - API server status (always operational if you get a response!)
    - Database connection (Day 28+)
    - Web3 connection (Day 25+)
    - Cache service (Day 28+)

    ## Example Usage

    ```bash
    curl http://localhost:8000/health
    ```

    ## Response

    ```json
    {
      "status": "healthy",
      "timestamp": "2024-01-15T10:30:45.123456",
      "services": {
        "api": "operational",
        "database": "not_configured",
        "web3": "not_configured"
      }
    }
    ```

    ## Status Codes

    - `200 OK`: All services healthy
    - `503 Service Unavailable`: One or more services down (Day 28+)
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": "operational",
        "services": {
            "api": "operational",
            "database": "not_configured",    # Will implement Day 28+
            "web3": "not_configured",        # Will implement Day 25+
            "cache": "not_configured"        # Will implement Day 28+
        },
        "version": "0.1.0-day001",
        "day": "001/030"
    }


# ====================================================================================
# STARTUP/SHUTDOWN EVENTS
# ====================================================================================

@app.on_event("startup")
async def startup_event():
    """
    Runs when the server starts

    Future use:
    - Initialize database connections
    - Connect to Web3 provider
    - Start background tasks
    """
    print("=" * 80)
    print("🚀 DeFi ANALYTICS PLATFORM API")
    print("=" * 80)
    print(f"Day: 001/030")
    print(f"Version: 0.1.0-day001")
    print(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"\n📚 Documentation:")
    print(f"   Swagger UI: http://localhost:8000/docs")
    print(f"   ReDoc:      http://localhost:8000/redoc")
    print(f"\n✅ Server started successfully!")
    print("=" * 80)


@app.on_event("shutdown")
async def shutdown_event():
    """
    Runs when the server shuts down

    Future use:
    - Close database connections
    - Cleanup Web3 connections
    - Stop background tasks
    """
    print("\n" + "=" * 80)
    print("👋 Shutting down DeFi Analytics Platform API")
    print("=" * 80)


# ====================================================================================
# RUN APPLICATION (Development Only)
# ====================================================================================

if __name__ == "__main__":
    import uvicorn

    # Get configuration from environment
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    debug = os.getenv("DEBUG", "True").lower() == "true"

    print(f"\n🔧 Starting server on {host}:{port}")
    print(f"Debug mode: {debug}\n")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,          # Auto-reload on code changes (development only)
        log_level="info"
    )
```

**✅ Checkpoint**: File created at `src/api/main.py`

---

### **Step 5: Run the Server** (10 min)

```bash
# Navigate to API directory
cd src/api

# Run the server
python main.py
```

**Expected output:**
```
🔧 Starting server on 0.0.0.0:8000
Debug mode: True

================================================================================
🚀 DeFi ANALYTICS PLATFORM API
================================================================================
Day: 001/030
Version: 0.1.0-day001
Environment: development

📚 Documentation:
   Swagger UI: http://localhost:8000/docs
   ReDoc:      http://localhost:8000/redoc

✅ Server started successfully!
================================================================================
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**✅ Checkpoint**: Server running without errors

---

## 🧪 Testing (15 min)

### **Test 1: Root Endpoint**

Open a NEW terminal (keep server running) and run:

```bash
curl http://localhost:8000/
```

**Expected output:**
```json
{
  "message": "DeFi Analytics Platform API",
  "version": "0.1.0-day001",
  "day": "001/030",
  "documentation": {
    "swagger": "/docs",
    "redoc": "/redoc"
  },
  "status": "operational",
  "endpoints": {
    "general": [
      "GET /",
      "GET /health"
    ],
    "liquidity": "Coming Day 6-12",
    "risk": "Coming Day 13-18",
    "yield": "Coming Day 19-24",
    "portfolio": "Coming Day 22-24"
  },
  "environment": "development"
}
```

**✅ Test passed!**

---

### **Test 2: Health Check**

```bash
curl http://localhost:8000/health
```

**Expected output:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:45.123456",
  "uptime": "operational",
  "services": {
    "api": "operational",
    "database": "not_configured",
    "web3": "not_configured",
    "cache": "not_configured"
  },
  "version": "0.1.0-day001",
  "day": "001/030"
}
```

**✅ Test passed!**

---

### **Test 3: Formatted Output with jq**

If you have `jq` installed:

```bash
curl -s http://localhost:8000/health | jq
```

This gives you pretty-printed JSON with colors!

---

### **Test 4: Check Response Headers**

```bash
curl -v http://localhost:8000/health
```

Look for:
```
< HTTP/1.1 200 OK
< content-type: application/json
< access-control-allow-origin: *
```

---

### **Test 5: API Documentation**

Open your browser and visit:

1. **Swagger UI**: http://localhost:8000/docs
   - Interactive API documentation
   - Try out endpoints directly
   - See request/response schemas

2. **ReDoc**: http://localhost:8000/redoc
   - Alternative documentation view
   - Better for reading
   - Cleaner layout

**✅ Both documentation pages load successfully!**

---

## 🎉 Day 001 Complete!

### **What You Built:**

✅ Python virtual environment
✅ FastAPI application with 2 endpoints
✅ CORS middleware configured
✅ Auto-generated API documentation
✅ Environment variable configuration
✅ Startup/shutdown event handlers

### **What You Learned:**

- FastAPI app initialization
- Creating GET endpoints
- Pydantic response models
- Middleware configuration
- API documentation (Swagger/ReDoc)
- Environment variables with dotenv
- Testing with curl

---

## 📊 Progress

```
[████░░░░░░░░░░░░░░░░░░░░░░░░░░] Day 001/030 (3.3%)

Foundation:     [████░░░░░░] 1/5 days
Liquidity:      [░░░░░░░░░░] 0/7 days
Risk:           [░░░░░░░░░░] 0/6 days
Yield:          [░░░░░░░░░░] 0/6 days
Data/Production:[░░░░░░░░░░] 0/6 days
```

---

## 🐛 Troubleshooting

### **Problem: Port 8000 already in use**

```bash
# Check what's using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port
# Edit .env and change API_PORT=8001
```

### **Problem: Module not found**

```bash
# Make sure you're in the right directory
pwd
# Should show: /home/user/defi-analytics-platform/src/api

# Make sure venv is activated
which python
# Should show: /home/user/defi-analytics-platform/venv/bin/python
```

### **Problem: Import errors**

```bash
# Run from src/api directory
cd /home/user/defi-analytics-platform/src/api
python main.py
```

---

## 📚 Bonus: Understanding the Code

### **What is FastAPI?**
- Modern Python web framework
- Automatic API documentation
- Type hints for validation
- Fast (based on Starlette and Pydantic)

### **What is CORS?**
- Cross-Origin Resource Sharing
- Allows browser to make requests from different domains
- We set `allow_origins=["*"]` for development
- In production, restrict to specific domains

### **What is Uvicorn?**
- ASGI server (Asynchronous Server Gateway Interface)
- Runs FastAPI applications
- `reload=True` auto-restarts on code changes

### **What is dotenv?**
- Loads environment variables from `.env` file
- Keeps secrets out of code
- Use for API keys, database URLs, etc.

---

## 🚀 Next Steps

**Tomorrow (Day 002)**: Pydantic Request/Response Models
- Create POST endpoints
- Input validation
- Error handling
- Request body parsing

**Prepare for Day 002:**
- Keep server running to test changes
- Read about Pydantic BaseModel
- Think about what data structures we'll need

---

## 💾 Save Your Work

```bash
# Stop the server (CTRL+C)

# From project root
cd /home/user/defi-analytics-platform

# Check git status
git status

# Stage changes
git add src/ .env.example requirements-day001.txt

# Commit
git commit -m "Day 001: FastAPI setup with health check endpoint

- Initialize FastAPI application
- Add root and health check endpoints
- Configure CORS middleware
- Set up API documentation (Swagger/ReDoc)
- Add environment variable configuration
- Create virtual environment and install dependencies

Day 001/030 complete ✓"

# Push (if using git)
git push origin your-branch
```

---

**🎊 Congratulations on completing Day 001!**

*Tomorrow we'll add POST endpoints with Pydantic validation. Rest well!*

---

**Day 001/030 Complete** ✅ | **Next**: Day 002 - Request/Response Models
