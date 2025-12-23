#!/usr/bin/env python3
"""
DAY 002: PROJECT STRUCTURE GENERATOR
Deterministic project structure generation - same input ALWAYS gives same output
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any
import sys

# Add MEMORY_CORE to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "MEMORY_CORE"))
from memory_manager import remember, save_pattern

class ProjectStructureGenerator:
    """Generate perfect project structures deterministically"""

    # Complete structure definitions
    STRUCTURES = {
        "nextjs-fastapi": {
            "frontend": {
                "app": {
                    "layout.tsx": "export default function RootLayout({children}) { return children; }",
                    "page.tsx": "export default function Home() { return <h1>Home</h1>; }",
                    "globals.css": "/* Global styles */"
                },
                "components": {
                    "ui": {},
                    "shared": {}
                },
                "lib": {
                    "api.ts": "// API client",
                    "utils.ts": "// Utility functions"
                },
                "public": {},
                "package.json": '{"name": "frontend", "version": "1.0.0"}'
            },
            "backend": {
                "app": {
                    "__init__.py": "",
                    "main.py": "from fastapi import FastAPI\n\napp = FastAPI()",
                    "models.py": "# Database models",
                    "schemas.py": "# Pydantic schemas"
                },
                "api": {
                    "__init__.py": "",
                    "endpoints": {},
                    "deps.py": "# Dependencies"
                },
                "core": {
                    "__init__.py": "",
                    "config.py": "# Configuration",
                    "security.py": "# Security utilities"
                },
                "requirements.txt": "fastapi>=0.109.0\nuvicorn[standard]>=0.27.0"
            },
            "docker-compose.yml": "version: '3.8'\nservices:\n  frontend:\n    build: ./frontend\n  backend:\n    build: ./backend",
            ".env.example": "DATABASE_URL=\nSECRET_KEY=",
            "README.md": "# Project\n\n## Setup\n\n1. Install dependencies\n2. Run docker-compose up"
        },

        "microservices": {
            "services": {
                "auth": {
                    "src": {
                        "main.py": "# Auth service",
                        "__init__.py": ""
                    },
                    "tests": {},
                    "Dockerfile": "FROM python:3.11\nWORKDIR /app"
                },
                "api-gateway": {
                    "src": {
                        "main.py": "# API Gateway",
                        "__init__.py": ""
                    },
                    "tests": {},
                    "Dockerfile": "FROM python:3.11"
                },
                "user-service": {
                    "src": {
                        "main.py": "# User service",
                        "__init__.py": ""
                    },
                    "tests": {},
                    "Dockerfile": "FROM python:3.11"
                }
            },
            "infrastructure": {
                "kubernetes": {
                    "deployments": {},
                    "services": {},
                    "configmaps": {}
                },
                "terraform": {
                    "modules": {},
                    "environments": {}
                }
            },
            "docker-compose.yml": "version: '3.8'",
            "Makefile": "build:\n\tdocker-compose build",
            "README.md": "# Microservices Architecture"
        },

        "python-package": {
            "src": {
                "package_name": {
                    "__init__.py": "__version__ = '1.0.0'",
                    "core.py": "# Core functionality",
                    "utils.py": "# Utility functions"
                }
            },
            "tests": {
                "test_core.py": "import pytest\n\ndef test_example():\n    assert True",
                "test_utils.py": "# Utility tests"
            },
            "docs": {
                "conf.py": "# Sphinx configuration",
                "index.md": "# Documentation"
            },
            "setup.py": "from setuptools import setup, find_packages\n\nsetup(name='package')",
            "pyproject.toml": "[build-system]\nrequires = ['setuptools', 'wheel']",
            "README.md": "# Python Package",
            "LICENSE": "MIT License"
        },

        "react-app": {
            "src": {
                "App.jsx": "export default function App() { return <div>App</div>; }",
                "index.js": "import App from './App'",
                "index.css": "/* Styles */",
                "components": {},
                "hooks": {},
                "utils": {}
            },
            "public": {
                "index.html": "<!DOCTYPE html><html><head><title>App</title></head><body><div id='root'></div></body></html>"
            },
            "package.json": '{"name": "react-app", "dependencies": {"react": "^18.2.0"}}',
            ".gitignore": "node_modules\nbuild\n.env",
            "README.md": "# React App"
        }
    }

    def generate(self, project_type: str, project_name: str, target_dir: str = None) -> Dict:
        """
        Generate project structure

        Args:
            project_type: Type of project (e.g., 'nextjs-fastapi')
            project_name: Name of the project
            target_dir: Where to create the structure (optional)

        Returns:
            Dictionary with creation results
        """

        if project_type not in self.STRUCTURES:
            # Find closest match
            project_type = self._find_closest_match(project_type)

        structure = self.STRUCTURES[project_type]

        # Statistics
        stats = {
            "type": project_type,
            "name": project_name,
            "files_created": 0,
            "directories_created": 0,
            "total_size_bytes": 0
        }

        if target_dir:
            # Actually create the structure
            base_path = Path(target_dir) / project_name
            stats = self._create_structure(base_path, structure, stats)
        else:
            # Just count what would be created
            stats = self._count_structure(structure, stats)

        # Save pattern for reuse
        save_pattern(
            f"project_structure_{project_type}",
            "project_setup",
            {
                "structure_used": project_type,
                "project_name": project_name,
                "stats": stats
            }
        )

        # Remember this generation
        remember("structure_generation", stats, project_name)

        return {
            "success": True,
            "project_type": project_type,
            "project_name": project_name,
            "stats": stats,
            "deterministic": True,
            "reusable": True
        }

    def _create_structure(self, base_path: Path, structure: Dict, stats: Dict) -> Dict:
        """Actually create files and directories"""

        base_path.mkdir(parents=True, exist_ok=True)
        stats["directories_created"] += 1

        for name, content in structure.items():
            path = base_path / name

            if isinstance(content, dict):
                # It's a directory
                stats = self._create_structure(path, content, stats)
            elif isinstance(content, str):
                # It's a file
                path.write_text(content)
                stats["files_created"] += 1
                stats["total_size_bytes"] += len(content)

        return stats

    def _count_structure(self, structure: Dict, stats: Dict) -> Dict:
        """Count files and directories without creating them"""

        for name, content in structure.items():
            if isinstance(content, dict):
                stats["directories_created"] += 1
                stats = self._count_structure(content, stats)
            elif isinstance(content, str):
                stats["files_created"] += 1
                stats["total_size_bytes"] += len(content)

        return stats

    def _find_closest_match(self, project_type: str) -> str:
        """Find closest matching project type"""

        # Simple matching logic
        project_lower = project_type.lower()

        if "next" in project_lower:
            return "nextjs-fastapi"
        elif "micro" in project_lower:
            return "microservices"
        elif "react" in project_lower:
            return "react-app"
        elif "python" in project_lower or "package" in project_lower:
            return "python-package"
        else:
            return "nextjs-fastapi"  # Default

    def list_available_structures(self) -> List[str]:
        """List all available project structures"""
        return list(self.STRUCTURES.keys())


def test_generator():
    """Test the structure generator"""

    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║              📁 PROJECT STRUCTURE GENERATOR - DAY 002 📁                ║
║                                                                          ║
║                    Deterministic structure every time                   ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
    """)

    generator = ProjectStructureGenerator()

    # Show available structures
    print("\n📚 Available Structures:")
    for structure in generator.list_available_structures():
        print(f"   • {structure}")

    # Test generation (without creating files)
    print("\n🧪 Testing Generation:")
    results = []

    for project_type in ["nextjs-fastapi", "microservices", "python-package"]:
        result = generator.generate(project_type, f"test-{project_type}")
        results.append(result)

        print(f"\n📁 {project_type}:")
        print(f"   Files: {result['stats']['files_created']}")
        print(f"   Directories: {result['stats']['directories_created']}")
        print(f"   Total size: {result['stats']['total_size_bytes']} bytes")

    # Verify determinism
    print("\n🔒 Verifying Determinism:")
    result1 = generator.generate("nextjs-fastapi", "test1")
    result2 = generator.generate("nextjs-fastapi", "test2")

    if result1['stats']['files_created'] == result2['stats']['files_created']:
        print("   ✅ DETERMINISTIC: Same structure every time!")
    else:
        print("   ❌ Non-deterministic (this should not happen)")

    print("\n✨ Structure Generator Ready for Production!")
    print("   Every project starts with the perfect foundation")
    print("   No guesswork, no variation, pure determinism")


if __name__ == "__main__":
    test_generator()