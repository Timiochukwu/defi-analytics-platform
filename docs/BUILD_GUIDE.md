# DeFi Analytics Platform - Step-by-Step Build Guide

> **Complete guide to building this project from scratch in the correct order**

This guide shows you **exactly** how to build the entire DeFi Analytics Platform step-by-step, in the right order, with explanations of dependencies.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Phase 1: Project Foundation](#phase-1-project-foundation)
3. [Phase 2: Backend Core](#phase-2-backend-core)
4. [Phase 3: Backend Business Logic](#phase-3-backend-business-logic)
5. [Phase 4: Backend API](#phase-4-backend-api)
6. [Phase 5: Frontend Setup](#phase-5-frontend-setup)
7. [Phase 6: Testing Infrastructure](#phase-6-testing-infrastructure)
8. [Phase 7: Docker & Deployment](#phase-7-docker--deployment)
9. [Phase 8: CI/CD Pipeline](#phase-8-cicd-pipeline)
10. [Verification & Testing](#verification--testing)

---

## Prerequisites

Install these before starting:

```bash
# Python 3.9 or higher
python --version  # Should be 3.9+

# Node.js 18 or higher
node --version    # Should be 18+

# Git
git --version

# Docker (optional, for deployment)
docker --version
```

---

## Phase 1: Project Foundation

### Step 1.1: Create Project Directory

```bash
mkdir defi-analytics-platform
cd defi-analytics-platform
git init
```

**Why:** This is your project root. Everything else goes inside here.

---

### Step 1.2: Create .gitignore

**File:** `.gitignore`

**Why:** Prevent committing sensitive files, dependencies, and build artifacts.

**Dependencies:** None (do this FIRST!)

<details>
<summary>Click to see .gitignore content</summary>

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
build/
dist/
*.egg-info/

# Virtual environments
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp

# Jupyter
.ipynb_checkpoints

# Data files
*.csv
*.xlsx
*.db
*.sqlite

# Environment
.env
.env.local

# Logs
*.log
logs/

# OS
.DS_Store

# Node.js
frontend/node_modules/
frontend/.next/
frontend/out/

# Web3 keys (IMPORTANT!)
*.key
*.pem
private_keys/
```
</details>

---

### Step 1.3: Create README.md

**File:** `README.md`

**Why:** Project documentation (the file you're reading now exists in the actual project)

**Dependencies:** None

**Action:** Copy the existing README.md or create a basic one describing your project.

---

### Step 1.4: Create Directory Structure

```bash
# Backend directories
mkdir -p src/{analytics,risk,optimization,data,api}
mkdir -p src/{models,schemas,utils,config,middleware}

# Data directories
mkdir -p data/{raw,processed,cache}
mkdir -p logs
mkdir -p reports

# Testing
mkdir -p tests/{test_analytics,test_risk,test_optimization,test_data,test_api}

# Scripts & docs
mkdir -p scripts
mkdir -p docs

# Dashboard
mkdir -p dashboard

# Add .gitkeep to preserve empty directories
touch data/raw/.gitkeep data/processed/.gitkeep data/cache/.gitkeep
touch logs/.gitkeep reports/.gitkeep
```

**Why:** Creates the skeleton structure for all files. Directories must exist before you put files in them!

**Dependencies:** None

---

### Step 1.5: Create Python __init__.py Files

```bash
# Make Python recognize these as packages
touch src/__init__.py
touch src/analytics/__init__.py
touch src/risk/__init__.py
touch src/optimization/__init__.py
touch src/data/__init__.py
touch src/api/__init__.py
touch src/models/__init__.py
touch src/schemas/__init__.py
touch src/utils/__init__.py
touch src/config/__init__.py
touch src/middleware/__init__.py
touch tests/__init__.py
touch tests/test_analytics/__init__.py
touch tests/test_risk/__init__.py
touch tests/test_optimization/__init__.py
touch tests/test_data/__init__.py
touch tests/test_api/__init__.py
```

**Why:** Python needs `__init__.py` to treat directories as importable packages.

**Dependencies:** Directories from Step 1.4 must exist.

---

### Step 1.6: Create requirements.txt

**File:** `requirements.txt`

**Why:** Lists all Python dependencies. You need this BEFORE creating a virtual environment.

**Dependencies:** None

<details>
<summary>Click to see requirements.txt (Core dependencies only for now)</summary>

```txt
# Core Data Science
pandas>=2.0.0
numpy>=1.24.0
scipy>=1.11.0

# Blockchain & Web3
web3>=6.11.0
eth-abi>=4.2.0
eth-account>=0.10.0
eth-utils>=2.3.0

# DeFi Protocols & APIs
python-dotenv>=1.0.0
requests>=2.31.0
aiohttp>=3.9.0

# Database
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
redis>=5.0.0

# API & Web
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.4.0

# Dashboard
streamlit>=1.28.0
plotly>=5.17.0

# Visualization
matplotlib>=3.8.0
seaborn>=0.13.0

# Utilities
python-json-logger>=2.0.7
colorlog>=6.8.0
```
</details>

---

### Step 1.7: Create Virtual Environment & Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Why:** Isolates project dependencies from system Python.

**Dependencies:** Requires `requirements.txt` from Step 1.6.

---

## Phase 2: Backend Core

**Goal:** Build the foundation utilities and configuration that everything else depends on.

### Step 2.1: Create Configuration Module

**File:** `src/config/settings.py`

**Why:** Centralized configuration. Many modules will import this.

**Dependencies:** `python-dotenv` from requirements.txt

**Order:** Create this EARLY because other modules will import `get_settings()`.

<details>
<summary>Click to see settings.py template</summary>

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "DeFi Analytics Platform"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    DATABASE_URL: str = "postgresql://user:password@localhost:5432/defi_analytics"
    REDIS_URL: str = "redis://localhost:6379/0"

    ETHEREUM_RPC_URL: str = "http://localhost:8545"

    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
```
</details>

**File:** `src/config/__init__.py`

```python
from .settings import Settings, get_settings

__all__ = ["Settings", "get_settings"]
```

---

### Step 2.2: Create Utility Modules

**Order:** Create utilities BEFORE business logic because business logic will use them.

#### 2.2a: Logger Utility

**File:** `src/utils/logger.py`

**Why:** Every module needs logging. Create this early.

**Dependencies:** `colorlog` package

<details>
<summary>Click to see logger.py</summary>

```python
import logging
import sys
import colorlog

def setup_logging(level: str = "INFO") -> None:
    log_level = getattr(logging, level.upper(), logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
        }
    )
    console_handler.setFormatter(console_formatter)

    logging.basicConfig(level=log_level, handlers=[console_handler])

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
```
</details>

#### 2.2b: Math Utilities

**File:** `src/utils/math_utils.py`

**Why:** Business logic modules will need these math functions.

**Dependencies:** None (just Python standard library)

<details>
<summary>Click to see math_utils.py</summary>

```python
import math

def calculate_percentage_change(old_value: float, new_value: float) -> float:
    if old_value == 0:
        return 0.0 if new_value == 0 else float('inf')
    return ((new_value - old_value) / old_value) * 100

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    if denominator == 0:
        return default
    return numerator / denominator

def calculate_apy_from_apr(apr: float, compounds_per_year: int = 365) -> float:
    return math.pow(1 + apr / compounds_per_year, compounds_per_year) - 1
```
</details>

#### 2.2c: Web3 Helpers

**File:** `src/utils/web3_helpers.py`

**Why:** Blockchain interaction utilities needed by data collectors.

**Dependencies:** `web3` package

<details>
<summary>Click to see web3_helpers.py</summary>

```python
from web3 import Web3
from eth_utils import is_address, to_checksum_address

def get_web3_provider(rpc_url: str = None) -> Web3:
    if rpc_url is None:
        from src.config import get_settings
        rpc_url = get_settings().ETHEREUM_RPC_URL

    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        raise ConnectionError(f"Failed to connect to {rpc_url}")
    return w3

def validate_address(address: str) -> bool:
    return is_address(address)

def to_checksum(address: str) -> str:
    if not validate_address(address):
        raise ValueError(f"Invalid address: {address}")
    return to_checksum_address(address)
```
</details>

**File:** `src/utils/__init__.py`

```python
from .logger import get_logger, setup_logging
from .math_utils import calculate_percentage_change, safe_divide
from .web3_helpers import get_web3_provider, validate_address

__all__ = [
    "get_logger", "setup_logging",
    "calculate_percentage_change", "safe_divide",
    "get_web3_provider", "validate_address"
]
```

---

### Step 2.3: Create Data Models

**File:** `src/models/protocol.py`, `position.py`, `portfolio.py`

**Why:** These define your data structure. Create before business logic that uses them.

**Dependencies:** Python `dataclasses` and `datetime` (standard library)

**Order:** Models → Schemas → Business Logic → API

<details>
<summary>Click to see models/protocol.py example</summary>

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum

class ProtocolType(Enum):
    LENDING = "lending"
    DEX = "dex"
    YIELD_AGGREGATOR = "yield_aggregator"

@dataclass
class Protocol:
    protocol_id: str
    name: str
    protocol_type: ProtocolType
    chain: str
    tvl_usd: float
    contract_address: str

    audit_score: Optional[float] = None
    days_deployed: Optional[int] = None
    has_bug_bounty: bool = False

    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
```
</details>

Create similar files for `position.py` and `portfolio.py`.

**File:** `src/models/__init__.py`

```python
from .protocol import Protocol
from .position import Position
from .portfolio import Portfolio

__all__ = ["Protocol", "Position", "Portfolio"]
```

---

## Phase 3: Backend Business Logic

**Goal:** Create the core analytics, risk, and optimization modules.

**Order:** These can be built in parallel since they don't depend on each other.

### Step 3.1: Liquidity Analyzer

**File:** `src/analytics/liquidity_analyzer.py`

**Why:** Core analytics functionality.

**Dependencies:**
- `numpy`, `pandas` (from requirements.txt)
- `src/utils/math_utils.py` (from Phase 2)

**Order:** Build this after utilities are ready.

<details>
<summary>Click to see liquidity_analyzer.py skeleton</summary>

```python
import numpy as np
import pandas as pd
from dataclasses import dataclass
from src.utils import safe_divide, get_logger

logger = get_logger(__name__)

@dataclass
class SlippageResult:
    amount_out: float
    slippage_percent: float
    price_impact: float
    effective_price: float

class LiquidityAnalyzer:
    def calculate_slippage_constant_product(
        self,
        reserve_in: float,
        reserve_out: float,
        amount_in: float,
        fee: float = 0.003
    ) -> SlippageResult:
        """Calculate slippage using constant product formula (x * y = k)"""

        # Apply fee
        amount_in_with_fee = amount_in * (1 - fee)

        # Constant product formula
        k = reserve_in * reserve_out
        new_reserve_in = reserve_in + amount_in_with_fee
        new_reserve_out = k / new_reserve_in
        amount_out = reserve_out - new_reserve_out

        # Calculate metrics
        price_before = reserve_in / reserve_out
        price_after = new_reserve_in / new_reserve_out
        slippage_percent = ((price_after - price_before) / price_before) * 100

        return SlippageResult(
            amount_out=amount_out,
            slippage_percent=slippage_percent,
            price_impact=slippage_percent,
            effective_price=amount_in / amount_out if amount_out > 0 else 0
        )

    def calculate_pool_quality_score(
        self,
        tvl: float,
        volume_24h: float,
        fee_tier: float,
        reserve_ratio: float
    ) -> dict:
        """Score pool quality on a 0-100 scale"""

        # TVL score (higher is better)
        tvl_score = min(100, (tvl / 1_000_000) * 10)

        # Volume/TVL ratio score
        turnover = safe_divide(volume_24h, tvl, default=0)
        volume_score = min(100, turnover * 100)

        # Balance score (closer to 1.0 is better)
        balance_score = (1 - abs(1 - reserve_ratio)) * 100

        # Overall score (weighted average)
        overall_score = (tvl_score * 0.3 + volume_score * 0.4 + balance_score * 0.3)

        # Rating
        if overall_score >= 90: rating = "A+"
        elif overall_score >= 80: rating = "A"
        elif overall_score >= 70: rating = "B"
        elif overall_score >= 60: rating = "C"
        else: rating = "D"

        return {
            "overall_score": overall_score,
            "rating": rating,
            "tvl_score": tvl_score,
            "volume_score": volume_score,
            "balance_score": balance_score
        }
```
</details>

**File:** `src/analytics/__init__.py`

```python
from .liquidity_analyzer import LiquidityAnalyzer

__all__ = ["LiquidityAnalyzer"]
```

**Test it:**

```python
# In Python shell or Jupyter notebook
from src.analytics import LiquidityAnalyzer

analyzer = LiquidityAnalyzer()
result = analyzer.calculate_slippage_constant_product(
    reserve_in=2_000_000,
    reserve_out=1_000,
    amount_in=10_000
)
print(result)
```

---

### Step 3.2: Risk Models

**File:** `src/risk/defi_risk_models.py`

**Why:** Risk assessment functionality.

**Dependencies:**
- `numpy`, `pandas`
- `src/utils/math_utils.py`

<details>
<summary>Click to see risk model skeleton</summary>

```python
from dataclasses import dataclass
from enum import Enum
from src.utils import get_logger

logger = get_logger(__name__)

class RiskLevel(Enum):
    VERY_LOW = "Very Low"
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"
    CRITICAL = "Critical"

@dataclass
class SmartContractRisk:
    protocol_name: str
    overall_risk_score: float
    risk_level: RiskLevel
    audit_score: float
    code_complexity_score: float
    time_deployed_score: float

class SmartContractRiskAnalyzer:
    def assess_smart_contract_risk(
        self,
        protocol_name: str,
        auditors: list,
        code_lines: int,
        days_deployed: int,
        tvl_usd: float,
        **kwargs
    ) -> SmartContractRisk:
        """Assess smart contract risk"""

        # Audit score (more audits = better)
        audit_score = min(100, len(auditors) * 30)

        # Code complexity (more lines = more risk)
        complexity_risk = min(100, (code_lines / 1000) * 5)

        # Time deployed (longer = better)
        time_score = min(100, (days_deployed / 365) * 40)

        # Overall risk (lower is better)
        overall_risk = (
            (100 - audit_score) * 0.4 +
            complexity_risk * 0.3 +
            (100 - time_score) * 0.3
        )

        # Determine risk level
        if overall_risk < 20:
            risk_level = RiskLevel.VERY_LOW
        elif overall_risk < 40:
            risk_level = RiskLevel.LOW
        elif overall_risk < 60:
            risk_level = RiskLevel.MODERATE
        elif overall_risk < 80:
            risk_level = RiskLevel.HIGH
        else:
            risk_level = RiskLevel.CRITICAL

        return SmartContractRisk(
            protocol_name=protocol_name,
            overall_risk_score=overall_risk,
            risk_level=risk_level,
            audit_score=audit_score,
            code_complexity_score=complexity_risk,
            time_deployed_score=time_score
        )
```
</details>

Continue with similar patterns for other business logic modules.

---

## Phase 4: Backend API

**Goal:** Create FastAPI endpoints that expose your business logic.

**Dependencies:** All business logic from Phase 3 must be complete first.

### Step 4.1: Create API Schemas

**File:** `src/schemas/requests.py`

**Why:** Define what data your API accepts.

**Dependencies:** `pydantic` package

<details>
<summary>Click to see requests.py</summary>

```python
from pydantic import BaseModel, Field

class SlippageRequest(BaseModel):
    reserve_in: float = Field(..., gt=0)
    reserve_out: float = Field(..., gt=0)
    amount_in: float = Field(..., gt=0)
    fee: float = Field(0.003, ge=0, le=1)

class PoolQualityRequest(BaseModel):
    tvl: float = Field(..., gt=0)
    volume_24h: float = Field(..., ge=0)
    fee_tier: float = Field(..., ge=0)
    reserve_ratio: float = Field(..., gt=0, le=1)
```
</details>

**File:** `src/schemas/responses.py`

```python
from pydantic import BaseModel

class SlippageResponse(BaseModel):
    amount_out: float
    slippage_percent: float
    price_impact: float
    effective_price: float
```

**File:** `src/schemas/__init__.py`

```python
from .requests import *
from .responses import *
```

---

### Step 4.2: Create Main API File

**File:** `src/api/main.py`

**Why:** This is your FastAPI application entry point.

**Dependencies:**
- `fastapi`, `uvicorn`
- All business logic modules from Phase 3
- Schemas from Step 4.1

<details>
<summary>Click to see main.py</summary>

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.config import get_settings
from src.analytics import LiquidityAnalyzer
from src.risk import SmartContractRiskAnalyzer
from src.schemas.requests import SlippageRequest, PoolQualityRequest
from src.schemas.responses import SlippageResponse

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="DeFi Analytics Platform API"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize analyzers
liquidity_analyzer = LiquidityAnalyzer()
risk_analyzer = SmartContractRiskAnalyzer()

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.post("/api/liquidity/slippage", response_model=SlippageResponse)
def calculate_slippage(request: SlippageRequest):
    result = liquidity_analyzer.calculate_slippage_constant_product(
        reserve_in=request.reserve_in,
        reserve_out=request.reserve_out,
        amount_in=request.amount_in,
        fee=request.fee
    )
    return SlippageResponse(**result.__dict__)

@app.post("/api/liquidity/pool-quality")
def score_pool_quality(request: PoolQualityRequest):
    result = liquidity_analyzer.calculate_pool_quality_score(
        tvl=request.tvl,
        volume_24h=request.volume_24h,
        fee_tier=request.fee_tier,
        reserve_ratio=request.reserve_ratio
    )
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
```
</details>

**Test your API:**

```bash
# Run the API
python -m src.api.main

# In another terminal, test it:
curl http://localhost:8000/health

# Visit interactive docs
open http://localhost:8000/docs
```

---

## Phase 5: Frontend Setup

**Goal:** Create the Next.js frontend.

**Dependencies:** Backend API must be working (Phase 4).

### Step 5.1: Create Frontend Directory

```bash
mkdir frontend
cd frontend
```

---

### Step 5.2: Initialize Next.js

```bash
npx create-next-app@latest . --typescript --tailwind --app --no-src
```

**Answer the prompts:**
- TypeScript: Yes
- ESLint: Yes
- Tailwind CSS: Yes
- `app/` directory: Yes
- Import alias: Yes (@/*)

**Why:** This creates the basic Next.js structure.

---

### Step 5.3: Install Additional Dependencies

```bash
npm install recharts axios swr ethers lucide-react clsx tailwind-merge
npm install --save-dev @tailwindcss/forms
```

**Why:** These are needed for charts, API calls, and UI components.

---

### Step 5.4: Configure Tailwind

**File:** `frontend/tailwind.config.js`

(Use the comprehensive config from the files I created earlier)

---

### Step 5.5: Create API Client

**File:** `frontend/src/lib/api.ts`

**Why:** Centralize API calls. Components will import from here.

```typescript
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const liquidityApi = {
  calculateSlippage: async (data: any) => {
    const response = await api.post('/api/liquidity/slippage', data)
    return response.data
  },

  scorePoolQuality: async (data: any) => {
    const response = await api.post('/api/liquidity/pool-quality', data)
    return response.data
  },
}

export default api
```

---

### Step 5.6: Create Main Page

**File:** `frontend/src/app/page.tsx`

**Why:** This is your main dashboard UI.

**Dependencies:** API client from Step 5.5

(Use the page.tsx I created earlier with the full dashboard)

---

### Step 5.7: Test Frontend

```bash
npm run dev
```

Visit http://localhost:3000

---

## Phase 6: Testing Infrastructure

**Goal:** Add automated tests.

**Dependencies:** All business logic from Phase 3.

### Step 6.1: Create Test Configuration

**File:** `tests/conftest.py`

**Why:** Pytest fixtures shared across all tests.

```python
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

@pytest.fixture
def sample_pool_data():
    return {
        "reserve_in": 2_000_000,
        "reserve_out": 1_000,
        "tvl": 100_000_000,
        "volume_24h": 80_000_000,
        "fee_tier": 0.003,
    }
```

---

### Step 6.2: Create Sample Tests

**File:** `tests/test_analytics/test_liquidity_analyzer.py`

```python
import pytest
from src.analytics import LiquidityAnalyzer

class TestLiquidityAnalyzer:
    def test_calculate_slippage(self, sample_pool_data):
        analyzer = LiquidityAnalyzer()
        result = analyzer.calculate_slippage_constant_product(
            reserve_in=sample_pool_data["reserve_in"],
            reserve_out=sample_pool_data["reserve_out"],
            amount_in=10_000
        )
        assert result.slippage_percent >= 0
        assert result.amount_out > 0
```

**Run tests:**

```bash
pytest tests/
```

---

## Phase 7: Docker & Deployment

**Goal:** Containerize your application.

**Dependencies:** Working backend and frontend.

### Step 7.1: Create Environment Files

**File:** `.env.example`

(Use the comprehensive .env.example I created)

```bash
cp .env.example .env
# Edit .env with your actual values
```

---

### Step 7.2: Create Dockerfiles

**File:** `Dockerfile` (backend)

(Use the Dockerfile I created earlier)

**File:** `frontend/Dockerfile`

(Use the frontend Dockerfile I created)

---

### Step 7.3: Create Docker Compose

**File:** `docker-compose.yml`

(Use the comprehensive docker-compose.yml I created)

---

### Step 7.4: Test Docker

```bash
docker-compose up --build
```

---

## Phase 8: CI/CD Pipeline

**Goal:** Automate testing and deployment.

**Dependencies:** Everything must be working.

### Step 8.1: Create GitHub Actions

**File:** `.github/workflows/ci.yml`

(Use the CI workflow I created)

---

### Step 8.2: Push to GitHub

```bash
git add .
git commit -m "Initial commit: DeFi Analytics Platform"
git remote add origin YOUR_GITHUB_URL
git push -u origin main
```

---

## Verification & Testing

### Final Checklist

```bash
# 1. Python tests pass
pytest tests/

# 2. Backend API works
python -m src.api.main
curl http://localhost:8000/health

# 3. Frontend works
cd frontend && npm run dev

# 4. Docker works
docker-compose up

# 5. Lint passes
flake8 src/
black --check src/

# 6. Build succeeds
cd frontend && npm run build
```

---

## Common Issues & Solutions

### Issue 1: Import errors

**Problem:** `ModuleNotFoundError: No module named 'src'`

**Solution:**
```bash
# Make sure you're in the project root
# Add src to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Issue 2: Database connection fails

**Problem:** Can't connect to PostgreSQL

**Solution:**
```bash
# Start PostgreSQL with Docker
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=password postgres:15

# Or update .env to use SQLite for testing
DATABASE_URL=sqlite:///./test.db
```

### Issue 3: Frontend can't reach backend

**Problem:** CORS errors or connection refused

**Solution:**
1. Ensure backend is running: `python -m src.api.main`
2. Check NEXT_PUBLIC_API_URL in frontend/.env.local
3. Verify CORS settings in src/api/main.py

---

## Dependency Graph

```
Phase 1 (Foundation)
    ↓
Phase 2 (Core Backend)
    ├── config/settings.py
    ├── utils/logger.py
    ├── utils/math_utils.py
    └── models/*.py
    ↓
Phase 3 (Business Logic)
    ├── analytics/liquidity_analyzer.py  (uses utils, models)
    ├── risk/defi_risk_models.py         (uses utils, models)
    └── optimization/yield_optimizer.py   (uses utils, models)
    ↓
Phase 4 (API)
    ├── schemas/*.py                      (independent)
    └── api/main.py                       (uses everything above)
    ↓
Phase 5 (Frontend)
    └── frontend/                         (uses API from Phase 4)
    ↓
Phase 6 (Tests)
    └── tests/                            (tests Phase 2-4)
    ↓
Phase 7 (Docker)
    └── Deployment configs                (packages everything)
    ↓
Phase 8 (CI/CD)
    └── GitHub Actions                    (automates everything)
```

---

## Next Steps

After completing all phases:

1. **Customize** the analytics logic for your specific needs
2. **Add more protocols** (Uniswap, Curve, etc.)
3. **Implement authentication** for production
4. **Add database migrations** with Alembic
5. **Monitor with Prometheus/Grafana**
6. **Deploy to cloud** (AWS, GCP, Azure)

---

## Summary

**You've built:**
- ✅ Complete backend with analytics, risk models, and API
- ✅ Modern frontend with Next.js and Tailwind
- ✅ Comprehensive testing infrastructure
- ✅ Docker deployment configuration
- ✅ CI/CD pipeline with GitHub Actions

**Time estimate:**
- Following this guide: 4-8 hours
- Learning as you go: 1-2 days
- Full customization: 1-2 weeks

**Remember:** Build in order! Each phase depends on the previous ones.
