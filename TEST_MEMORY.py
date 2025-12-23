#!/usr/bin/env python3
"""
🔍 TEST & VERIFY MEMORY SYSTEM

Kör denna för att se EXAKT vad som kommer laddas när ACTIVATE_MEMORY.py körs.
Detta visar vad nästa agent kommer att "veta" utan risk för hallucination.

Användning:
    python TEST_MEMORY.py        # Visa vad som kommer laddas
    python TEST_MEMORY.py --dry   # Torrkörning av aktivering
    python TEST_MEMORY.py --full  # Full verifiering med alla detaljer
"""

import os
import sys
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import argparse

# Add MEMORY_CORE to path
sys.path.insert(0, str(Path(__file__).parent / "MEMORY_CORE"))

def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print('='*80)

def test_handoff_content():
    """Test and display what's in the latest handoff"""

    print_section("📋 HANDOFF CONTENT CHECK")

    handoff_file = Path(__file__).parent / "MEMORY_CORE" / "handoffs" / "latest.json"

    if not handoff_file.exists():
        print("❌ NO HANDOFF FILE FOUND!")
        print("   This means the next session will start fresh.")
        return None

    try:
        with open(handoff_file, 'r', encoding='utf-8') as f:
            handoff = json.load(f)

        print(f"✅ Handoff found from: {handoff['timestamp']}")
        print(f"   Session ID: {handoff['session_id']}")
        print(f"   Agent model: {handoff.get('agent_model', 'unknown')}")

        # Show what the agent will know
        print("\n📚 WHAT THE NEXT AGENT WILL KNOW:")

        if 'data' in handoff:
            data = handoff['data']

            # Current state
            if 'current_state' in data:
                print("\n  Current State:")
                for key, value in data['current_state'].items():
                    print(f"    • {key}: {value}")

            # Completed tasks
            if 'completed_today' in data:
                print(f"\n  Completed ({len(data['completed_today'])} items):")
                for item in data['completed_today'][:5]:  # Show first 5
                    print(f"    ✓ {item}")
                if len(data['completed_today']) > 5:
                    print(f"    ... and {len(data['completed_today']) - 5} more")

            # Next steps
            if 'next_steps' in data:
                print("\n  Next Steps:")
                if 'immediate' in data['next_steps']:
                    for step in data['next_steps']['immediate'][:3]:
                        print(f"    → {step}")

            # Important paths
            if 'important_paths' in data:
                print("\n  Key Locations:")
                for name, path in data['important_paths'].items():
                    print(f"    • {name}: {path}")

        # Skills identified
        if 'skills_identified' in handoff:
            skills = handoff['skills_identified']
            if 'ready' in skills:
                print(f"\n  Ready Skills: {', '.join(skills['ready'])}")

        # Patterns discovered
        if 'patterns_discovered' in handoff:
            print(f"\n  Patterns Found: {len(handoff['patterns_discovered'])}")
            for pattern in handoff['patterns_discovered'][:2]:
                print(f"    • {pattern['key']}: {pattern['solution']}")

        return handoff

    except Exception as e:
        print(f"❌ ERROR READING HANDOFF: {e}")
        return None

def test_database_content():
    """Test what's in the database"""

    print_section("💾 DATABASE CONTENT CHECK")

    db_path = Path(__file__).parent / "MEMORY_CORE" / "central_memory.db"

    if not db_path.exists():
        print("ℹ️ No database exists yet - will be created on first run")
        return

    try:
        conn = sqlite3.connect(db_path)

        # Check memories
        memory_count = conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
        print(f"📊 Total memories: {memory_count}")

        if memory_count > 0:
            # Show recent memories
            cursor = conn.execute("""
                SELECT type, context, timestamp
                FROM memories
                ORDER BY timestamp DESC
                LIMIT 5
            """)
            print("\n  Recent Memories:")
            for row in cursor:
                print(f"    • [{row[0]}] {row[1]} - {row[2]}")

        # Check patterns
        pattern_count = conn.execute("SELECT COUNT(*) FROM patterns").fetchone()[0]
        print(f"\n🎯 Total patterns: {pattern_count}")

        if pattern_count > 0:
            cursor = conn.execute("""
                SELECT pattern_key, success_count
                FROM patterns
                ORDER BY success_count DESC
                LIMIT 3
            """)
            print("  Top Patterns:")
            for row in cursor:
                print(f"    • {row[0]} (used {row[1]} times)")

        # Check sessions
        session_count = conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
        print(f"\n🔑 Total sessions: {session_count}")

        if session_count > 0:
            cursor = conn.execute("""
                SELECT session_id, start_time, end_time, status
                FROM sessions
                ORDER BY start_time DESC
                LIMIT 1
            """)
            row = cursor.fetchone()
            if row:
                print(f"  Last session: {row[0][:8]}...")
                print(f"    Started: {row[1]}")
                print(f"    Ended: {row[2] or 'Still active'}")
                print(f"    Status: {row[3]}")

        # Check skills
        skill_count = conn.execute("SELECT COUNT(*) FROM skills_used").fetchone()[0]
        print(f"\n🛠️ Skills tracked: {skill_count}")

        if skill_count > 0:
            cursor = conn.execute("""
                SELECT skill_name, COUNT(*) as uses,
                       SUM(CASE WHEN success THEN 1 ELSE 0 END) as successes
                FROM skills_used
                GROUP BY skill_name
                ORDER BY uses DESC
                LIMIT 3
            """)
            print("  Most Used Skills:")
            for row in cursor:
                success_rate = (row[2] / row[1] * 100) if row[1] > 0 else 0
                print(f"    • {row[0]}: {row[1]} uses ({success_rate:.0f}% success)")

        conn.close()

    except Exception as e:
        print(f"❌ ERROR READING DATABASE: {e}")

def verify_file_changes():
    """Check what files have been modified recently"""

    print_section("📁 RECENT FILE CHANGES")

    root_dir = Path(__file__).parent
    recent_files = []

    # Check for files modified in last 24 hours
    cutoff_time = datetime.now() - timedelta(hours=24)

    for file_path in root_dir.rglob("*"):
        if file_path.is_file() and not str(file_path).startswith('.'):
            try:
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                if mtime > cutoff_time:
                    recent_files.append((file_path, mtime))
            except:
                pass

    # Sort by modification time
    recent_files.sort(key=lambda x: x[1], reverse=True)

    if recent_files:
        print(f"Files modified in last 24 hours ({len(recent_files)} total):")
        for file_path, mtime in recent_files[:10]:  # Show top 10
            rel_path = file_path.relative_to(root_dir)
            time_ago = datetime.now() - mtime
            hours_ago = time_ago.total_seconds() / 3600
            print(f"  • {rel_path} ({hours_ago:.1f}h ago)")
    else:
        print("No files modified in last 24 hours")

def simulate_activation():
    """Simulate what ACTIVATE_MEMORY.py will do"""

    print_section("🎭 ACTIVATION SIMULATION")

    print("This is what will happen when ACTIVATE_MEMORY.py runs:\n")

    # Step 1
    print("1. Initialize Central Memory System")
    print("   → Create/connect to MEMORY_CORE/central_memory.db")

    # Step 2
    print("\n2. Start New Session")
    session_id = f"sim_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    print(f"   → Session ID: {session_id}")
    print(f"   → Working dir: {os.getcwd()}")

    # Step 3
    print("\n3. Load Previous Context")
    handoff_file = Path(__file__).parent / "MEMORY_CORE" / "handoffs" / "latest.json"
    if handoff_file.exists():
        print("   ✅ Will load handoff from latest.json")
        with open(handoff_file, 'r') as f:
            handoff = json.load(f)
            if 'handoff_message' in handoff:
                print("\n   Handoff Message:")
                for line in handoff['handoff_message'].split('\n'):
                    if line.strip():
                        print(f"   {line}")
    else:
        print("   ℹ️ No handoff - will start fresh")

    # Step 4
    print("\n4. Display System Status")
    print("   → Show memory statistics")
    print("   → Show recent patterns")
    print("   → Show skill usage")

    # Step 5
    print("\n5. Set Environment Variables")
    print(f"   → DATAZENTR_SESSION_ID={session_id}")
    print("   → DATAZENTR_MEMORY_ACTIVE=true")

    print("\n✅ Agent will have FULL CONTEXT and can continue work!")

def verify_context_integrity():
    """Verify that the context is complete and consistent"""

    print_section("🔐 CONTEXT INTEGRITY CHECK")

    issues = []
    warnings = []

    # Check handoff exists
    handoff_file = Path(__file__).parent / "MEMORY_CORE" / "handoffs" / "latest.json"
    if not handoff_file.exists():
        issues.append("No handoff file - agent will start without context")
    else:
        try:
            with open(handoff_file, 'r') as f:
                handoff = json.load(f)

            # Check age of handoff
            timestamp = datetime.fromisoformat(handoff['timestamp'].replace('T', ' '))
            age = datetime.now() - timestamp
            if age.days > 7:
                warnings.append(f"Handoff is {age.days} days old - context might be stale")

            # Check required fields
            required = ['session_id', 'timestamp', 'data']
            for field in required:
                if field not in handoff:
                    issues.append(f"Missing required field: {field}")

            # Verify paths still exist
            if 'data' in handoff and 'important_paths' in handoff['data']:
                for name, path in handoff['data']['important_paths'].items():
                    full_path = Path(__file__).parent / path
                    if not full_path.exists():
                        warnings.append(f"Path no longer exists: {name} -> {path}")

        except Exception as e:
            issues.append(f"Cannot parse handoff: {e}")

    # Check database
    db_path = Path(__file__).parent / "MEMORY_CORE" / "central_memory.db"
    if db_path.exists():
        try:
            conn = sqlite3.connect(db_path)
            # Test basic query
            conn.execute("SELECT COUNT(*) FROM memories")
            conn.close()
        except Exception as e:
            issues.append(f"Database corrupted: {e}")

    # Display results
    if not issues and not warnings:
        print("✅ CONTEXT INTEGRITY: PERFECT")
        print("   The agent will have complete and accurate context!")
    else:
        if issues:
            print("❌ CRITICAL ISSUES FOUND:")
            for issue in issues:
                print(f"   • {issue}")

        if warnings:
            print("\n⚠️ WARNINGS:")
            for warning in warnings:
                print(f"   • {warning}")

        print("\n🔧 RECOMMENDATIONS:")
        if issues:
            print("   1. Run ACTIVATE_MEMORY.py to initialize properly")
            print("   2. Create a new handoff if needed")
        if warnings:
            print("   1. Review and update stale context")
            print("   2. Verify paths and update if needed")

def main():
    """Main test function"""

    parser = argparse.ArgumentParser(description='Test and verify memory system')
    parser.add_argument('--dry', action='store_true', help='Dry run of activation')
    parser.add_argument('--full', action='store_true', help='Full verification with all details')
    args = parser.parse_args()

    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║                    🔍 MEMORY SYSTEM TEST & VERIFY 🔍                    ║
║                                                                          ║
║         See EXACTLY what the next agent will know and remember          ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
    """)

    # Run tests
    handoff = test_handoff_content()
    test_database_content()

    if args.full:
        verify_file_changes()

    if args.dry:
        simulate_activation()

    # Always run integrity check
    verify_context_integrity()

    # Summary
    print_section("📊 TEST SUMMARY")

    if handoff:
        print("✅ Handoff available - agent will have context")
        if 'data' in handoff and 'next_steps' in handoff['data']:
            if 'immediate' in handoff['data']['next_steps']:
                print(f"✅ Clear next steps defined ({len(handoff['data']['next_steps']['immediate'])} immediate tasks)")
    else:
        print("⚠️ No handoff - agent will start fresh")

    db_exists = (Path(__file__).parent / "MEMORY_CORE" / "central_memory.db").exists()
    if db_exists:
        print("✅ Database exists - historical patterns available")
    else:
        print("ℹ️ No database yet - will be created on activation")

    print("\n💡 TO ACTIVATE MEMORY SYSTEM:")
    print("   python ACTIVATE_MEMORY.py")

    print("\n🔧 TO CREATE CHECKPOINT NOW:")
    print("   python AUTO_CHECKPOINT.py")

if __name__ == "__main__":
    main()