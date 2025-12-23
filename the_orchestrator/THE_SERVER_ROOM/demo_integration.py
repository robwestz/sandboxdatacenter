"""
Demo: Neural Database Integration with Agent Systems
Shows how to integrate the Neural Memory with your AI agents
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add the current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from neural_db import NeuralMemoryManager, MemoryPattern

# ============================================================
# SIMULATED AGENT SYSTEM
# ============================================================

class IntelligentAgent:
    """An agent that uses neural memory for enhanced decision-making"""

    def __init__(self, agent_name: str, project_context: str):
        self.name = agent_name
        self.context = project_context
        self.memory = NeuralMemoryManager()
        self.session_id = None
        self.interaction_count = 0

    async def initialize(self):
        """Initialize the agent with neural memory"""
        print(f"🤖 {self.name} initializing...")
        await self.memory.initialize()
        self.session_id = await self.memory.start_session(self.context)
        print(f"✅ {self.name} ready with neural memory!")

    async def shutdown(self):
        """Clean shutdown of the agent"""
        summary = await self.memory.end_session()
        await self.memory.shutdown()
        print(f"🔌 {self.name} shutdown. Interactions: {summary.get('interaction_count', 0)}")

    async def process_task(self, task: str, task_type: str = "general") -> Dict[str, Any]:
        """Process a task with memory assistance"""
        self.interaction_count += 1
        print(f"\n{'='*60}")
        print(f"📋 Task #{self.interaction_count}: {task}")
        print(f"{'='*60}")

        # Step 1: Check memory for similar patterns
        print("🔍 Checking neural memory for similar patterns...")
        similar_patterns = await self.memory.recall(task, limit=3)

        response = {
            "task": task,
            "suggested_approach": None,
            "similar_patterns": [],
            "confidence": 0.0,
            "execution_result": None
        }

        if similar_patterns:
            print(f"💡 Found {len(similar_patterns)} relevant patterns:")
            for pattern, similarity in similar_patterns:
                print(f"   • {pattern.pattern_key} ({similarity:.0%} match)")
                print(f"     Content: {json.dumps(pattern.content, indent=6)}")
                response["similar_patterns"].append({
                    "key": pattern.pattern_key,
                    "content": pattern.content,
                    "similarity": similarity
                })

            # Use the best pattern as suggested approach
            best_pattern = similar_patterns[0][0]
            response["suggested_approach"] = best_pattern.content
            response["confidence"] = similar_patterns[0][1]
        else:
            print("   No similar patterns found - will use default approach")

        # Step 2: Execute the task (simulated)
        print("\n🚀 Executing task...")
        execution_result = await self._execute_task(task, response["suggested_approach"])
        response["execution_result"] = execution_result

        # Step 3: Learn from the execution
        if execution_result["success"]:
            print("✅ Task completed successfully!")

            # Save successful pattern for future use
            pattern_key = f"{task_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            await self.memory.remember(
                pattern_key,
                {
                    "task": task,
                    "approach": execution_result["approach"],
                    "result": execution_result["result"],
                    "performance": execution_result.get("performance", {})
                },
                pattern_type=task_type
            )
            print(f"💾 Pattern saved: {pattern_key}")
        else:
            print(f"❌ Task failed: {execution_result.get('error', 'Unknown error')}")

        # Step 4: Track the interaction
        await self.memory.track(
            prompt=task,
            response=json.dumps(execution_result),
            success=execution_result["success"]
        )

        return response

    async def _execute_task(self, task: str, suggested_approach: Dict = None) -> Dict:
        """Simulate task execution"""
        # In a real system, this would actually execute the task
        await asyncio.sleep(0.5)  # Simulate processing time

        # Simulated execution results based on task type
        if "API" in task or "api" in task:
            return {
                "success": True,
                "approach": suggested_approach or {"method": "REST call with retry"},
                "result": "API call successful after 2 retries",
                "performance": {"retries": 2, "latency_ms": 250}
            }
        elif "database" in task.lower() or "query" in task.lower():
            return {
                "success": True,
                "approach": suggested_approach or {"method": "connection pooling"},
                "result": "Query executed successfully",
                "performance": {"query_time_ms": 45, "rows_returned": 142}
            }
        elif "error" in task.lower() or "fix" in task.lower():
            return {
                "success": True,
                "approach": suggested_approach or {"method": "stack trace analysis"},
                "result": "Error resolved by updating dependency",
                "performance": {"resolution_time_minutes": 15}
            }
        else:
            return {
                "success": True,
                "approach": {"method": "standard execution"},
                "result": f"Task '{task}' completed",
                "performance": {"execution_time_ms": 100}
            }

# ============================================================
# DEMONSTRATION SCENARIOS
# ============================================================

async def scenario_single_agent():
    """Demo: Single agent learning over time"""
    print("\n" + "="*70)
    print("🎬 SCENARIO 1: Single Agent Learning Over Time")
    print("="*70)

    agent = IntelligentAgent("DataProcessor", "data_pipeline_project")
    await agent.initialize()

    # Process various tasks
    tasks = [
        ("Handle API rate limiting errors", "error_handling"),
        ("Optimize database query performance", "optimization"),
        ("Fix authentication timeout issues", "bug_fix"),
        ("Handle API throttling with backoff", "error_handling"),  # Similar to first
        ("Implement database connection pooling", "optimization"),  # Similar to second
    ]

    for task, task_type in tasks:
        await agent.process_task(task, task_type)
        await asyncio.sleep(1)  # Small delay between tasks

    await agent.shutdown()

async def scenario_multi_agent_collaboration():
    """Demo: Multiple agents sharing knowledge"""
    print("\n" + "="*70)
    print("🎬 SCENARIO 2: Multi-Agent Knowledge Sharing")
    print("="*70)

    # Create multiple agents working on related projects
    agents = [
        IntelligentAgent("APIAgent", "microservice_a"),
        IntelligentAgent("DataAgent", "microservice_b"),
        IntelligentAgent("SecurityAgent", "microservice_c"),
    ]

    # Initialize all agents
    for agent in agents:
        await agent.initialize()

    # Agent 1 learns something
    print("\n📚 Phase 1: APIAgent learns about rate limiting")
    await agents[0].process_task(
        "Implement exponential backoff for API calls",
        "api_pattern"
    )

    # Agent 2 benefits from Agent 1's learning
    print("\n📚 Phase 2: DataAgent encounters similar problem")
    await agents[1].process_task(
        "Handle rate limiting in external API integration",
        "api_pattern"
    )

    # Agent 3 adds security perspective
    print("\n📚 Phase 3: SecurityAgent adds security layer")
    await agents[2].process_task(
        "Add JWT token refresh with exponential backoff",
        "security_pattern"
    )

    # All agents shutdown
    for agent in agents:
        await agent.shutdown()

async def scenario_evolving_knowledge():
    """Demo: Knowledge evolution across sessions"""
    print("\n" + "="*70)
    print("🎬 SCENARIO 3: Knowledge Evolution Across Sessions")
    print("="*70)

    # Session 1: Initial learning
    print("\n📅 Day 1: Initial Discovery")
    agent1 = IntelligentAgent("LearnerBot", "evolving_project")
    await agent1.initialize()

    await agent1.process_task("Implement caching strategy", "architecture")
    await agent1.process_task("Handle cache invalidation", "architecture")

    await agent1.shutdown()

    # Session 2: Building on previous knowledge
    print("\n📅 Day 7: Building on Previous Knowledge")
    agent2 = IntelligentAgent("LearnerBot", "evolving_project")
    await agent2.initialize()

    await agent2.process_task("Implement distributed caching", "architecture")
    await agent2.process_task("Optimize cache hit ratio", "optimization")

    await agent2.shutdown()

    # Session 3: Advanced patterns emerge
    print("\n📅 Day 30: Advanced Patterns Emerge")
    agent3 = IntelligentAgent("LearnerBot", "evolving_project")
    await agent3.initialize()

    await agent3.process_task("Implement multi-tier caching with Redis", "architecture")

    await agent3.shutdown()

# ============================================================
# ANALYTICS AND INSIGHTS
# ============================================================

async def show_database_insights():
    """Display insights from the neural database"""
    print("\n" + "="*70)
    print("📊 NEURAL DATABASE INSIGHTS")
    print("="*70)

    memory = NeuralMemoryManager()
    await memory.initialize()

    # Get top patterns
    print("\n🏆 Top Patterns in Database:")
    top_patterns = await memory.db.get_top_patterns(limit=5)
    for i, pattern in enumerate(top_patterns, 1):
        print(f"{i}. {pattern.pattern_key}")
        print(f"   Type: {pattern.pattern_type}")
        print(f"   Usage: {pattern.usage_count} times")
        print(f"   Success Rate: {pattern.success_count}/{pattern.usage_count}")

    # Get context statistics
    contexts = ["data_pipeline_project", "microservice_a", "microservice_b",
                "microservice_c", "evolving_project"]

    print("\n📈 Context Statistics:")
    for context in contexts:
        stats = await memory.db.get_context_stats(context)
        if stats and stats.get('session_count', 0) > 0:
            print(f"\n{context}:")
            print(f"  • Sessions: {stats.get('session_count', 0)}")
            print(f"  • Interactions: {stats.get('total_interactions', 0)}")
            print(f"  • Patterns: {stats.get('pattern_count', 0)}")

    await memory.shutdown()

# ============================================================
# MAIN EXECUTION
# ============================================================

async def main():
    """Run all demonstration scenarios"""

    print("\n" + "🧠"*35)
    print("NEURAL DATABASE INTEGRATION DEMONSTRATION")
    print("Showing how agents learn and share knowledge over time")
    print("🧠"*35)

    # Run scenarios
    await scenario_single_agent()
    await asyncio.sleep(2)

    await scenario_multi_agent_collaboration()
    await asyncio.sleep(2)

    await scenario_evolving_knowledge()
    await asyncio.sleep(2)

    # Show insights
    await show_database_insights()

    print("\n" + "="*70)
    print("✨ DEMONSTRATION COMPLETE!")
    print("The neural database now contains learned patterns that future")
    print("agents can use to solve problems more efficiently.")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(main())