# 🏭 THE FACTORY - Usage Instructions

## Quick Start

### 1. Basic Usage

```bash
# Build from a specification file
python run_factory.py specs/project_spec.md

# Build from a direct prompt
python run_factory.py "Create a REST API for a blog"

# Interactive mode
python run_factory.py
```

### 2. Using Genesis Prime Directly

```bash
# Build with specification
python bootstrap/genesis_prime.py --spec project_spec.md --output ./my_project --build

# Build from prompt
python bootstrap/genesis_prime.py --prompt "Create a todo app" --build

# Validate environment
python bootstrap/genesis_prime.py --validate
```

## Creating Specifications

### Simple Format

Create a markdown file (`my_project.md`):

```markdown
# My Project Name

Brief description of what you want to build.

## Type: web_app
## Complexity: simple

## OBJECTIVES
- Main goal 1
- Main goal 2
- Main goal 3

## FEATURES
### Core Features
- Feature 1
- Feature 2
- Feature 3
```

### Detailed Format

For more control, specify technical details:

```markdown
# Advanced Project

Detailed description here.

## Type: api_service
## Complexity: moderate
## Paradigm: neural

## OBJECTIVES
- Build a scalable API
- Implement authentication
- Add caching layer

## FEATURES
### Core Features
- User management
- Authentication
- Data CRUD operations

### Optional Features
- Rate limiting
- Webhooks
- Analytics

## TECHNICAL SPECIFICATIONS
- **Language**: Python
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Cache**: Redis

## ARCHITECTURE
- **Pattern**: Microservices-ready
- **Scale**: 1000 users initially
- **Security**: JWT authentication

## OUTPUT
- Source code
- Docker configuration
- API documentation
- Tests
- Deployment scripts
```

## Project Types

The Factory supports these project types:

- **web_app**: Full-stack web applications
- **api_service**: REST APIs and microservices
- **cli_tool**: Command-line tools
- **library**: Reusable libraries
- **data_pipeline**: Data processing systems
- **ai_system**: AI/ML applications
- **custom**: Any other type

## Complexity Levels

- **simple**: Small projects (5-10 files)
- **moderate**: Standard projects (20-50 files)
- **complex**: Large projects (50-200 files)
- **extreme**: Enterprise systems (200+ files)

## Examples

### 1. Simple Todo App

```bash
python run_factory.py specs/simple_todo.md
```

### 2. Task Management System

```bash
python run_factory.py specs/project_spec.md
```

### 3. From Prompt

```bash
python run_factory.py "Create a blog platform with user authentication, comments, and categories"
```

### 4. Custom Output Directory

```bash
python bootstrap/genesis_prime.py --spec my_spec.md --output /path/to/output --build
```

## Output Structure

The Factory creates a complete project structure:

```
outputs/your_project/
├── src/                  # Source code
├── tests/               # Test files
├── docs/                # Documentation
├── config/              # Configuration files
├── scripts/             # Utility scripts
├── README.md            # Project documentation
├── requirements.txt     # Dependencies (Python)
├── package.json        # Dependencies (Node.js)
├── docker-compose.yml  # Docker configuration
└── .gitignore          # Git ignore file
```

## Advanced Features

### Resume from Checkpoint

If a build is interrupted:

```bash
python bootstrap/genesis_prime.py --resume checkpoint_id
```

### Specify Orchestration Paradigm

```bash
python bootstrap/genesis_prime.py --spec spec.md --paradigm neural --build
```

### Set Complexity Level

```bash
python bootstrap/genesis_prime.py --spec spec.md --complexity complex --build
```

## Troubleshooting

### Environment Validation

Check if The Factory is properly configured:

```bash
python bootstrap/genesis_prime.py --validate
```

### Common Issues

1. **Import errors**: Run `python make_standalone.py` to set up standalone mode
2. **Missing dependencies**: Install with `pip install -r requirements.txt`
3. **Permission errors**: Ensure write access to output directory
4. **Spec not found**: Check file path and ensure file exists

## System Modes

The Factory operates in three modes:

1. **Integrated Mode**: Full SOVEREIGN system available
2. **Standalone Mode**: Using local lib/ directory
3. **Minimal Mode**: Basic fallback implementations only

The system automatically detects and uses the best available mode.

## Tips for Best Results

1. **Be Specific**: Detailed specifications produce better results
2. **Use Examples**: Provide example data or UI mockups in your spec
3. **Define Success**: Clearly state what constitutes a successful build
4. **Specify Tech Stack**: If you have preferences, state them clearly
5. **Include Quality Requirements**: Mention testing, documentation, and performance needs

## Getting Help

- Check the documentation in `docs/`
- Review example specifications in `specs/`
- Look at the architecture in `ARCHITECTURE_DECISIONS.md`
- Review the detailed analysis in `DETAILED_ANALYSIS.md`

---

*The Factory - Building the builders that build themselves* 🏗️