# API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, the API is open for development. In production, use JWT tokens:

```bash
# Get token
POST /api/auth/token
{
  "username": "user",
  "password": "password"
}

# Use token
Authorization: Bearer <token>
```

## Endpoints

### Health Check

#### GET /health
Check API status

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

---

### Liquidity Analysis

#### POST /api/liquidity/slippage
Calculate slippage for a trade

**Request**:
```json
{
  "reserve_in": 2000000,
  "reserve_out": 1000,
  "amount_in": 10000,
  "fee": 0.003
}
```

**Response**:
```json
{
  "amount_out": 4.995,
  "slippage_percent": 0.50,
  "price_impact": 0.48,
  "effective_price": 2000.40,
  "minimum_received": 4.945
}
```

#### POST /api/liquidity/pool-quality
Score a liquidity pool

**Request**:
```json
{
  "tvl": 100000000,
  "volume_24h": 80000000,
  "fee_tier": 0.0005,
  "reserve_ratio": 0.98
}
```

**Response**:
```json
{
  "overall_score": 93.5,
  "rating": "A+",
  "tvl_score": 95.0,
  "volume_score": 92.0,
  "efficiency_score": 94.0,
  "balance_score": 93.0
}
```

---

### Risk Assessment

#### POST /api/risk/smart-contract
Assess smart contract risk

**Request**:
```json
{
  "protocol_name": "Aave",
  "auditors": ["Trail of Bits", "OpenZeppelin"],
  "code_lines": 15000,
  "days_deployed": 900,
  "tvl_usd": 5000000000,
  "upgrade_mechanism": "Timelock + Multisig",
  "has_bug_bounty": true,
  "admin_control_level": "Low"
}
```

**Response**:
```json
{
  "overall_risk_score": 18.2,
  "risk_level": "Very Low",
  "factors": {
    "audit_risk": 10.0,
    "complexity_risk": 25.0,
    "time_risk": 5.0,
    "admin_risk": 15.0
  },
  "recommendations": [
    "Protocol has excellent security practices",
    "Multiple audits from reputable firms",
    "Long deployment history indicates stability"
  ],
  "timestamp": "2024-01-01T12:00:00Z"
}
```

#### POST /api/risk/liquidation
Assess liquidation risk

**Request**:
```json
{
  "protocol_name": "Aave",
  "asset": "ETH",
  "collateral_value_usd": 100000,
  "debt_value_usd": 60000
}
```

**Response**:
```json
{
  "health_factor": 1.433,
  "distance_to_liquidation_percent": 30.23,
  "risk_level": "Low",
  "liquidation_price": 1400.0,
  "safe_borrow_limit_usd": 70000
}
```

---

### Yield Optimization

#### GET /api/yield/opportunities
Get yield opportunities

**Query Parameters**:
- `min_apy` (optional): Minimum APY
- `max_risk` (optional): Maximum risk score
- `min_tvl` (optional): Minimum TVL

**Response**:
```json
{
  "opportunities": [
    {
      "protocol": "Aave",
      "asset": "USDC",
      "apy": 8.5,
      "tvl_usd": 1200000,
      "risk_score": 18.2,
      "risk_rating": "Very Low",
      "yield_type": "lending",
      "liquidity_score": 95.0
    }
  ],
  "count": 1
}
```

---

### Portfolio Management

#### POST /api/portfolio/build
Build a portfolio

**Request**:
```json
{
  "capital_usd": 100000,
  "strategy": "balanced",
  "target_apy": 15.0
}
```

**Response**:
```json
{
  "strategy": "balanced",
  "total_capital_usd": 100000,
  "expected_apy": 12.5,
  "portfolio_risk_score": 28.5,
  "sharpe_ratio": 1.85,
  "allocations": [
    {
      "protocol": "Aave",
      "asset": "USDC",
      "weight_percent": 30.0,
      "allocated_usd": 30000,
      "expected_apy": 8.5,
      "risk_score": 18.2
    },
    {
      "protocol": "Curve",
      "asset": "3Pool",
      "weight_percent": 25.0,
      "allocated_usd": 25000,
      "expected_apy": 12.1,
      "risk_score": 22.5
    }
  ],
  "diversification_score": 85.0,
  "timestamp": "2024-01-01T12:00:00Z"
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "error": "Error type",
  "detail": "Detailed error message",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Common Error Codes

- `400` - Bad Request (invalid parameters)
- `401` - Unauthorized (missing/invalid token)
- `404` - Not Found
- `422` - Validation Error
- `429` - Rate Limit Exceeded
- `500` - Internal Server Error

---

## Rate Limits

- **Default**: 60 requests per minute
- **Burst**: 100 requests
- **Headers**:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

---

## Interactive Documentation

Visit these URLs when the server is running:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json
