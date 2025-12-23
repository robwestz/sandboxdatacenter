#!/usr/bin/env python3
"""
Chain Reactor - The Factory's Agent Spawning Engine (FIXED)

Creates cascading chains of agents that spawn more agents.
Now with comprehensive error handling and validation.
"""

import asyncio
import uuid
from pathlib import Path
from typing import Dict, List, Any, Optional
from enum import Enum
import sys
import logging

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Use ImportManager for dependencies
from bootstrap.import_manager import get_import_manager

# Import error handling
try:
    from lib.error_handling import (
        RecoveryManager, ValidationEngine, CircuitBreaker,
        ValidationError, CircuitOpenError
    )
    ERROR_HANDLING_AVAILABLE = True
except ImportError:
    ERROR_HANDLING_AVAILABLE = False

# Import fallback agent implementation
from lib.fallback_implementations import SimpleAgent, SimpleChainReactor, AgentRole

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentRole(Enum):
    ARCHITECT = "architect"
    ANALYZER = "analyzer"
    BUILDER = "builder"
    TESTER = "tester"
    REVIEWER = "reviewer"
    DEPLOYER = "deployer"
    DOCUMENTER = "documenter"
    MANAGER = "manager"


class AgentBlueprint:
    """Defines agent spawning patterns"""

    def __init__(self, role: AgentRole):
        self.role = role
        self.max_children = self._determine_max_children()
        self.spawn_probability = self._determine_spawn_probability()
        self.auto_spawn_threshold = self._determine_threshold()

    def _determine_max_children(self):
        """Determine max children based on role"""
        role_children = {
            AgentRole.MANAGER: 10,
            AgentRole.ARCHITECT: 5,
            AgentRole.ANALYZER: 3,
            AgentRole.BUILDER: 2,
            AgentRole.TESTER: 1,
            AgentRole.REVIEWER: 1,
            AgentRole.Deployer: 2,
            AgentRole.DOCUMENTER: 0
        }
        return role_children.get(self.role, 3)

    def _determine_spawn_probability(self):
        """Determine spawn probability"""
        probabilities = {
            AgentRole.MANAGER: 0.9,
            AgentRole.ARCHITECT: 0.7,
            AgentRole.ANALYZER: 0.6,
            AgentRole.BUILDER: 0.5,
            AgentRole.TESTER: 0.3,
            AgentRole.REVIEWER: 0.2,
            AgentRole.DEPLOYER: 0.4,
            AgentRole.DOCUMENTER: 0.1
        }
        return probabilities.get(self.role, 0.5)

    def _determine_threshold(self):
        """Determine complexity threshold for auto-spawning"""
        return 0.6


class Agent:
    """Represents a single agent in the chain"""

    def __init__(self, role: AgentRole, task: Dict[str, Any], parent_id: Optional[str] = None):
        self.id = str(uuid.uuid4())
        self.role = role
        self.task = task
        self.parent_id = parent_id
        self.children = []
        self.status = "created"
        self.output = None
        self.blueprint = AgentBlueprint(role)

    def __repr__(self):
        return f"Agent({self.role.value}, id={self.id[:8]})"


class ChainReactor:
    """
    Manages the chain reaction of agent spawning with error handling.
    """

    def __init__(self, max_agents: int = 100, max_depth: int = 10):
        """Initialize ChainReactor with limits and error handling"""
        self.max_agents = max_agents
        self.max_depth = max_depth
        self.agents = {}
        self.spawn_count = 0
        self.execution_graph = {}

        # Error handling components
        if ERROR_HANDLING_AVAILABLE:
            self.recovery_manager = RecoveryManager(max_retries=3)
            self.validation_engine = ValidationEngine()
            self.circuit_breaker = CircuitBreaker(
                name="chain_reactor",
                failure_threshold=5,
                recovery_timeout=30
            )
        else:
            self.recovery_manager = None
            self.validation_engine = None
            self.circuit_breaker = None

        logger.info(f"ChainReactor initialized (max_agents={max_agents}, max_depth={max_depth})")

    async def spawn_agent(self,
                          role: AgentRole,
                          task: Dict[str, Any],
                          parent_id: Optional[str] = None) -> Agent:
        """
        Spawn a new agent with validation and error handling.
        """
        # Validate inputs
        if self.validation_engine:
            validation = self.validation_engine.validate_preconditions(
                "agent_spawning",
                {
                    "role": role,
                    "task": task,
                    "max_agents": self.max_agents,
                    "current_count": self.spawn_count
                }
            )
            if not validation.is_valid:
                raise ValidationError(f"Agent spawn validation failed: {validation.errors}")

        # Check limits
        if self.spawn_count >= self.max_agents:
            logger.warning(f"Agent limit reached: {self.spawn_count}/{self.max_agents}")
            raise RuntimeError(f"Maximum agent limit ({self.max_agents}) reached")

        # Check circuit breaker
        if self.circuit_breaker and not self.circuit_breaker.allow_request():
            raise CircuitOpenError("Circuit breaker open - too many failures")

        try:
            # Create agent
            agent = Agent(role, task, parent_id)
            self.agents[agent.id] = agent
            self.spawn_count += 1

            # Track lineage
            if parent_id and parent_id in self.agents:
                self.agents[parent_id].children.append(agent.id)

            logger.info(f"Spawned {agent}")

            # Record success
            if self.circuit_breaker:
                self.circuit_breaker.on_success()

            return agent

        except Exception as e:
            logger.error(f"Failed to spawn agent: {e}")
            if self.circuit_breaker:
                self.circuit_breaker.on_failure()

            # Try fallback if available
            if self.recovery_manager:
                try:
                    # Use SimpleAgent as fallback
                    simple_agent = SimpleAgent(role=role)
                    logger.info(f"Using SimpleAgent fallback for {role.value}")
                    return simple_agent
                except Exception as fallback_error:
                    logger.error(f"Fallback also failed: {fallback_error}")

            raise

    async def _propagate_chain(self,
                               agent: Agent,
                               depth: int,
                               max_agents: int) -> Dict[str, Any]:
        """
        Propagate the chain reaction with timeout and error handling.
        """
        # Depth check
        if depth >= self.max_depth:
            logger.info(f"Max depth {self.max_depth} reached")
            return await self._execute_agent_task(agent)

        # Agent count check
        if self.spawn_count >= max_agents:
            logger.info(f"Max agents {max_agents} reached")
            return await self._execute_agent_task(agent)

        # Timeout protection
        try:
            async with asyncio.timeout(60):  # 60 second timeout per propagation
                # Analyze task complexity
                complexity = self._analyze_task_complexity(agent.task)

                # Decide whether to spawn children
                if complexity > agent.blueprint.auto_spawn_threshold:
                    # Decompose task
                    subtasks = self._decompose_task(agent.task, agent.blueprint)

                    # Spawn children for subtasks
                    children_results = []
                    for subtask in subtasks[:agent.blueprint.max_children]:
                        if self.spawn_count >= max_agents:
                            break

                        # Determine child role
                        child_role = self._determine_child_role(subtask, agent.blueprint)

                        if child_role:
                            try:
                                # Spawn child with error handling
                                child = await self.spawn_agent(child_role, subtask, agent.id)

                                # Recursive propagation
                                result = await self._propagate_chain(child, depth + 1, max_agents)
                                children_results.append(result)

                            except Exception as e:
                                logger.error(f"Child spawn/execution failed: {e}")
                                # Continue with other children
                                continue

                    # Synthesize results
                    agent.output = self._synthesize_results(agent, children_results)
                else:
                    # Execute task directly
                    agent.output = await self._execute_agent_task(agent)

                return {
                    "agent_id": agent.id,
                    "role": agent.role.value,
                    "output": agent.output,
                    "children": len(agent.children),
                    "depth": depth
                }

        except asyncio.TimeoutError:
            logger.error(f"Agent {agent.id} timed out at depth {depth}")
            return {
                "agent_id": agent.id,
                "error": "timeout",
                "depth": depth
            }
        except Exception as e:
            logger.error(f"Propagation error for {agent.id}: {e}")
            return {
                "agent_id": agent.id,
                "error": str(e),
                "depth": depth
            }

    def _analyze_task_complexity(self, task: Dict[str, Any]) -> float:
        """Analyze task complexity to decide on spawning"""
        # Simple heuristic - can be made more sophisticated
        complexity = 0.5  # Base complexity

        # Increase based on task attributes
        if task.get("scope", "") in ["large", "complex", "distributed"]:
            complexity += 0.3

        if len(task.get("requirements", [])) > 5:
            complexity += 0.2

        return min(1.0, complexity)

    def _decompose_task(self, task: Dict[str, Any], blueprint: AgentBlueprint) -> List[Dict[str, Any]]:
        """Decompose task into subtasks"""
        subtasks = []

        # Role-specific decomposition
        if blueprint.role == AgentRole.ARCHITECT:
            subtasks = [
                {"name": "Design components", "type": "design"},
                {"name": "Define interfaces", "type": "interface"},
                {"name": "Plan integration", "type": "integration"}
            ]
        elif blueprint.role == AgentRole.BUILDER:
            subtasks = [
                {"name": "Implement core", "type": "implementation"},
                {"name": "Add features", "type": "features"}
            ]
        else:
            # Generic decomposition
            subtasks = [
                {"name": f"Subtask 1 of {task.get('name', 'task')}", "type": "generic"},
                {"name": f"Subtask 2 of {task.get('name', 'task')}", "type": "generic"}
            ]

        return subtasks

    def _determine_child_role(self, subtask: Dict[str, Any], parent_blueprint: AgentBlueprint) -> Optional[AgentRole]:
        """Determine appropriate role for child agent"""
        task_type = subtask.get("type", "generic")

        # Role mapping based on task type
        role_map = {
            "design": AgentRole.ARCHITECT,
            "analysis": AgentRole.ANALYZER,
            "implementation": AgentRole.BUILDER,
            "features": AgentRole.BUILDER,
            "testing": AgentRole.TESTER,
            "review": AgentRole.REVIEWER,
            "documentation": AgentRole.DOCUMENTER,
            "deployment": AgentRole.DEPLOYER
        }

        return role_map.get(task_type, AgentRole.BUILDER)

    def _synthesize_results(self, agent: Agent, children_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Synthesize results from children"""
        return {
            "agent": agent.role.value,
            "synthesized": True,
            "children_count": len(children_results),
            "children_outputs": children_results
        }

    async def _execute_agent_task(self, agent: Agent) -> Dict[str, Any]:
        """Execute the agent's task with error handling"""
        try:
            logger.info(f"[*] {agent.role.value} agent executing...")

            # Simulate work with validation
            await asyncio.sleep(0.2)

            # Validate output
            output = {
                "status": "success",
                "agent": agent.role.value,
                "task": agent.task.get("name", "unnamed"),
                "result": f"Completed by {agent.role.value}"
            }

            if self.validation_engine:
                validation = self.validation_engine.validate_output(
                    output,
                    "agent_execution",
                    {"type": dict, "nullable": False}
                )
                if not validation.is_valid:
                    raise ValidationError(f"Output validation failed: {validation.errors}")

            return output

        except Exception as e:
            logger.error(f"Agent execution failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "agent": agent.role.value
            }

    async def initiate_chain_reaction(self,
                                       initial_role: AgentRole,
                                       initial_task: Dict[str, Any],
                                       max_agents: Optional[int] = None) -> Dict[str, Any]:
        """
        Start the chain reaction with error recovery.
        """
        max_agents = max_agents or self.max_agents

        logger.info(f"🔥 Initiating chain reaction with {initial_role.value}")

        try:
            # Spawn initial agent
            if self.recovery_manager:
                root_agent = await self.recovery_manager.execute_with_retry(
                    operation=lambda: self.spawn_agent(initial_role, initial_task),
                    operation_name="initial_spawn"
                )
            else:
                root_agent = await self.spawn_agent(initial_role, initial_task)

            # Start propagation
            result = await self._propagate_chain(root_agent, depth=0, max_agents=max_agents)

            # Summary
            logger.info(f"[OK] Chain reaction complete: {self.spawn_count} agents spawned")

            return {
                "status": "success",
                "root_agent": root_agent.id,
                "total_spawned": self.spawn_count,
                "result": result
            }

        except Exception as e:
            logger.error(f"Chain reaction failed: {e}")

            # Try fallback with SimpleChainReactor
            if self.recovery_manager:
                try:
                    logger.info("Attempting fallback with SimpleChainReactor")
                    simple_reactor = SimpleChainReactor(max_agents=max_agents)
                    result = await simple_reactor.spawn_chain(
                        initial_role=initial_role,
                        initial_task=initial_task
                    )
                    return result
                except Exception as fallback_error:
                    logger.error(f"Fallback also failed: {fallback_error}")

            return {
                "status": "failed",
                "error": str(e),
                "agents_spawned": self.spawn_count
            }

    def get_statistics(self) -> Dict[str, Any]:
        """Get chain reactor statistics"""
        return {
            "total_agents": self.spawn_count,
            "max_agents": self.max_agents,
            "agents_by_role": self._count_by_role(),
            "max_depth_reached": self._calculate_max_depth(),
            "circuit_breaker_status": (
                self.circuit_breaker.state.value
                if self.circuit_breaker
                else "not_available"
            )
        }

    def _count_by_role(self) -> Dict[str, int]:
        """Count agents by role"""
        counts = {}
        for agent in self.agents.values():
            role = agent.role.value
            counts[role] = counts.get(role, 0) + 1
        return counts

    def _calculate_max_depth(self) -> int:
        """Calculate maximum depth reached"""
        max_depth = 0

        def calculate_depth(agent_id: str, current_depth: int = 0):
            nonlocal max_depth
            max_depth = max(max_depth, current_depth)

            if agent_id in self.agents:
                for child_id in self.agents[agent_id].children:
                    calculate_depth(child_id, current_depth + 1)

        # Start from root agents (no parent)
        for agent_id, agent in self.agents.items():
            if agent.parent_id is None:
                calculate_depth(agent_id, 0)

        return max_depth