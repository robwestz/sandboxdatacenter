# ⚡ QUICK REFERENCE - THE FACTORY

**For rapid lookup during implementation**

---

## 📂 FILE LOCATIONS

### Bootstrap Files (Need Fixing)
```
bootstrap/genesis_prime.py       - Lines 19-30: Hard imports, 381-400: Simulation
bootstrap/chain_reactor.py       - Lines 19: Hard imports, NO error handling
bootstrap/sovereign_loader.py    - Lines 15-16: Hard paths, 60-77: Partial error handling
make_standalone.py               - Lines 154-188: Doesn't fix imports
```

### New Files to Create
```
bootstrap/import_manager.py                      - Smart dependency resolution
lib/error_handling/recovery_manager.py           - Retry + fallback
lib/error_handling/validation_engine.py          - Input/output validation
lib/error_handling/circuit_breaker.py            - Prevent cascading failures
lib/error_handling/retry_logic.py                - Exponential backoff
lib/fallback_implementations/simple_orchestrator.py  - Standalone fallback
lib/fallback_implementations/simple_agent.py     - Basic agent
lib/fallback_implementations/mock_neural.py      - Neural fallback
lib/state_management/checkpoint_manager.py       - State persistence
lib/state_management/progress_tracker.py         - Progress tracking
```

---

## 🔴 CRITICAL BUGS TO FIX

### Bug #1: Hard-coded Imports
**Location:** genesis_prime.py:20, chain_reactor.py:19, sovereign_loader.py:15-16
**Problem:** Points to THE_ORCHESTRATOR even after make_standalone
**Fix:** Replace with ImportManager

### Bug #2: No Error Handling in chain_reactor
**Location:** Entire file
**Problem:** Any exception crashes system
**Fix:** Wrap all async operations with try-catch and recovery

### Bug #3: Simulation Not Implementation
**Location:** genesis_prime.py:381-400
**Problem:** Just sleeps and returns mock data
**Fix:** Actually spawn agents or use SimpleOrchestrator

### Bug #4: Import Failure Continues
**Location:** genesis_prime.py:23-30
**Problem:** Catches ImportError but continues without fallback
**Fix:** Set fallback orchestrator when imports fail

### Bug #5: No Output Validation
**Location:** genesis_prime.py:491-532
**Problem:** Never checks if output is valid
**Fix:** Add ValidationEngine checks

---

## 🎯 VALIDATION CHECKLIST

### Before Any Operation
- [ ] Input parameters not None
- [ ] Required fields present
- [ ] Values within valid ranges
- [ ] Resources available (memory, disk)

### After Any Operation
- [ ] Operation returned successfully
- [ ] Output is not None
- [ ] Output matches expected format
- [ ] Side effects occurred (files created, etc)

### Code Validation
```python
# Syntax check
compile(code, '<string>', 'exec')

# Format check
ast.parse(code)
```

### File Validation
```python
# Exists
path.exists()

# Not empty
path.stat().st_size > 0

# Writable
os.access(path, os.W_OK)
```

---

## 🔄 ERROR HANDLING PATTERNS

### Pattern 1: Retry with Backoff
```python
for attempt in range(max_retries):
    try:
        return await operation()
    except Exception as e:
        if attempt == max_retries - 1:
            raise
        await asyncio.sleep(2 ** attempt)
```

### Pattern 2: Fallback Cascade
```python
strategies = [primary, fallback1, fallback2]
for strategy in strategies:
    try:
        return await strategy()
    except Exception:
        continue
raise AllStrategiesFailedError()
```

### Pattern 3: Circuit Breaker
```python
if circuit_breaker.is_open():
    raise CircuitOpenError()

try:
    result = await operation()
    circuit_breaker.on_success()
    return result
except Exception:
    circuit_breaker.on_failure()
    raise
```

### Pattern 4: Timeout Protection
```python
try:
    return await asyncio.wait_for(operation(), timeout=300)
except asyncio.TimeoutError:
    raise OperationTimeoutError()
```

---

## 📝 IMPORT MANAGER LOGIC

```python
def detect_mode():
    # Check for lib/
    if (Path(__file__).parent.parent / "lib").exists():
        return "standalone"

    # Check for THE_ORCHESTRATOR
    if (Path(__file__).parent.parent.parent / "THE_ORCHESTRATOR").exists():
        return "integrated"

    return "minimal"

def get_orchestrator():
    mode = detect_mode()

    if mode == "integrated":
        try:
            from THE_ORCHESTRATOR.SOVEREIGN_AGENTS import TheSovereign
            return TheSovereign
        except ImportError:
            pass

    if mode == "standalone":
        try:
            from lib.SOVEREIGN_AGENTS import TheSovereign
            return TheSovereign
        except ImportError:
            pass

    # Fallback
    from lib.fallback_implementations import SimpleOrchestrator
    return SimpleOrchestrator
```

---

## 🏗️ SIMPLE ORCHESTRATOR INTERFACE

```python
class SimpleOrchestrator:
    async def build_project(self, spec, output_dir):
        # 1. Validate spec
        self.validator.validate_spec(spec)

        # 2. Create structure
        self.create_directory_structure(output_dir)

        # 3. Generate files
        files = self.generate_files(spec)

        # 4. Write files
        for path, content in files.items():
            self.write_file(path, content)

        # 5. Validate output
        self.validator.validate_output(output_dir)

        return {"status": "success", "output_dir": output_dir}
```

---

## 🧪 TEST COMMAND CHEATSHEET

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_recovery_manager.py -v

# Run with coverage
pytest tests/ --cov=lib --cov=bootstrap

# Run only failed tests
pytest --lf

# Run with detailed output
pytest -vv -s

# Test standalone mode
rm -rf lib/ && python make_standalone.py && pytest tests/test_standalone_mode.py
```

---

## 📊 VALIDATION PROTOCOL

```python
# Validate spec
assert spec.name
assert len(spec.features['core']) > 0
assert spec.complexity in ComplexityLevel

# Validate strategy
assert 1 <= strategy['num_agents'] <= 200
assert strategy['paradigm'] in VALID_PARADIGMS

# Validate output
assert output_dir.exists()
assert (output_dir / "README.md").exists()
assert (output_dir / "src").exists()
```

---

## 🚨 COMMON EXCEPTIONS

```python
class ValidationError(Exception):
    """Input or output validation failed"""

class RecoveryFailedError(Exception):
    """All recovery attempts failed"""

class CircuitOpenError(Exception):
    """Circuit breaker is open"""

class OperationTimeoutError(Exception):
    """Operation exceeded timeout"""

class OutputValidationError(ValidationError):
    """Output doesn't meet requirements"""

class CheckpointNotFoundError(Exception):
    """Checkpoint doesn't exist"""
```

---

## 💾 CHECKPOINT FORMAT

```json
{
  "checkpoint_id": "phase_2_architecture",
  "timestamp": "2025-12-10T15:30:00Z",
  "phase": "architecture",
  "spec": { "name": "...", "..." },
  "completed_phases": ["analysis"],
  "current_state": {
    "agents_spawned": 5,
    "artifacts": {"analysis": "..."}
  },
  "can_resume": true
}
```

---

## 🎯 SUCCESS INDICATORS

### System is Working When:
```bash
# Make standalone succeeds
python make_standalone.py
# Output: ✅ All dependencies copied

# Build succeeds
python bootstrap/genesis_prime.py --build
# Output: ✅ Build complete

# Tests pass
pytest tests/
# Output: All tests passed

# Output exists and is valid
ls outputs/project_root/
# Contains: README.md, src/, tests/, docs/
```

### System Has Issues When:
- ImportError from bootstrap files
- "Module not found" errors
- "Always success" in agent output (simulation)
- No files in outputs/
- Tests fail with AttributeError

---

## 🔧 DEBUGGING COMMANDS

```bash
# Check imports
python -c "from bootstrap.import_manager import ImportManager; print(ImportManager().detect_mode())"

# Check SOVEREIGN available
python -c "from lib.SOVEREIGN_AGENTS import TheSovereign; print('OK')"

# Check fallback available
python -c "from lib.fallback_implementations import SimpleOrchestrator; print('OK')"

# List checkpoints
ls -la checkpoints/

# Verify output structure
tree outputs/project_root/
```

---

## 📈 PROGRESS TRACKING

Use TodoWrite to track:
```python
todos = [
    {"content": "Create error handling infrastructure", "status": "in_progress"},
    {"content": "Fix genesis_prime.py imports", "status": "pending"},
    {"content": "Add validation to chain_reactor", "status": "pending"},
    # etc
]
```

---

## 🎓 PRINCIPLES TO REMEMBER

1. **Validate everything** - Never trust input or output
2. **Fail explicitly** - Better to crash with clear error than corrupt state
3. **Retry with backoff** - Transient failures are common
4. **Fallback gracefully** - Always have a simpler alternative
5. **Checkpoint frequently** - Enable resume from failure
6. **Timeout all operations** - Prevent hangs
7. **Log with context** - Debugging requires information
8. **Test both paths** - Happy path AND error path

---

This reference should speed up implementation by providing quick access to critical information without re-reading full files.
