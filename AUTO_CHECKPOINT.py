#!/usr/bin/env python3
"""
🔄 AUTO CHECKPOINT SYSTEM - Never Lose Progress

Detta system säkerställer att ALLT arbete sparas kontinuerligt.
Även om sessionen avslutas oväntat, finns alltid en checkpoint att återställa från.

Användning:
    python AUTO_CHECKPOINT.py              # Skapa checkpoint nu
    python AUTO_CHECKPOINT.py --watch      # Övervaka och spara var 5:e minut
    python AUTO_CHECKPOINT.py --track      # Spåra alla ändringar i realtid
"""

import os
import sys
import json
import time
import hashlib
import threading
from datetime import datetime
from pathlib import Path
import argparse
import subprocess
from typing import Dict, List, Any

# Add MEMORY_CORE to path
sys.path.insert(0, str(Path(__file__).parent / "MEMORY_CORE"))

from memory_manager import CentralMemorySystem

class AutoCheckpoint:
    """Automatic checkpoint system for continuous progress saving"""

    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.checkpoint_dir = self.root_dir / "MEMORY_CORE" / "checkpoints"
        self.checkpoint_dir.mkdir(exist_ok=True, parents=True)
        self.memory = CentralMemorySystem()
        self.last_checkpoint = None
        self.file_hashes = {}
        self.changes_since_checkpoint = []

    def create_checkpoint(self, reason: str = "manual") -> str:
        """Create a checkpoint RIGHT NOW"""

        checkpoint_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        checkpoint_file = self.checkpoint_dir / f"checkpoint_{checkpoint_id}.json"

        print(f"\n🔄 Creating checkpoint: {checkpoint_id}")
        print(f"   Reason: {reason}")

        # Gather current state
        checkpoint_data = {
            "checkpoint_id": checkpoint_id,
            "timestamp": datetime.now().isoformat(),
            "reason": reason,
            "working_directory": os.getcwd(),
            "session_id": self.memory.session_id,

            # Current work context
            "current_context": self.gather_current_context(),

            # Recent changes
            "recent_changes": self.detect_recent_changes(),

            # Memory snapshot
            "memory_snapshot": self.snapshot_memory(),

            # Git status if available
            "git_status": self.get_git_status(),

            # Open files/processes
            "active_state": self.get_active_state(),

            # Changes since last checkpoint
            "changes_log": self.changes_since_checkpoint
        }

        # Save checkpoint
        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint_data, f, indent=2, default=str)

        # Also update "latest_checkpoint.json"
        latest_file = self.checkpoint_dir / "latest_checkpoint.json"
        with open(latest_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint_data, f, indent=2, default=str)

        # Save to memory system
        self.memory.remember(
            "checkpoint",
            {
                "id": checkpoint_id,
                "reason": reason,
                "changes": len(self.changes_since_checkpoint)
            },
            context="auto_checkpoint"
        )

        # Reset change tracking
        self.changes_since_checkpoint = []
        self.last_checkpoint = datetime.now()

        print(f"   ✅ Checkpoint saved: {checkpoint_file.name}")
        print(f"   📊 Tracked {len(checkpoint_data['recent_changes'])} file changes")

        return checkpoint_id

    def gather_current_context(self) -> Dict:
        """Gather the current working context"""

        context = {
            "timestamp": datetime.now().isoformat(),
            "working_files": [],
            "recent_commands": [],
            "active_tasks": []
        }

        # Find recently modified files (last hour)
        cutoff = datetime.now().timestamp() - 3600
        for file_path in self.root_dir.rglob("*"):
            if file_path.is_file() and not any(part.startswith('.') for part in file_path.parts):
                try:
                    if file_path.stat().st_mtime > cutoff:
                        rel_path = file_path.relative_to(self.root_dir)
                        context["working_files"].append(str(rel_path))
                except:
                    pass

        # Get recent memories from database
        recent_memories = self.memory.recall(limit=10)
        context["recent_activities"] = [
            {
                "type": mem.type,
                "context": mem.context,
                "time": str(mem.timestamp)
            }
            for mem in recent_memories
        ]

        # Check for todo lists or task tracking
        handoff_file = self.root_dir / "MEMORY_CORE" / "handoffs" / "latest.json"
        if handoff_file.exists():
            try:
                with open(handoff_file, 'r') as f:
                    handoff = json.load(f)
                    if 'data' in handoff and 'next_steps' in handoff['data']:
                        if 'immediate' in handoff['data']['next_steps']:
                            context["active_tasks"] = handoff['data']['next_steps']['immediate']
            except:
                pass

        return context

    def detect_recent_changes(self) -> List[Dict]:
        """Detect what files have changed since last checkpoint"""

        changes = []
        current_hashes = {}

        # Check key directories
        key_dirs = [
            "Skills",
            "MEMORY_CORE",
            "Projects",
            "The_orchestrator"
        ]

        for dir_name in key_dirs:
            dir_path = self.root_dir / dir_name
            if dir_path.exists():
                for file_path in dir_path.rglob("*"):
                    if file_path.is_file() and file_path.suffix in ['.py', '.md', '.json', '.txt']:
                        try:
                            # Calculate file hash
                            with open(file_path, 'rb') as f:
                                file_hash = hashlib.md5(f.read()).hexdigest()

                            rel_path = str(file_path.relative_to(self.root_dir))
                            current_hashes[rel_path] = file_hash

                            # Check if changed
                            if rel_path in self.file_hashes:
                                if self.file_hashes[rel_path] != file_hash:
                                    changes.append({
                                        "file": rel_path,
                                        "action": "modified",
                                        "timestamp": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                                    })
                            else:
                                changes.append({
                                    "file": rel_path,
                                    "action": "created",
                                    "timestamp": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                                })
                        except:
                            pass

        # Check for deleted files
        for old_path in self.file_hashes:
            if old_path not in current_hashes:
                changes.append({
                    "file": old_path,
                    "action": "deleted",
                    "timestamp": datetime.now().isoformat()
                })

        # Update hash cache
        self.file_hashes = current_hashes

        return changes

    def snapshot_memory(self) -> Dict:
        """Take a snapshot of the current memory state"""

        try:
            stats = self.memory.get_memory_stats()
            patterns = self.memory.get_pattern()
            skills = self.memory.get_skill_stats()

            return {
                "statistics": stats,
                "top_patterns": patterns[:5] if patterns else [],
                "skill_usage": skills,
                "total_memories": stats.get('total_memories', 0),
                "memory_types": stats.get('memory_types', {})
            }
        except:
            return {"error": "Could not snapshot memory"}

    def get_git_status(self) -> Dict:
        """Get git status if in a git repo"""

        try:
            # Check if git repo
            result = subprocess.run(
                ['git', 'status', '--short'],
                capture_output=True,
                text=True,
                cwd=self.root_dir,
                timeout=5
            )

            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                return {
                    "is_git_repo": True,
                    "modified_files": len([l for l in lines if l.startswith(' M')]),
                    "new_files": len([l for l in lines if l.startswith('??')]),
                    "staged_files": len([l for l in lines if l.startswith('A ')]),
                    "status_summary": lines[:10] if lines[0] else []  # First 10 status lines
                }
            else:
                return {"is_git_repo": False}
        except:
            return {"is_git_repo": False}

    def get_active_state(self) -> Dict:
        """Get current active state (open files, running processes, etc)"""

        state = {
            "timestamp": datetime.now().isoformat(),
            "python_scripts": [],
            "recent_outputs": []
        }

        # Check for running Python scripts
        try:
            result = subprocess.run(
                ['tasklist', '/FI', 'IMAGENAME eq python.exe'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                state["python_processes"] = len([l for l in lines if 'python.exe' in l.lower()])
        except:
            pass

        return state

    def watch_mode(self, interval_minutes: int = 5):
        """Run in watch mode - auto checkpoint every N minutes"""

        print(f"👁️ WATCH MODE ACTIVATED")
        print(f"   Will checkpoint every {interval_minutes} minutes")
        print(f"   Press Ctrl+C to stop\n")

        # Initial checkpoint
        self.create_checkpoint("watch_mode_start")

        try:
            while True:
                time.sleep(interval_minutes * 60)
                self.create_checkpoint(f"auto_{interval_minutes}min")
                self.log_change(f"Auto checkpoint after {interval_minutes} minutes")
        except KeyboardInterrupt:
            print("\n\n⏹️ Watch mode stopped")
            self.create_checkpoint("watch_mode_end")

    def track_changes_realtime(self):
        """Track changes in real-time"""

        print(f"📡 REAL-TIME TRACKING ACTIVATED")
        print(f"   Monitoring all changes...")
        print(f"   Press Ctrl+C to stop\n")

        # Initial file scan
        self.detect_recent_changes()

        try:
            while True:
                changes = self.detect_recent_changes()
                if changes:
                    print(f"\n🔔 Changes detected at {datetime.now().strftime('%H:%M:%S')}:")
                    for change in changes[:5]:  # Show max 5
                        print(f"   • {change['action']}: {change['file']}")

                    # Log changes
                    for change in changes:
                        self.log_change(f"{change['action']}: {change['file']}")

                    # Auto checkpoint if significant changes
                    if len(changes) > 10:
                        print(f"   ⚠️ Significant changes ({len(changes)} files) - creating checkpoint")
                        self.create_checkpoint(f"significant_changes_{len(changes)}_files")

                time.sleep(30)  # Check every 30 seconds
        except KeyboardInterrupt:
            print("\n\n⏹️ Tracking stopped")
            if self.changes_since_checkpoint:
                print(f"   📊 {len(self.changes_since_checkpoint)} changes tracked")
                self.create_checkpoint("tracking_stopped")

    def log_change(self, change: str):
        """Log a change for the next checkpoint"""
        self.changes_since_checkpoint.append({
            "timestamp": datetime.now().isoformat(),
            "change": change
        })

    def restore_checkpoint(self, checkpoint_id: str = None):
        """Restore from a checkpoint"""

        if checkpoint_id:
            checkpoint_file = self.checkpoint_dir / f"checkpoint_{checkpoint_id}.json"
        else:
            checkpoint_file = self.checkpoint_dir / "latest_checkpoint.json"

        if not checkpoint_file.exists():
            print(f"❌ Checkpoint not found: {checkpoint_file}")
            return False

        try:
            with open(checkpoint_file, 'r') as f:
                checkpoint = json.load(f)

            print(f"\n📂 RESTORING CHECKPOINT: {checkpoint['checkpoint_id']}")
            print(f"   Created: {checkpoint['timestamp']}")
            print(f"   Reason: {checkpoint['reason']}")

            # Show what was active
            if 'current_context' in checkpoint:
                context = checkpoint['current_context']
                if context.get('working_files'):
                    print(f"\n   Working files ({len(context['working_files'])}):")
                    for file in context['working_files'][:5]:
                        print(f"     • {file}")

                if context.get('active_tasks'):
                    print(f"\n   Active tasks:")
                    for task in context['active_tasks'][:3]:
                        print(f"     → {task}")

            # Show memory state
            if 'memory_snapshot' in checkpoint:
                snapshot = checkpoint['memory_snapshot']
                print(f"\n   Memory state:")
                print(f"     • Total memories: {snapshot.get('total_memories', 0)}")
                if 'memory_types' in snapshot:
                    for mem_type, count in snapshot['memory_types'].items():
                        print(f"     • {mem_type}: {count}")

            print(f"\n✅ Checkpoint loaded - context restored!")
            return checkpoint

        except Exception as e:
            print(f"❌ Error restoring checkpoint: {e}")
            return False

    def list_checkpoints(self):
        """List all available checkpoints"""

        print("\n📚 AVAILABLE CHECKPOINTS:")

        checkpoints = []
        for cp_file in self.checkpoint_dir.glob("checkpoint_*.json"):
            if cp_file.name != "latest_checkpoint.json":
                try:
                    with open(cp_file, 'r') as f:
                        cp_data = json.load(f)
                        checkpoints.append({
                            "file": cp_file.name,
                            "id": cp_data['checkpoint_id'],
                            "timestamp": cp_data['timestamp'],
                            "reason": cp_data['reason']
                        })
                except:
                    pass

        # Sort by timestamp
        checkpoints.sort(key=lambda x: x['timestamp'], reverse=True)

        if checkpoints:
            for cp in checkpoints[:10]:  # Show last 10
                dt = datetime.fromisoformat(cp['timestamp'])
                age = datetime.now() - dt
                hours_ago = age.total_seconds() / 3600

                print(f"\n   📍 ID: {cp['id']}")
                print(f"      Created: {hours_ago:.1f} hours ago")
                print(f"      Reason: {cp['reason']}")
        else:
            print("   No checkpoints found")

def main():
    """Main entry point"""

    parser = argparse.ArgumentParser(description='Automatic checkpoint system')
    parser.add_argument('--watch', action='store_true', help='Watch mode - auto checkpoint every 5 min')
    parser.add_argument('--track', action='store_true', help='Track all changes in real-time')
    parser.add_argument('--list', action='store_true', help='List all checkpoints')
    parser.add_argument('--restore', type=str, help='Restore specific checkpoint')
    parser.add_argument('--interval', type=int, default=5, help='Checkpoint interval in minutes')
    args = parser.parse_args()

    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║                    🔄 AUTO CHECKPOINT SYSTEM 🔄                         ║
║                                                                          ║
║                      Never lose progress again!                         ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
    """)

    checkpoint_system = AutoCheckpoint()

    if args.list:
        checkpoint_system.list_checkpoints()
    elif args.restore:
        checkpoint_system.restore_checkpoint(args.restore)
    elif args.watch:
        checkpoint_system.watch_mode(args.interval)
    elif args.track:
        checkpoint_system.track_changes_realtime()
    else:
        # Default: Create checkpoint now
        checkpoint_id = checkpoint_system.create_checkpoint("manual")

        print("\n💡 OPTIONS:")
        print("   --watch     Auto-checkpoint every 5 minutes")
        print("   --track     Track all file changes in real-time")
        print("   --list      Show all checkpoints")
        print("   --restore   Restore a specific checkpoint")

        print("\n📝 Checkpoint can be restored with:")
        print(f"   python AUTO_CHECKPOINT.py --restore {checkpoint_id}")

if __name__ == "__main__":
    main()