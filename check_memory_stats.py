#!/usr/bin/env python3
"""Quick memory statistics checker"""

import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / "MEMORY_CORE" / "central_memory.db"
conn = sqlite3.connect(str(db_path))

print("📊 DATABASE STATS:")
sessions = conn.execute("SELECT * FROM sessions").fetchall()
memories = conn.execute("SELECT * FROM memories").fetchall()
patterns = conn.execute("SELECT * FROM patterns").fetchall()
skills = conn.execute("SELECT * FROM skills_used").fetchall()

print(f"   Sessions: {len(sessions)}")
print(f"   Memories: {len(memories)}")
print(f"   Patterns: {len(patterns)}")
print(f"   Skills: {len(skills)}")

print("\n🔑 ACTIVE SESSION:")
active = conn.execute("SELECT session_id, start_time, status FROM sessions WHERE status = 'active'").fetchall()
for session in active:
    print(f"   ID: {session[0][:8]}...")
    print(f"   Started: {session[1]}")
    print(f"   Status: {session[2]}")

print("\n💾 RECENT MEMORIES (last 5):")
recent = conn.execute("SELECT type, context, timestamp FROM memories ORDER BY timestamp DESC LIMIT 5").fetchall()
for mem in recent:
    print(f"   [{mem[0]}] {mem[1]} - {mem[2]}")

conn.close()
