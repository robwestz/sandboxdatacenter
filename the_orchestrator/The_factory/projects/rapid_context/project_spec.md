# RAPID CONTEXT - REVOLUTIONARY CODEBASE UNDERSTANDING SYSTEM

```yaml
_meta:
  paradigm: "neural"                          # Pattern recognition for code analysis
  orchestration_style: "aggressive"           # Maximum speed
  quality_tolerance: "standard"               # Balance speed vs accuracy
  optimization_rounds: 2                      # Quick refinement
  learning_enabled: true                      # Learn from analysis patterns
  token_efficiency: "maximum"                 # Critical requirement

_constraints:
  max_agents: 30                              # Lightweight, focused team
  max_build_time: "10 minutes"                # Ultra-fast delivery
  target_loc: "2000-3000"                     # Compact, efficient code
  min_test_coverage: 80                       # Reliable but not excessive
  token_budget: "minimal"                     # Core innovation constraint

_behaviors:
  on_analysis: "spawn_pattern_recognizer"     # Identify code patterns instantly
  on_discovery: "spawn_indexer"               # Build structural map
  on_understanding: "spawn_suggestion_engine" # Generate improvement ideas
  on_completion: "cache_learnings"            # Reuse knowledge

project:
  name: "Rapid Context"
  tagline: "Understand Any Codebase in Seconds, Not Minutes"
  type: "cli_tool_with_library"
  market: "developers_and_ai_agents"
```

---

## PRIMARY DIRECTIVE

Build an **ultra-fast, token-efficient codebase analysis tool** that revolutionizes how AI agents understand code repositories. This tool must complete analysis in **seconds instead of minutes** by using intelligent sampling, pattern recognition, and structural inference rather than exhaustive reading.

**Core Innovation:**
- Traditional `/init`: Reads everything, takes 2-5 minutes, uses 50k+ tokens
- **Rapid Context**: Samples intelligently, takes 10-30 seconds, uses <5k tokens
- Provides 80% of the value at 10% of the cost

---

## PROBLEM STATEMENT

**Current Pain Points:**
1. **Claude Code's /init is slow** - Takes minutes to analyze codebases
2. **Token inefficient** - Burns through context budget before actual work
3. **No incremental understanding** - Must re-analyze on every session
4. **Missing gap analysis** - Doesn't highlight what's incomplete/broken
5. **No actionable suggestions** - Just describes, doesn't propose improvements

**Our Solution:**
A lightweight CLI tool that:
- Analyzes folder structure in <5 seconds
- Identifies file purposes through pattern matching (not full reads)
- Detects missing components via architectural inference
- Generates top 10 actionable ideas using existing code patterns
- Outputs concise markdown suitable for LLM context (<3k tokens)

---

## CORE FEATURES

### Feature 1: Lightning-Fast Structure Analysis (5 agents)

**What:** Map entire codebase structure without reading every file

**How:**
```yaml
Strategy: Smart Sampling
  - Read directory tree (instant)
  - Identify file types by extension
  - Sample 1 file per directory type (e.g., one .tsx, one .py)
  - Infer patterns from samples
  - Use naming conventions to guess purposes

Techniques:
  - Convention detection: (src/, lib/, tests/, docs/)
  - Framework detection: (package.json → Node, requirements.txt → Python)
  - Pattern matching: (*_test.py → test file, index.* → entry point)
  - Structural inference: (routes/ → routing, components/ → UI)
```

**Output Example:**
```markdown
## Structure Map
- Framework: React + FastAPI (detected from package.json + requirements.txt)
- Entry Points: src/index.tsx, backend/main.py
- Components: 23 React components in src/components/
- API Endpoints: 8 routes in backend/routes/
- Tests: 15 test files (Jest + Pytest)
- Missing: Docker setup, CI/CD config
```

### Feature 2: Purpose Inference Engine (8 agents)

**What:** Understand what each file/folder does WITHOUT reading full content

**How:**
```yaml
Smart Analysis:
  1. Read first 10 lines of each file type sample
  2. Extract imports/exports
  3. Identify patterns:
     - Class definitions → Object models
     - Function signatures → API contracts
     - Import statements → Dependencies
  4. Cross-reference to build understanding

Example:
  File: user_service.py
  First 10 lines: "from fastapi import APIRouter\nfrom .models import User"
  Inference: "User management API service using FastAPI models"
```

**Output Example:**
```markdown
## Purpose Analysis
- `src/components/UserList.tsx` - UI component for displaying user tables
- `backend/services/auth.py` - JWT authentication service
- `backend/models/user.py` - User database model (SQLAlchemy)
- `lib/utils/validation.py` - Input validation utilities
```

### Feature 3: Gap Detection System (5 agents)

**What:** Identify what's MISSING for system to be complete/functional

**How:**
```yaml
Architectural Patterns:
  Web App Expected:
    - Frontend, Backend, Database, Tests, Deployment

  Check Each Layer:
    ✓ Frontend exists → src/
    ✓ Backend exists → backend/
    ✗ Database migrations missing → No migrations/ folder
    △ Tests incomplete → Only 60% of files have test counterparts
    ✗ Deployment missing → No Dockerfile, docker-compose.yml
    ✗ Documentation incomplete → No API docs, outdated README

  Cross-Reference Patterns:
    - If auth.py exists but no tests/test_auth.py → Missing auth tests
    - If User model exists but no migrations → Missing user table migration
    - If API routes but no OpenAPI spec → Missing API documentation
```

**Output Example:**
```markdown
## Missing Components
1. **Database Migrations** - Models exist but no migration system
2. **API Documentation** - 8 endpoints lack OpenAPI/Swagger specs
3. **Error Handling** - No global error handler in FastAPI
4. **Docker Setup** - No containerization for deployment
5. **CI/CD Pipeline** - No GitHub Actions or similar
6. **Test Coverage** - Only 60% of backend code has tests
7. **Logging** - No structured logging system
8. **Monitoring** - No health check endpoints
```

### Feature 4: Intelligent Suggestion Engine (10 agents)

**What:** Generate top 10 actionable ideas using existing code patterns

**How:**
```yaml
Pattern Recognition:
  1. Analyze existing code style/patterns
  2. Identify what works well
  3. Detect repeated patterns that could be DRY'd
  4. Find opportunities for new features using existing components
  5. Suggest architectural improvements based on current structure

Suggestion Categories:
  - Missing Features (using existing patterns)
  - Code Improvements (refactoring opportunities)
  - New Tools/Utilities (based on current needs)
  - Architecture Enhancements (scalability/maintainability)
  - Quality Improvements (tests, docs, monitoring)

Prioritization:
  - High Impact + Low Effort = Top priority
  - Leverage existing code = Higher ranking
  - Fill critical gaps = Elevated priority
```

**Output Example:**
```markdown
## Top 10 Actionable Ideas

### 1. User Export Feature (High Impact, Low Effort)
**Why:** You have User model + CSV utility in lib/
**How:** Combine existing UserService.get_all() + csv_writer()
**Effort:** 30 minutes | **Files:** 1 new endpoint, 1 test

### 2. Automated API Documentation
**Why:** 8 endpoints exist but no docs
**How:** Add FastAPI OpenAPI auto-generation (built-in)
**Effort:** 15 minutes | **Files:** main.py config

### 3. User Search Endpoint
**Why:** UserList.tsx has search UI but no backend
**How:** Add to user_service.py using existing DB patterns
**Effort:** 45 minutes | **Files:** 1 endpoint, 1 test

### 4. Docker Development Environment
**Why:** Team setup is manual and error-prone
**How:** Dockerfile + docker-compose.yml for all services
**Effort:** 1 hour | **Files:** 2 new configs

### 5. Reusable Form Validation Hook
**Why:** Validation logic repeated in 5+ components
**How:** Extract to custom React hook using existing validators
**Effort:** 30 minutes | **Files:** 1 new hook, update 5 components

### 6. Database Migration System
**Why:** Models exist but schema changes are manual
**How:** Add Alembic, generate initial migration from models
**Effort:** 1 hour | **Files:** migrations/ folder, config

### 7. Generic Error Handler Middleware
**Why:** Error handling duplicated across routes
**How:** FastAPI middleware using existing error patterns
**Effort:** 30 minutes | **Files:** 1 middleware, update main.py

### 8. Logging Utility Wrapper
**Why:** print() statements everywhere, hard to debug
**How:** Structured logging using your existing config pattern
**Effort:** 45 minutes | **Files:** 1 logger util, update 10 files

### 9. Health Check Endpoint
**Why:** No way to monitor service status
**How:** Simple /health endpoint checking DB + dependencies
**Effort:** 20 minutes | **Files:** 1 endpoint

### 10. Component Storybook
**Why:** 23 components, no visual documentation
**How:** Storybook setup for React components
**Effort:** 2 hours | **Files:** Storybook config, stories per component
```

### Feature 5: Token-Efficient Output Format (2 agents)

**What:** Generate ultra-concise markdown optimized for LLM context

**How:**
```yaml
Optimization Techniques:
  - Use bullet points, not prose
  - Abbreviate where clear (e.g., "DB" not "Database")
  - Group related items
  - Use symbols (✓✗△) instead of words
  - Code examples only when adding value
  - Omit obvious information
  - Prioritize actionable over descriptive

Target: <3000 tokens for typical project
Compare: /init often 20k-50k tokens
Savings: 85-90% token reduction
```

---

## TECHNICAL ARCHITECTURE

### System Components

```yaml
architecture:
  cli_tool:                                   # 30% of effort
    entry_point: rapid-context
    commands:
      - analyze <path>                        # Main command
      - watch <path>                          # Continuous monitoring
      - diff <path1> <path2>                  # Compare two states
      - export <format>                       # JSON, Markdown, HTML

  analysis_engine:                            # 40% of effort
    components:
      - structure_mapper:
          strategy: "Directory tree + sampling"
          speed: "<2 seconds for 1000 files"

      - purpose_inferencer:
          strategy: "Pattern matching + first-N-lines"
          models: "Convention rules + heuristics"

      - gap_detector:
          strategy: "Expected vs Actual comparison"
          patterns: "Framework-specific templates"

      - suggestion_engine:
          strategy: "Pattern recognition + combination"
          ranking: "Impact × (1/Effort) × CodeReuse"

  output_generator:                           # 20% of effort
    formats:
      - markdown: "Primary, LLM-optimized"
      - json: "Machine-readable for tools"
      - html: "Human-readable reports"

  cache_system:                               # 10% of effort
    purpose: "Incremental analysis, reuse learnings"
    storage: ".rapid-context/ folder"
    invalidation: "On file changes (watch mode)"
```

### Technology Stack

```yaml
tech_stack:
  language: Python 3.11+

  core_libraries:
    - click: "CLI framework"
    - tree-sitter: "Fast syntax parsing (optional, for advanced)"
    - pathlib: "Path operations"
    - jinja2: "Template engine for output"
    - pyyaml: "Config file support"

  optional_enhancements:
    - watchdog: "File system monitoring"
    - rich: "Beautiful terminal output"
    - pygments: "Syntax highlighting"

  packaging:
    - poetry: "Dependency management"
    - pyinstaller: "Single-binary distribution"
```

---

## IMPLEMENTATION STRATEGY

### Phase 1: Core Engine (40% of effort, 3-4 minutes)

**Team Alpha: Structure Mapper (3 agents)**
```python
# Pseudo-implementation
class StructureMapper:
    def map_directory(path: Path) -> StructureMap:
        # 1. Build file tree (os.walk)
        # 2. Group by extension
        # 3. Detect framework (check for marker files)
        # 4. Identify entry points (main.*, index.*, __init__.*)
        # 5. Return structured map

    def sample_files(structure: StructureMap) -> Dict[str, File]:
        # Sample 1 file per directory per type
        # Priority: Entry points > Common patterns > Random
```

**Team Beta: Purpose Inferencer (5 agents)**
```python
class PurposeInferencer:
    def infer_purpose(file: File) -> Purpose:
        # 1. Read first N lines (N=10 default)
        # 2. Extract imports/exports
        # 3. Match against pattern library
        # 4. Assign confidence score

    def build_dependency_graph(files: List[File]) -> Graph:
        # Cross-reference imports to understand relationships
```

### Phase 2: Intelligence Layer (40% of effort, 3-4 minutes)

**Team Gamma: Gap Detector (3 agents)**
```python
class GapDetector:
    def detect_gaps(structure: StructureMap, purposes: Dict) -> List[Gap]:
        # 1. Load framework template (e.g., "react-fastapi")
        # 2. Compare expected vs actual
        # 3. Find missing components
        # 4. Identify incomplete implementations
```

**Team Delta: Suggestion Engine (7 agents)**
```python
class SuggestionEngine:
    def generate_suggestions(structure, purposes, gaps) -> List[Suggestion]:
        # 1. Pattern recognition (find reusable components)
        # 2. Gap filling (suggest missing pieces)
        # 3. Improvement opportunities (refactoring)
        # 4. Feature ideas (combine existing code)
        # 5. Rank by impact/effort/code_reuse
        # 6. Return top 10
```

### Phase 3: Output & UX (20% of effort, 2-3 minutes)

**Team Epsilon: Output Generator (2 agents)**
```python
class OutputGenerator:
    def generate_markdown(analysis: Analysis) -> str:
        # Use Jinja2 templates
        # Optimize for token efficiency
        # Include only actionable information

    def estimate_tokens(markdown: str) -> int:
        # Rough estimation: words * 1.3
        # Ensure <3k target
```

---

## REVOLUTIONARY FEATURES

### 1. Incremental Understanding (Watch Mode)
```yaml
Innovation: "Continuous analysis as code changes"

How it works:
  - Initial analysis cached in .rapid-context/
  - File watcher detects changes
  - Re-analyze only changed files + dependents
  - Update delta report

Use case:
  Developer makes changes → Auto-update understanding
  Agent session continues → Fresh context without re-init
```

### 2. Pattern Library System
```yaml
Innovation: "Learns common patterns, reuses knowledge"

Patterns detected:
  - "FastAPI + SQLAlchemy" → Expect models/, routes/, migrations/
  - "React + TypeScript" → Expect components/, hooks/, types/
  - "Pytest pattern" → test_*.py parallel to source files

Learning:
  - Successful analyses cached
  - User corrections stored
  - Pattern library grows over time
```

### 3. Differential Analysis
```yaml
Innovation: "Compare two codebases or states"

Use cases:
  - Before/after refactoring
  - Feature branch vs main
  - Two different projects (identify reusable components)

Command: rapid-context diff ./project-v1 ./project-v2
Output: What's new, what's removed, what's changed
```

### 4. Export for AI Agents
```yaml
Innovation: "Perfect format for LLM consumption"

Optimizations:
  - Hierarchical structure (easy to skim)
  - Actionable focus (not just descriptive)
  - Token-counted (stays within budgets)
  - Copy-paste ready (markdown code blocks)

Integration:
  - Paste into Claude/GPT prompt
  - Use as project context
  - Feed into autonomous agents
```

---

## OUTPUT EXAMPLES

### Example 1: Small Project (~50 files)

```markdown
# Rapid Context Analysis - Todo App

**Analyzed:** 47 files in 3.2 seconds | **Tokens:** ~1,200

## Stack
React 18 + FastAPI + SQLite | Docker ready

## Structure
```
✓ Frontend (React): 18 components, 5 hooks
✓ Backend (FastAPI): 4 endpoints, 2 models
△ Tests: 8 files (60% coverage)
✗ Deployment: No CI/CD
```

## Purpose Map
- `/src/App.tsx` - Main app, routing
- `/src/components/TodoList.tsx` - Todo display/edit
- `/backend/main.py` - API entry, 4 CRUD endpoints
- `/backend/models.py` - Todo + User models

## Missing
1. User authentication (models exist, no implementation)
2. Database migrations (using SQLAlchemy but no Alembic)
3. Error handling (no global error boundary)
4. API tests (only frontend tested)

## Top 5 Ideas
1. **Add Todo Filtering** - Frontend has search UI, no backend (20min)
2. **User Login** - Models ready, add JWT auth (1hr)
3. **Docker Compose** - Dockerfile exists, add compose (15min)
4. **API Docs** - Enable FastAPI OpenAPI (5min)
5. **Todo Categories** - Extend model + UI component pattern (45min)
```

### Example 2: Large Project (~500 files)

```markdown
# Rapid Context Analysis - E-commerce Platform

**Analyzed:** 487 files in 12.8 seconds | **Tokens:** ~2,800

## Stack
Next.js + NestJS + PostgreSQL + Redis | Kubernetes ready

## Structure (Monorepo)
```
✓ Frontend: 78 components, 23 pages, 15 hooks
✓ Backend: 34 modules, 12 microservices
✓ Tests: 156 files (82% coverage)
✓ Infra: K8s configs, Terraform
△ Docs: API documented, architecture outdated
```

## Microservices Map
1. **user-service** - Auth, profiles (NestJS + PostgreSQL)
2. **product-service** - Catalog, search (NestJS + Elasticsearch)
3. **order-service** - Cart, checkout (NestJS + PostgreSQL + Stripe)
4. **notification-service** - Email, SMS (NestJS + Redis queue)

## Missing
1. Service mesh (microservices exist, no Istio/Linkerd)
2. Distributed tracing (no Jaeger/OpenTelemetry)
3. Rate limiting (exposed APIs lack protection)
4. Database backup automation (manual only)
5. Load testing suite (no performance benchmarks)

## Top 10 Ideas
1. **Admin Dashboard** - Reuse components from customer UI (2hrs)
2. **Product Recommendations** - Combine order history + ML model stub (3hrs)
3. **Inventory Alerts** - Use existing product service + notification (1hr)
4. **Checkout Analytics** - Track abandonment using current events (1hr)
5. **Bulk Product Import** - CSV upload using existing product create (2hrs)
6. **User Wishlists** - New table + reuse product display components (2hrs)
7. **Discount Code System** - Extend order service, UI exists (3hrs)
8. **GraphQL Gateway** - Unify microservices with Apollo (4hrs)
9. **Real-time Inventory** - WebSocket on product service (2hrs)
10. **Multi-currency Support** - Extend order service with rates API (3hrs)
```

---

## DELIVERABLES

```yaml
outputs:
  cli_tool:
    - rapid-context (executable binary)
    - Configuration: .rapidcontext.yml (optional customization)

  python_library:
    - rapid_context/ package (importable for custom use)
    - API for programmatic access

  documentation:
    - README.md (Quick start, examples)
    - CLI_REFERENCE.md (All commands, flags)
    - PATTERNS.md (Supported frameworks, extending patterns)
    - API_DOCS.md (Python library usage)

  tests:
    - Unit tests (80% coverage)
    - Integration tests (CLI commands)
    - Performance benchmarks (speed tests)

  examples:
    - Example analyses for common project types
    - Sample output formats
    - Integration scripts (use in CI/CD)
```

---

## SUCCESS METRICS

```yaml
performance_targets:
  speed:
    - Small project (<100 files): <5 seconds
    - Medium project (100-1000 files): <15 seconds
    - Large project (1000-5000 files): <60 seconds

  token_efficiency:
    - Output size: <3000 tokens for typical project
    - Reduction vs /init: >85%

  accuracy:
    - Structure mapping: 95%+ accuracy
    - Purpose inference: 80%+ accuracy
    - Gap detection: 70%+ recall
    - Suggestion relevance: 70%+ user approval

quality_targets:
  - All code type-hinted (Python 3.11+)
  - 80%+ test coverage
  - Zero external dependencies for core (optional for enhancements)
  - Single-binary distribution option
  - Cross-platform (Windows, Mac, Linux)
```

---

## USAGE EXAMPLES

### Basic Analysis
```bash
# Analyze current directory
rapid-context analyze .

# Analyze specific path
rapid-context analyze /path/to/project

# Output to file
rapid-context analyze . --output analysis.md

# JSON format (for tools)
rapid-context analyze . --format json
```

### Watch Mode (Continuous)
```bash
# Monitor for changes, update analysis
rapid-context watch .

# Watch and serve via HTTP (for IDE integration)
rapid-context watch . --serve 8080
```

### Differential Analysis
```bash
# Compare two states
rapid-context diff ./before ./after

# Compare branches
rapid-context diff --git main feature-branch
```

### Custom Configuration
```yaml
# .rapidcontext.yml
sampling:
  lines_per_file: 15          # Read first N lines
  files_per_dir: 2            # Sample N files per directory

ignore:
  - node_modules/
  - .git/
  - dist/
  - build/

patterns:
  custom:
    - pattern: "*_controller.py"
      purpose: "API controller"
    - pattern: "use*.tsx"
      purpose: "React custom hook"

suggestions:
  max_count: 10
  min_impact: "medium"
  max_effort: "4 hours"
```

---

## ANTI-REQUIREMENTS

```yaml
do_not_build:
  - ✗ Full AST parsing (too slow, use tree-sitter selectively)
  - ✗ AI/LLM integration (keep it deterministic, fast, offline)
  - ✗ Code execution (security risk, not needed)
  - ✗ Full file content indexing (defeats token efficiency)
  - ✗ GUI application (CLI + library only)
  - ✗ Cloud service (local-first tool)
  - ✗ Database requirement (filesystem + cache only)
```

---

## FUTURE ENHANCEMENTS (Out of Scope for v1.0)

```yaml
potential_v2_features:
  - IDE integration (VSCode extension)
  - GitHub Action (auto-comment on PRs)
  - API server mode (HTTP API for tooling)
  - Machine learning suggestions (beyond pattern matching)
  - Multi-repo analysis (monorepo support)
  - Collaboration features (shared analyses)
  - Visualization (interactive graphs)
```

---

## COMPETITIVE ADVANTAGE

**vs Claude Code /init:**
- **10-20x faster** (seconds vs minutes)
- **90% less tokens** (<3k vs 20-50k)
- **Gap detection** (tells you what's missing)
- **Actionable suggestions** (not just description)

**vs GitHub Copilot Workspace:**
- **Offline-first** (no cloud dependency)
- **Deterministic** (consistent results)
- **Extensible** (pattern library, customization)
- **Privacy** (code stays local)

**vs Manual README:**
- **Always current** (generated on demand)
- **Comprehensive** (doesn't miss hidden patterns)
- **Structured** (consistent format)
- **Actionable** (includes suggestions, not just description)

---

## FINAL NOTES

This tool represents a **paradigm shift** in how AI agents understand codebases:

**Traditional:** Read everything → Slow, expensive
**Rapid Context:** Sample smartly → Fast, cheap, good enough

**Key Insight:** You don't need to read every line to understand what a project does. Conventions, structure, and sampling give you 80% of the picture in 10% of the time.

**Target Users:**
1. AI Agents (Claude, GPT) - Fast context loading
2. Developers - Quick codebase orientation
3. Teams - Onboarding new members
4. Tools - Automated analysis in CI/CD

**Success Definition:**
When developers and AI agents reach for Rapid Context FIRST before diving into code - we've won.

---

**END OF SPECIFICATION**

*Build this in under 10 minutes. Make it blazing fast. Make it indispensable.*
