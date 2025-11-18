# Contributing to DeFi Analytics Platform

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## Getting Started

### 1. Fork the Repository
```bash
git clone https://github.com/yourusername/defi-analytics-platform.git
cd defi-analytics-platform
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### 3. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## Development Workflow

### Backend Development

1. **Write Code**
   - Follow PEP 8 style guide
   - Add type hints
   - Write docstrings

2. **Write Tests**
   ```bash
   # Write tests in tests/
   pytest tests/test_your_module.py
   ```

3. **Run Linters**
   ```bash
   make lint
   # or
   flake8 src/ tests/
   black src/ tests/
   isort src/ tests/
   mypy src/
   ```

4. **Format Code**
   ```bash
   make format
   # or
   black src/ tests/
   isort src/ tests/
   ```

### Frontend Development

1. **Write Code**
   - Follow TypeScript best practices
   - Use functional components
   - Add PropTypes/TypeScript types

2. **Run Linter**
   ```bash
   cd frontend
   npm run lint
   ```

3. **Test Locally**
   ```bash
   npm run dev
   ```

## Testing

### Backend Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_analytics/test_liquidity_analyzer.py
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Commit Guidelines

### Commit Message Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

### Examples
```bash
feat(analytics): add impermanent loss calculator

Implement IL calculation for Uniswap V2 and V3 pools
with support for custom price ranges.

Closes #123
```

```bash
fix(api): handle division by zero in slippage calculation

Add safe_divide utility function to prevent crashes
when pool reserves are zero.
```

## Pull Request Process

### 1. Update Documentation
- Update README.md if needed
- Add docstrings to new functions
- Update API documentation

### 2. Add Tests
- Write unit tests for new features
- Ensure all tests pass
- Maintain >80% code coverage

### 3. Submit PR
- Fill out the PR template
- Link related issues
- Request review from maintainers

### 4. Code Review
- Address reviewer feedback
- Make requested changes
- Re-request review

### 5. Merge
- Squash commits if needed
- Wait for CI to pass
- Maintainer will merge

## Code Style

### Python
```python
# Good
def calculate_slippage(
    reserve_in: float,
    reserve_out: float,
    amount_in: float
) -> SlippageResult:
    """
    Calculate slippage for a trade.

    Args:
        reserve_in: Input token reserve
        reserve_out: Output token reserve
        amount_in: Amount to trade

    Returns:
        SlippageResult with calculation details
    """
    # Implementation
    pass
```

### TypeScript/React
```typescript
// Good
interface PoolQualityProps {
  tvl: number
  volume24h: number
  feeTier: number
}

export const PoolQuality: React.FC<PoolQualityProps> = ({
  tvl,
  volume24h,
  feeTier,
}) => {
  // Implementation
}
```

## Adding New Features

### Backend Feature
1. Create module in `src/`
2. Add models in `src/models/`
3. Add schemas in `src/schemas/`
4. Add API routes in `src/api/routes/`
5. Write tests in `tests/`
6. Update documentation

### Frontend Feature
1. Create component in `src/components/`
2. Add types in `src/types/`
3. Add API calls in `src/lib/api.ts`
4. Update pages in `src/app/`
5. Add tests
6. Update documentation

## Questions?

- Open an issue for bugs
- Use discussions for questions
- Join our Discord (if available)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
