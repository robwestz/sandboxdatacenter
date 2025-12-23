#!/usr/bin/env python3
"""
AGENT HANDOFF SYSTEM
Integrates with MEMORY_CORE to create living session context.

Each agent at session end creates a structured handoff that the NEXT agent reads.
This handoff contains:
- What THIS agent accomplished
- What was hard/failed (lessons learned)
- Current system state
- Recommended next steps
- Issues discovered
- Code changes made

Next agent reads this via memory system, making context truly continuous.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
import sys

# UTF-8 fix for Windows Sandbox
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class AgentHandoffManager:
    """Manages agent-to-agent knowledge transfer through memory system."""
    
    def __init__(self):
        self.db_path = Path('MEMORY_CORE/central_memory.db')
        self.handoff_dir = Path('MEMORY_CORE/agent_handoffs')
        self.handoff_dir.mkdir(exist_ok=True)
        
    def create_session_handoff(self, session_id: str, data: dict) -> bool:
        """
        Create a handoff record for next agent.
        
        Args:
            session_id: Current session ID
            data: Dict containing:
                - accomplishments: What was done
                - issues_encountered: Problems faced
                - solutions_applied: How they were solved
                - current_state: System status
                - next_steps: Recommendations
                - code_changes: Files modified
                - warnings: Critical info for next agent
        """
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Create handoff record
            handoff = {
                'session_id': session_id,
                'timestamp': datetime.now().isoformat(),
                'agent_id': data.get('agent_id', 'unknown'),
                'accomplishments': data.get('accomplishments', []),
                'issues_encountered': data.get('issues_encountered', []),
                'solutions_applied': data.get('solutions_applied', []),
                'current_state': data.get('current_state', {}),
                'next_steps': data.get('next_steps', []),
                'code_changes': data.get('code_changes', []),
                'warnings': data.get('warnings', []),
                'knowledge_score': data.get('knowledge_score', 0),  # From verification
                'test_results': data.get('test_results', {}),
            }
            
            # Store in handoffs table
            cursor.execute("""
                INSERT INTO handoffs 
                (session_id, timestamp, handoff_data)
                VALUES (?, ?, ?)
            """, (
                session_id,
                handoff['timestamp'],
                json.dumps(handoff, indent=2)
            ))
            
            # Save to JSON file too (backup)
            handoff_file = self.handoff_dir / f"handoff_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            handoff_file.write_text(json.dumps(handoff, indent=2))
            
            conn.commit()
            conn.close()
            
            return True
        except Exception as e:
            print(f"[ERROR] Failed to create handoff: {e}")
            return False
    
    def get_latest_handoff(self) -> dict:
        """Retrieve the most recent agent handoff."""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Get latest handoff
            cursor.execute("""
                SELECT handoff_data FROM handoffs 
                ORDER BY timestamp DESC 
                LIMIT 1
            """)
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return json.loads(result[0])
            return None
        except Exception as e:
            print(f"[ERROR] Failed to get latest handoff: {e}")
            return None
    
    def print_agent_briefing(self):
        """Print current state briefing for new agent."""
        print("\n" + "="*70)
        print("AGENT HANDOFF BRIEFING - Start Here!")
        print("="*70)
        
        handoff = self.get_latest_handoff()
        
        if not handoff:
            print("\n[INFO] No previous agent handoff found.")
            print("This appears to be the first session.")
            print("Read AGENT_BRIEFING.md for system overview.")
            return
        
        print(f"\nPrevious Agent Session:")
        print(f"  Session ID: {handoff['session_id']}")
        print(f"  Timestamp: {handoff['timestamp']}")
        print(f"  Agent: {handoff['agent_id']}")
        print(f"  Knowledge Score: {handoff['knowledge_score']}%")
        
        if handoff['accomplishments']:
            print(f"\n[ACCOMPLISHMENTS] What previous agent did:")
            for acc in handoff['accomplishments']:
                print(f"  ✓ {acc}")
        
        if handoff['issues_encountered']:
            print(f"\n[ISSUES ENCOUNTERED] Be aware of:")
            for issue in handoff['issues_encountered']:
                print(f"  ⚠️  {issue}")
        
        if handoff['solutions_applied']:
            print(f"\n[SOLUTIONS] Already applied:")
            for sol in handoff['solutions_applied']:
                print(f"  ✓ {sol}")
        
        if handoff['warnings']:
            print(f"\n[CRITICAL WARNINGS]")
            for warn in handoff['warnings']:
                print(f"  !!! {warn}")
        
        if handoff['next_steps']:
            print(f"\n[RECOMMENDED NEXT STEPS]")
            for i, step in enumerate(handoff['next_steps'], 1):
                print(f"  {i}. {step}")
        
        if handoff['code_changes']:
            print(f"\n[CODE CHANGES IN THIS SESSION]")
            print("  Files modified:")
            for change in handoff['code_changes']:
                print(f"    - {change}")
        
        print("\n" + "="*70)
        print("Ready to continue? Run: python TEST_MEMORY.py")
        print("="*70 + "\n")


def generate_handoff_at_session_end():
    """
    Call this when ending a session.
    Creates handoff record for next agent.
    """
    
    print("\n" + "="*70)
    print("CREATING AGENT HANDOFF FOR NEXT AGENT")
    print("="*70)
    
    manager = AgentHandoffManager()
    
    # Collect session data
    handoff_data = {
        'agent_id': input("\nAgent ID/Name (for records): ") or "Unknown",
        'accomplishments': [],
        'issues_encountered': [],
        'solutions_applied': [],
        'next_steps': [],
        'code_changes': [],
        'warnings': [],
        'current_state': {},
        'knowledge_score': int(input("Your knowledge score (0-100): ") or "80"),
    }
    
    print("\n[ACCOMPLISHMENTS] What did you complete?")
    print("(Enter each item, blank line to finish)")
    while True:
        item = input("  - ").strip()
        if not item:
            break
        handoff_data['accomplishments'].append(item)
    
    print("\n[ISSUES] Any problems encountered?")
    print("(Enter each, blank line to finish)")
    while True:
        item = input("  - ").strip()
        if not item:
            break
        handoff_data['issues_encountered'].append(item)
    
    print("\n[SOLUTIONS] How were they solved?")
    while True:
        item = input("  - ").strip()
        if not item:
            break
        handoff_data['solutions_applied'].append(item)
    
    print("\n[NEXT STEPS] What should next agent do?")
    while True:
        item = input("  - ").strip()
        if not item:
            break
        handoff_data['next_steps'].append(item)
    
    print("\n[FILES] Which files did you modify?")
    while True:
        item = input("  - ").strip()
        if not item:
            break
        handoff_data['code_changes'].append(item)
    
    print("\n[WARNINGS] Any critical info for next agent?")
    while True:
        item = input("  - ").strip()
        if not item:
            break
        handoff_data['warnings'].append(item)
    
    # Get current session ID from memory system
    try:
        conn = sqlite3.connect(str(manager.db_path))
        cursor = conn.cursor()
        session_id = cursor.execute(
            "SELECT session_id FROM sessions ORDER BY timestamp DESC LIMIT 1"
        ).fetchone()
        conn.close()
        session_id = session_id[0] if session_id else "unknown"
    except:
        session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create handoff
    if manager.create_session_handoff(session_id, handoff_data):
        print("\n[OK] Handoff created successfully!")
        print(f"     Session: {session_id}")
        print(f"     Next agent will see this on startup.")
        print("\nNow run:")
        print("  python AUTO_CHECKPOINT.py")
        print("  python SANDBOX_EXPORT.py")
        print("  git add -A && git commit && git push")
    else:
        print("\n[ERROR] Failed to create handoff.")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--create':
        # Create handoff at session end
        generate_handoff_at_session_end()
    else:
        # Print current briefing (run on startup)
        manager = AgentHandoffManager()
        manager.print_agent_briefing()
