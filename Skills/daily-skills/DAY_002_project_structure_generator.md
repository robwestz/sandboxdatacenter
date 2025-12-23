# Day 002: Project Structure Generator
*Created: 2024-12-22*
*Value: Ensures deterministic project structure every time*

## Skill Definition
Generates perfect project structure based on project type, ensuring every project starts with the optimal foundation.

## Why This Matters for THE_DATAZENtr
- **Determinism**: Same project type ALWAYS gets same structure
- **No Guessing**: Agents don't need to "figure out" structure
- **Pattern Library**: Each structure becomes a reusable pattern
- **Time Saved**: 30-60 minutes per project

## Trigger Phrases
- "create project structure for [type]"
- "setup [framework] project"
- "initialize repository structure"
- "scaffold new application"

## Core Functionality
```python
class ProjectStructureGenerator:
    """Deterministic project structure generation"""

    STRUCTURES = {
        "nextjs-fastapi": {
            "frontend/": {
                "app/": ["layout.tsx", "page.tsx"],
                "components/": ["ui/", "shared/"],
                "lib/": ["api.ts", "utils.ts"],
                "public/": [],
                "styles/": ["globals.css"]
            },
            "backend/": {
                "app/": ["main.py", "models.py", "schemas.py"],
                "api/": ["endpoints/", "deps.py"],
                "core/": ["config.py", "security.py"],
                "services/": [],
                "tests/": []
            },
            "shared/": {
                "types/": ["index.ts"],
                "constants/": ["index.ts"]
            },
            "docker/": ["Dockerfile.frontend", "Dockerfile.backend"],
            "": ["docker-compose.yml", ".env.example", "README.md"]
        },

        "microservices": {
            "services/": {
                "auth/": ["src/", "tests/", "Dockerfile"],
                "api-gateway/": ["src/", "tests/", "Dockerfile"],
                "user-service/": ["src/", "tests/", "Dockerfile"],
                "notification/": ["src/", "tests/", "Dockerfile"]
            },
            "infrastructure/": {
                "kubernetes/": ["deployments/", "services/", "configmaps/"],
                "terraform/": ["modules/", "environments/"],
                "scripts/": ["deploy.sh", "rollback.sh"]
            },
            "shared/": {
                "proto/": [],
                "libs/": []
            },
            "": ["docker-compose.yml", "Makefile", "README.md"]
        },

        "python-package": {
            "src/": {
                "package_name/": ["__init__.py", "core.py", "utils.py"],
            },
            "tests/": ["test_core.py", "test_utils.py"],
            "docs/": ["conf.py", "index.md"],
            "examples/": ["basic_usage.py"],
            "": ["setup.py", "pyproject.toml", "README.md", "LICENSE"]
        },

        "enterprise-api": {
            "src/": {
                "api/": ["controllers/", "middleware/", "validators/"],
                "domain/": ["entities/", "repositories/", "services/"],
                "infrastructure/": ["database/", "cache/", "queue/"],
                "application/": ["commands/", "queries/", "events/"]
            },
            "tests/": {
                "unit/": [],
                "integration/": [],
                "e2e/": []
            },
            "config/": ["default.json", "production.json", "test.json"],
            "scripts/": ["migrate.js", "seed.js"],
            "": [".env.example", "Dockerfile", "docker-compose.yml"]
        }
    }

    def generate(self, project_type: str, name: str) -> dict:
        """Generate structure for project type"""

        if project_type not in self.STRUCTURES:
            # Find closest match
            project_type = self.find_closest_match(project_type)

        structure = self.STRUCTURES[project_type]

        # Save pattern for future use
        save_pattern(
            f"project_structure_{project_type}",
            "project_setup",
            {"structure": structure, "used_for": name}
        )

        return {
            "structure": structure,
            "files_created": self.count_files(structure),
            "type": project_type,
            "deterministic": True
        }

    def count_files(self, structure: dict) -> int:
        """Count total files in structure"""
        count = 0
        for key, value in structure.items():
            if isinstance(value, list):
                count += len(value)
            elif isinstance(value, dict):
                count += self.count_files(value)
        return count
```

## Integration with Memory
```python
# Structure is saved and reused
from MEMORY_CORE.memory_manager import remember, recall

# Save successful structure
remember("project_structure", {
    "type": "nextjs-fastapi",
    "project": "datazentr-webapp",
    "success": True
})

# Recall for similar projects
patterns = recall("project_structure", "nextjs-fastapi")
```

## Example Usage
```bash
# Generate structure
python -c "
from Skills.daily_skills.day_002 import ProjectStructureGenerator
gen = ProjectStructureGenerator()
structure = gen.generate('nextjs-fastapi', 'my-app')
print(f'Created {structure['files_created']} files/folders')
"
```

## Success Metrics
- Structure generation: <2 seconds
- Consistency: 100% (same input = same output)
- Time saved: 30-60 minutes per project
- Pattern reuse: Increases with each use

## Contribution to Determinism
This skill ensures that:
1. **No Variation**: Same project type ALWAYS gets same structure
2. **No Decisions**: Structure is pre-determined, not invented
3. **Pattern Growth**: Each use improves the pattern library
4. **Future Proof**: New project types can be added without changing logic

## Link to Monetization
- Enterprises pay for consistency
- Reduces onboarding time for new developers
- Part of the "Project Genesis" product ($10k value)