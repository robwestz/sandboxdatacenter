#!/usr/bin/env python3
"""
Enhanced Migration Analyzer v0.2
Nu med Neural DB integration - den lär sig!
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Lägg till THE_SERVER_ROOM till path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "The_orchestrator" / "THE_SERVER_ROOM"))

try:
    from neural_db import NeuralMemoryManager
    NEURAL_ENABLED = True
except ImportError:
    print("⚠️  Neural DB not available - running in basic mode")
    NEURAL_ENABLED = False

from simple_migration import SimpleMigrationAnalyzer, create_demo_output

class SmartMigrationAnalyzer(SimpleMigrationAnalyzer):
    """
    Version 0.2 - Nu med minne!
    """

    def __init__(self, legacy_path: str):
        super().__init__(legacy_path)
        self.memory = NeuralMemoryManager() if NEURAL_ENABLED else None
        self.patterns_found = []

    async def analyze_with_memory(self) -> Dict:
        """Analysera och lär från tidigare projekt"""

        # Kör basic analysis
        analysis = self.scan_project()

        if self.memory:
            await self.memory.initialize()

            # Sök efter liknande projekt
            print("🧠 Searching neural memory for similar projects...")
            similar = await self.memory.recall(
                f"PHP migration {analysis['total_lines']} lines {analysis['complexity']}"
            )

            if similar:
                print(f"💡 Found {len(similar)} similar migration patterns!")
                for pattern, confidence in similar[:3]:
                    print(f"  • {pattern.pattern_key}: {confidence:.0%} match")
                    self.patterns_found.append(pattern.content)

            # Spara denna analys för framtiden
            await self.memory.remember(
                f"migration_analysis_{self.legacy_path.name}_{datetime.now().strftime('%Y%m%d')}",
                {
                    "project": analysis['project'],
                    "complexity": analysis['complexity'],
                    "lines": analysis['total_lines'],
                    "uses_database": analysis['uses_database'],
                    "timestamp": datetime.now().isoformat()
                },
                pattern_type="analysis"
            )

            await self.memory.shutdown()

        return analysis

    def generate_smart_plan(self) -> Dict:
        """Generera plan baserad på tidigare erfarenheter"""

        plan = self.generate_migration_plan()

        # Lägg till insights från patterns
        if self.patterns_found:
            plan["ai_insights"] = []

            for pattern in self.patterns_found:
                if isinstance(pattern, dict):
                    if "approach" in pattern:
                        plan["ai_insights"].append(f"✨ Proven approach: {pattern.get('approach', 'N/A')}")
                    if "performance" in pattern:
                        plan["ai_insights"].append(f"⚡ Performance tip: {pattern.get('performance', 'N/A')}")

        # Justera tidsuppskattning baserat på erfarenhet
        if self.patterns_found:
            # Vi har gjort detta förut - går snabbare!
            plan["estimated_hours"] *= 0.7
            plan["confidence"] = "HIGH - Similar projects completed successfully"
        else:
            plan["confidence"] = "MEDIUM - First time with this pattern"

        return plan

    async def generate_smart_code(self, component: str) -> str:
        """Generera kod baserat på patterns"""

        if not self.memory:
            return f"# TODO: Implement {component}"

        await self.memory.initialize()

        # Sök efter kod-patterns
        patterns = await self.memory.recall(f"PHP to Python migration {component}")

        code = f"""# Generated from patterns
# Component: {component}
# Confidence: {len(patterns)} patterns found

"""

        if patterns:
            best_pattern = patterns[0][0]
            if isinstance(best_pattern.content, dict) and "code" in best_pattern.content:
                code += best_pattern.content["code"]
            else:
                code += f"""
# Pattern found: {best_pattern.pattern_key}
# TODO: Implement based on pattern
"""
        else:
            code += f"""
# No patterns found - generating fresh
import fastapi
from typing import Optional

# TODO: Implement {component}
"""

        await self.memory.shutdown()

        return code

async def interactive_demo():
    """Interaktiv demo med val"""

    print("""
╔══════════════════════════════════════════════════════════════╗
║        SMART LEGACY MIGRATION ANALYZER v0.2                   ║
║              Now with Neural Memory! 🧠                       ║
╚══════════════════════════════════════════════════════════════╝
    """)

    print("What would you like to analyze?")
    print("1. Demo PHP project (built-in)")
    print("2. Custom path")
    print("3. Generate sample migration code")

    choice = input("\nChoice (1-3): ").strip()

    if choice == "1":
        # Demo projekt
        demo_path = Path("demo_legacy_project")
        demo_path.mkdir(exist_ok=True)

        # Skapa demo filer
        (demo_path / "index.php").write_text("""<?php
session_start();
require_once 'database.php';

class UserController {
    public function listUsers() {
        $db = new Database();
        $users = $db->query("SELECT * FROM users");
        return $users;
    }
}
?>""")

        analyzer = SmartMigrationAnalyzer(demo_path)

    elif choice == "2":
        path = input("Enter path to PHP project: ").strip()
        analyzer = SmartMigrationAnalyzer(Path(path))

    else:
        # Generate code
        analyzer = SmartMigrationAnalyzer(Path("."))
        code = await analyzer.generate_smart_code("UserController")
        print("\n📝 Generated Migration Code:")
        print("=" * 60)
        print(code)
        print("=" * 60)
        return

    # Kör smart analys
    print("\n🔍 Analyzing project...")
    analysis = await analyzer.analyze_with_memory()

    print("\n📊 Generating smart migration plan...")
    plan = analyzer.generate_smart_plan()

    print("\n💰 Calculating quote...")
    quote = analyzer.generate_quote(plan)

    # Visa resultat
    output = create_demo_output(analysis, plan, quote)
    print(output)

    # Visa AI insights om de finns
    if "ai_insights" in plan and plan["ai_insights"]:
        print("\n🤖 AI INSIGHTS FROM PREVIOUS MIGRATIONS:")
        print("━" * 60)
        for insight in plan["ai_insights"]:
            print(insight)
        print()

    # Spara resultat
    result = {
        "timestamp": datetime.now().isoformat(),
        "analysis": analysis,
        "plan": plan,
        "quote": quote,
        "patterns_used": len(analyzer.patterns_found)
    }

    output_file = f"smart_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)

    print(f"💾 Analysis saved to: {output_file}")

    # Visa nästa steg
    print("\n🎯 NEXT STEPS:")
    print("1. Send this analysis to potential client")
    print("2. Schedule demo call")
    print("3. Close the deal!")

if __name__ == "__main__":
    # Håll momentum - kör direkt!
    asyncio.run(interactive_demo())