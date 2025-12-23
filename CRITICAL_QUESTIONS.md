# CRITICAL VERIFICATION QUESTIONS
**For testing if a new agent has ~95% session knowledge**

These are not trivia questions - they test ARCHITECTURAL UNDERSTANDING that proves an agent has internalized this session's work.

---

## PRIMARY VERIFICATION QUESTION (Must Pass)

### Question: Why Does This System Use THREE Backup Layers?

**Setup:** You're working in Windows Sandbox on the Datacenter project. You've made critical progress - added new memories, modified core scripts, updated documentation. The sandbox is about to be shut down. You have three backup options:

1. **ZIP Export** (`python SANDBOX_EXPORT.py`) → Creates file on Desktop
2. **GitHub Push** (`git push`) → Pushes to robwestz/sandboxdatacenter
3. **Host File-Sharing** → Copy to C:\Users\robin\Documents\Sanboxdatacenter\

**Question:** Why would using ONLY GitHub be insufficient? What does the ZIP provide that GitHub cannot? When would host file-sharing save you?

---

## CORRECT ANSWER (95%+ Knowledge)

**Full correct answer includes:**

### 1. Windows Sandbox Ephemeral Nature
- [ ] Windows Sandbox state is lost on shutdown
- [ ] Working directory volatile unless backed up
- [ ] Need complete workspace preservation, not just code

### 2. What ZIP Provides That GitHub Doesn't
- [ ] Captures ALL files: code, config, memory database, checkpoints
- [ ] Includes `.env` with API keys (never pushed to GitHub)
- [ ] Includes `MEMORY_CORE/` directory with session context
- [ ] Includes non-git-tracked files (IDE settings, test artifacts, etc)
- [ ] Complete binary integrity via SHA-256 checksum
- [ ] Compression: ~75% ratio (5.9 MB → 1.43 MB)

### 3. Why GitHub Alone Fails
- [ ] Can't contain `.env` (security) - stored in `.gitignore`
- [ ] Can't contain `MEMORY_CORE/central_memory.db` - not tracked
- [ ] Can't contain `MEMORY_CORE/checkpoints/` - not tracked
- [ ] So: Cloning from GitHub gets code but LOSES all session context
- [ ] Without memory database, previous memories are gone
- [ ] Without checkpoints, session history is lost

### 4. What Host File-Sharing Solves
- [ ] Copy-paste may be disabled (security restriction)
- [ ] File-sharing usually works even when copy-paste disabled
- [ ] Can share test reports, large files host ↔ sandbox
- [ ] Acts as manual transfer mechanism if network fails

### 5. Complete Backup Strategy
```
BEFORE SHUTDOWN:
  1. python AUTO_CHECKPOINT.py                # Save checkpoint
  2. python SANDBOX_EXPORT.py                 # Compressed ZIP (1-5 sec)
  3. git add -A && git commit && git push     # Push changes (5-30 sec)
  4. (optional) Copy reports to C:\Users\robin\Documents\...

NEXT SESSION:
  Option A - Full Restoration:
    - Copy ZIP from Desktop → sandbox
    - python SANDBOX_IMPORT.py                # Restores everything
    - python TEST_MEMORY.py                   # Verify memories loaded
  
  Option B - Code Only (requires Git):
    - git clone https://github.com/robwestz/...
    - python TEST_MEMORY.py                   # Loads from central_memory.db
    - (loses any uncommitted work since last git push)
  
  Option C - Hybrid (Best Safety):
    - python SANDBOX_IMPORT.py                # Use ZIP
    - git pull origin master                  # Get latest code
    - python TEST_MEMORY.py                   # All context preserved
```

### 6. Why Each Layer Is Critical
- **ZIP:** Guarantees complete workspace preservation + memory context
- **GitHub:** Enables collaboration, version history, remote backup
- **Host File-Sharing:** Fallback when network/transfer issues occur

**If full sandbox lost:** ZIP on host can restore everything  
**If host storage lost:** GitHub has code history  
**If both lost:** You still have dev machine copy + GitHub remote  

---

## SECONDARY VERIFICATION QUESTIONS (Should Also Know)

### Q2: GitHub GH007 Error

**Scenario:** You run `git push -u origin master` and get:
```
error: GH007: Your push would publish a private email address
! [remote rejected] master -> master (push declined due to email privacy restrictions)
```

**Question:** 
1. Why does this happen?
2. What's the COMPLETE fix (all 3 steps)?
3. Why is `git config user.email` alone insufficient?

**Expected Answer:**
1. GitHub privacy settings + commit author metadata doesn't match private email config
2. Fix:
   ```bash
   git config user.email "robwestz@users.noreply.github.com"
   git commit --amend --author="Robin West <robwestz@users.noreply.github.com>" --no-edit
   git push -u origin master --force
   ```
3. Because git commit already has author metadata embedded in the commit object. Config alone affects new commits, not existing ones. `--amend` rewrites the commit object with new author. `--force` replaces remote history.

---

### Q3: Memory System Architecture

**Question:** After importing workspace from ZIP, how does memory context restore? Walk through:
1. Where is memory stored?
2. How does import restore it?
3. What if `MEMORY_CORE/central_memory.db` was deleted before export?

**Expected Answer:**
1. SQLite database at `MEMORY_CORE/central_memory.db` + checkpoints in `MEMORY_CORE/checkpoints/`
2. `SANDBOX_IMPORT.py` extracts entire `.zip` → restores directory structure including `MEMORY_CORE/`
3. Memories are gone (they're only in the database). But checkpoints are restored, allowing context reinit.

---

### Q4: Windows Encoding Issue

**Question:** A developer runs `SANDBOX_EXPORT.py` and gets:
```
UnicodeEncodeError: 'charmap' codec can't encode characters in position 0-75: 
character maps to <undefined>
```

Why? How was it fixed?

**Expected Answer:**
- Windows Sandbox console uses cp1252 encoding, not UTF-8
- Box-drawing characters and emoji can't encode in cp1252
- Fixed by: Adding `sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')` at script start
- Only affects console output; file I/O unaffected

---

### Q5: Startup Sequence

**Question:** After `python SANDBOX_IMPORT.py` completes, what 3 commands would you run to verify the system is functional?

**Expected Answer:**
```bash
python TEST_MEMORY.py           # Verify memories loaded from DB
python check_memory_stats.py    # Show session/memory counts
python ACTIVATE_MEMORY.py       # Activate current session
```

Why in this order: Verify existing context → Check stats → Create new session entry

---

## KNOWLEDGE SCORING

| Question | Correct = | Weight |
|----------|-----------|--------|
| Q1 (Three-layer strategy) | Full answer with all 6 parts | 40% |
| Q2 (GH007 error) | All 3 steps + explanation | 30% |
| Q3 (Memory restoration) | Explains DB + checkpoints + loss scenario | 15% |
| Q4 (Unicode issue) | Identifies cp1252 → UTF-8 fix | 10% |
| Q5 (Startup sequence) | Correct order + timing | 5% |

**Score Calculation:**
- 100% correct on Q1 = 40 points
- 100% correct on Q2 = 30 points
- etc.
- **95%+ total = Agent has sufficient knowledge to continue**
- **<80% total = Agent should read AGENT_BRIEFING.md + documentation**

---

## HOW TO USE THIS FILE

### For New Agent in Next Session:
```bash
# 1. Clone repo
git clone https://github.com/robwestz/sandboxdatacenter.git
cd sandboxdatacenter

# 2. Read briefing
cat AGENT_BRIEFING.md

# 3. Self-test with this file
cat CRITICAL_QUESTIONS.md

# 4. Run verification
python verify_session_knowledge.py

# 5. If score >= 95%: Ready to work!
python TEST_MEMORY.py
python ACTIVATE_MEMORY.py
```

### For Human User:
Use PRIMARY VERIFICATION QUESTION as litmus test. If agent answers it well, they're ready to continue development.

---

## SUCCESS METRIC

**An agent who can correctly answer the PRIMARY VERIFICATION QUESTION has:**
- ✓ Understood the system architecture
- ✓ Internalized why each component exists
- ✓ Can make intelligent decisions about backups
- ✓ Can troubleshoot issues independently
- ✓ ~95% of this session's knowledge in one question

**If they can ALSO answer Q2-Q5:** They're ready for ANY task continuation without additional context.
