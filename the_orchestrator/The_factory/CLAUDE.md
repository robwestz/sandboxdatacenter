# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

The Factory is a meta-orchestration platform that builds complete software projects through recursive agent spawning. It operates standalone with intelligent fallback mechanisms, supporting up to 200 concurrent agents across 10 recursive levels.

## Key Commands

### Setup & Installation
```bash
# First-time setup (creates venv, installs dependencies, generates scripts)
python setup.py

# Activate environment
activate.bat              # Windows
source activate.sh        # Linux/Mac
```

### Running Builds

```bash
# Quick run (recommended)
factory.bat "Build a todo app with React"                    # Windows
./factory.sh "Build a todo app with React"                   # Linux/Mac

# From project directory with existing spec
python run_factory.py --project projects/my-app

# From specification file
python run_factory.py --spec examples/specs/gui_project_spec.md

# Interactive mode (menu-driven)
python run_factory.py

# Direct Genesis Prime execution
python bootstrap/genesis_prime.py --spec project_spec.md --output ./output
```

### Development Workflow
```bash
# When making changes to core files, test with a simple build first
python run_factory.py "Create a simple CLI tool"

# Check build output and logs
ls projects/project-name-*/output/
cat projects/project-name-*/logs/build.log
cat projects/project-name-*/.factory_metadata.json
```

## Architecture Overview

### Execution Flow
```
run_factory.py (Entry)
    ↓ Parse specification & setup project
Genesis Prime (bootstrap/genesis_prime.py)
    ↓ Determine strategy & initialize
Import Manager (bootstrap/import_manager.py)
    ↓ Smart dependency resolution with fallbacks
Chain Reactor (bootstrap/chain_reactor.py)
    ↓ Recursive agent spawning
Orchestrator (Simple or SOVEREIGN)
    ↓ Coordinate build phases
Output (projects/name-timestamp/output/)
```

### Three-Tier Fallback System

**INTEGRATED Mode** (Best)
- Uses THE_ORCHESTRATOR with full SOVEREIGN capabilities
- Neural pattern learning, multi-paradigm orchestration
- Requires: `../THE_ORCHESTRATOR/` directory

**STANDALONE Mode** (Good)
- Uses `lib/fallback_implementations/`
- SimpleOrchestrator, error handling, checkpoints
- Requires: `lib/` directory with implementations

**MINIMAL Mode** (Emergency)
- Inline minimal implementations
- Basic structure generation only
- Always available

The system automatically detects and uses the best available mode.

### Critical Components

**ImportManager** (`bootstrap/import_manager.py`)
- Detects environment and provides appropriate components
- All imports go through: `get_orchestrator()`, `get_chain_reactor()`, `get_sovereign_classes()`
- NEVER import SOVEREIGN components directly - always use ImportManager

**Genesis Prime** (`bootstrap/genesis_prime.py`)
- Meta-orchestrator that initiates all builds
- Parses specifications (Markdown/YAML/JSON)
- Contains ProjectSpecification dataclass (includes `tech_stack` field)
- Determines orchestration strategy based on complexity

**Chain Reactor** (`bootstrap/chain_reactor.py`)
- Recursive agent spawning engine
- Each agent can spawn children based on task complexity
- Roles: ARCHITECT (max 10 children), DEVELOPER (8), BUILDER (8), TESTER (3), etc.
- Complexity threshold: if `calculate_complexity(task) > auto_spawn_threshold`, spawn children

**SimpleOrchestrator** (`lib/fallback_implementations/simple_orchestrator.py`)
- Standalone build orchestrator (6 phases: validate, analyze, design, structure, files, validate)
- Accesses `spec.tech_stack` - ensure ProjectSpecification has this field
- All file writes use `encoding='utf-8'` for Windows compatibility

## Project Specification Format

Supports three formats (auto-detected):

**Markdown** (Primary):
```markdown
# Project Name

Description paragraph

## Type: web_app
## Complexity: moderate

## OBJECTIVES
- Build core functionality
- Include tests

## FEATURES
### Core Features
- Feature 1
- Feature 2
```

**YAML**:
```yaml
name: Project Name
type: web_app
complexity: moderate
tech_stack: [Python, FastAPI, React]
```

**JSON**:
```json
{
  "name": "Project Name",
  "type": "web_app",
  "tech_stack": ["Python", "FastAPI"]
}
```

### ProjectSpecification Fields
```python
name: str                              # Required
description: str
type: ProjectType                      # web_app, api, cli_tool, library, custom
complexity: ComplexityLevel            # simple, moderate, complex, extreme
objectives: List[str]
features: Dict[str, List[str]]         # {core: [], optional: []}
tech_stack: List[str]                  # IMPORTANT: Must be present
architecture: Dict[str, Any]
technical: Dict[str, str]
quality: Dict[str, str]
```

## Directory Structure

```
Fabriken/
├── bootstrap/              # Core orchestration engine
│   ├── genesis_prime.py    # Meta-orchestrator (entry point for builds)
│   ├── chain_reactor.py    # Agent spawning logic
│   ├── import_manager.py   # Smart dependency resolution
│   └── sovereign_loader.py # Dynamic SOVEREIGN integration
├── lib/                    # Standalone implementations
│   ├── fallback_implementations/
│   │   ├── simple_orchestrator.py  # Main standalone builder
│   │   ├── simple_agent.py
│   │   └── mock_neural.py
│   ├── error_handling/
│   │   ├── circuit_breaker.py      # Prevent cascading failures
│   │   ├── recovery_manager.py     # Retry with exponential backoff
│   │   └── validation_engine.py
│   └── state_management/
│       ├── checkpoint_manager.py   # Resumable builds
│       └── progress_tracker.py
├── run_factory.py          # User-facing entry point
├── setup.py                # First-time installation
├── projects/               # Generated projects (timestamped)
│   └── name-YYYYMMDD-HHMMSS/
│       ├── project_spec.md
│       ├── .factory_metadata.json
│       ├── logs/
│       └── output/         # Generated code here
├── examples/specs/         # Example specifications
├── templates/              # Spec templates
└── docs/                   # Documentation
    ├── system/             # Architecture docs
    └── guides/             # Usage guides
```

## Important Patterns & Conventions

### Safe Print Pattern
Windows console encoding issues are handled with `safe_print()`:
```python
def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        # Replace emojis/unicode with ASCII
        text = text.replace('✅', '[OK]').replace('❌', '[X]')...
        print(text)
```
Use `safe_print()` instead of `print()` in all user-facing output.

### File Writing Pattern
Always specify encoding for Windows compatibility:
```python
file_path.write_text(content, encoding='utf-8')
```

### Error Handling Pattern
```python
try:
    # Try advanced implementation
    from SOVEREIGN import AdvancedClass
except ImportError:
    # Fall back to simple implementation
    from lib.fallback_implementations import SimpleClass
```

### Async Pattern
All build operations are async:
```python
async def build_project(...):
    result = await orchestrator.build()
    return result

# At entry point:
asyncio.run(build_project(...))
```

### Agent Spawning Logic
```python
# In chain_reactor.py:
complexity = calculate_complexity(task)
if complexity > agent.auto_spawn_threshold:
    subtasks = decompose_task(task)
    for subtask in subtasks[:agent.max_children]:
        child = spawn_agent(determine_role(subtask), subtask)
        await propagate_chain(child, depth + 1, max_depth)
```

## Common Modifications

### Adding a New Field to ProjectSpecification
1. Add to dataclass in `bootstrap/genesis_prime.py` (~line 97)
2. Initialize in `__post_init__()` (~line 113)
3. Update all three parsers:
   - `_parse_markdown_spec()` (~line 263)
   - `_parse_json_spec()` (~line 349)
   - `_parse_yaml_spec()` (~line 371)
4. Update any code that accesses the field (e.g., `simple_orchestrator.py`)

### Adding a New Agent Role
1. Add to `AgentRole` enum in `lib/fallback_implementations/simple_agent.py`
2. Set `max_children` in role configuration
3. Add role-specific logic in `chain_reactor.py`'s `determine_child_role()`

### Adding a New Build Phase
1. Add to `BuildPhase` enum in `lib/state_management/progress_tracker.py`
2. Implement phase logic in orchestrator's `build()` method
3. Add checkpoint after phase completion

### Fixing Encoding Issues
1. Add emoji/unicode to `safe_print()` replacements dict in:
   - `run_factory.py` (~line 43)
   - `bootstrap/genesis_prime.py` (~line 63)
2. Ensure all `write_text()` calls use `encoding='utf-8'`

## State Management & Recovery

### Checkpoints
Saved to `.factory_checkpoints/`:
```python
# Save
checkpoint_manager.save_checkpoint("phase_name", state_dict)

# Resume
if checkpoint_manager.can_resume("phase_name"):
    state = checkpoint_manager.load_checkpoint("phase_name")
```

### Build Metadata
Every build creates `.factory_metadata.json` with:
- Timestamps, duration, status
- Agents spawned, files created
- Spec path, auto-generation flag
- Phase completion info

### Circuit Breakers
Prevent cascading failures:
- CLOSED → normal operation
- OPEN → too many failures, blocking requests
- HALF_OPEN → testing recovery

Access via: `self.circuit_breaker` in Genesis Prime

## Output Structure

Generated projects follow this structure:
```
projects/project-name-YYYYMMDD-HHMMSS/
├── project_spec.md              # Original specification
├── .factory_metadata.json       # Build metadata
├── logs/
│   └── build.log               # Detailed logs
└── output/
    ├── README.md               # Generated documentation
    ├── config.json             # Project configuration
    ├── .gitignore
    ├── requirements.txt        # Python dependencies
    ├── src/
    │   ├── __init__.py
    │   └── main.py            # Entry point with class structure
    ├── tests/
    │   ├── __init__.py
    │   └── test_main.py       # Basic tests
    ├── docs/
    ├── scripts/
    └── config/
```

## Debugging Tips

### Build Failures
1. Check `.factory_metadata.json` for status and error
2. Review `logs/build.log` for detailed traces
3. Check ImportManager mode in logs: "STANDALONE"/"INTEGRATED"/"MINIMAL"
4. Verify `spec.tech_stack` is populated (common issue)
5. Test with simpler spec if complex one fails

### Import Errors
1. Check that `lib/` directory exists and has content
2. Verify ImportManager initialization in logs
3. Don't import SOVEREIGN directly - use ImportManager getters
4. Check fallback cascade is working (warnings in logs)

### Encoding Errors
1. Ensure all print statements use `safe_print()`
2. Verify all file writes use `encoding='utf-8'`
3. Add missing unicode chars to replacement dict
4. Check Windows console code page (should be 65001/UTF-8)

### Agent Spawning Issues
1. Verify complexity calculation is working
2. Check role max_children limits aren't too restrictive
3. Ensure depth doesn't exceed max_depth (10)
4. Review agent role hierarchy (ARCHITECT → DEVELOPER → BUILDER → TESTER)

## Testing Strategy

No automated test suite, but validate changes with:
```bash
# Simple build (fast, ~10 seconds)
python run_factory.py "Create a hello world CLI tool"

# Medium build (moderate, ~30 seconds)
python run_factory.py --spec examples/specs/simple_api.md

# Complex build (slow, minutes)
python run_factory.py --spec examples/specs/gui_project_spec.md
```

Check output:
- Files created in `output/` directory
- No exceptions in logs
- Metadata shows success status
- Generated README is coherent

## Integration Points

### SOVEREIGN Integration
If `../THE_ORCHESTRATOR/` exists:
- ImportManager switches to INTEGRATED mode
- Full agent consciousness capabilities
- Neural pattern learning
- Multi-paradigm orchestration
- Access to APEX systems (SPARK, LAB, FORGE)

### External Systems
- No external dependencies at runtime
- Optional: THE_ORCHESTRATOR for advanced features
- Optional: LBOF for bulk orchestration
- Standalone mode works without any external systems

## Key Architectural Insights

1. **Graceful Degradation**: System always works, capability varies by mode
2. **Recursive Spawning**: 1 orchestrator → 10 architects → 80 builders → 240 testers (capped at 200)
3. **Complexity-Based Scaling**: Auto-determines agents/strategy from project complexity
4. **Zero Hard Dependencies**: Core functionality works with Python stdlib only
5. **Async-First**: All builds use asyncio for parallel execution
6. **Checkpoint-Driven**: Resume from any phase failure
7. **Self-Contained**: Entire system is a portable folder
