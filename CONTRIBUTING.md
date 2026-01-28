# Contributing Guidelines

## Welcome to the US Visa Prediction Model Project!

Thank you for your interest in contributing. This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

- Be respectful and constructive in all interactions
- Report issues or concerns to the project maintainers
- No harassment, discrimination, or abusive behavior

## Getting Started

### Prerequisites
- Python 3.10+
- Docker & Docker Compose
- Git

### Development Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd MLOPs-Clasification-Model
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements-dev.txt
```

4. **Setup pre-commit hooks**
```bash
pre-commit install
```

5. **Create .env file**
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Development Workflow

### Branch Naming
- Feature: `feature/description`
- Bug fix: `bugfix/description`
- Hotfix: `hotfix/description`

### Making Changes

1. Create a feature branch
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes following code style guidelines

3. Run tests
```bash
pytest tests/ -v --cov=us_visa
```

4. Run linting
```bash
black us_visa tests
flake8 us_visa tests
mypy us_visa
```

5. Commit with meaningful messages
```bash
git commit -m "feat: add new feature description"
```

## Code Style Guidelines

### Python Style
- Follow PEP 8
- Use type hints for function parameters and returns
- Maximum line length: 100 characters
- Use black for formatting
- Use isort for import organization

### Example:
```python
def predict_visa(
    data: USVisaPredictionRequest,
    request_id: Optional[str] = None,
) -> USVisaPredictionResponse:
    """
    Predict visa approval.
    
    Args:
        data: Prediction request with feature values
        request_id: Optional unique request identifier
        
    Returns:
        Prediction response with result and status
    """
    # Implementation
    pass
```

### Documentation
- Docstrings for all public functions and classes
- Use Google-style docstrings
- Include examples for complex functions
- Keep README.md updated

## Testing

### Writing Tests
```python
def test_prediction_with_valid_data(self, sample_visa_data):
    """Test prediction with valid input data"""
    response = client.post("/predict", json=sample_visa_data)
    assert response.status_code == 200
    assert "prediction" in response.json()
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=us_visa

# Run specific test file
pytest tests/test_schemas.py -v
```

### Test Requirements
- Aim for >80% code coverage
- Test both happy path and error cases
- Use fixtures for reusable test data
- Mock external dependencies

## Pull Request Process

1. **Before submitting**
   - Update documentation
   - Add/update tests
   - Run linting and formatting
   - Ensure all tests pass

2. **Create Pull Request**
   - Clear title and description
   - Reference any related issues (#123)
   - Explain the changes and motivation

3. **PR Description Template**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Added unit tests
- [ ] Added integration tests
- [ ] All tests pass locally

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Tested locally
```

4. **Code Review**
   - Address reviewer comments
   - Push updates to the same branch
   - Request re-review when ready

## Reporting Issues

### Bug Reports
Include:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS
- Relevant logs

### Feature Requests
Include:
- Clear description
- Use cases and benefits
- Potential implementation approach
- Any relevant references

## Commit Message Guidelines

Format:
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting)
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `test`: Test addition/modification
- `chore`: Build, dependencies, etc.

Example:
```
feat(api): add request rate limiting

Implement token bucket rate limiting for API endpoints
to prevent abuse and ensure fair usage.

Closes #123
```

## Running the Application Locally

### With Docker Compose
```bash
docker-compose up -d
```

Services available:
- API: http://localhost:8080
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

### Without Docker
```bash
# Terminal 1: Start MongoDB (if using local)
mongod

# Terminal 2: Run the application
python app.py
```

## Documentation

- Keep README.md updated
- Document new features
- Update API documentation in docstrings
- Add examples for new functionality

## Questions?

- Check existing documentation
- Search existing issues
- Create a discussion for questions
- Contact maintainers

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to this project!
