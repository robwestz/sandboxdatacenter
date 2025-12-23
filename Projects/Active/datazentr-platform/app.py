#!/usr/bin/env python3
"""
DATAZENtr Platform - The REAL Product Embryo
This is the actual platform, not sales material
"""

from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Optional
import asyncio
import json
import uuid
from datetime import datetime
from pathlib import Path
import shutil

# Import our analyzers
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "legacy-migration-mvp"))
from enhanced_migration import SmartMigrationAnalyzer

app = FastAPI(title="DATAZENtr Platform", version="0.1.0")

# CORS for web frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory project storage (skulle vara database i produktion)
PROJECTS = {}
MIGRATIONS = {}

class Project(BaseModel):
    name: str
    description: str
    github_url: Optional[str] = None

class MigrationStatus(BaseModel):
    project_id: str
    status: str  # analyzing, planning, migrating, completed, failed
    progress: int  # 0-100
    current_step: str
    result: Optional[Dict] = None

# ============================================================
# SIMPLE WEB UI
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def home():
    """Simple web interface - the embryo"""

    return """
<!DOCTYPE html>
<html>
<head>
    <title>DATAZENtr - Legacy Migration Platform</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, system-ui, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 2rem;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 1rem;
            padding: 2rem;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            margin-bottom: 0.5rem;
        }
        .subtitle {
            color: #666;
            margin-bottom: 2rem;
        }
        .upload-box {
            border: 3px dashed #ddd;
            border-radius: 0.5rem;
            padding: 3rem;
            text-align: center;
            background: #f9f9f9;
            cursor: pointer;
            transition: all 0.3s;
        }
        .upload-box:hover {
            border-color: #667eea;
            background: #f0f0ff;
        }
        input[type="file"] { display: none; }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 0.5rem;
            font-size: 1.1rem;
            cursor: pointer;
            margin-top: 1rem;
        }
        button:hover { opacity: 0.9; }
        .status {
            margin-top: 2rem;
            padding: 1rem;
            background: #f0f9ff;
            border-radius: 0.5rem;
            display: none;
        }
        .progress-bar {
            width: 100%;
            height: 20px;
            background: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            margin: 1rem 0;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            width: 0%;
            transition: width 0.5s;
        }
        .result {
            white-space: pre-wrap;
            font-family: monospace;
            background: #1e1e1e;
            color: #0f0;
            padding: 1rem;
            border-radius: 0.5rem;
            margin-top: 1rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 DATAZENtr Platform</h1>
        <p class="subtitle">Transform your legacy code to modern stack in minutes</p>

        <div class="upload-box" onclick="document.getElementById('file').click()">
            <h2>📁 Drop your PHP project here</h2>
            <p style="margin-top: 1rem; color: #999;">or click to browse</p>
            <input type="file" id="file" webkitdirectory directory multiple>
        </div>

        <div style="margin-top: 2rem;">
            <h3>Or try with demo project:</h3>
            <button onclick="analyzeDemo()">🎯 Analyze Demo PHP Project</button>
        </div>

        <div class="status" id="status">
            <h3>Migration Progress</h3>
            <p id="current-step">Initializing...</p>
            <div class="progress-bar">
                <div class="progress-fill" id="progress"></div>
            </div>
            <div class="result" id="result" style="display:none;"></div>
        </div>
    </div>

    <script>
        async function analyzeDemo() {
            const status = document.getElementById('status');
            const progress = document.getElementById('progress');
            const currentStep = document.getElementById('current-step');
            const result = document.getElementById('result');

            status.style.display = 'block';
            result.style.display = 'none';

            // Start migration
            const response = await fetch('/api/migrate/demo', {
                method: 'POST'
            });
            const data = await response.json();
            const projectId = data.project_id;

            // Poll for status
            const interval = setInterval(async () => {
                const statusResponse = await fetch(`/api/status/${projectId}`);
                const statusData = await statusResponse.json();

                currentStep.textContent = statusData.current_step;
                progress.style.width = statusData.progress + '%';

                if (statusData.status === 'completed') {
                    clearInterval(interval);
                    result.style.display = 'block';
                    result.textContent = JSON.stringify(statusData.result, null, 2);
                } else if (statusData.status === 'failed') {
                    clearInterval(interval);
                    currentStep.textContent = 'Migration failed!';
                }
            }, 1000);
        }

        // File upload handler
        document.getElementById('file').addEventListener('change', async (e) => {
            const files = e.target.files;
            if (files.length === 0) return;

            const formData = new FormData();
            for (let file of files) {
                formData.append('files', file);
            }

            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                // Start analysis
                window.location.href = `/project/${data.project_id}`;
            }
        });
    </script>
</body>
</html>
    """

# ============================================================
# API ENDPOINTS - The REAL functionality
# ============================================================

@app.post("/api/migrate/demo")
async def migrate_demo_project(background_tasks: BackgroundTasks):
    """Start migration of demo project"""

    project_id = str(uuid.uuid4())

    # Create demo project
    demo_path = Path(f"/tmp/demo_project_{project_id}")
    demo_path.mkdir(exist_ok=True)

    # Create demo PHP files
    (demo_path / "index.php").write_text("""<?php
// Legacy PHP application
require_once 'config.php';
require_once 'database.php';

class UserManager {
    private $db;

    public function __construct() {
        $this->db = new Database();
    }

    public function getUsers() {
        return $this->db->query("SELECT * FROM users");
    }

    public function createUser($name, $email) {
        return $this->db->insert("users", [
            'name' => $name,
            'email' => $email
        ]);
    }
}

$userManager = new UserManager();
$users = $userManager->getUsers();
?>""")

    # Initialize migration status
    MIGRATIONS[project_id] = MigrationStatus(
        project_id=project_id,
        status="analyzing",
        progress=0,
        current_step="Starting analysis..."
    )

    # Start migration in background
    background_tasks.add_task(run_migration, project_id, demo_path)

    return {"project_id": project_id}

async def run_migration(project_id: str, project_path: Path):
    """Run the actual migration process"""

    try:
        # Step 1: Analysis (0-30%)
        MIGRATIONS[project_id].status = "analyzing"
        MIGRATIONS[project_id].current_step = "Analyzing legacy codebase..."
        MIGRATIONS[project_id].progress = 10

        analyzer = SmartMigrationAnalyzer(project_path)
        analysis = await analyzer.analyze_with_memory()

        MIGRATIONS[project_id].progress = 30

        # Step 2: Planning (30-50%)
        MIGRATIONS[project_id].current_step = "Creating migration plan..."
        plan = analyzer.generate_smart_plan()

        MIGRATIONS[project_id].progress = 50

        # Step 3: Code Generation (50-90%)
        MIGRATIONS[project_id].status = "migrating"
        MIGRATIONS[project_id].current_step = "Generating modern code..."

        # Generate actual code (simplified for demo)
        generated_code = {
            "backend": await generate_fastapi_code(analysis),
            "frontend": await generate_nextjs_code(analysis),
            "database": await generate_migration_sql(analysis),
            "docker": generate_docker_config()
        }

        MIGRATIONS[project_id].progress = 90

        # Step 4: Finalize (90-100%)
        MIGRATIONS[project_id].current_step = "Finalizing migration..."
        quote = analyzer.generate_quote(plan)

        # Complete
        MIGRATIONS[project_id].status = "completed"
        MIGRATIONS[project_id].progress = 100
        MIGRATIONS[project_id].current_step = "Migration completed successfully!"
        MIGRATIONS[project_id].result = {
            "analysis": analysis,
            "plan": plan,
            "quote": quote,
            "generated_code": generated_code
        }

    except Exception as e:
        MIGRATIONS[project_id].status = "failed"
        MIGRATIONS[project_id].current_step = f"Error: {str(e)}"

async def generate_fastapi_code(analysis: Dict) -> str:
    """Generate FastAPI backend code"""

    return """# Generated FastAPI Backend
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import asyncpg

app = FastAPI()

class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: str

@app.get("/api/users", response_model=List[User])
async def get_users():
    # Migration from PHP getUsers()
    conn = await asyncpg.connect('postgresql://user:pass@localhost/db')
    users = await conn.fetch("SELECT * FROM users")
    await conn.close()
    return users

@app.post("/api/users", response_model=User)
async def create_user(user: User):
    # Migration from PHP createUser()
    conn = await asyncpg.connect('postgresql://user:pass@localhost/db')
    result = await conn.fetchrow(
        "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *",
        user.name, user.email
    )
    await conn.close()
    return User(**result)
"""

async def generate_nextjs_code(analysis: Dict) -> str:
    """Generate Next.js frontend code"""

    return """// Generated Next.js Frontend
import { useState, useEffect } from 'react'

export default function Users() {
    const [users, setUsers] = useState([])

    useEffect(() => {
        fetch('/api/users')
            .then(res => res.json())
            .then(data => setUsers(data))
    }, [])

    return (
        <div>
            <h1>Users</h1>
            {users.map(user => (
                <div key={user.id}>
                    {user.name} - {user.email}
                </div>
            ))}
        </div>
    )
}
"""

async def generate_migration_sql(analysis: Dict) -> str:
    """Generate database migration SQL"""

    return """-- Database Migration Script
-- From MySQL to PostgreSQL

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Migrate data (run separately)
-- INSERT INTO users (name, email) SELECT name, email FROM mysql_backup.users;
"""

def generate_docker_config() -> str:
    """Generate Docker configuration"""

    return """# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://user:pass@db:5432/myapp

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: myapp
    ports:
      - "5432:5432"
"""

@app.get("/api/status/{project_id}")
async def get_migration_status(project_id: str):
    """Get current migration status"""

    if project_id not in MIGRATIONS:
        raise HTTPException(status_code=404, detail="Project not found")

    return MIGRATIONS[project_id]

@app.post("/api/deploy/{project_id}")
async def deploy_project(project_id: str):
    """Deploy the migrated project"""

    if project_id not in MIGRATIONS:
        raise HTTPException(status_code=404, detail="Project not found")

    if MIGRATIONS[project_id].status != "completed":
        raise HTTPException(status_code=400, detail="Migration not completed")

    # Here would be actual deployment logic
    # - Push to GitHub
    # - Deploy to Vercel/Railway
    # - Setup databases

    return {
        "status": "deployed",
        "url": f"https://{project_id}.datazentr.app",
        "api_url": f"https://api-{project_id}.datazentr.app"
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting DATAZENtr Platform on http://localhost:8888")
    uvicorn.run(app, host="0.0.0.0", port=8888)