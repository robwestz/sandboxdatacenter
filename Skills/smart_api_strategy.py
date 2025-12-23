#!/usr/bin/env python3
"""
💰 SMART API CREDIT STRATEGY
Intelligent system that chooses between free agent work vs paid API calls

Philosophy: Use free when possible, API when valuable
"""

import os
import json
from typing import Dict, Any, Tuple, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

# Add MEMORY_CORE
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "MEMORY_CORE"))
from memory_manager import get_memory, remember, save_pattern

class TaskComplexity(Enum):
    """Task complexity levels"""
    TRIVIAL = "trivial"      # Agent can do easily
    SIMPLE = "simple"        # Agent can do well
    MODERATE = "moderate"    # Agent can do, API might be better
    COMPLEX = "complex"      # API recommended
    CRITICAL = "critical"    # API required for accuracy

class ExecutionMode(Enum):
    """How to execute the task"""
    AGENT_ONLY = "agent_only"           # Free - use session agent
    API_ONLY = "api_only"               # Paid - use external API
    HYBRID = "hybrid"                   # Mixed - agent + API validation
    AGENT_WITH_FALLBACK = "agent_fallback"  # Try agent first, API if fails

@dataclass
class CostAnalysis:
    """Cost-benefit analysis for a task"""
    task_type: str
    complexity: TaskComplexity
    estimated_tokens: int
    estimated_cost_usd: float
    agent_capability: float  # 0-1 score
    api_advantage: float     # How much better API would be
    recommendation: ExecutionMode
    reasoning: str

class SmartAPIStrategy:
    """
    Intelligent decision system for when to use APIs vs agent
    """

    # Task patterns that agent handles well (FREE)
    AGENT_STRONG_TASKS = {
        "code_analysis": 0.9,      # Agent is great at analyzing code
        "documentation": 0.95,      # Excellent at writing docs
        "refactoring": 0.85,        # Good at refactoring
        "testing": 0.8,             # Can write tests well
        "planning": 0.9,            # Great at planning
        "file_operations": 0.95,    # File read/write/edit
        "git_operations": 0.9,      # Git commands
        "pattern_matching": 0.85,   # Finding patterns
        "code_generation": 0.8,     # Generating new code
        "debugging": 0.75,          # Debugging assistance
    }

    # Tasks where APIs add significant value
    API_VALUABLE_TASKS = {
        "real_time_data": 0.95,     # APIs required for live data
        "large_scale_analysis": 0.8, # API better for huge codebases
        "multi_model_consensus": 0.9, # Multiple models for validation
        "specialized_domains": 0.85,  # Domain-specific APIs
        "production_deployment": 0.9, # Critical production tasks
        "security_scanning": 0.85,    # Security-critical analysis
        "performance_profiling": 0.8, # Performance analysis
        "cost_optimization": 0.75,    # Complex optimization
    }

    # Cost thresholds (in USD)
    COST_THRESHOLDS = {
        "trivial_max": 0.01,      # Max $0.01 for trivial tasks
        "simple_max": 0.05,        # Max $0.05 for simple tasks
        "moderate_max": 0.25,      # Max $0.25 for moderate tasks
        "complex_max": 1.00,       # Max $1.00 for complex tasks
        "critical_max": 5.00,      # Max $5.00 for critical tasks
    }

    def __init__(self):
        """Initialize the strategy system"""
        self.memory = get_memory()
        self.cost_tracker = CostTracker()
        self.load_historical_patterns()

    def analyze_task(self, task_description: str, context: Dict[str, Any] = None) -> CostAnalysis:
        """
        Analyze a task and recommend execution mode

        Args:
            task_description: What needs to be done
            context: Additional context (file size, criticality, etc)

        Returns:
            CostAnalysis with recommendation
        """

        # Determine task type and complexity
        task_type = self._identify_task_type(task_description)
        complexity = self._assess_complexity(task_description, context)

        # Estimate costs
        estimated_tokens = self._estimate_tokens(task_description, context)
        estimated_cost = self._calculate_cost(estimated_tokens)

        # Assess capabilities
        agent_capability = self.AGENT_STRONG_TASKS.get(task_type, 0.5)
        api_advantage = self.API_VALUABLE_TASKS.get(task_type, 0.3)

        # Make recommendation
        recommendation, reasoning = self._recommend_mode(
            complexity,
            agent_capability,
            api_advantage,
            estimated_cost,
            context
        )

        analysis = CostAnalysis(
            task_type=task_type,
            complexity=complexity,
            estimated_tokens=estimated_tokens,
            estimated_cost_usd=estimated_cost,
            agent_capability=agent_capability,
            api_advantage=api_advantage,
            recommendation=recommendation,
            reasoning=reasoning
        )

        # Save pattern for learning
        self._save_decision_pattern(analysis)

        return analysis

    def _identify_task_type(self, task_description: str) -> str:
        """Identify what type of task this is"""

        task_lower = task_description.lower()

        # Check for keywords
        if any(word in task_lower for word in ["analyze", "review", "examine"]):
            return "code_analysis"
        elif any(word in task_lower for word in ["document", "readme", "guide"]):
            return "documentation"
        elif any(word in task_lower for word in ["refactor", "improve", "optimize"]):
            return "refactoring"
        elif any(word in task_lower for word in ["test", "testing", "coverage"]):
            return "testing"
        elif any(word in task_lower for word in ["plan", "strategy", "design"]):
            return "planning"
        elif any(word in task_lower for word in ["real-time", "live", "current"]):
            return "real_time_data"
        elif any(word in task_lower for word in ["security", "vulnerability", "scan"]):
            return "security_scanning"
        elif any(word in task_lower for word in ["deploy", "production", "release"]):
            return "production_deployment"
        else:
            return "general"

    def _assess_complexity(self, task_description: str, context: Dict = None) -> TaskComplexity:
        """Assess task complexity"""

        if not context:
            context = {}

        # Check file/data size
        file_size = context.get("file_size_mb", 0)
        file_count = context.get("file_count", 1)

        # Check criticality
        is_production = context.get("production", False)
        is_security = context.get("security_critical", False)

        # Complexity rules
        if is_production or is_security:
            return TaskComplexity.CRITICAL

        if file_size > 100 or file_count > 1000:
            return TaskComplexity.COMPLEX

        if file_size > 10 or file_count > 100:
            return TaskComplexity.MODERATE

        if file_size > 1 or file_count > 10:
            return TaskComplexity.SIMPLE

        return TaskComplexity.TRIVIAL

    def _estimate_tokens(self, task_description: str, context: Dict = None) -> int:
        """Estimate token usage for API calls"""

        base_tokens = len(task_description.split()) * 2  # Rough estimate

        if context:
            file_size = context.get("file_size_mb", 0)
            # Estimate tokens based on file size
            base_tokens += int(file_size * 1000)  # ~1000 tokens per MB

        return base_tokens

    def _calculate_cost(self, tokens: int) -> float:
        """Calculate estimated cost in USD"""

        # Rough pricing (adjust based on actual API)
        # Assuming $0.01 per 1000 tokens for input, $0.03 for output
        input_cost = (tokens / 1000) * 0.01
        output_cost = (tokens / 1000) * 0.03  # Assume similar output size

        return input_cost + output_cost

    def _recommend_mode(
        self,
        complexity: TaskComplexity,
        agent_capability: float,
        api_advantage: float,
        estimated_cost: float,
        context: Dict = None
    ) -> Tuple[ExecutionMode, str]:
        """
        Make recommendation on execution mode

        Returns:
            (mode, reasoning)
        """

        # Rule 1: If agent is very capable (>0.8) and API advantage is low (<0.4)
        if agent_capability > 0.8 and api_advantage < 0.4:
            return (
                ExecutionMode.AGENT_ONLY,
                f"Agent handles this well ({agent_capability:.0%} capability), "
                f"API adds little value ({api_advantage:.0%}). Save credits!"
            )

        # Rule 2: If task is critical, use API or hybrid
        if complexity == TaskComplexity.CRITICAL:
            if estimated_cost > self.COST_THRESHOLDS["critical_max"]:
                return (
                    ExecutionMode.HYBRID,
                    f"Critical task needs validation, but cost (${estimated_cost:.2f}) "
                    f"is high. Using hybrid approach."
                )
            else:
                return (
                    ExecutionMode.API_ONLY,
                    f"Critical task requires API accuracy. "
                    f"Cost (${estimated_cost:.2f}) is acceptable."
                )

        # Rule 3: If API has significant advantage and cost is reasonable
        if api_advantage > 0.7:
            threshold_key = f"{complexity.value}_max"
            max_cost = self.COST_THRESHOLDS.get(threshold_key, 0.25)

            if estimated_cost <= max_cost:
                return (
                    ExecutionMode.API_ONLY,
                    f"API significantly better ({api_advantage:.0%} advantage), "
                    f"cost (${estimated_cost:.2f}) within budget."
                )
            else:
                return (
                    ExecutionMode.AGENT_WITH_FALLBACK,
                    f"API better but expensive. Try agent first, "
                    f"use API only if needed."
                )

        # Rule 4: For moderate complexity with decent agent capability
        if complexity == TaskComplexity.MODERATE and agent_capability > 0.6:
            return (
                ExecutionMode.AGENT_WITH_FALLBACK,
                f"Agent can likely handle this ({agent_capability:.0%}), "
                f"API as backup if needed."
            )

        # Rule 5: Default to agent for simple/trivial tasks
        if complexity in [TaskComplexity.TRIVIAL, TaskComplexity.SIMPLE]:
            return (
                ExecutionMode.AGENT_ONLY,
                f"Simple task, agent can handle. Save ${estimated_cost:.2f}!"
            )

        # Default: Use agent with fallback
        return (
            ExecutionMode.AGENT_WITH_FALLBACK,
            "Balanced approach: Try agent first, use API if quality insufficient."
        )

    def _save_decision_pattern(self, analysis: CostAnalysis):
        """Save decision pattern for future learning"""

        pattern = {
            "timestamp": datetime.now().isoformat(),
            "task_type": analysis.task_type,
            "complexity": analysis.complexity.value,
            "recommendation": analysis.recommendation.value,
            "estimated_cost": analysis.estimated_cost_usd,
            "reasoning": analysis.reasoning
        }

        remember("api_decision", pattern, "cost_optimization")

    def load_historical_patterns(self):
        """Load historical patterns to improve decisions"""

        # Load past decisions
        patterns = self.memory.recall("api_decision", "cost_optimization", limit=100)

        # Analyze success rates
        # (This would be expanded with actual success tracking)
        pass

    def execute_with_strategy(self, task: str, executor_func: callable, api_func: callable = None) -> Any:
        """
        Execute a task using the recommended strategy

        Args:
            task: Task description
            executor_func: Function for agent execution
            api_func: Function for API execution (if available)

        Returns:
            Task result
        """

        # Analyze task
        analysis = self.analyze_task(task)

        print(f"\n💰 Cost Analysis:")
        print(f"   Task: {analysis.task_type}")
        print(f"   Complexity: {analysis.complexity.value}")
        print(f"   Agent capability: {analysis.agent_capability:.0%}")
        print(f"   API advantage: {analysis.api_advantage:.0%}")
        print(f"   Estimated cost: ${analysis.estimated_cost_usd:.3f}")
        print(f"   Recommendation: {analysis.recommendation.value}")
        print(f"   Reasoning: {analysis.reasoning}")

        # Execute based on recommendation
        if analysis.recommendation == ExecutionMode.AGENT_ONLY:
            print("   ✅ Using FREE agent execution")
            return executor_func()

        elif analysis.recommendation == ExecutionMode.API_ONLY:
            if api_func:
                print(f"   💳 Using API (cost: ${analysis.estimated_cost_usd:.3f})")
                result = api_func()
                self.cost_tracker.track_usage(analysis.estimated_cost_usd, "api_call")
                return result
            else:
                print("   ⚠️ API recommended but not available, using agent")
                return executor_func()

        elif analysis.recommendation == ExecutionMode.HYBRID:
            print("   🔄 Using hybrid approach")
            agent_result = executor_func()
            if api_func:
                api_result = api_func()
                self.cost_tracker.track_usage(analysis.estimated_cost_usd, "validation")
                # Compare/merge results
                return self._merge_results(agent_result, api_result)
            return agent_result

        elif analysis.recommendation == ExecutionMode.AGENT_WITH_FALLBACK:
            print("   🔄 Trying agent first...")
            try:
                result = executor_func()
                if self._validate_result(result):
                    print("   ✅ Agent succeeded, no API needed!")
                    return result
                else:
                    if api_func:
                        print("   🔄 Agent result insufficient, using API")
                        result = api_func()
                        self.cost_tracker.track_usage(analysis.estimated_cost_usd, "fallback")
                        return result
            except Exception as e:
                if api_func:
                    print(f"   ⚠️ Agent failed ({e}), using API")
                    result = api_func()
                    self.cost_tracker.track_usage(analysis.estimated_cost_usd, "recovery")
                    return result
                raise

    def _validate_result(self, result: Any) -> bool:
        """Validate if agent result is good enough"""
        # Implement validation logic
        # For now, assume valid if not None/empty
        return result is not None and result != ""

    def _merge_results(self, agent_result: Any, api_result: Any) -> Any:
        """Merge agent and API results"""
        # Implement merging logic based on task type
        # For now, prefer API result but include agent insights
        return {
            "primary": api_result,
            "agent_insights": agent_result,
            "merged": True
        }


class CostTracker:
    """Track API costs over time"""

    def __init__(self):
        self.session_costs = []
        self.total_saved = 0.0

    def track_usage(self, cost: float, reason: str):
        """Track API usage"""
        self.session_costs.append({
            "timestamp": datetime.now().isoformat(),
            "cost": cost,
            "reason": reason
        })

    def track_savings(self, saved: float):
        """Track money saved by using agent"""
        self.total_saved += saved

    def get_session_summary(self) -> Dict:
        """Get cost summary for session"""
        total_spent = sum(c["cost"] for c in self.session_costs)

        return {
            "total_spent": total_spent,
            "total_saved": self.total_saved,
            "api_calls": len(self.session_costs),
            "efficiency_ratio": self.total_saved / (total_spent + 0.001),  # Avoid div by 0
            "details": self.session_costs
        }


def demonstrate_strategy():
    """Demonstrate the smart API strategy"""

    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║                    💰 SMART API CREDIT STRATEGY 💰                      ║
║                                                                          ║
║            Use FREE agent when possible, API when valuable              ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
    """)

    strategy = SmartAPIStrategy()

    # Test different scenarios
    test_cases = [
        {
            "task": "Write documentation for this Python function",
            "context": {"file_size_mb": 0.1}
        },
        {
            "task": "Analyze this legacy codebase for migration",
            "context": {"file_size_mb": 50, "file_count": 500}
        },
        {
            "task": "Deploy to production environment",
            "context": {"production": True}
        },
        {
            "task": "Find security vulnerabilities in the code",
            "context": {"security_critical": True}
        },
        {
            "task": "Refactor this small utility function",
            "context": {"file_size_mb": 0.01}
        },
        {
            "task": "Get real-time stock prices",
            "context": {"real_time": True}
        }
    ]

    total_saved = 0
    total_spent = 0

    print("\n📊 STRATEGY ANALYSIS:\n")
    for i, test in enumerate(test_cases, 1):
        print(f"{i}. {test['task']}")

        analysis = strategy.analyze_task(test["task"], test.get("context"))

        print(f"   Mode: {analysis.recommendation.value}")
        print(f"   Cost if API: ${analysis.estimated_cost_usd:.3f}")

        if analysis.recommendation == ExecutionMode.AGENT_ONLY:
            total_saved += analysis.estimated_cost_usd
            print(f"   💚 SAVED: ${analysis.estimated_cost_usd:.3f}")
        else:
            total_spent += analysis.estimated_cost_usd

        print()

    print("="*70)
    print(f"💰 TOTAL SAVED: ${total_saved:.2f}")
    print(f"💳 TOTAL SPENT: ${total_spent:.2f}")
    print(f"📈 EFFICIENCY: {(total_saved/(total_saved+total_spent)*100):.0f}% cost reduction")


if __name__ == "__main__":
    demonstrate_strategy()