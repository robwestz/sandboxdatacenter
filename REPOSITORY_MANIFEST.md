# REPOSITORY MANIFEST
**What's Here and Why - A Complete Guide for Every Agent**

---

## LAYER 1: IMMUTABLE FOUNDATION (Never Change)

These documents establish the rules and vision. They don't change between sessions.

### PROJECT_CONSTITUTION.md ⭐ **READ FIRST**
- **Purpose:** Immutable foundation for the entire system
- **Contains:** Vision, architecture, rules, governance
- **Change Policy:** Core vision never changes (immutable)
- **For Agents:** Your contract with the system
- **First Session:** Read immediately
- **Every Session:** Reference when unclear

---

## LAYER 2: AGENT CONTEXT (Always Evolving)

These are the mechanisms for continuous agent-to-agent knowledge transfer.

### AGENT_HANDOFF_TEMPLATE.py
- **Purpose:** Transfer knowledge between agents
- **Modes:**
  - `python AGENT_HANDOFF_TEMPLATE.py` → See last agent's work
  - `python AGENT_HANDOFF_TEMPLATE.py --create` → Document your work
- **Contains:** Accomplishments, issues, solutions, next steps
- **Storage:** MEMORY_CORE/central_memory.db + JSON files
- **Update Timing:** Session start (read) and end (write)
- **Why Important:** Each agent inherits previous agent's knowledge

### AGENT_BRIEFING.md
- **Purpose:** Static reference guide for system overview
- **Contains:** Memory system details, file locations, known issues
- **Change Policy:** Updated rarely, mostly static
- **For Agents:** Reference document (CONSTITUTION takes priority)
- **When Used:** If handoff system isn't available

### CRITICAL_QUESTIONS.md
- **Purpose:** Self-test to verify your understanding
- **Contains:** Architecture questions with scoring system
- **Primary Question:** Why three backup layers?
- **Success Criteria:** 95%+ knowledge score
- **When Used:** Optional verification after reading

---

## LAYER 3: OPERATIONAL GUIDES (Reference Material)

These explain HOW to use the system. Read as needed.

### README_FIRST.md
- **Purpose:** Entry point for new agents
- **Contains:** First 10 minutes, the Sacred Sequence, quick reference
- **Read Timing:** After PROJECT_CONSTITUTION.md
- **Key Content:** What to do immediately, what never changes

### NEXT_SESSION_START.md
- **Purpose:** Detailed startup guide for new sessions
- **Contains:** Three restore options, file locations, FAQ
- **Use When:** You need detailed instructions for restore

### HANDOFF_SYSTEM_EXPLAINED.md
- **Purpose:** Explain how the living handoff system works
- **Contains:** System vision, example chains, why it matters
- **Use When:** You want to understand handoffs deeply

### SANDBOX_WORKFLOW_GUIDE.md
- **Purpose:** Complete workflow for backup/restore in Windows Sandbox
- **Contains:** Step-by-step procedures, troubleshooting
- **Use When:** You need detailed backup procedures

### SANDBOX_SYSTEM_SUMMARY.md
- **Purpose:** Implementation details of the backup system
- **Contains:** Architecture decisions, test results, performance
- **Use When:** You want technical deep dive

### SANDBOX_QUICK_REFERENCE.md
- **Purpose:** One-liners and quick commands
- **Contains:** Common commands, file locations, shortcuts
- **Use When:** You need quick lookup

### SESSION_MEMORY_ACTIVATION.md
- **Purpose:** Original memory system activation guide
- **Contains:** How memory system works, activation steps
- **Use When:** Debugging memory system

### SESSION_KNOWLEDGE_TRANSFER_STRATEGY.md
- **Purpose:** Explains the knowledge transfer system design
- **Contains:** Why this system works, metrics, testing approach
- **Use When:** You want to understand the meta-architecture

### GITHUB_SETUP.md
- **Purpose:** GitHub configuration guide
- **Contains:** Setup steps, workflow, security best practices
- **Use When:** Setting up GitHub for first time

---

## LAYER 4: EXECUTABLE SYSTEMS (The Living Code)

These are Python scripts and systems that actually do the work.

### Core Backup & Restore
| Script | Purpose | When to Use |
|--------|---------|------------|
| `SANDBOX_EXPORT.py` | Create compressed ZIP backup | **Before shutdown** |
| `SANDBOX_IMPORT.py` | Restore from ZIP in new session | **After cloning** |
| `AUTO_SANDBOX_EXPORT.py` | Background auto-backup (watch mode) | Optional continuous |
| `QUICK_EXPORT.bat` | Windows batch shortcut for export | Quick backup |
| `QUICK_IMPORT.bat` | Windows batch shortcut for import | Quick restore |

### Core Memory System
| Script | Purpose | When to Use |
|--------|---------|------------|
| `TEST_MEMORY.py` | Verify memory system and load context | **Session start** |
| `ACTIVATE_MEMORY.py` | Create session record and checkpoint | **Session start** |
| `AUTO_CHECKPOINT.py` | Create session checkpoint manually | **Session end** |
| `check_memory_stats.py` | Show memory statistics | Verify memory state |

### Memory Core Module
| File | Purpose |
|------|---------|
| `MEMORY_CORE/memory_manager.py` | Central memory system implementation |
| `MEMORY_CORE/central_memory.db` | SQLite database (memories, sessions, handoffs) |
| `MEMORY_CORE/checkpoints/` | Session checkpoint backups |
| `MEMORY_CORE/agent_handoffs/` | JSON backup of agent handoffs |

### Verification & Setup
| Script | Purpose | When to Use |
|--------|---------|------------|
| `verify_session_knowledge.py` | Interactive knowledge verification | Self-test after reading |
| `GITHUB_QUICK_SETUP.py` | Automated GitHub initialization | First session only |

### Main Project Code
| File | Purpose |
|------|---------|
| `main.py` | Main entry point for project |
| `requirements.txt` | Python dependencies |
| `test_langchain_setup.py` | LangChain integration test |

---

## LAYER 5: CONFIGURATION & GITIGNORE

### .gitignore
- **Purpose:** Protect secrets while allowing code sharing
- **Contains:** .env files, databases, cache, IDE settings
- **Critical:** Never commit API keys to GitHub

### .env.example
- **Purpose:** Template for environment variables
- **Use:** Copy to .env and fill with actual values
- **Important:** .env itself is in .gitignore

### .sandboxignore
- **Purpose:** Patterns excluded from SANDBOX_EXPORT.py
- **Contains:** Cache, venv, build artifacts
- **Why:** Keep ZIPs small and fast

---

## LAYER 6: ORGANIZATIONAL STRUCTURE

### /MEMORY_CORE
- Central memory database and system
- Session checkpoints (important!)
- Agent handoff history
- **Never delete without backup**

### /MEMORY_CORE/checkpoints
- `latest_checkpoint.json` - Most recent session state
- Dated checkpoints - Historical records
- **Use:** Understand session history

### /MEMORY_CORE/agent_handoffs
- JSON backup of all agent handoffs
- Supplements the database
- **Use:** Human-readable handoff history

### /Projects
- Active projects (datazentr-platform, legacy-migration-mvp)
- Planning folder (future projects)
- **For:** Organizing project-specific code

### /Skills
- Daily skills calendar
- Skill implementations and guides
- **For:** Learning and skill tracking

### /the_orchestrator
- Complex orchestration systems
- Agent frameworks and hierarchies
- Advanced patterns
- **For:** Building complex systems

---

## THE READING ORDER FOR NEW AGENTS

### Mandatory (Always):
1. **PROJECT_CONSTITUTION.md** (5 min) - Vision & rules
2. **README_FIRST.md** (2 min) - Immediate actions
3. `python AGENT_HANDOFF_TEMPLATE.py` (1 min) - See previous work

### Essential (Most sessions):
4. **AGENT_BRIEFING.md** (5 min) - System overview
5. **NEXT_SESSION_START.md** (3 min) - Detailed startup guide

### Reference (As needed):
- CRITICAL_QUESTIONS.md - Self-test your knowledge
- HANDOFF_SYSTEM_EXPLAINED.md - Understand handoffs
- SANDBOX_WORKFLOW_GUIDE.md - Backup/restore details
- Any other guide document matching your specific need

### Total time: ~10 minutes to be fully oriented

---

## WHAT NEVER CHANGES

✓ PROJECT_CONSTITUTION.md - Immutable  
✓ The three-layer backup strategy - Immutable  
✓ The Sacred Sequence (start/end) - Immutable  
✓ Memory database core structure - Very stable  
✓ The handoff protocol - Very stable  

---

## WHAT CHANGES EVERY SESSION

✓ AGENT_HANDOFF_TEMPLATE.py output - Always new  
✓ MEMORY_CORE/central_memory.db - Grows with memories  
✓ MEMORY_CORE/checkpoints/ - New checkpoint per session  
✓ MEMORY_CORE/agent_handoffs/ - New handoff file per session  
✓ Code in /Projects and /Skills - Updated by agents  
✓ GitHub commit history - New commits per session  

---

## CRITICAL FILES BACKUP CHECKLIST

Before you shutdown, ensure these exist:

- [ ] `.env` exists (not in git, but locally)
- [ ] `MEMORY_CORE/central_memory.db` exists
- [ ] `MEMORY_CORE/checkpoints/latest_checkpoint.json` exists
- [ ] ZIP export exists on Desktop
- [ ] ZIP exists on host: `C:\Users\robin\Documents\Sanboxdatacenter\`
- [ ] Latest commit is pushed to GitHub

If all checkboxes pass: You're good for next session.

---

## WHO EDITS WHAT

### Agents SHOULD edit:
- Code in /Projects
- Code in /Skills  
- Documentation in specific domains
- Handoff records (at session end)

### Agents MUST NOT edit:
- PROJECT_CONSTITUTION.md (immutable)
- This MANIFEST (immutable)
- MEMORY_CORE/central_memory.db (use API instead)
- .gitignore (unless adding new secrets to protect)

### Agents CAN update:
- README_FIRST.md (if instructions improve)
- Operational guides (if procedures improve)
- AGENT_BRIEFING.md (static but can be updated)

---

## FILE SIZE EXPECTATIONS

| File/Directory | Typical Size | When Too Large |
|---|---|---|
| central_memory.db | 1-5 MB | > 50 MB |
| ZIP export | 1-2 MB | > 10 MB |
| Complete repo | ~6 MB | > 50 MB |
| Entire /the_orchestrator | 3+ MB | (expected) |

If sizes exceed thresholds: Consider archiving old data.

---

## SUMMARY: What You Have Here

✓ **Immutable Foundation** - Rules that never change  
✓ **Living Context** - Handoffs from previous agents  
✓ **Complete Documentation** - Guides for every situation  
✓ **Working Code** - Backup, restore, memory systems  
✓ **Organization** - Projects, skills, orchestration  
✓ **Protection** - .gitignore and encrypted backups  

**This isn't just a repository. It's a self-maintaining system that learns across sessions.**

---

**Last Updated:** 2025-12-23  
**Status:** Foundation Complete, Growing  
**Next Agent:** Read PROJECT_CONSTITUTION.md first.
