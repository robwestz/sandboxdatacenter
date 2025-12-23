# 🚀 START HERE - OPUS IMPLEMENTATION GUIDE

**You are Opus. This is your entry point.**

---

## ⚡ 30-SECOND OVERVIEW

**Mission:** Transform The Factory from prototype to production-ready
**Timeline:** 15-25 hours of implementation
**Deliverable:** Standalone, robust, validated system

**Current State:** ~30% working (mostly simulation)
**Target State:** 100% production-ready with full error handling

---

## 📖 READING ORDER (First 30 Minutes)

Read these files in EXACTLY this order for optimal token usage:

### 1. **OPUS_MISSION_BRIEF.md** (5 min)
**Purpose:** Complete mission overview, decisions to make, checklist
**Key sections:**
- Executive summary
- Critical decision points
- Implementation checklist
- Success criteria

### 2. **DETAILED_ANALYSIS.md** (15 min)
**Purpose:** Technical deep-dive, all bugs and gaps identified
**Key sections:**
- Critical problems (bugs to fix)
- Missing validation points
- Required new files
- Testing requirements

### 3. **QUICK_REFERENCE.md** (5 min)
**Purpose:** Quick lookup during implementation
**Use:** Keep open for reference while coding

### 4. **Current Implementation** (5 min - skim only)
Skim these to understand structure (don't read in detail):
- `bootstrap/genesis_prime.py` - Main orchestrator
- `bootstrap/chain_reactor.py` - Agent spawning
- `bootstrap/sovereign_loader.py` - Dependency loader

**You'll read these in detail as you fix them.**

---

## 🎯 YOUR FIRST TASKS (Next 2 Hours)

### Step 1: Create TodoWrite Tracker (5 min)
```python
# Use TodoWrite to track entire mission
todos = [
    {"content": "Make architectural decisions", "status": "in_progress"},
    {"content": "Create error handling infrastructure", "status": "pending"},
    # ... rest of checklist from OPUS_MISSION_BRIEF.md
]
```

### Step 2: Make Architectural Decisions (1-2 hours)
**Read:** OPUS_MISSION_BRIEF.md section "CRITICAL DECISION POINTS"

**Make these decisions:**

1. **Standalone Architecture:** A, B, or C?
   - Option C (Hybrid) recommended but you decide
   - Document rationale

2. **Error Handling Strategy:** Per-operation or phase-level?
   - Consider trade-offs
   - Document choice

3. **Validation Strategy:** Eager, lazy, or hybrid?
   - Balance thoroughness vs performance
   - Document approach

**Create:** `ARCHITECTURE_DECISIONS.md` documenting all decisions

### Step 3: Begin Implementation (rest of time)
**Follow:** OPUS_MISSION_BRIEF.md "IMPLEMENTATION CHECKLIST"

**Order:**
1. Error handling infrastructure (CRITICAL)
2. Fallback implementations (CRITICAL)
3. Import manager (CRITICAL)
4. Fix bootstrap files (CRITICAL)
5. Tests and validation

---

## 🎪 WORKFLOW EXAMPLE

```bash
# 1. Read mission files
Read OPUS_MISSION_BRIEF.md
Read DETAILED_ANALYSIS.md
Read QUICK_REFERENCE.md

# 2. Create todo tracker
TodoWrite(todos=[...])

# 3. Make decisions
Write ARCHITECTURE_DECISIONS.md

# 4. Start implementing
mkdir -p lib/error_handling
Write lib/error_handling/recovery_manager.py
Write lib/error_handling/validation_engine.py
# etc...

# 5. Test as you go
Bash pytest tests/test_recovery_manager.py

# 6. Update todos
TodoWrite(todos=[...])  # Mark completed

# 7. Continue through checklist
```

---

## 🚨 CRITICAL CONSTRAINTS

**MUST DO:**
- Validate ALL inputs and outputs
- Handle ALL error cases
- Provide fallbacks for ALL dependencies
- Test ALL code paths
- Document ALL decisions

**MUST NOT:**
- Skip validation for "brevity"
- Assume operations succeed
- Leave hard-coded paths
- Ignore error cases
- Use bare `except:`

**STRINGENCY > EVERYTHING**
If correct error handling requires more code, write more code.
If validation requires more checks, add more checks.

---

## 💡 DECISION-MAKING FRAMEWORK

When facing choices, optimize for:
1. **Robustness** (handles errors gracefully)
2. **Stringency** (validates correctness)
3. **Maintainability** (clear, simple code)
4. **Simplicity** (fewer moving parts)
5. **Performance** (only if above are satisfied)

---

## 🎯 SUCCESS CHECKLIST

The mission succeeds when:

### Functional
- [ ] `make_standalone.py` creates working standalone system
- [ ] `genesis_prime.py --build` builds a project
- [ ] Generated output is valid and complete
- [ ] Works in both standalone and integrated modes

### Robustness
- [ ] Recovers from import errors
- [ ] Recovers from file errors
- [ ] Recovers from agent failures
- [ ] Retries with exponential backoff
- [ ] Falls back when primary fails
- [ ] Checkpoints and can resume

### Quality
- [ ] All tests pass
- [ ] No hard-coded paths
- [ ] All inputs validated
- [ ] All outputs validated
- [ ] Full error handling coverage
- [ ] Documented architecture decisions

---

## 📚 REFERENCE FILES

**For implementation:**
- OPUS_MISSION_BRIEF.md - Your main guide
- DETAILED_ANALYSIS.md - Technical details
- QUICK_REFERENCE.md - Quick lookups

**For context:**
- README.md - System overview
- SYSTEM_LLM.md - Capability matrix (what it SHOULD do)
- INSTRUCTIONS.md - LLM usage guide

**For understanding current code:**
- bootstrap/genesis_prime.py
- bootstrap/chain_reactor.py
- bootstrap/sovereign_loader.py
- make_standalone.py

---

## 🐛 IF YOU GET STUCK

**Problem:** Don't understand the vision
**Solution:** Read `README.md` and `SYSTEM_LLM.md`

**Problem:** Don't know what to implement
**Solution:** Re-read OPUS_MISSION_BRIEF.md checklist

**Problem:** Don't know how to fix a bug
**Solution:** Check DETAILED_ANALYSIS.md for that specific file

**Problem:** Need quick reference
**Solution:** Check QUICK_REFERENCE.md

**Problem:** Architectural uncertainty
**Solution:** Document both options in ARCHITECTURE_DECISIONS.md and choose

**Problem:** Tests failing
**Solution:** Check DETAILED_ANALYSIS.md testing requirements

---

## 💬 COMMUNICATION PROTOCOL

As you work:

1. **Update TodoWrite regularly** - Shows progress
2. **Document decisions** - In ARCHITECTURE_DECISIONS.md
3. **Log significant discoveries** - Create IMPLEMENTATION_NOTES.md
4. **Report blockers immediately** - Ask for guidance

---

## 🎓 GUIDING PRINCIPLES

```
┌─────────────────────────────────────┐
│  "Robustness over brevity"         │
│  "Validation over assumption"      │
│  "Explicit over implicit"          │
│  "Fail safe, not fail silent"     │
│  "Stringency is non-negotiable"   │
└─────────────────────────────────────┘
```

---

## ⚡ QUICK START COMMANDS

```bash
# Navigate to the factory
cd the_factory

# Verify current state
ls -la bootstrap/
ls -la lib/  # Might not exist yet

# Start mission
# 1. Read mission files (you are here)
# 2. Create todos
# 3. Make decisions
# 4. Implement
# 5. Test
# 6. Validate
# 7. Document
# 8. Deliver
```

---

## 🏁 YOU ARE READY

You now have everything needed to complete this mission:

✅ **Clear objective** - Production-ready standalone system
✅ **Complete analysis** - All problems identified
✅ **Detailed plan** - Step-by-step checklist
✅ **Reference materials** - Quick lookups available
✅ **Success criteria** - Clear definition of done
✅ **Quality standards** - Stringency requirements defined

**Next action:** Read OPUS_MISSION_BRIEF.md in detail

**Remember:** This is a significant engineering effort. Take time to understand before implementing. Quality over speed. Robustness over brevity.

**You've got this! 🚀**

---

*"The Factory builds builders. Your job is to ensure those builders are bulletproof."*
