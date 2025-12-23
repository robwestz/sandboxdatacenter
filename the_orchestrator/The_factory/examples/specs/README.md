# 💡 Example Specifications

Real-world examples of optimal Factory specifications for different project types.

## Files

### gui_project_spec.md
**Complete commercial-grade SaaS platform specification.**

A full-scale example demonstrating:
- Hybrid orchestration (all paradigms)
- 200 agents across 7 layers
- Commercial features (subscriptions, billing, multi-tenancy)
- Enterprise security
- Production deployment
- 15,000-20,000 LOC target

**Complexity:** Very High
**Estimated time:** 4-5 hours
**Quality:** Commercial-grade

**Use for:**
- Learning advanced specification patterns
- Building production SaaS platforms
- Understanding enterprise requirements
- Showcasing Factory capabilities

### How to use examples:

**Option 1: Direct use**
```bash
cp examples/specs/gui_project_spec.md projects/my-project/project_spec.md
python run_factory.py --project projects/my-project
```

**Option 2: As template**
```bash
# Copy and modify for your needs
cp examples/specs/gui_project_spec.md projects/my-project/project_spec.md
nano projects/my-project/project_spec.md
# Adjust features, tech stack, complexity
python run_factory.py --project projects/my-project
```

**Option 3: Learning reference**
Study these specs to understand:
- How to structure hierarchical decomposition
- How to trigger parallel teams
- How to create quality cascades
- How to define integration points
- How to allocate resources efficiently

## Complexity Levels

- **Simple (10-20 agents, 10-30 min):** Basic CRUD apps, CLIs
- **Medium (30-80 agents, 1-3 hours):** Full-stack web apps with auth
- **Complex (100-200 agents, 3-6 hours):** SaaS platforms, microservices

More examples coming soon!
