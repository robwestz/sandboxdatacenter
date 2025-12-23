# PROJECT CONSTITUTION - Datacenter Sandbox Intelligence System

**Established:** 2025-12-23  
**Status:** Immutable Foundation (Updated by core vision only, never by session agents)  
**Last Review:** 2025-12-23

---

## PART I: PROJECT VISION & PURPOSE

### What We Are Building

A **living, self-aware development environment** that survives across Windows Sandbox sessions through intelligent memory persistence, automated backups, and continuous agent-to-agent knowledge transfer.

The Datacenter is not just code—it's a **system that learns and preserves context** across multiple AI agents working in ephemeral environments.

### Core Problem We Solve

Windows Sandbox is **ephemeral by design**:
- State is lost on shutdown
- Each new session starts blank
- Context knowledge disappears
- Developers must re-familiarize themselves

**Our Solution:** A three-layer preservation system:
1. **Memory System** - Persistent SQLite database with session checkpoints
2. **Workspace Backup** - ZIP-based complete workspace preservation (75% compression)
3. **Version Control** - GitHub for code history and remote backup
4. **Handoff Chain** - Agent-to-agent knowledge transfer through living records

### Success Criteria

✓ Zero data loss between sessions  
✓ New agents can continue work in < 10 minutes  
✓ Full context preservation (code, config, memories, decisions)  
✓ Knowledge compounds (each agent improves understanding)  
✓ System is self-maintaining (no manual intervention needed)

---

## PART II: SYSTEM ARCHITECTURE (IMMUTABLE DESIGN)

### The Three-Layer Backup Strategy

**Layer 1: Memory System** (Primary for context)
- Location: `MEMORY_CORE/central_memory.db` (SQLite3)
- Purpose: Store patterns, skills, session context, decisions
- Persistence: Survives sandboxes via export/import
- Status: Always active, always growing

**Layer 2: Sandbox Export** (Primary for workspace)
- Format: ZIP with DEFLATE compression (level 9)
- Compression: ~75% ratio typical
- Contents: 383+ files, code, config, memory database, everything except cache
- Integrity: SHA-256 checksums for verification
- Backup location: C:\Users\robin\Documents\Sanboxdatacenter\ (host)
- Timing: **ALWAYS** before sandbox shutdown

**Layer 3: GitHub** (Secondary + version control)
- Repository: https://github.com/robwestz/sandboxdatacenter.git
- Branch: master
- Protection: .gitignore keeps .env and secrets safe
- Purpose: Remote backup, code history, collaboration
- Sync: After every session (commit + push)

**Layer 4: Host File-Sharing** (Emergency fallback)
- Purpose: Works when copy-paste is disabled
- Use case: Transfer files when primary methods fail
- Location: C:\Users\robin\Documents\ shared folder

### Why Each Layer Is Essential

**Memory alone ≠ enough**
- Only stores .env (excluded from git) and database
- Doesn't capture config files
- Doesn't preserve binary state

**Export alone ≠ enough**
- Needs to be pushed to host (file-sharing has limits)
- No version history
- No remote redundancy

**GitHub alone ≠ enough**
- Can't store .env with API keys (security violation)
- Can't store MEMORY_CORE database (not versioned)
- Loses uncommitted work

**All three together = Robust**
- Export captures everything (code + memory + config)
- GitHub provides history + remote safety
- Host file-sharing is emergency fallback
- Each layer covers others' weaknesses

---

## PART III: AGENT HANDOFF PROTOCOL (IMMUTABLE RULES)

### Session Start (Every Agent, Every Time)

**Non-Negotiable Sequence:**

1. **Clone or Import**
   ```bash
   # Either:
   git clone https://github.com/robwestz/sandboxdatacenter.git
   # OR:
   python SANDBOX_IMPORT.py
   ```

2. **See Foundation (This Document)**
   - Read: PROJECT_CONSTITUTION.md
   - Understand: Vision, architecture, rules

3. **See Latest Handoff**
   ```bash
   python AGENT_HANDOFF_TEMPLATE.py
   # Shows what previous agent did, issues, solutions, next steps
   ```

4. **Activate Memory**
   ```bash
   python TEST_MEMORY.py
   python ACTIVATE_MEMORY.py
   python check_memory_stats.py
   ```

5. **Work with Understanding**
   - You inherit full context
   - You know the rules
   - You understand where we're going

### Session End (Every Agent, Every Time)

**Non-Negotiable Sequence:**

1. **Create Handoff**
   ```bash
   python AGENT_HANDOFF_TEMPLATE.py --create
   # Document:
   # - What YOU accomplished
   # - Issues YOU encountered
   # - Solutions YOU applied
   # - Next steps for NEXT agent
   # - Code changes YOU made
   # - Warnings for NEXT agent
   ```

2. **Save Checkpoint**
   ```bash
   python AUTO_CHECKPOINT.py
   ```

3. **Create Backup**
   ```bash
   python SANDBOX_EXPORT.py
   # Creates dated ZIP on Desktop
   ```

4. **Push to GitHub**
   ```bash
   git add -A
   git commit -m "Session end: [your summary]"
   git push origin master
   ```

5. **Verify on Host**
   - Check: C:\Users\robin\Documents\Sanboxdatacenter\ has ZIP
   - Check: GitHub shows new commit

**If Any Step Fails:**
- Do NOT shutdown sandbox
- Troubleshoot step by step
- Last handoff will still guide next agent
- But missing backup is risk

---

## PART IV: ARCHITECTURAL PRINCIPLES (IMMUTABLE)

### Memory System Philosophy

**Principle 1: Memory is Sacred**
- Never delete memories without explicit reason
- Memories compound value over time
- Bad memories (failures) are valuable too
- Store WHY, not just WHAT

**Principle 2: Handoffs Are Living History**
- Each agent's handoff is permanent record
- Handoffs show project evolution
- Can analyze patterns across sessions
- Next agent learns from all previous agents

**Principle 3: Context Must be Continuous**
- No agent should start from scratch
- Every session builds on previous knowledge
- New agent starts at where last agent ended
- Progress is additive, never reset

### Backup Philosophy

**Principle 4: Three Backups Are Better Than One**
- Single backup = single point of failure
- Three layers = overlapping redundancy
- Export fails? GitHub has the code
- GitHub down? Host has the ZIP
- Host inaccessible? Memory DB in export

**Principle 5: Backup Timing is Non-Negotiable**
- Export BEFORE shutdown (not "when you remember")
- Push AFTER export succeeds
- This order is mandatory
- First failure stops shutdown

**Principle 6: Know What You're Protecting**
- Export includes: Code + config + memory + everything
- GitHub includes: Code + history (secrets excluded)
- Memory includes: Decisions + patterns + context
- Host includes: Emergency files
- **Together:** Complete project state

### Code Evolution Philosophy

**Principle 7: Breaking Changes Need Justification**
- Architecture is set (three-layer backup)
- Can't remove export system without replacement
- Can't change memory DB schema without migration
- Large changes need handoff explanation

**Principle 8: Improvements Should Be Additive**
- New agents add features
- Don't remove working systems
- Deprecate thoughtfully with warnings
- Document why you changed something

**Principle 9: Backward Compatibility Matters**
- Old ZIPs should still import
- Old memory records should still work
- Old checkpoints should still load
- Test this before you commit

---

## PART V: MAINTENANCE RULES (IMMUTABLE GUARDRAILS)

### Rules Every Agent Must Follow

**Rule 1: The Export-Push Sequence**
```
Modify Code
    ↓
Test Locally
    ↓
Commit to Git
    ↓
Run AUTO_CHECKPOINT.py (save session)
    ↓
Run SANDBOX_EXPORT.py (create ZIP)
    ↓
git push origin master (push to GitHub)
    ↓
Verify ZIP on host (C:\Users\robin\Documents\Sanboxdatacenter\)
```

**Rule 2: Never Skip Handoff**
- Not "optional" if running out of time
- 2 minutes to document is worth it
- Next agent needs to understand your work
- Write minimum: accomplishments + next steps

**Rule 3: .gitignore is Sacred**
- Never commit .env (has API keys)
- Never commit MEMORY_CORE/central_memory.db directly
- Never commit IDE-specific settings
- Check: `git status` before pushing
- Principle: Protect secrets, always

**Rule 4: Memory Database Integrity**
- Never manually edit central_memory.db
- Use: `python ACTIVATE_MEMORY.py` to add sessions
- Use: `memory.remember()` to add memories
- Trust the system, don't hack it

**Rule 5: Checkpoint Before Major Changes**
- About to refactor something big?
- Run: `python AUTO_CHECKPOINT.py` first
- This creates a savepoint
- Next agent can see what you changed

**Rule 6: Test Import After Export**
- Export works ≠ import will work
- Before next session: Ideally test
- If can't test: Run verify script in new session
- Verify: `python verify_session_knowledge.py`

**Rule 7: Keep Files Small**
- Memory DB: Should stay < 50MB (it's SQLite)
- ZIPs: Should compress to < 5MB (current: ~1.4MB)
- If growing: Consider archiving old checkpoints
- Alert: Document if crossing thresholds

**Rule 8: Version the Documentation**
- This constitution: Immutable (never change)
- AGENT_BRIEFING.md: Static reference (rarely changes)
- Handoffs: Living records (always changing)
- Know which is which

---

## PART VI: PROJECT GOVERNANCE (WHO DECIDES WHAT)

### What Can Never Change

- **This Document** (PROJECT_CONSTITUTION.md)
- **The Three-Layer Backup Strategy**
- **The Export-Push Sequence**
- **The Memory System Core**
- **The Handoff Protocol**

These are the foundation. They survive all sessions.

### What Can Change (With Justification)

- Specific file locations (with migration path)
- Implementation details (if backward compatible)
- Tool versions (document the change)
- Compression ratios (if performance improves)
- New features (if they don't break existing systems)

### What Should Change Often

- Specific handoff content (what agents did)
- Memory records (new learnings)
- Code in specific domains
- Documentation examples
- Test coverage

### What Requires Explicit Decision

- Removing any backup layer
- Changing database schema
- Altering the commit structure
- Switching version control
- Abandoning memory system

---

## PART VII: ONBOARDING ANY NEW AGENT

### The Three Questions Every Agent Must Answer

**Question 1: Why Three Backups?**
> "Explain why GitHub alone is insufficient. What does ZIP provide that GitHub cannot? When would host file-sharing save you?"

Correct answer shows understanding of the architecture.

**Question 2: What's Your First Task?**
> "On session start, what must you do before writing any code?"

Correct answer: Read constitution, see handoff, activate memory.

**Question 3: What's Your Last Task?**
> "Before shutdown, what's the sequence and why does order matter?"

Correct answer: Checkpoint → Export → Push, in that order.

### Expected Knowledge Path

1. **Minute 1:** Read PROJECT_CONSTITUTION.md (this)
2. **Minute 2:** Run AGENT_HANDOFF_TEMPLATE.py (see context)
3. **Minute 3:** Read recommended next steps from handoff
4. **Minute 4:** Run TEST_MEMORY.py and ACTIVATE_MEMORY.py
5. **Minute 5:** Ready to work

At this point, agent has:
- ✓ Vision and purpose
- ✓ Architecture understanding  
- ✓ Rules and guidelines
- ✓ Previous agent's context
- ✓ Memory system activated

**Knowledge: ~95% of what's needed**

---

## PART VIII: EVOLUTION & CONTINUOUS IMPROVEMENT

### How the System Grows

**Session 1:**
- Foundation laid (this document)
- First agent creates first handoff
- First backup created

**Session 2:**
- New agent reads constitution + first handoff
- Inherits knowledge, adds more
- Creates second handoff (more detailed)

**Session 3-N:**
- Each agent reads constitution + all previous handoffs
- Understands full evolution
- Adds their contribution
- System knowledge compounds

### Metrics That Matter

Over time, you can analyze:
- How long does onboarding take? (Should decrease)
- How many issues recur? (Should decrease)
- How large are handoffs? (Should be consistent)
- How many times is export needed? (Should always be 1)
- Code stability: (Should increase)

### Sustainability Check

Every agent should ask:
- "Can a new agent understand my work?"
- "Did I document why, not just what?"
- "Are my changes backward compatible?"
- "Would I trust this if I were the next agent?"

If answer is yes to all four: You've succeeded.

---

## FINAL PRINCIPLE: Why This Matters

The Datacenter isn't just about backing up files. It's about **preserving knowledge** in a system where the execution environment is ephemeral.

Every decision in this constitution exists to answer one question:

> **How do we ensure that work done by Agent A is fully understood and continued by Agent B?**

And the answer is:
1. **Memory** - Store decisions and patterns
2. **Exports** - Preserve complete state
3. **Handoffs** - Transfer knowledge explicitly
4. **Rules** - Make system behavior predictable
5. **Constitution** - Keep the vision alive

This is the difference between code that's backed up and **a system that learns**.

---

## Quick Reference: The Sacred Sequence

```
EVERY SESSION START:
  1. Read this (PROJECT_CONSTITUTION.md)
  2. Run: python AGENT_HANDOFF_TEMPLATE.py
  3. Run: python TEST_MEMORY.py
  4. Run: python ACTIVATE_MEMORY.py
  → Ready to work

EVERY SESSION END:
  1. Run: python AGENT_HANDOFF_TEMPLATE.py --create
  2. Run: python AUTO_CHECKPOINT.py
  3. Run: python SANDBOX_EXPORT.py
  4. Run: git add -A && git commit && git push
  → Ready for next agent
```

**This sequence, in this order, every session, forever.**

---

**End of PROJECT_CONSTITUTION.md**

*This document is the foundation. All other documents (briefings, handoffs, guides) are built on top of this. Don't change this without explicit reason. Don't ignore this to save time. Don't work around this for convenience.*

*This is the contract between sessions. Honor it.*
