# Day 002: Pydantic Request/Response Models

> **Time**: 1.5-2 hours | **Difficulty**: ⭐⭐ Easy | **Builds on**: Day 001

---

## 🎯 What You'll Build Today

- ✅ Pydantic request models with validation
- ✅ POST endpoint that accepts JSON
- ✅ Field validation (min/max, required/optional)
- ✅ Error handling (400, 422, 500)
- ✅ Example: Simple percentage calculator API

---

## 📦 Dependencies

**No new dependencies!** We use what we installed on Day 001:
- `pydantic>=2.4.0` (already installed)

---

## 📂 Files to Modify/Create

```
src/api/
├── main.py          ← MODIFY (add new endpoint)
└── models.py        ← CREATE (Pydantic models)
```

---

## 🚀 Step-by-Step Implementation

### **Step 1: Create Pydantic Models** (20 min)

Create `src/api/models.py`:

```python
"""
=============================================================================
PYDANTIC MODELS - Request/Response Schemas
=============================================================================

DAY 002: Data Validation

PURPOSE:
- Define request/response data structures
- Automatic validation
- Auto-generated documentation
- Type safety

LEARNING GOALS:
- Pydantic BaseModel
- Field validation
- Optional vs required fields
- Custom validators

DAY: 002/030
=============================================================================
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime


# ====================================================================================
# CALCULATION MODELS (Day 002)
# ====================================================================================

class PercentageRequest(BaseModel):
    """
    Request model for percentage calculation

    Example:
        Input:  {"value": 100, "percentage": 10}
        Output: 110 (100 + 10% of 100)
    """
    value: float = Field(
        ...,
        description="Base value",
        example=100.0,
        gt=0  # Must be greater than 0
    )
    percentage: float = Field(
        ...,
        description="Percentage to add (e.g., 10 for 10%)",
        example=10.0,
        ge=-100,  # Must be >= -100 (can't reduce by more than 100%)
        le=1000   # Max 1000% increase
    )

    class Config:
        json_schema_extra = {
            "example": {
                "value": 100.0,
                "percentage": 10.0
            }
        }


class PercentageResponse(BaseModel):
    """
    Response model for percentage calculation
    """
    original_value: float = Field(..., description="Input value")
    percentage: float = Field(..., description="Percentage applied")
    result: float = Field(..., description="Calculated result")
    change: float = Field(..., description="Absolute change")

    class Config:
        json_schema_extra = {
            "example": {
                "original_value": 100.0,
                "percentage": 10.0,
                "result": 110.0,
                "change": 10.0
            }
        }


class APYCalculationRequest(BaseModel):
    """
    Request model for APY (Annual Percentage Yield) calculation

    Formula: APY = ((ending_value / starting_value) ^ (365 / days)) - 1

    Example:
        Deposited: $10,000
        After 30 days: $10,100
        APY = ((10100/10000)^(365/30)) - 1 = 12.7% annual
    """
    starting_value: float = Field(
        ...,
        description="Initial deposit amount in USD",
        example=10000.0,
        gt=0
    )
    ending_value: float = Field(
        ...,
        description="Final value in USD",
        example=10100.0,
        gt=0
    )
    days: int = Field(
        ...,
        description="Number of days elapsed",
        example=30,
        gt=0,
        le=365
    )

    @validator('ending_value')
    def ending_must_be_positive(cls, v, values):
        """Validate ending value makes sense"""
        if 'starting_value' in values and v < 0:
            raise ValueError('Ending value must be positive')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "starting_value": 10000.0,
                "ending_value": 10100.0,
                "days": 30
            }
        }


class APYCalculationResponse(BaseModel):
    """
    Response model for APY calculation
    """
    starting_value: float
    ending_value: float
    days: int
    apy_percent: float = Field(..., description="Annual Percentage Yield")
    daily_rate_percent: float = Field(..., description="Average daily return rate")
    total_return_percent: float = Field(..., description="Total return for the period")

    class Config:
        json_schema_extra = {
            "example": {
                "starting_value": 10000.0,
                "ending_value": 10100.0,
                "days": 30,
                "apy_percent": 12.68,
                "daily_rate_percent": 0.033,
                "total_return_percent": 1.0
            }
        }


# ====================================================================================
# ERROR RESPONSE MODELS
# ====================================================================================

class ErrorResponse(BaseModel):
    """
    Standard error response
    """
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    detail: Optional[str] = Field(None, description="Additional error details")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Invalid input data",
                "detail": "Value must be greater than 0",
                "timestamp": "2024-01-15T10:30:45.123456"
            }
        }
```

**✅ Checkpoint**: `src/api/models.py` created

---

### **Step 2: Add Endpoints to main.py** (30 min)

Modify `src/api/main.py` - add these imports at the top:

```python
from models import (
    PercentageRequest,
    PercentageResponse,
    APYCalculationRequest,
    APYCalculationResponse,
    ErrorResponse
)
from fastapi import HTTPException, status
```

Then add these endpoints before the `if __name__ == "__main__":` section:

```python
# ====================================================================================
# CALCULATION ENDPOINTS (Day 002)
# ====================================================================================

@app.post(
    "/api/calculate/percentage",
    tags=["Calculations"],
    summary="Calculate percentage increase/decrease",
    response_model=PercentageResponse,
    responses={
        400: {"model": ErrorResponse},
        422: {"model": ErrorResponse}
    }
)
async def calculate_percentage(request: PercentageRequest) -> PercentageResponse:
    """
    # Calculate Percentage Increase/Decrease

    Adds a percentage to a base value.

    ## Formula

    ```
    result = value * (1 + percentage/100)
    ```

    ## Example 1: 10% Increase

    **Input:**
    ```json
    {
      "value": 100,
      "percentage": 10
    }
    ```

    **Output:**
    ```json
    {
      "original_value": 100.0,
      "percentage": 10.0,
      "result": 110.0,
      "change": 10.0
    }
    ```

    ## Example 2: 20% Decrease

    **Input:**
    ```json
    {
      "value": 100,
      "percentage": -20
    }
    ```

    **Output:**
    ```json
    {
      "original_value": 100.0,
      "percentage": -20.0,
      "result": 80.0,
      "change": -20.0
    }
    ```

    ## Validation

    - `value` must be > 0
    - `percentage` must be between -100 and 1000
    """
    try:
        # Calculate result
        multiplier = 1 + (request.percentage / 100)
        result = request.value * multiplier
        change = result - request.value

        return PercentageResponse(
            original_value=request.value,
            percentage=request.percentage,
            result=round(result, 2),
            change=round(change, 2)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Calculation error: {str(e)}"
        )


@app.post(
    "/api/calculate/apy",
    tags=["Calculations"],
    summary="Calculate Annual Percentage Yield (APY)",
    response_model=APYCalculationResponse,
    responses={
        400: {"model": ErrorResponse},
        422: {"model": ErrorResponse}
    }
)
async def calculate_apy(request: APYCalculationRequest) -> APYCalculationResponse:
    """
    # Calculate APY (Annual Percentage Yield)

    Calculate annualized return based on a period's performance.

    ## Formula

    ```
    APY = ((ending_value / starting_value) ^ (365 / days)) - 1
    ```

    ## Example: 30-Day DeFi Yield

    You deposited $10,000 in Aave. After 30 days, you have $10,100.
    What's the APY?

    **Input:**
    ```json
    {
      "starting_value": 10000,
      "ending_value": 10100,
      "days": 30
    }
    ```

    **Calculation:**
    ```
    Growth = 10100 / 10000 = 1.01 (1% in 30 days)
    APY = (1.01 ^ (365/30)) - 1 = 0.1268 = 12.68%
    ```

    **Output:**
    ```json
    {
      "starting_value": 10000.0,
      "ending_value": 10100.0,
      "days": 30,
      "apy_percent": 12.68,
      "daily_rate_percent": 0.033,
      "total_return_percent": 1.0
    }
    ```

    ## Why APY Matters in DeFi

    - Compare yields across different time periods
    - DeFi protocols often report different periods (daily, weekly, monthly)
    - APY normalizes everything to annual basis
    - Helps compare traditional finance vs DeFi returns

    ## Validation

    - All values must be positive
    - Days must be between 1 and 365
    """
    try:
        # Calculate total return
        total_return = (request.ending_value / request.starting_value) - 1

        # Calculate APY (annualized)
        periods_per_year = 365 / request.days
        apy = ((request.ending_value / request.starting_value) ** periods_per_year) - 1

        # Calculate daily rate
        daily_rate = total_return / request.days

        return APYCalculationResponse(
            starting_value=request.starting_value,
            ending_value=request.ending_value,
            days=request.days,
            apy_percent=round(apy * 100, 2),
            daily_rate_percent=round(daily_rate * 100, 3),
            total_return_percent=round(total_return * 100, 2)
        )

    except ZeroDivisionError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Starting value cannot be zero"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"APY calculation error: {str(e)}"
        )
```

Also update the version in the root endpoint:

```python
@app.get("/", ...)
async def root() -> Dict[str, Any]:
    return {
        "message": "DeFi Analytics Platform API",
        "version": "0.2.0-day002",  # ← UPDATE THIS
        "day": "002/030",             # ← UPDATE THIS
        # ... rest remains same
        "endpoints": {
            "general": [
                "GET /",
                "GET /health"
            ],
            "calculations": [              # ← ADD THIS
                "POST /api/calculate/percentage",
                "POST /api/calculate/apy"
            ],
            "liquidity": "Coming Day 6-12",
            # ... rest remains same
        }
    }
```

**✅ Checkpoint**: Endpoints added to `main.py`

---

### **Step 3: Test the New Endpoints** (20 min)

Restart your server:

```bash
# Stop server (CTRL+C)
# Start again
cd src/api
python main.py
```

#### **Test 1: Percentage Calculation**

```bash
curl -X POST http://localhost:8000/api/calculate/percentage \
  -H "Content-Type: application/json" \
  -d '{
    "value": 100,
    "percentage": 10
  }'
```

**Expected output:**
```json
{
  "original_value": 100.0,
  "percentage": 10.0,
  "result": 110.0,
  "change": 10.0
}
```

**✅ Test passed!**

---

#### **Test 2: Percentage Decrease**

```bash
curl -X POST http://localhost:8000/api/calculate/percentage \
  -H "Content-Type: application/json" \
  -d '{
    "value": 1000,
    "percentage": -25
  }'
```

**Expected output:**
```json
{
  "original_value": 1000.0,
  "percentage": -25.0,
  "result": 750.0,
  "change": -250.0
}
```

---

#### **Test 3: APY Calculation**

```bash
curl -X POST http://localhost:8000/api/calculate/apy \
  -H "Content-Type: application/json" \
  -d '{
    "starting_value": 10000,
    "ending_value": 10100,
    "days": 30
  }'
```

**Expected output:**
```json
{
  "starting_value": 10000.0,
  "ending_value": 10100.0,
  "days": 30,
  "apy_percent": 12.68,
  "daily_rate_percent": 0.033,
  "total_return_percent": 1.0
}
```

**✅ Test passed!**

---

#### **Test 4: Validation Error (Negative Value)**

```bash
curl -X POST http://localhost:8000/api/calculate/percentage \
  -H "Content-Type: application/json" \
  -d '{
    "value": -100,
    "percentage": 10
  }'
```

**Expected output (422 error):**
```json
{
  "detail": [
    {
      "type": "greater_than",
      "loc": ["body", "value"],
      "msg": "Input should be greater than 0",
      "input": -100,
      "ctx": {"gt": 0}
    }
  ]
}
```

**✅ Validation working!**

---

#### **Test 5: Missing Field**

```bash
curl -X POST http://localhost:8000/api/calculate/percentage \
  -H "Content-Type: application/json" \
  -d '{
    "value": 100
  }'
```

**Expected output (422 error):**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "percentage"],
      "msg": "Field required",
      "input": {"value": 100}
    }
  ]
}
```

**✅ Required field validation working!**

---

### **Step 4: Test with Swagger UI** (10 min)

1. Open http://localhost:8000/docs

2. Find "Calculations" section

3. Click "POST /api/calculate/percentage"

4. Click "Try it out"

5. Modify the example JSON

6. Click "Execute"

7. See the response!

**✅ Interactive documentation working!**

---

## 🎉 Day 002 Complete!

### **What You Built:**

✅ Pydantic request/response models
✅ 2 new POST endpoints (percentage, APY)
✅ Field validation (min/max, required/optional)
✅ Custom validators
✅ Error responses (400, 422, 500)
✅ Financial calculation (APY formula)

### **What You Learned:**

- Pydantic BaseModel
- Field() with validation constraints
- Custom @validator decorators
- HTTP status codes (200, 400, 422, 500)
- HTTPException for errors
- POST endpoint creation
- Request body parsing
- Response models

---

## 📊 Progress

```
[████████░░░░░░░░░░░░░░░░░░░░] Day 002/030 (6.7%)

Foundation:     [████████░░] 2/5 days
Liquidity:      [░░░░░░░░░░] 0/7 days
Risk:           [░░░░░░░░░░] 0/6 days
Yield:          [░░░░░░░░░░] 0/6 days
Data/Production:[░░░░░░░░░░] 0/6 days
```

---

## 💡 Key Concepts

### **What is Pydantic?**
- Data validation library
- Uses Python type hints
- Automatic error messages
- Powers FastAPI's magic!

### **Validation Constraints:**
```python
Field(
    ...,              # ... = required
    gt=0,             # Greater than 0
    ge=0,             # Greater than or equal to 0
    lt=100,           # Less than 100
    le=100,           # Less than or equal to 100
    min_length=1,     # For strings
    max_length=100,   # For strings
    regex="^[A-Z]"    # Pattern matching
)
```

### **HTTP Status Codes:**
- `200 OK`: Success
- `400 Bad Request`: Client error (invalid data)
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

---

## 🐛 Troubleshooting

### **Problem: Cannot import models**

```bash
# Make sure you're running from src/api
cd /home/user/defi-analytics-platform/src/api
python main.py
```

### **Problem: Validation not working**

```bash
# Check Pydantic version
pip show pydantic
# Should be >= 2.4.0
```

---

## 🚀 Next Steps

**Tomorrow (Day 003)**: Data Structures & Enums
- Create DeFi-specific enums (RiskLevel, YieldType)
- Dataclasses for complex responses
- Type hints for nested structures

---

**Day 002/030 Complete** ✅ | **Next**: Day 003 - Enums & Dataclasses
