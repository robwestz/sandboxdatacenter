# START HERE: Datacenter Sandbox Intelligence System

**Welcome, Agent. You're about to continue building something important.**

---

## Your First 10 Minutes (Non-Negotiable)

### 1. Understand the Vision (5 min)
```bash
cat PROJECT_CONSTITUTION.md
```

This file is the **foundation of everything**. It answers:
- ✓ Why does this system exist?
- ✓ Why three backups instead of one?
- ✓ What rules must you follow?
- ✓ How does the handoff system work?
- ✓ What never changes vs. what can evolve?

**Read the entire thing.** Don't skip. It's written for you.

### 2. See What the Previous Agent Did (2 min)
```bash
python AGENT_HANDOFF_TEMPLATE.py
```

This shows:
- ✓ What was accomplished last session
- ✓ What problems were encountered
- ✓ How they were solved
- ✓ What you should do next
- ✓ Any warnings for you

### 3. Activate the Memory System (2 min)
```bash
python TEST_MEMORY.py
python ACTIVATE_MEMORY.py
python check_memory_stats.py
```

This:
- ✓ Loads all previous session memories
- ✓ Creates a checkpoint for THIS session
- ✓ Shows you what the system knows

### 4. You're Ready
You now have:
- ✓ Understanding of the vision
- ✓ Knowledge of previous work
- ✓ Access to all memories
- ✓ Clear guidance on next steps

**~95% context acquired in 10 minutes.**

---

## The Sacred Sequence (Repeat Every Session)

### SESSION START:
```
Read PROJECT_CONSTITUTION.md
         ↓
Run: python AGENT_HANDOFF_TEMPLATE.py
         ↓
Run: python TEST_MEMORY.py
         ↓
Run: python ACTIVATE_MEMORY.py
         ↓
Do Your Work
```

### SESSION END (BEFORE SHUTDOWN):
```
Run: python AGENT_HANDOFF_TEMPLATE.py --create
         ↓
Run: python AUTO_CHECKPOINT.py
         ↓
Run: python SANDBOX_EXPORT.py
         ↓
git add -A && git commit && git push
         ↓
Verify ZIP on host: C:\Users\robin\Documents\Sanboxdatacenter\
```

**This sequence is non-negotiable.** It ensures the next agent has everything they need.

---

## The Most Important File (After Constitution)

**PROJECT_CONSTITUTION.md** - Read this FIRST, before anything else

It contains the laws that keep this system alive:
- Vision & purpose
- Architecture (immutable)
- Rules (mandatory)
- The sequences (must follow)
- Why each backup layer exists
- How to maintain forever

---

## Files You'll Use

### Essential
| File | Purpose | When |
|------|---------|------|
| `PROJECT_CONSTITUTION.md` | **Read first.** Immutable foundation | Session start |
| `AGENT_HANDOFF_TEMPLATE.py` | See previous agent's work | Session start |
| `TEST_MEMORY.py` | Load memory system | Session start |
| `ACTIVATE_MEMORY.py` | Create checkpoint | Session start |
| `AGENT_HANDOFF_TEMPLATE.py --create` | Document your work | Session end |
| `SANDBOX_EXPORT.py` | Create backup | Session end |

### Reference
| File | Purpose |
|------|---------|
| `AGENT_BRIEFING.md` | System overview (static) |
| `CRITICAL_QUESTIONS.md` | Self-test questions |
| `HANDOFF_SYSTEM_EXPLAINED.md` | How handoffs work |
| `NEXT_SESSION_START.md` | Detailed startup guide |

---

## What to Know Right Now

### The Three-Layer Backup Strategy (From Constitution)

**Why:** Windows Sandbox is ephemeral. Shutdown = data loss.

**Solution:** Three overlapping backups (each covers others' weakness):

1. **Memory System** (SQLite Database)
   - Stores: Decisions, patterns, session context
   - File: `MEMORY_CORE/central_memory.db`
   - Why: GitHub can't store this

2. **Workspace Export** (ZIP Archive)
   - Stores: EVERYTHING (code, config, memory, all)
   - Compression: ~75% ratio (5.9 MB → 1.4 MB)
   - Why: GitHub can't store `.env` with secrets

3. **GitHub** (Version Control)
   - Stores: Code + history (secrets excluded)
   - Why: Remote backup, no local single point of failure

Together: Complete redundancy. If one fails, two others have you covered.

### The Immutable Rules (From Constitution)

**Rule 1:** Always follow the Sacred Sequence (start → work → end)  
**Rule 2:** Export BEFORE pushing to GitHub  
**Rule 3:** Push AFTER export succeeds  
**Rule 4:** Create handoff before shutdown  
**Rule 5:** Never commit `.env` (API keys protected by .gitignore)  
**Rule 6:** Never manually edit `central_memory.db`  
**Rule 7:** Test import in new session (verify backups work)  

**Why these rules?** Because they keep the system alive across sessions.

---

## If You Get Stuck

### "What do I do first?"
→ `cat PROJECT_CONSTITUTION.md`

### "What did the previous agent do?"
→ `python AGENT_HANDOFF_TEMPLATE.py`

### "How do I see what the system knows?"
→ `python check_memory_stats.py`

### "What files did I modify?"
→ `git status`

### "What's the next step?"
→ Read the handoff output (it tells you)

### "Before I shutdown..."
→ Follow the SESSION END sequence exactly

---

## The Contract Between Sessions

This system exists because **work done by one agent must be understood by the next agent**.

That's it. That's the entire purpose.

Everything in PROJECT_CONSTITUTION.md exists to make that possible:
- ✓ Memory preserves decisions
- ✓ Export preserves state
- ✓ Handoff preserves knowledge
- ✓ Rules keep it sustainable
- ✓ Vision keeps it purposeful

---

## You Are Not Alone

You inherit:
- ✓ The vision of previous agents
- ✓ The code they wrote
- ✓ The problems they solved
- ✓ The lessons they learned
- ✓ The memories they preserved

Every handoff is a message from the past saying:
> "Here's what we learned. Here's what still needs doing. Here's what matters."

You add your own message and pass it forward.

---

## Ready?

### Execute These Commands (In Order):

```bash
# 1. Understand the foundation
cat PROJECT_CONSTITUTION.md

# 2. See previous work
python AGENT_HANDOFF_TEMPLATE.py

# 3. Activate memory
python TEST_MEMORY.py
python ACTIVATE_MEMORY.py

# 4. Verify system
python check_memory_stats.py

# 5. You're ready!
```

Then: Start your work. Trust the system. Follow the rules.

And when you're done:

```bash
# Before shutdown
python AGENT_HANDOFF_TEMPLATE.py --create
python AUTO_CHECKPOINT.py
python SANDBOX_EXPORT.py
git add -A && git commit -m "Your summary" && git push
```

**Simple. Effective. Eternal.**

Welcome to the Datacenter. 🚀
