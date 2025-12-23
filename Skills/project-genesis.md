# Skill: Project Genesis
Version: 1.0.0
Category: Project Management
Tags: [initialization, planning, architecture, setup]
Prerequisites: []

## Purpose
Initialize a new project with proper structure, documentation, and orchestration setup. Ensures every project starts with deterministic structure and clear goals.

## Triggers
- "Start a new project"
- "Initialize a [type] application"
- "Create a new [framework] project"
- "Set up a new repository"

## Workflow

### Phase 1: Discovery & Planning
1. **Understand the Vision**
   - What problem does this solve?
   - Who are the users?
   - What are the success criteria?

2. **Check Neural Database**
   - Search for similar projects
   - Identify reusable patterns
   - Learn from past successes/failures

3. **Define Scope**
   - Core features (MVP)
   - Future enhancements
   - Out of scope items

### Phase 2: Architecture Design
1. **Choose Architecture Pattern**
   - Monolith vs Microservices
   - Serverless vs Traditional
   - Event-driven vs Request-response

2. **Technology Stack**
   - Programming language(s)
   - Framework(s)
   - Database(s)
   - Infrastructure

3. **Integration Points**
   - External services
   - APIs needed
   - Data flows

### Phase 3: Project Structure
1. **Create Directory Structure**
   ```
   project-name/
   ├── .claude/           # Claude Code configuration
   │   ├── commands/      # Custom commands
   │   └── prompts/       # Project-specific prompts
   ├── src/               # Source code
   ├── tests/             # Test suites
   ├── docs/              # Documentation
   ├── scripts/           # Automation scripts
   └── config/            # Configuration files
   ```

2. **Initialize Version Control**
   - Create .gitignore
   - Set up branch strategy
   - Define commit conventions

3. **Setup Development Environment**
   - Docker configuration
   - Environment variables
   - Development dependencies

### Phase 4: Documentation
1. **Create README.md**
   - Project overview
   - Quick start guide
   - Architecture overview
   - Contributing guidelines

2. **Technical Documentation**
   - API documentation
   - Database schema
   - Deployment guide
   - Troubleshooting

3. **Project Charter**
   - Goals and objectives
   - Timeline
   - Stakeholders
   - Success metrics

### Phase 5: Quality Assurance
1. **Testing Strategy**
   - Unit tests
   - Integration tests
   - E2E tests
   - Performance tests

2. **CI/CD Pipeline**
   - Build automation
   - Test automation
   - Deployment automation
   - Monitoring setup

3. **Code Quality**
   - Linting rules
   - Formatting standards
   - Code review process
   - Security scanning

### Phase 6: Neural Integration
1. **Register with Neural Database**
   - Create project context
   - Initialize pattern tracking
   - Set up learning events

2. **Connect to SOVEREIGN**
   - Agent configuration
   - Orchestration rules
   - Quality gates

3. **Enable Memory Persistence**
   - Session tracking
   - Decision logging
   - Pattern mining

## Inputs Required
- **Project Name**: Unique identifier
- **Project Type**: web-app, api, library, cli, etc.
- **Primary Language**: Python, JavaScript, Go, etc.
- **Target Users**: Who will use this
- **Core Features**: 3-5 main features

## Expected Outputs
- Complete project structure
- Documentation templates
- Development environment
- CI/CD configuration
- Neural DB integration
- SOVEREIGN orchestration setup

## Success Metrics
- ✅ All directories created
- ✅ README is comprehensive
- ✅ Tests are runnable
- ✅ CI/CD pipeline works
- ✅ Neural DB connected
- ✅ First commit made

## Common Pitfalls
- **Over-engineering**: Start simple, evolve complexity
- **Missing documentation**: Document as you go
- **No tests**: Write tests from day one
- **Ignoring patterns**: Check Neural DB first
- **Scope creep**: Stick to MVP initially

## Example Usage

```bash
/skill project-genesis

# Follow the interactive prompts:
Project Name: awesome-api
Project Type: rest-api
Primary Language: python
Target Users: developers
Core Features: authentication, data-processing, webhooks

# System will:
1. Search Neural DB for similar APIs
2. Create optimal structure
3. Setup FastAPI with best practices
4. Configure Docker & tests
5. Initialize git repository
6. Create comprehensive README
7. Setup CI/CD with GitHub Actions
8. Register with Neural Database
```

## Related Skills
- `/skill api-design` - For API-specific patterns
- `/skill testing-strategy` - For test architecture
- `/skill docker-setup` - For containerization
- `/skill ci-cd-pipeline` - For automation

## Neural Database Patterns
This skill automatically creates these patterns:
- `project_init_[timestamp]` - Project initialization record
- `tech_stack_[project]` - Technology choices
- `architecture_[project]` - Architecture decisions

## Evolution Notes
- v1.1.0 (planned): Add template selection
- v1.2.0 (planned): Multi-language support
- v2.0.0 (planned): AI-driven architecture recommendations