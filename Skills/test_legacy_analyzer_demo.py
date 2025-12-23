#!/usr/bin/env python3
"""
Demo test for Legacy Analyzer - works without API keys
Shows the structure and capabilities
"""

import sys
from pathlib import Path
import json

# Add MEMORY_CORE to path
sys.path.insert(0, str(Path(__file__).parent.parent / "MEMORY_CORE"))
from memory_manager import remember, save_pattern

def demo_legacy_analyzer():
    """Demo the Legacy Analyzer without requiring API keys"""

    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║               🔍 LEGACY ANALYZER - DEMO MODE 🔍                         ║
║                                                                          ║
║            Demonstrating capabilities without API keys                  ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
    """)

    # Simulate analyzing a legacy codebase
    demo_analysis = {
        "overview": {
            "total_files": 847,
            "total_lines": 125000,
            "languages": ["Java", "JavaScript", "SQL"],
            "frameworks": ["Spring Boot 1.x", "jQuery", "Oracle DB"],
            "age_estimate": "8-10 years"
        },
        "tech_debt": {
            "score": 8.5,
            "critical_issues": [
                "Outdated Spring Boot version (1.x)",
                "No test coverage",
                "Hardcoded credentials found",
                "SQL injection vulnerabilities"
            ],
            "estimated_fix_hours": 2400
        },
        "migration_complexity": {
            "score": "HIGH",
            "reasons": [
                "Tightly coupled architecture",
                "Custom ORM implementation",
                "No documentation"
            ]
        },
        "business_impact": {
            "current_maintenance_cost": "$300,000/year",
            "downtime_risk": "HIGH",
            "security_vulnerabilities": 23
        }
    }

    print("📂 Analyzing legacy system...")
    print("\n📊 Analysis Results:")
    print(f"   Total files: {demo_analysis['overview']['total_files']}")
    print(f"   Total lines: {demo_analysis['overview']['total_lines']:,}")
    print(f"   Tech debt score: {demo_analysis['tech_debt']['score']}/10")
    print(f"   Critical issues: {len(demo_analysis['tech_debt']['critical_issues'])}")

    # Generate migration plan
    demo_migration_plan = {
        "phases": [
            {
                "phase": 1,
                "name": "Foundation & Testing",
                "duration": "2 months",
                "cost": "$50,000",
                "tasks": [
                    "Add comprehensive test suite",
                    "Set up CI/CD pipeline",
                    "Document existing functionality"
                ]
            },
            {
                "phase": 2,
                "name": "Security & Updates",
                "duration": "1 month",
                "cost": "$25,000",
                "tasks": [
                    "Fix security vulnerabilities",
                    "Update dependencies",
                    "Remove hardcoded credentials"
                ]
            },
            {
                "phase": 3,
                "name": "Architecture Modernization",
                "duration": "3 months",
                "cost": "$75,000",
                "tasks": [
                    "Migrate to Spring Boot 3.x",
                    "Implement microservices",
                    "Containerize with Docker"
                ]
            }
        ],
        "total_cost": "$150,000",
        "total_duration": "6 months",
        "roi_timeline": "12 months"
    }

    print("\n📋 Migration Plan Generated:")
    for phase in demo_migration_plan['phases']:
        print(f"   Phase {phase['phase']}: {phase['name']}")
        print(f"      Duration: {phase['duration']}")
        print(f"      Cost: {phase['cost']}")

    # Calculate ROI
    current_cost = 300000
    new_cost = 150000
    savings = current_cost - new_cost

    print("\n💰 ROI Analysis:")
    print(f"   Current yearly cost: ${current_cost:,}")
    print(f"   Migration cost: ${new_cost:,}")
    print(f"   First year savings: ${savings:,}")
    print(f"   ROI: {(savings/new_cost)*100:.0f}%")
    print(f"   Payback period: {new_cost/savings*12:.0f} months")

    # Save demo results
    remember("demo_analysis", demo_analysis, "legacy_demo")
    save_pattern("legacy_migration_demo", "demo", demo_migration_plan)

    print("\n✅ Demo Analysis Complete!")
    print("\n🎯 Value Proposition:")
    print("   • Turn $300k/year maintenance into $30k/year")
    print("   • Eliminate security vulnerabilities")
    print("   • Enable 10x faster feature development")
    print("   • Future-proof your technology stack")

    print("\n📞 Ready to analyze YOUR legacy system?")
    print("   With real API keys, this tool provides:")
    print("   • AI-powered code analysis")
    print("   • Detailed migration roadmaps")
    print("   • Accurate cost estimates")
    print("   • Risk assessments")

    return demo_analysis, demo_migration_plan

if __name__ == "__main__":
    demo_legacy_analyzer()