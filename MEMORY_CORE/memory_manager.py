"""
🧠 CENTRAL MEMORY MANAGER - The Universal Memory System for THE_DATAZENtr
Consolidates all memory systems into one simple interface
"""

import os
import json
import sqlite3
import hashlib
import pickle
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import sys

# Add paths for existing systems
sys.path.append(str(Path(__file__).parent.parent / "The_orchestrator"))

@dataclass
class Memory:
    """Universal memory object"""
    id: str
    type: str  # pattern, skill, project, session, learning
    content: Dict[str, Any]
    context: str
    timestamp: datetime
    session_id: Optional[str] = None
    success_rate: float = 1.0
    usage_count: int = 0
    tags: List[str] = None

class CentralMemorySystem:
    """
    The ONE memory system to rule them all.
    Simple interface that works across all components.
    """

    def __init__(self, db_path: str = None):
        """Initialize the central memory system"""
        self.root_dir = Path(__file__).parent.parent
        self.db_path = db_path or str(self.root_dir / "MEMORY_CORE" / "central_memory.db")
        self.session_id = self._generate_session_id()
        self.init_database()
        self.load_last_session()

    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        timestamp = datetime.now().isoformat()
        return hashlib.sha256(timestamp.encode()).hexdigest()[:16]

    def init_database(self):
        """Initialize the central database"""
        conn = sqlite3.connect(self.db_path)

        # Main memory table - simplified but powerful
        conn.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                content TEXT NOT NULL,
                context TEXT,
                session_id TEXT,
                timestamp TIMESTAMP,
                success_rate REAL DEFAULT 1.0,
                usage_count INTEGER DEFAULT 0,
                tags TEXT
            )
        ''')

        # Session tracking
        conn.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                agent_model TEXT,
                working_dir TEXT,
                status TEXT,
                handoff_data TEXT
            )
        ''')

        # Quick patterns table for fast lookup
        conn.execute('''
            CREATE TABLE IF NOT EXISTS patterns (
                pattern_key TEXT PRIMARY KEY,
                pattern_type TEXT,
                solution TEXT,
                success_count INTEGER DEFAULT 0,
                failure_count INTEGER DEFAULT 0,
                last_used TIMESTAMP,
                metadata TEXT
            )
        ''')

        # Skills tracking
        conn.execute('''
            CREATE TABLE IF NOT EXISTS skills_used (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                skill_name TEXT,
                session_id TEXT,
                timestamp TIMESTAMP,
                success BOOLEAN,
                execution_time REAL,
                context TEXT
            )
        ''')

        # Create indexes
        conn.execute('CREATE INDEX IF NOT EXISTS idx_type ON memories(type)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_session ON memories(session_id)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON memories(timestamp)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_pattern_type ON patterns(pattern_type)')

        conn.commit()
        conn.close()

    # ========== CORE MEMORY OPERATIONS ==========

    def remember(self, memory_type: str, content: Any, context: str = None, tags: List[str] = None) -> str:
        """
        Remember anything - the universal memory function

        Examples:
            memory.remember("pattern", {"solution": "use Redis for caching"}, "performance")
            memory.remember("learning", {"insight": "Always validate input"}, "security")
            memory.remember("project_state", current_project_data, "project_x")
        """
        memory = Memory(
            id=hashlib.sha256(f"{memory_type}{json.dumps(content)}".encode()).hexdigest()[:16],
            type=memory_type,
            content=content if isinstance(content, dict) else {"data": content},
            context=context or "general",
            timestamp=datetime.now(),
            session_id=self.session_id,
            tags=tags or []
        )

        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            INSERT OR REPLACE INTO memories
            (id, type, content, context, session_id, timestamp, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            memory.id,
            memory.type,
            json.dumps(memory.content),
            memory.context,
            memory.session_id,
            memory.timestamp,
            json.dumps(memory.tags)
        ))
        conn.commit()
        conn.close()

        return memory.id

    def recall(self, memory_type: str = None, context: str = None, limit: int = 10) -> List[Memory]:
        """
        Recall memories - flexible retrieval

        Examples:
            memory.recall("pattern", "api_design")  # Get API patterns
            memory.recall(context="current_project")  # Get all project memories
            memory.recall()  # Get recent memories
        """
        conn = sqlite3.connect(self.db_path)

        query = "SELECT * FROM memories WHERE 1=1"
        params = []

        if memory_type:
            query += " AND type = ?"
            params.append(memory_type)

        if context:
            query += " AND context = ?"
            params.append(context)

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        cursor = conn.execute(query, params)
        memories = []

        for row in cursor:
            memories.append(Memory(
                id=row[0],
                type=row[1],
                content=json.loads(row[2]),
                context=row[3],
                timestamp=datetime.fromisoformat(row[5]) if row[5] else None,
                session_id=row[4],
                success_rate=row[6],
                usage_count=row[7],
                tags=json.loads(row[8]) if row[8] else []
            ))

        conn.close()
        return memories

    def search(self, query: str, limit: int = 10) -> List[Memory]:
        """
        Search all memories with text matching
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute('''
            SELECT * FROM memories
            WHERE content LIKE ?
            OR context LIKE ?
            OR tags LIKE ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (f"%{query}%", f"%{query}%", f"%{query}%", limit))

        memories = []
        for row in cursor:
            memories.append(Memory(
                id=row[0],
                type=row[1],
                content=json.loads(row[2]),
                context=row[3],
                timestamp=datetime.fromisoformat(row[5]) if row[5] else None,
                session_id=row[4],
                success_rate=row[6],
                usage_count=row[7],
                tags=json.loads(row[8]) if row[8] else []
            ))

        conn.close()
        return memories

    # ========== PATTERN MANAGEMENT ==========

    def save_pattern(self, pattern_key: str, pattern_type: str, solution: Dict[str, Any]):
        """Save a successful pattern for reuse"""
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            INSERT OR REPLACE INTO patterns
            (pattern_key, pattern_type, solution, last_used, success_count)
            VALUES (?, ?, ?, ?, COALESCE((SELECT success_count FROM patterns WHERE pattern_key = ?), 0) + 1)
        ''', (pattern_key, pattern_type, json.dumps(solution), datetime.now(), pattern_key))
        conn.commit()
        conn.close()

    def get_pattern(self, pattern_type: str = None) -> List[Dict]:
        """Get successful patterns"""
        conn = sqlite3.connect(self.db_path)

        if pattern_type:
            cursor = conn.execute(
                'SELECT * FROM patterns WHERE pattern_type = ? ORDER BY success_count DESC',
                (pattern_type,)
            )
        else:
            cursor = conn.execute('SELECT * FROM patterns ORDER BY success_count DESC LIMIT 10')

        patterns = []
        for row in cursor:
            patterns.append({
                'key': row[0],
                'type': row[1],
                'solution': json.loads(row[2]),
                'success_count': row[3],
                'failure_count': row[4],
                'last_used': row[5]
            })

        conn.close()
        return patterns

    # ========== SESSION MANAGEMENT ==========

    def start_session(self, agent_model: str = "claude", working_dir: str = None):
        """Start a new session"""
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            INSERT INTO sessions (session_id, start_time, agent_model, working_dir, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (self.session_id, datetime.now(), agent_model, working_dir or os.getcwd(), "active"))
        conn.commit()
        conn.close()

    def end_session(self, handoff_data: Dict = None):
        """End current session and prepare handoff"""
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            UPDATE sessions
            SET end_time = ?, status = ?, handoff_data = ?
            WHERE session_id = ?
        ''', (datetime.now(), "completed", json.dumps(handoff_data) if handoff_data else None, self.session_id))
        conn.commit()
        conn.close()

        # Create handoff file
        if handoff_data:
            self.create_handoff(handoff_data)

    def load_last_session(self) -> Optional[Dict]:
        """Load the most recent session's handoff data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute('''
            SELECT session_id, handoff_data, end_time
            FROM sessions
            WHERE status = 'completed' AND handoff_data IS NOT NULL
            ORDER BY end_time DESC
            LIMIT 1
        ''')

        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                'session_id': row[0],
                'handoff_data': json.loads(row[1]) if row[1] else {},
                'ended_at': row[2]
            }
        return None

    # ========== SKILL TRACKING ==========

    def track_skill(self, skill_name: str, success: bool, execution_time: float = 0, context: str = None):
        """Track skill usage"""
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            INSERT INTO skills_used
            (skill_name, session_id, timestamp, success, execution_time, context)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (skill_name, self.session_id, datetime.now(), success, execution_time, context))
        conn.commit()
        conn.close()

    def get_skill_stats(self) -> Dict:
        """Get skill usage statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute('''
            SELECT
                skill_name,
                COUNT(*) as uses,
                SUM(CASE WHEN success THEN 1 ELSE 0 END) as successes,
                AVG(execution_time) as avg_time
            FROM skills_used
            GROUP BY skill_name
            ORDER BY uses DESC
        ''')

        stats = {}
        for row in cursor:
            stats[row[0]] = {
                'uses': row[1],
                'successes': row[2],
                'success_rate': row[2] / row[1] if row[1] > 0 else 0,
                'avg_time': row[3]
            }

        conn.close()
        return stats

    # ========== HANDOFF MANAGEMENT ==========

    def create_handoff(self, data: Dict):
        """Create a handoff file for the next session"""
        handoff_dir = self.root_dir / "MEMORY_CORE" / "handoffs"
        handoff_dir.mkdir(exist_ok=True)

        handoff_file = handoff_dir / f"handoff_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        handoff_content = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "working_directory": os.getcwd(),
            "data": data,
            "recent_memories": [asdict(m) for m in self.recall(limit=20)],
            "active_patterns": self.get_pattern(),
            "skill_stats": self.get_skill_stats()
        }

        with open(handoff_file, 'w', encoding='utf-8') as f:
            json.dump(handoff_content, f, indent=2, default=str)

        # Also create a latest.json symlink-like file
        latest_file = handoff_dir / "latest.json"
        with open(latest_file, 'w', encoding='utf-8') as f:
            json.dump(handoff_content, f, indent=2, default=str)

    def load_latest_handoff(self) -> Optional[Dict]:
        """Load the most recent handoff file"""
        handoff_dir = self.root_dir / "MEMORY_CORE" / "handoffs"
        latest_file = handoff_dir / "latest.json"

        if latest_file.exists():
            with open(latest_file, 'r', encoding='utf-8') as f:
                return json.load(f)

        return None

    # ========== STATISTICS & HEALTH ==========

    def get_memory_stats(self) -> Dict:
        """Get overall memory system statistics"""
        conn = sqlite3.connect(self.db_path)

        stats = {
            'total_memories': conn.execute('SELECT COUNT(*) FROM memories').fetchone()[0],
            'total_patterns': conn.execute('SELECT COUNT(*) FROM patterns').fetchone()[0],
            'total_sessions': conn.execute('SELECT COUNT(*) FROM sessions').fetchone()[0],
            'total_skills_used': conn.execute('SELECT COUNT(*) FROM skills_used').fetchone()[0],
            'memory_types': {}
        }

        # Count by type
        cursor = conn.execute('SELECT type, COUNT(*) FROM memories GROUP BY type')
        for row in cursor:
            stats['memory_types'][row[0]] = row[1]

        # Most successful patterns
        cursor = conn.execute('SELECT pattern_key, success_count FROM patterns ORDER BY success_count DESC LIMIT 5')
        stats['top_patterns'] = [{'key': row[0], 'uses': row[1]} for row in cursor]

        conn.close()
        return stats

    def health_check(self) -> Dict:
        """Check if memory system is healthy"""
        try:
            stats = self.get_memory_stats()
            return {
                'status': 'healthy' if stats['total_memories'] > 0 else 'empty',
                'stats': stats,
                'session_id': self.session_id,
                'db_path': self.db_path
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

# ========== CONVENIENCE FUNCTIONS ==========

_memory_instance = None

def get_memory() -> CentralMemorySystem:
    """Get or create the singleton memory instance"""
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = CentralMemorySystem()
    return _memory_instance

def remember(memory_type: str, content: Any, context: str = None) -> str:
    """Quick remember function"""
    return get_memory().remember(memory_type, content, context)

def recall(memory_type: str = None, context: str = None, limit: int = 10) -> List:
    """Quick recall function"""
    return get_memory().recall(memory_type, context, limit)

def save_pattern(key: str, pattern_type: str, solution: Dict):
    """Quick pattern save"""
    get_memory().save_pattern(key, pattern_type, solution)

def track_skill(name: str, success: bool, time: float = 0):
    """Quick skill tracking"""
    get_memory().track_skill(name, success, time)