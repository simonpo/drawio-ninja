# Contributing to Draw.io Whisperer

## Development Setup

### Prerequisites

- Python 3.6 or higher (3.11+ recommended)
- Git

### Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/simonpo/drawio-ninja.git
   cd drawio-ninja
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   # For basic usage (validation script only)
   pip install -r requirements.txt
   
   # For development (includes linting, type checking, testing)
   pip install -r requirements-dev.txt
   ```

4. **Verify installation**
   ```bash
   python validate.py examples/simple-flowchart.drawio
   ```

### Development Workflow

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Run validation on test diagrams: `python validate.py examples/*.drawio`
4. Commit with clear messages: `git commit -m "Add: brief description"`
5. Push and open a pull request

### Code Quality

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Keep functions focused and documented
- Test with multiple diagram examples before submitting

### Testing

Run the validation script against all examples:
```bash
for file in examples/*.drawio; do
  echo "Validating $file"
  python validate.py "$file"
done
```

### Questions?

Open an issue for discussion before starting major changes.
