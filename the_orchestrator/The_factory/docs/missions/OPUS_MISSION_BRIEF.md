# 🎯 OPUS MISSION BRIEF: THE FACTORY - PRODUCTION HARDENING

**MISSION:** Transform The Factory from prototype to production-ready standalone system with guaranteed stringency and bulletproof error handling.

**CONTEXT:** You are Opus running in Claude Code CLI. You have full access to file operations, code generation, and execution. This is a complete architectural redesign and implementation mission.

**CRITICAL:** This system must work standalone (without THE_ORCHESTRATOR), handle all errors gracefully, and GUARANTEE output quality. No shortcuts on stringency.

---

## 📋 EXECUTIVE SUMMARY

**Current State:** The Factory is a meta-orchestration system with excellent vision but incomplete implementation:
- Only ~30% implemented (mostly simulation)
- Hard dependency on THE_ORCHESTRATOR (will fail standalone)
- Minimal error handling (crashes on first problem)
- No validation of outputs
- No recovery mechanisms

**Target State:** Production-ready standalone system that:
- Runs completely standalone (no external dependencies)
- Handles all errors with retry, fallback, and recovery
- Validates all inputs and outputs
- Guarantees stringency (correct output or fail explicitly with recovery options)
- Can resume from failures
- Works in both standalone and integrated modes

**Your Task:**
1. Make architectural decisions (see CRITICAL DECISION POINTS below)
2. Implement complete error handling infrastructure
3. Create fallback implementations for standalone mode
4. Fix all bootstrap files to work standalone
5. Validate the entire system works end-to-end

---

## 🗂️ REQUIRED CONTEXT - READ THESE FILES IN ORDER

**Read these files to understand current state** (read in this order for token efficiency):

### Phase 1: Understanding the Vision (READ THESE)
1. `the_factory/previous_conversation_claude_cli.md` - Full history and original intent
2. `the_factory/README.md` - System architecture overview
3. `the_factory/SYSTEM_LLM.md` - Complete capability matrix

### Phase 2: Current Implementation (READ THESE)
4. `the_factory/bootstrap/genesis_prime.py` - Main orchestrator (CRITICAL GAPS HERE)
5. `the_factory/bootstrap/chain_reactor.py` - Agent spawning (NO ERROR HANDLING)
6. `the_factory/bootstrap/sovereign_loader.py` - Dependency loader (FAILS STANDALONE)
7. `the_factory/make_standalone.py` - Standalone setup (INCOMPLETE)

### Phase 3: Analysis (CREATED FOR YOU - READ THIS)
8. **`the_factory/DETAILED_ANALYSIS.md`** ← I'm creating this next, contains:
   - Complete gap analysis
   - All missing error handling points
   - Architectural problems
   - Detailed implementation requirements
   - Validation points needed

**Token Optimization:** After reading Phase 1-2, you can use `Grep` and `Read` with offsets for specific sections rather than re-reading entire files.

---

## 🎯 CRITICAL DECISION POINTS

You must make these architectural decisions and document them:

### DECISION 1: Standalone Architecture Strategy

**Choose ONE approach and justify:**

**Option A: Full SOVEREIGN Integration**
```yaml
Approach: Copy all SOVEREIGN code into lib/
Pros:
  - Complete functionality (all paradigms available)
  - Proven, tested code
  - No reimplementation needed
Cons:
  - Heavy (~50+ files, several MB)
  - Maintenance burden (duplicate code)
  - Updates from THE_ORCHESTRATOR require manual sync
Size: ~50-70 files
Complexity: Low implementation, high maintenance
```

**Option B: Lightweight Custom Implementation**
```yaml
Approach: Build minimal orchestrator from scratch
Pros:
  - Lightweight (<100KB)
  - Full control
  - Easy maintenance
  - No external dependencies
Cons:
  - Must reimplement functionality
  - Missing advanced paradigms
  - More testing needed
Size: ~5-10 files
Complexity: High implementation, low maintenance
```

**Option C: Hybrid Approach (RECOMMENDED by Sonnet)**
```yaml
Approach: Minimal core + optional SOVEREIGN
Pros:
  - Works standalone (minimal core)
  - Enhanced when SOVEREIGN available
  - Fallback cascade: SOVEREIGN → Simple → Minimal
  - Balanced complexity
Cons:
  - Must maintain two code paths
  - More complex logic for mode detection
Size: ~20-25 files
Complexity: Medium both ways
```

**YOUR DECISION:** [Document here which you choose and why]

**Rationale:** [Explain trade-offs and why this is optimal]

---

### DECISION 2: Error Handling Strategy

**Choose recovery strategy granularity:**

**Option A: Per-Operation Recovery**
```python
# Every operation wrapped
result = recovery_manager.execute_with_retry(
    operation=lambda: spawn_agent(...),
    max_retries=3
)
```
- Pros: Granular control, precise recovery
- Cons: Verbose, many try-catch blocks

**Option B: Phase-Level Recovery**
```python
# Each phase (analysis, architecture, build) wrapped
result = recovery_manager.execute_phase(
    phase=AnalysisPhase(...),
    fallback=SimplifiedAnalysis
)
```
- Pros: Cleaner code, natural boundaries
- Cons: Less granular recovery

**YOUR DECISION:** [Document here]

---

### DECISION 3: Validation Strategy

**Choose when to validate:**

**Option A: Eager Validation (Validate Everything Immediately)**
- Validate inputs before every operation
- Catch errors early
- Cost: More validations, potentially redundant

**Option B: Lazy Validation (Validate at Phase Boundaries)**
- Validate at key checkpoints only
- Less overhead
- Risk: Errors detected later

**Option C: Hybrid (Validate Critical Paths Eagerly, Rest at Boundaries)**
- Balance of both

**YOUR DECISION:** [Document here]

---

## 🏗️ IMPLEMENTATION CHECKLIST

Complete these in order. Check off as you complete:

### PHASE 1: FOUNDATION (CRITICAL - Must Complete)

- [ ] **Decision Documentation**
  - Document all architectural decisions above
  - Create `the_factory/ARCHITECTURE_DECISIONS.md`
  - Justify each choice with reasoning

- [ ] **Create Error Handling Infrastructure**
  - [ ] `lib/error_handling/__init__.py`
  - [ ] `lib/error_handling/recovery_manager.py`
    - Retry with exponential backoff
    - Fallback cascade
    - Circuit breaker integration
  - [ ] `lib/error_handling/validation_engine.py`
    - Pre-condition validation
    - Post-condition validation
    - Output quality validation
    - Schema validation
  - [ ] `lib/error_handling/circuit_breaker.py`
    - State machine (closed/open/half-open)
    - Failure threshold tracking
    - Auto-reset logic
  - [ ] `lib/error_handling/retry_logic.py`
    - Exponential backoff
    - Jitter for distributed systems
    - Max retry configuration

- [ ] **Create Fallback Implementations**
  - [ ] `lib/fallback_implementations/__init__.py`
  - [ ] `lib/fallback_implementations/simple_orchestrator.py`
    - Minimal orchestrator (no SOVEREIGN dependency)
    - Sequential task execution
    - Basic agent management
  - [ ] `lib/fallback_implementations/simple_agent.py`
    - Basic agent implementation
    - Task execution
    - Result collection
  - [ ] `lib/fallback_implementations/mock_neural.py`
    - Mock neural overlay (when real unavailable)
    - In-memory pattern storage
    - No persistence required

- [ ] **Create State Management**
  - [ ] `lib/state_management/__init__.py`
  - [ ] `lib/state_management/checkpoint_manager.py`
    - Save state after each phase
    - Load from checkpoint
    - Rollback capability
    - State validation
  - [ ] `lib/state_management/progress_tracker.py`
    - Track agent status
    - Calculate progress percentage
    - ETA estimation
    - Report generation

- [ ] **Create Import Manager**
  - [ ] `bootstrap/import_manager.py`
    - Auto-detect standalone vs integrated mode
    - Dynamic import with fallback cascade
    - Dependency verification
    - Configuration management
  - [ ] Test both modes work

### PHASE 2: CORE FIXES (CRITICAL)

- [ ] **Fix genesis_prime.py**
  - [ ] Replace hard-coded imports (line 19-30) with import_manager
  - [ ] Add ValidationEngine integration:
    - Validate spec before parsing (line 90-96)
    - Validate parsed spec (line 98-135)
    - Validate strategy (line 235-276)
  - [ ] Add RecoveryManager integration:
    - Wrap spawn_chain_reaction with retry
    - Add checkpoint saves after each phase
    - Add progress tracking
  - [ ] Add error handling:
    - Try-catch around parse_specification
    - Try-catch around spawn_chain_reaction
    - Try-catch around generate_output_structure
    - Fallback to SimpleOrchestrator if SOVEREIGN fails
  - [ ] Fix simulate_agent_work (line 381-400):
    - Actually spawn agents (if SOVEREIGN available)
    - OR use SimpleOrchestrator (if standalone)
    - Add timeout protection
    - Validate output

- [ ] **Fix chain_reactor.py**
  - [ ] Add error handling in _propagate_chain (line 224-296):
    - Timeout protection
    - Deadlock detection
    - Memory monitoring
  - [ ] Add validation in spawn_agent (line 191-222):
    - Validate role is valid
    - Check task has required fields
    - Post-spawn verification
  - [ ] Add validation in _execute_agent_task (line 388-405):
    - Validate task before execution
    - Timeout for long-running tasks
    - Validate output
  - [ ] Add CircuitBreaker integration:
    - Prevent cascading failures
    - Stop spawning if too many failures

- [ ] **Fix sovereign_loader.py**
  - [ ] Add critical module verification (line 31-58)
  - [ ] Add fallback when modules missing
  - [ ] Fix create_orchestrator (line 217-241):
    - Add fallback to SimpleOrchestrator
    - Validate orchestrator creation
  - [ ] Add mode detection:
    - Check if lib/ exists → standalone
    - Check if THE_ORCHESTRATOR exists → integrated
    - Fail gracefully if neither

- [ ] **Fix make_standalone.py**
  - [ ] Update imports in copied files automatically
  - [ ] Fix sys.path.insert statements to use lib/
  - [ ] Create all __init__.py files
  - [ ] Verify dependencies after copying
  - [ ] Generate import_manager configuration
  - [ ] Test standalone mode works

### PHASE 3: VALIDATION & TESTING

- [ ] **Create Test Suite**
  - [ ] `tests/__init__.py`
  - [ ] `tests/test_error_handling.py`
    - Test retry logic
    - Test fallback cascade
    - Test circuit breaker
  - [ ] `tests/test_validation.py`
    - Test pre-condition validation
    - Test post-condition validation
    - Test output validation
  - [ ] `tests/test_import_manager.py`
    - Test standalone mode detection
    - Test integrated mode detection
    - Test fallback imports
  - [ ] `tests/test_genesis_prime.py`
    - Test spec parsing
    - Test strategy determination
    - Test build process
  - [ ] `tests/test_chain_reactor.py`
    - Test agent spawning
    - Test chain propagation
    - Test error recovery
  - [ ] `tests/test_standalone_mode.py`
    - Test full build in standalone
    - Test fallback orchestrator
  - [ ] `tests/test_integrated_mode.py`
    - Test with SOVEREIGN available

- [ ] **Integration Testing**
  - [ ] Test simple project end-to-end
  - [ ] Test with intentional failures (verify recovery)
  - [ ] Test checkpoint resume
  - [ ] Test both standalone and integrated modes

### PHASE 4: DOCUMENTATION & FINALIZATION

- [ ] **Update Documentation**
  - [ ] Update `README.md` with new architecture
  - [ ] Update `STANDALONE_SETUP.md` with correct instructions
  - [ ] Create `ARCHITECTURE_DECISIONS.md` with all decisions
  - [ ] Create `ERROR_HANDLING_GUIDE.md` for users
  - [ ] Update `INSTRUCTIONS.md` for LLM usage

- [ ] **Create Example Specs**
  - [ ] Update `specs/example_todo_app.md`
  - [ ] Create `specs/example_simple.md` (minimal test case)
  - [ ] Create `specs/example_with_errors.md` (test error handling)

---

## ✅ SUCCESS CRITERIA

The mission is complete when ALL of these are true:

### Functional Requirements
- [ ] `python the_factory/make_standalone.py` completes successfully
- [ ] `python the_factory/bootstrap/genesis_prime.py --build` works in standalone mode
- [ ] System builds a simple project (todo app) successfully
- [ ] All tests pass (`pytest tests/`)
- [ ] No hard-coded dependencies on THE_ORCHESTRATOR paths

### Error Handling Requirements
- [ ] System recovers from network errors
- [ ] System recovers from import errors
- [ ] System recovers from agent failures
- [ ] Circuit breaker activates after repeated failures
- [ ] Retry logic works with exponential backoff
- [ ] Fallback cascade works (SOVEREIGN → Simple → Minimal)

### Validation Requirements
- [ ] All inputs validated before operations
- [ ] All outputs validated after operations
- [ ] Invalid specs rejected with clear error messages
- [ ] Generated code is valid (syntax check)
- [ ] Generated files actually created

### State Management Requirements
- [ ] Checkpoints saved after each phase
- [ ] Can resume from checkpoint after interruption
- [ ] Progress tracking shows current status
- [ ] Can rollback on failure

### Mode Detection Requirements
- [ ] Auto-detects standalone mode correctly
- [ ] Auto-detects integrated mode correctly
- [ ] Falls back gracefully when SOVEREIGN missing
- [ ] Works with lib/ dependencies
- [ ] Works with THE_ORCHESTRATOR dependencies

### Stringency Requirements
- [ ] System NEVER silently fails
- [ ] All errors logged with context
- [ ] User notified of all failures
- [ ] Recovery attempts documented
- [ ] Final output validated for quality

---

## 📊 VALIDATION PROTOCOL

After implementation, run this validation sequence:

```bash
# 1. Clean state
rm -rf the_factory/lib/
rm -rf the_factory/outputs/

# 2. Make standalone
cd the_factory
python make_standalone.py

# Expected output:
# ✅ Created lib directory
# ✅ All dependencies copied
# ✅ Imports updated
# ✅ Verification passed

# 3. Run tests
pytest tests/ -v

# Expected: All tests pass

# 4. Build simple project
python bootstrap/genesis_prime.py --build --spec specs/example_simple.md

# Expected output:
# ✅ Specification parsed
# ✅ Strategy determined
# ✅ Chain reaction completed
# ✅ Output validated
# ✅ Build complete

# 5. Verify output exists
ls -la outputs/project_root/
# Should contain generated project files

# 6. Test error recovery (intentional failure)
python bootstrap/genesis_prime.py --build --spec specs/example_with_errors.md

# Expected output:
# ⚠️ Error detected: [error message]
# 🔄 Retrying (attempt 1/3)...
# 🔄 Retrying (attempt 2/3)...
# 🔄 Fallback to SimpleOrchestrator
# ✅ Build complete (with fallback)

# 7. Test checkpoint resume
# (Interrupt build mid-way with Ctrl+C, then resume)
python bootstrap/genesis_prime.py --resume

# Expected output:
# 📂 Loading checkpoint
# ⏭️ Skipping completed phases
# ▶️ Resuming from Phase 3...
```

---

## 🚨 CRITICAL CONSTRAINTS

**MUST NOT:**
- Simplify error handling for "brevity" - full robustness required
- Skip validation steps - stringency is non-negotiable
- Leave hard-coded paths to THE_ORCHESTRATOR
- Assume operations succeed - validate everything
- Use print() for errors - use proper logging

**MUST:**
- Handle ALL possible failure modes
- Validate ALL inputs and outputs
- Provide fallbacks for ALL dependencies
- Log ALL errors with full context
- Test ALL error paths
- Document ALL architectural decisions

**Token Economy Note:**
- Be smart about file reading (use offsets, grep)
- But NEVER skip validation or error handling to save tokens
- If robustness requires more code, write more code
- Stringency > Brevity

---

## 📝 DELIVERABLES

When complete, provide:

1. **ARCHITECTURE_DECISIONS.md** - All decisions documented with rationale
2. **IMPLEMENTATION_SUMMARY.md** - What was built, how it works
3. **All new files** - Complete implementations
4. **Updated bootstrap files** - All fixes applied
5. **Test suite** - All tests passing
6. **Validation report** - Results of validation protocol
7. **User guide update** - Updated instructions

---

## 🔧 TOOLS & APPROACH

**Available Tools:**
- `Read` - Read files (use offsets for large files)
- `Write` - Create new files
- `Edit` - Modify existing files
- `Glob` - Find files by pattern
- `Grep` - Search code
- `Bash` - Run commands (tests, validation)
- `Task` - Spawn sub-agents if needed (for complex searches)

**Recommended Approach:**

1. **READ PHASE** (30 min):
   - Read files in order specified above
   - Read `DETAILED_ANALYSIS.md` (I'm creating next) thoroughly
   - Build mental model of system

2. **DECISION PHASE** (1-2 hours):
   - Make all architectural decisions
   - Document rationale
   - Create `ARCHITECTURE_DECISIONS.md`

3. **IMPLEMENTATION PHASE** (12-20 hours):
   - Work through checklist systematically
   - Test as you go
   - Use TodoWrite to track progress

4. **VALIDATION PHASE** (2-4 hours):
   - Run full validation protocol
   - Fix any issues found
   - Ensure all success criteria met

5. **DOCUMENTATION PHASE** (1-2 hours):
   - Update all documentation
   - Create implementation summary
   - Provide handoff report

---

## 🎯 START HERE

**Your first actions should be:**

1. Read the required context files (listed above)
2. Read `DETAILED_ANALYSIS.md` (comprehensive analysis by Sonnet)
3. Create and use TodoWrite to track the checklist
4. Make architectural decisions and document them
5. Begin PHASE 1: FOUNDATION

**Question anything unclear.** Better to ask than assume.

**This is a production system.** Quality and robustness are paramount.

---

**MISSION STATUS:** Ready to begin
**AWAITING:** Your architectural decisions and implementation

Good luck! This is a significant engineering effort, but the foundation is solid and the requirements are clear. Focus on stringency and robustness above all else.
