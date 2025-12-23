# The Factory - Standalone Distribution

This is a complete, portable distribution of The Factory.

## Quick Start (First Time)

### Step 1: Run Setup

**Windows:**
```cmd
python setup.py
```

**Linux/Mac:**
```bash
python3 setup.py
```

This will:
- Create a virtual environment
- Install all dependencies
- Create convenience scripts
- Verify installation

**Takes:** 10-30 seconds on first run

### Step 2: Start Building!

**Windows:**
```cmd
factory.bat "Build a todo app with React"
```

**Linux/Mac:**
```bash
./factory.sh "Build a todo app with React"
```

That's it! Your project will be in `projects/`

## Usage

### Natural Language (Easiest)
```bash
factory "Build me a REST API for a blog"
```

### From Project Directory
```bash
mkdir projects/my-app
nano projects/my-app/project_spec.md
# Write your spec...

factory --project projects/my-app
```

### From Example
```bash
factory --spec examples/specs/gui_project_spec.md
```

### Interactive Mode
```bash
factory
# Then follow the prompts
```

## What's Included

```
the_factory/
├── setup.py                 # Run this first!
├── factory.bat/.sh          # Use this to run (after setup)
├── activate.bat/.sh         # Activate environment manually
├── run_factory.py           # Main script
├── prompts/                 # AI agent system prompts
├── docs/                    # Complete documentation
├── examples/                # Example specifications
├── bootstrap/               # Core orchestration system
├── templates/               # Project templates
└── visual_explainer/        # Interactive demo
```

## Troubleshooting

**Q: Setup fails with "Python not found"**
A: Install Python 3.8+ from python.org

**Q: "ModuleNotFoundError" when running**
A: Run setup.py again

**Q: factory.bat/sh not found**
A: Run setup.py first - it creates these scripts

**Q: Want to use minimal dependencies?**
A: Use `requirements-minimal.txt` instead (edit setup.py to reference it)

## System Requirements

- Python 3.8 or higher
- 50MB disk space (500MB with venv)
- 2GB RAM minimum (8GB recommended for large projects)
- Internet connection (for first-time setup only)

## Documentation

- **Quick Start:** See above
- **Full Documentation:** docs/guides/INSTRUCTIONS.md
- **Writing Specs:** docs/guides/SPEC_OPTIMIZATION_LLM.md
- **Visual Demo:** Open visual_explainer/index.html in browser
- **Examples:** examples/specs/

## Support

- Documentation: docs/ directory
- Examples: examples/specs/
- Issues: Contact the distributor

---

**The Factory** - From idea to implementation in minutes, not months.
