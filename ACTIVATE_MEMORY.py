#!/usr/bin/env python3
"""
🧠 ONE-CLICK MEMORY ACTIVATION FOR THE_DATAZENtr

Kör denna fil vid varje sessionstart:
    python ACTIVATE_MEMORY.py

Det är ALLT som behövs! Minnet aktiveras, tidigare kontext laddas,
och du fortsätter exakt där du slutade.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Add MEMORY_CORE to path
sys.path.insert(0, str(Path(__file__).parent / "MEMORY_CORE"))

from memory_manager import CentralMemorySystem, get_memory

def print_banner():
    """Print a nice welcome banner"""
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║                    🧠 THE_DATAZENtr MEMORY SYSTEM 🧠                    ║
║                                                                          ║
║                      Activating Neural Memory Core...                    ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
    """)

def activate_memory():
    """Main activation sequence with full verification"""

    print_banner()

    # Initialize memory system
    print("📊 Initializing Central Memory System...")
    memory = CentralMemorySystem()

    # Start new session
    print(f"🔑 Starting session: {memory.session_id}")
    memory.start_session(
        agent_model=os.environ.get('ANTHROPIC_MODEL_ID', 'claude'),
        working_dir=os.getcwd()
    )

    # VERIFICATION: Show exactly what will be loaded
    print("\n" + "="*78)
    print("🔍 VERIFICATION: What this agent will know")
    print("="*78)

    # Load previous session if exists
    print("\n📂 Loading previous session context...")
    last_handoff = memory.load_latest_handoff()

    # Also check for checkpoints
    checkpoint_dir = Path(__file__).parent / "MEMORY_CORE" / "checkpoints"
    latest_checkpoint = checkpoint_dir / "latest_checkpoint.json"
    checkpoint_data = None

    if latest_checkpoint.exists():
        try:
            with open(latest_checkpoint, 'r') as f:
                checkpoint_data = json.load(f)
                checkpoint_time = datetime.fromisoformat(checkpoint_data['timestamp'].replace('T', ' '))
                age = datetime.now() - checkpoint_time
                hours_ago = age.total_seconds() / 3600

                print(f"\n🔄 Found checkpoint from {hours_ago:.1f} hours ago")
                print(f"   Checkpoint ID: {checkpoint_data['checkpoint_id']}")
                print(f"   Reason: {checkpoint_data['reason']}")

                # Show recent changes from checkpoint
                if 'recent_changes' in checkpoint_data and checkpoint_data['recent_changes']:
                    print(f"   Recent file changes: {len(checkpoint_data['recent_changes'])}")
                    for change in checkpoint_data['recent_changes'][:3]:
                        print(f"     • {change['action']}: {change['file']}")
        except Exception as e:
            print(f"   ⚠️ Could not load checkpoint: {e}")

    if last_handoff:
        print(f"✅ Found handoff from: {last_handoff['timestamp']}")
        print(f"   Previous session: {last_handoff['session_id']}")

        # Show recent memories
        if 'recent_memories' in last_handoff:
            print(f"\n💭 Recent memories: {len(last_handoff['recent_memories'])} items")
            for mem in last_handoff['recent_memories'][:5]:
                print(f"   - [{mem['type']}] {mem.get('context', 'general')}")

        # Show active patterns
        if 'active_patterns' in last_handoff:
            print(f"\n🎯 Active patterns: {len(last_handoff['active_patterns'])} patterns")
            for pattern in last_handoff['active_patterns'][:3]:
                print(f"   - {pattern['key']} (used {pattern['success_count']} times)")

        # Show skill stats
        if 'skill_stats' in last_handoff:
            skills = last_handoff['skill_stats']
            if skills:
                print(f"\n🛠️ Skills used:")
                for skill, stats in list(skills.items())[:5]:
                    print(f"   - {skill}: {stats['uses']} uses, {stats['success_rate']:.0%} success")

        # Show handoff data
        if 'data' in last_handoff and last_handoff['data']:
            print(f"\n📋 Handoff data available:")
            data = last_handoff['data']
            if 'current_task' in data:
                print(f"   Current task: {data['current_task']}")
            if 'next_steps' in data:
                print(f"   Next steps: {data['next_steps']}")
            if 'notes' in data:
                print(f"   Notes: {data['notes']}")
    else:
        print("ℹ️ No previous session found - starting fresh")

        # Check if there are any memories at all
        stats = memory.get_memory_stats()
        if stats['total_memories'] > 0:
            print(f"\n📚 Found existing memories in database:")
            print(f"   - Total memories: {stats['total_memories']}")
            print(f"   - Total patterns: {stats['total_patterns']}")
            print(f"   - Total sessions: {stats['total_sessions']}")

    # Health check
    print("\n🏥 System Health Check:")
    health = memory.health_check()
    print(f"   Status: {health['status'].upper()}")
    if health['status'] == 'healthy':
        print(f"   Total memories: {health['stats']['total_memories']}")
        print(f"   Total patterns: {health['stats']['total_patterns']}")

    # Show quick commands
    print("\n" + "="*78)
    print("✨ MEMORY SYSTEM ACTIVATED! ✨")
    print("="*78)
    print("""
Quick Python commands to use in your session:

  from MEMORY_CORE.memory_manager import remember, recall, save_pattern, track_skill

  # Remember something
  remember("learning", {"insight": "Always test first"}, "testing")

  # Recall memories
  memories = recall("pattern", "api_design")

  # Save a successful pattern
  save_pattern("rest_api", "api", {"framework": "FastAPI"})

  # Track skill usage
  track_skill("legacy_analyzer", success=True, time=30)

At session end, create handoff:
  from MEMORY_CORE.memory_manager import get_memory
  memory = get_memory()
  memory.end_session({
      "current_task": "Building X",
      "next_steps": "Test Y",
      "notes": "Remember Z"
  })
""")

    # Create activation receipt
    receipt_file = Path(__file__).parent / "MEMORY_CORE" / "activation_receipt.json"
    with open(receipt_file, 'w') as f:
        json.dump({
            "activated_at": datetime.now().isoformat(),
            "session_id": memory.session_id,
            "working_dir": os.getcwd(),
            "health": health
        }, f, indent=2)

    print(f"\n📝 Session ID: {memory.session_id}")
    print(f"📍 Working directory: {os.getcwd()}")
    print(f"💾 Database: {memory.db_path}")
    print("\n🚀 Ready to continue where we left off!\n")

    return memory

def main():
    """Main entry point"""
    try:
        memory = activate_memory()

        # Set up environment variable for other scripts
        os.environ['DATAZENTR_SESSION_ID'] = memory.session_id
        os.environ['DATAZENTR_MEMORY_ACTIVE'] = 'true'

        # Optional: Start background monitoring (uncomment if needed)
        # from memory_monitor import start_monitor
        # start_monitor(memory)

    except KeyboardInterrupt:
        print("\n\n⚠️ Memory activation interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error activating memory: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()