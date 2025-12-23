#!/usr/bin/env python3
"""
SESSION KNOWLEDGE VERIFICATION
Verifies that an agent has sufficient knowledge of the Datacenter system architecture.

This script provides:
1. System status overview
2. Critical architecture questions for knowledge verification
3. Quick setup validation

Run this in a new session after cloning to verify you're ready to continue work.
"""

import os
import sys
import sqlite3
from datetime import datetime
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    width = 70
    print("\n" + "=" * width)
    print(f" {text}")
    print("=" * width)

def print_section(text):
    """Print section header"""
    print(f"\n[*] {text}")
    print("-" * 70)

def check_git_status():
    """Check if we're in a git repository with correct remote"""
    try:
        import subprocess
        result = subprocess.run(
            ['git', 'remote', '-v'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if 'robwestz/sandboxdatacenter' in result.stdout:
            return True, result.stdout.strip()
        return False, "Wrong remote or not configured"
    except Exception as e:
        return False, str(e)

def check_memory_system():
    """Check memory system database"""
    db_path = Path('MEMORY_CORE/central_memory.db')
    
    if not db_path.exists():
        return False, "Memory database not found"
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Get session count
        sessions = cursor.execute("SELECT COUNT(*) FROM sessions").fetchone()
        memories = cursor.execute("SELECT COUNT(*) FROM memories").fetchone()
        checkpoints = cursor.execute(
            "SELECT COUNT(*) FROM checkpoints"
        ).fetchone()
        
        conn.close()
        
        return True, {
            'sessions': sessions[0] if sessions else 0,
            'memories': memories[0] if memories else 0,
            'checkpoints': checkpoints[0] if checkpoints else 0
        }
    except Exception as e:
        return False, f"Database error: {str(e)}"

def check_files_exist():
    """Check critical files exist"""
    critical_files = [
        'SANDBOX_EXPORT.py',
        'SANDBOX_IMPORT.py',
        'TEST_MEMORY.py',
        'ACTIVATE_MEMORY.py',
        'AGENT_BRIEFING.md',
        '.gitignore',
        'MEMORY_CORE/memory_manager.py',
        'MEMORY_CORE/central_memory.db',
    ]
    
    found = []
    missing = []
    
    for file in critical_files:
        if Path(file).exists():
            found.append(file)
        else:
            missing.append(file)
    
    return found, missing

def verify_agent_knowledge():
    """
    Ask critical architecture questions to verify agent understanding.
    These questions test 95% of session knowledge without reading entire repo.
    """
    print_header("ARCHITECTURE KNOWLEDGE VERIFICATION")
    
    questions = [
        {
            'id': 1,
            'title': 'Three-Layer Backup Strategy',
            'prompt': """
Question: Why does this system use THREE backup layers (Sandbox Export ZIP, 
GitHub, Host File-Sharing) instead of just one?

Expected answer should cover:
- Windows Sandbox is ephemeral (state lost on shutdown)
- ZIP export captures COMPLETE workspace including non-git-tracked files
- GitHub provides remote + version control but can't store .env/secrets
- Host file-sharing is workaround for copy-paste limitations
- Each layer serves different purpose

Rate your understanding (1-5): """,
            'weight': 40  # 40% of knowledge score
        },
        {
            'id': 2,
            'title': 'GitHub GH007 Error Fix',
            'prompt': """
Question: You try to push to GitHub and get:
  "error: GH007: Your push would publish a private email address"

What is the COMPLETE fix and why each step matters?

Expected answer should cover:
- Problem: GitHub privacy settings + wrong commit author
- Step 1: git config user.email "robwestz@users.noreply.github.com"
- Step 2: git commit --amend --author="Robin West <...>" 
- Step 3: git push -u origin master --force
- Why step 2: Author metadata in git object itself, config alone insufficient
- Why --force: Rewriting history with correct author

Rate your understanding (1-5): """,
            'weight': 30  # 30% of knowledge score
        },
        {
            'id': 3,
            'title': 'Memory System Persistence',
            'prompt': """
Question: How does the memory system preserve context across sandbox 
sessions? What files are involved?

Expected answer should cover:
- SQLite database at MEMORY_CORE/central_memory.db
- Checkpoint files in MEMORY_CORE/checkpoints/
- Export → Import cycle restores entire MEMORY_CORE directory
- Checkpoints contain session_id, timestamp, context
- Latest checkpoint is used for context restoration
- .gitkeep files preserve directory structure in git

Rate your understanding (1-5): """,
            'weight': 20  # 20% of knowledge score
        },
        {
            'id': 4,
            'title': 'Critical Startup Sequence',
            'prompt': """
Question: After importing the workspace in a new sandbox session, 
what is the correct sequence of commands to verify everything is working?

Expected answer should be:
1. python TEST_MEMORY.py          # Load previous memories
2. python check_memory_stats.py   # Verify stats
3. python ACTIVATE_MEMORY.py      # Activate current session
4. python AUTO_CHECKPOINT.py      # Create checkpoint

Why important: Validates memory persistence, creates new checkpoint,
ensures context is loaded before doing new work.

Rate your understanding (1-5): """,
            'weight': 10  # 10% of knowledge score
        },
    ]
    
    scores = []
    
    for q in questions:
        print_section(f"Q{q['id']}: {q['title']} (Weight: {q['weight']}%)")
        print(q['prompt'])
        
        try:
            response = input("Your rating: ").strip()
            score = int(response)
            if 1 <= score <= 5:
                scores.append((score, q['weight']))
            else:
                print("Invalid rating. Assuming 0.")
                scores.append((0, q['weight']))
        except ValueError:
            print("Invalid input. Assuming 0.")
            scores.append((0, q['weight']))
    
    # Calculate weighted score
    total_weight = sum(w for _, w in scores)
    weighted_sum = sum(s * w for s, w in scores)
    final_score = (weighted_sum / (total_weight * 5)) * 100 if total_weight > 0 else 0
    
    return final_score

def main():
    """Main verification flow"""
    print_header("SESSION KNOWLEDGE VERIFICATION")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Working directory: {os.getcwd()}")
    
    # Check 1: Git status
    print_section("Check 1: Git Repository")
    git_ok, git_info = check_git_status()
    if git_ok:
        print("[OK] Correct GitHub remote configured")
        print(git_info)
    else:
        print(f"[WARN] Git check failed: {git_info}")
    
    # Check 2: Memory system
    print_section("Check 2: Memory System")
    mem_ok, mem_info = check_memory_system()
    if mem_ok:
        print(f"[OK] Memory database found")
        print(f"    - Sessions: {mem_info['sessions']}")
        print(f"    - Memories: {mem_info['memories']}")
        print(f"    - Checkpoints: {mem_info['checkpoints']}")
    else:
        print(f"[WARN] Memory system check: {mem_info}")
    
    # Check 3: Critical files
    print_section("Check 3: Critical Files")
    found, missing = check_files_exist()
    print(f"[OK] Found {len(found)}/{len(found)+len(missing)} critical files")
    if missing:
        print("[WARN] Missing files:")
        for f in missing:
            print(f"  - {f}")
    
    # Check 4: Knowledge verification
    print_section("Check 4: Architecture Knowledge")
    print("\nPlease answer the following questions to verify your knowledge")
    print("of the system architecture. Be honest - this helps measure")
    print("whether you have sufficient context to continue development.\n")
    
    knowledge_score = verify_agent_knowledge()
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    print(f"\nKnowledge Score: {knowledge_score:.1f}%")
    print("\nInterpretation:")
    if knowledge_score >= 95:
        print("  [OK] EXCELLENT - You have sufficient knowledge to continue")
        print("       Can safely resume development without reading entire repo")
    elif knowledge_score >= 80:
        print("  [OK] GOOD - You have solid understanding")
        print("       Review AGENT_BRIEFING.md for details")
    elif knowledge_score >= 60:
        print("  [WARN] FAIR - You should review AGENT_BRIEFING.md carefully")
        print("         Consider reading key documentation files")
    else:
        print("  [FAIL] INSUFFICIENT - Please read AGENT_BRIEFING.md completely")
        print("         Then review SANDBOX_SYSTEM_SUMMARY.md")
        print("         Then review SANDBOX_WORKFLOW_GUIDE.md")
    
    print("\n" + "=" * 70)
    print("Next steps:")
    print("  1. If score >= 80%: Ready to start work")
    print("     python TEST_MEMORY.py")
    print("     python ACTIVATE_MEMORY.py")
    print("\n  2. Before shutdown: ALWAYS run")
    print("     python SANDBOX_EXPORT.py")
    print("     git add -A && git commit -m '...' && git push")
    print("\n" + "=" * 70 + "\n")
    
    return 0 if knowledge_score >= 80 else 1

if __name__ == '__main__':
    sys.exit(main())
