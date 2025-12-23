#!/usr/bin/env python3
"""
GENESIS PRIME - The Factory's Meta-Orchestrator (FIXED)
This is the first agent that starts the chain reaction of creation.
It reads project specifications and spawns the entire build process.

FIXED VERSION: Uses ImportManager for smart dependency resolution and
includes comprehensive error handling.
"""

import os
import sys
import json
import yaml
import asyncio
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Use ImportManager for smart imports
from bootstrap.import_manager import ImportManager, get_import_manager

# Initialize import manager
import_manager = get_import_manager()

# Import error handling and state management
try:
    from lib.error_handling import (
        RecoveryManager, ValidationEngine, CircuitBreaker,
        ValidationError, RecoveryFailedError
    )
    from lib.state_management import CheckpointManager, ProgressTracker, BuildPhase
    ERROR_HANDLING_AVAILABLE = True
except ImportError:
    safe_print("⚠️ Error handling not available - running in basic mode")
    ERROR_HANDLING_AVAILABLE = False

# Get SOVEREIGN components with fallback
BaseAgent, ConsciousnessSubstrate = import_manager.get_sovereign_classes()
NeuralCore, remember_pattern, get_recommendation = import_manager.get_neural_components()

# Import fallbacks
from lib.fallback_implementations import SimpleOrchestrator, SimpleChainReactor, AgentRole

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def safe_print(text):
    """Print text, falling back to ASCII if Unicode fails"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Replace common Unicode characters with ASCII equivalents
        replacements = {
            '✅': '[OK]', '❌': '[X]', '⚠️': '[!]', '⚠': '[!]',
            '🔍': '[?]', '📦': '[*]', '🎉': '!!!', '🏭': '[#]',
            '📁': '[D]', '📋': '[F]', '💡': '[i]', '✨': '[*]',
            '🚀': '>>>', '⏱': '[T]', '📊': '[G]', '🔧': '[T]',
            '💾': '[S]', '📍': '[L]', '🤖': '[R]', '👋': '[W]',
            '🎨': '[A]', '📝': '[E]', '🔥': '[F]',
            '╔': '=', '═': '=', '╗': '=', '║': '|', '╚': '=', '╝': '=',
            '╠': '|', '╣': '|', '╦': '=', '╩': '=', '╬': '+',
            '█': '#', '▓': '#', '▒': ':', '░': '.',
            '▀': '-', '▄': '_', '▌': '|', '▐': '|',
        }
        for unicode_char, ascii_char in replacements.items():
            text = text.replace(unicode_char, ascii_char)
        safe_print(text)


class ProjectType(Enum):
    WEB_APP = "web_app"
    API_SERVICE = "api"
    DATA_PIPELINE = "data_pipeline"
    AI_SYSTEM = "ai_system"
    CLI_TOOL = "cli_tool"
    LIBRARY = "library"
    CUSTOM = "custom"


class ComplexityLevel(Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    EXTREME = "extreme"


class OrchestrationParadigm(Enum):
    HIERARCHICAL = "hierarchical"
    SWARM = "swarm"
    NEURAL = "neural"
    TEMPORAL = "temporal"
    HYBRID = "hybrid"
    AUTO = "auto"


@dataclass
class ProjectSpecification:
    """Parsed project specification"""
    name: str = "Unknown Project"
    description: str = ""
    type: ProjectType = ProjectType.CUSTOM
    complexity: ComplexityLevel = ComplexityLevel.MODERATE
    paradigm: OrchestrationParadigm = OrchestrationParadigm.AUTO
    objectives: List[str] = None
    features: Dict[str, List[str]] = None
    architecture: Dict[str, Any] = None
    technical: Dict[str, str] = None
    quality: Dict[str, str] = None
    output: List[str] = None
    tech_stack: List[str] = None
    raw_spec: str = ""

    def __post_init__(self):
        if self.objectives is None:
            self.objectives = []
        if self.features is None:
            self.features = {"core": [], "optional": []}
        if self.architecture is None:
            self.architecture = {}
        if self.technical is None:
            self.technical = {}
        if self.quality is None:
            self.quality = {}
        if self.output is None:
            self.output = []
        if self.tech_stack is None:
            self.tech_stack = []


class GenesisPrime:
    """
    The Prime Orchestrator - First agent in The Factory.
    Reads specifications and initiates the chain reaction of creation.
    """

    def __init__(self, spec_path: str = None, output_dir: str = None, resume_checkpoint: str = None):
        self.spec_path = Path(spec_path) if spec_path else Path("specs/project_spec.md")
        self.output_dir = Path(output_dir) if output_dir else Path("outputs/project_root")
        self.resume_checkpoint = resume_checkpoint

        # Core components
        self.orchestrator = None
        self.chain_reactor = None
        self.project_spec = None

        # Error handling and state management
        if ERROR_HANDLING_AVAILABLE:
            self.recovery_manager = RecoveryManager(max_retries=3)
            self.validation_engine = ValidationEngine()
            self.circuit_breaker = CircuitBreaker(name="genesis_prime")
            self.checkpoint_manager = CheckpointManager()
            self.progress_tracker = ProgressTracker()
        else:
            self.recovery_manager = None
            self.validation_engine = None
            self.circuit_breaker = None
            self.checkpoint_manager = None
            self.progress_tracker = None

        # Initialize components
        self._initialize_components()

    def _initialize_components(self):
        """Initialize orchestrator and other components with fallback"""
        try:
            # Get orchestrator with fallback cascade
            self.orchestrator = import_manager.get_orchestrator(
                paradigm="SOVEREIGN",
                config={"name": "GenesisPrime"}
            )
            logger.info(f"Initialized orchestrator: {type(self.orchestrator).__name__}")

            # Get chain reactor
            self.chain_reactor = import_manager.get_component("chain_reactor")
            if not self.chain_reactor:
                self.chain_reactor = SimpleChainReactor(max_agents=100)
            logger.info(f"Initialized chain reactor: {type(self.chain_reactor).__name__}")

            # Try to initialize advanced components if available
            if BaseAgent and ConsciousnessSubstrate:
                try:
                    self.consciousness = ConsciousnessSubstrate()
                    logger.info("[OK] ConsciousnessSubstrate activated")
                except Exception as e:
                    logger.warning(f"Could not initialize consciousness: {e}")
                    self.consciousness = None

            if NeuralCore:
                try:
                    self.neural_core = NeuralCore()
                    logger.info("[OK] NeuralCore activated")
                except Exception as e:
                    logger.warning(f"Could not initialize neural core: {e}")
                    self.neural_core = None

        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            # Use minimal fallbacks
            self.orchestrator = SimpleOrchestrator()
            self.chain_reactor = SimpleChainReactor()

    def read_specification(self, spec_file: Path) -> str:
        """Read project specification from file or text"""
        # Validate file exists
        if not spec_file.exists():
            # Check if it's actually spec text passed as string
            if len(str(spec_file)) < 260 and "\n" in str(spec_file):
                # Likely spec text, not a path
                return str(spec_file)
            raise FileNotFoundError(f"Specification not found: {spec_file}")

        # Validate file is readable
        if not os.access(spec_file, os.R_OK):
            raise PermissionError(f"Cannot read specification: {spec_file}")

        # Validate file size
        file_size = spec_file.stat().st_size
        if file_size == 0:
            raise ValueError(f"Specification file is empty: {spec_file}")
        if file_size > 10_000_000:  # 10MB limit
            raise ValueError(f"Specification file too large: {file_size} bytes")

        # Read file
        try:
            with open(spec_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Validate content
            if len(content.strip()) < 10:
                raise ValueError("Specification content too short")

            return content

        except UnicodeDecodeError:
            raise ValueError(f"Specification file encoding error: {spec_file}")

    def parse_specification(self, spec_text: str) -> ProjectSpecification:
        """Parse specification into structured format with validation"""
        if not spec_text or len(spec_text.strip()) < 10:
            raise ValueError("Invalid specification text")

        # Initialize spec with defaults
        spec = ProjectSpecification()

        # Parse based on format
        if spec_text.strip().startswith('{'):
            # JSON format
            spec = self._parse_json_spec(spec_text)
        elif spec_text.strip().startswith('---'):
            # YAML format
            spec = self._parse_yaml_spec(spec_text)
        else:
            # Markdown or plain text format
            spec = self._parse_markdown_spec(spec_text)

        # Store raw spec
        spec.raw_spec = spec_text

        # Validate specification
        if self.validation_engine:
            result = self.validation_engine.validate_spec(spec)
            if not result.is_valid:
                logger.warning(f"Specification validation warnings: {result.errors}")
                # Don't fail, just warn

        return spec

    def _parse_markdown_spec(self, spec_text: str) -> ProjectSpecification:
        """Parse markdown format specification"""
        lines = spec_text.split('\n')
        spec = ProjectSpecification()

        # Extract basic info
        current_section = None

        # Try to extract tech stack from YAML frontmatter or content
        try:
            # Look for technology mentions in the spec
            tech_keywords = ['react', 'vue', 'angular', 'python', 'fastapi', 'django', 'flask',
                           'node', 'express', 'typescript', 'javascript', 'postgresql', 'mysql',
                           'mongodb', 'redis', 'docker', 'kubernetes', 'aws', 'azure', 'gcp',
                           'tailwind', 'bootstrap', 'nextjs', 'nuxt', 'svelte']

            spec_text_lower = spec_text.lower()
            for tech in tech_keywords:
                if tech in spec_text_lower:
                    spec.tech_stack.append(tech.title())
        except:
            pass

        for line in lines:
            line_stripped = line.strip()

            # Project name from H1
            if line.startswith("# "):
                spec.name = line[2:].strip()

            # Description from first paragraph
            elif spec.name and not spec.description and line_stripped and not line.startswith('#'):
                spec.description = line_stripped

            # Sections
            elif line.startswith("## "):
                current_section = line[3:].strip().upper()

            # Parse section content
            elif current_section and line_stripped:
                if "TYPE:" in line.upper():
                    type_str = line.split(':')[1].strip().lower().replace(' ', '_')
                    try:
                        spec.type = ProjectType(type_str)
                    except:
                        spec.type = ProjectType.CUSTOM

                elif "COMPLEXITY:" in line.upper():
                    comp_str = line.split(':')[1].strip().lower()
                    try:
                        spec.complexity = ComplexityLevel(comp_str)
                    except:
                        spec.complexity = ComplexityLevel.MODERATE

                elif current_section == "OBJECTIVES" and line_stripped.startswith(("-", "*", "•")):
                    spec.objectives.append(line_stripped.lstrip("-*• "))

                elif current_section == "FEATURES":
                    if line_stripped.startswith(("-", "*", "•")):
                        feature = line_stripped.lstrip("-*• ")
                        if "[core]" in feature.lower() or "core:" in feature.lower():
                            spec.features["core"].append(feature.replace("[core]", "").replace("Core:", "").strip())
                        elif "[optional]" in feature.lower() or "optional:" in feature.lower():
                            spec.features["optional"].append(feature.replace("[optional]", "").replace("Optional:", "").strip())
                        else:
                            spec.features["core"].append(feature)

        # Ensure we have at least basic info
        if spec.name == "Unknown Project":
            # Try to extract from first line
            first_line = next((l for l in lines if l.strip()), "")
            if first_line:
                spec.name = first_line.strip().lstrip("#").strip()

        if not spec.objectives:
            spec.objectives = ["Build a working system"]

        if not spec.features["core"]:
            spec.features["core"] = ["Basic functionality"]

        return spec

    def _parse_json_spec(self, spec_text: str) -> ProjectSpecification:
        """Parse JSON format specification"""
        try:
            data = json.loads(spec_text)
            spec = ProjectSpecification()

            spec.name = data.get('name', 'Unknown Project')
            spec.description = data.get('description', '')
            spec.type = ProjectType(data.get('type', 'custom'))
            spec.complexity = ComplexityLevel(data.get('complexity', 'moderate'))
            spec.objectives = data.get('objectives', [])
            spec.features = data.get('features', {"core": [], "optional": []})
            spec.tech_stack = data.get('tech_stack', [])
            spec.architecture = data.get('architecture', {})
            spec.technical = data.get('technical', {})
            spec.quality = data.get('quality', {})

            return spec
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.error(f"Failed to parse JSON spec: {e}")
            return self._parse_markdown_spec(spec_text)

    def _parse_yaml_spec(self, spec_text: str) -> ProjectSpecification:
        """Parse YAML format specification"""
        try:
            data = yaml.safe_load(spec_text)
            spec = ProjectSpecification()

            spec.name = data.get('name', 'Unknown Project')
            spec.description = data.get('description', '')
            spec.type = ProjectType(data.get('type', 'custom'))
            spec.complexity = ComplexityLevel(data.get('complexity', 'moderate'))
            spec.objectives = data.get('objectives', [])
            spec.features = data.get('features', {"core": [], "optional": []})
            spec.tech_stack = data.get('tech_stack', [])
            spec.architecture = data.get('architecture', {})
            spec.technical = data.get('technical', {})
            spec.quality = data.get('quality', {})

            return spec
        except (yaml.YAMLError, KeyError, ValueError) as e:
            logger.error(f"Failed to parse YAML spec: {e}")
            return self._parse_markdown_spec(spec_text)

    def determine_orchestration_strategy(self, spec: ProjectSpecification) -> Dict[str, Any]:
        """Determine optimal orchestration strategy based on specification"""
        strategy = {
            "paradigm": spec.paradigm.value,
            "num_agents": 5,
            "parallel_teams": 1,
            "iterations": 1,
            "quality_gates": True
        }

        # Auto-determine paradigm if needed
        if spec.paradigm == OrchestrationParadigm.AUTO:
            if spec.complexity == ComplexityLevel.SIMPLE:
                strategy["paradigm"] = "hierarchical"
                strategy["num_agents"] = 5
            elif spec.complexity == ComplexityLevel.MODERATE:
                strategy["paradigm"] = "swarm"
                strategy["num_agents"] = 20
            elif spec.complexity == ComplexityLevel.COMPLEX:
                strategy["paradigm"] = "neural"
                strategy["num_agents"] = 50
            else:  # EXTREME
                strategy["paradigm"] = "hybrid"
                strategy["num_agents"] = 100

        # Determine parallel teams
        if spec.complexity in [ComplexityLevel.COMPLEX, ComplexityLevel.EXTREME]:
            strategy["parallel_teams"] = 3 if spec.complexity == ComplexityLevel.COMPLEX else 5

        return strategy

    async def spawn_chain_reaction(self, spec: ProjectSpecification, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """
        INITIATE THE CHAIN REACTION
        Actually builds the project using orchestrator and agents
        """
        logger.info(f"🔥 INITIATING CHAIN REACTION for: {spec.name}")
        logger.info(f"   Strategy: {strategy}")

        # Start progress tracking
        if self.progress_tracker:
            self.progress_tracker.start_build()
            self.progress_tracker.start_phase(BuildPhase.BUILDING)

        # Use appropriate orchestrator
        if isinstance(self.orchestrator, SimpleOrchestrator):
            # Use simple orchestrator for basic builds
            result = await self.orchestrator.build_project(spec, self.output_dir)
        else:
            # Use advanced orchestrator if available
            try:
                result = await self.orchestrator.build_project(spec, self.output_dir)
            except Exception as e:
                logger.error(f"Advanced orchestrator failed: {e}")
                # Fallback to simple orchestrator
                logger.info("Falling back to SimpleOrchestrator")
                simple_orch = SimpleOrchestrator()
                result = await simple_orch.build_project(spec, self.output_dir)

        # Complete progress tracking
        if self.progress_tracker:
            self.progress_tracker.complete_phase(BuildPhase.BUILDING)
            self.progress_tracker.end_build(success=result.get('status') == 'success')

        return result

    def generate_output_structure(self, spec: ProjectSpecification):
        """Generate the output directory structure"""
        logger.info(f"Generating output structure in {self.output_dir}")

        # Create base directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # The actual project structure is created by the orchestrator
        # This just ensures the output directory exists
        logger.info(f"Output directory ready: {self.output_dir}")

    async def build(self):
        """Main build process with error handling"""
        try:
            # Check for resume
            if self.resume_checkpoint and self.checkpoint_manager:
                if self.checkpoint_manager.can_resume(self.resume_checkpoint):
                    logger.info(f"Resuming from checkpoint: {self.resume_checkpoint}")
                    state = self.checkpoint_manager.load_checkpoint(self.resume_checkpoint)
                    self.project_spec = state.get('project_spec')
                    # Continue from checkpoint
                else:
                    logger.warning(f"Cannot resume from checkpoint: {self.resume_checkpoint}")

            # Read specification
            logger.info(f"Reading specification from {self.spec_path}")
            spec_text = self.read_specification(self.spec_path)

            # Parse specification
            logger.info("Parsing specification...")
            self.project_spec = self.parse_specification(spec_text)
            logger.info(f"Project: {self.project_spec.name}")
            logger.info(f"Type: {self.project_spec.type.value}")
            logger.info(f"Complexity: {self.project_spec.complexity.value}")

            # Save checkpoint after parsing
            if self.checkpoint_manager:
                self.checkpoint_manager.save_checkpoint(
                    "parsed_spec",
                    {"project_spec": self.project_spec},
                    metadata={"phase": "specification"}
                )

            # Determine strategy
            logger.info("Determining orchestration strategy...")
            strategy = self.determine_orchestration_strategy(self.project_spec)

            # Generate output structure
            self.generate_output_structure(self.project_spec)

            # Spawn chain reaction (actual build)
            logger.info("Starting build process...")
            result = await self.spawn_chain_reaction(self.project_spec, strategy)

            # Final validation
            if result.get('status') == 'success':
                logger.info("[OK] BUILD COMPLETE!")
                logger.info(f"Output: {self.output_dir}")
                safe_print("\n" + "="*60)
                safe_print("🎉 THE FACTORY HAS COMPLETED YOUR PROJECT!")
                safe_print(f"📁 Output directory: {self.output_dir}")
                safe_print("="*60)
            else:
                logger.error("[X] Build failed")
                safe_print(f"\n❌ Build failed: {result.get('error', 'Unknown error')}")

            return result

        except Exception as e:
            logger.error(f"Build failed with error: {e}")
            if self.recovery_manager:
                # Try recovery
                logger.info("Attempting recovery...")
                try:
                    fallback = SimpleOrchestrator()
                    result = await fallback.build_project(
                        self.project_spec or ProjectSpecification(name="Recovery Build"),
                        self.output_dir
                    )
                    return result
                except Exception as recovery_error:
                    logger.error(f"Recovery also failed: {recovery_error}")

            raise


def main():
    """Main entry point with CLI interface"""
    parser = argparse.ArgumentParser(
        description="GENESIS PRIME - The Factory's Meta-Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Build from specification file
  python genesis_prime.py --spec project_spec.md --output ./my_project

  # Build from prompt
  python genesis_prime.py --prompt "Create a todo app with React"

  # Resume from checkpoint
  python genesis_prime.py --resume checkpoint_123

  # Build with specific paradigm
  python genesis_prime.py --spec spec.md --paradigm neural
        """
    )

    parser.add_argument('--spec', '-s', type=str, help='Path to project specification')
    parser.add_argument('--prompt', '-p', type=str, help='Direct prompt for project')
    parser.add_argument('--output', '-o', type=str, help='Output directory')
    parser.add_argument('--paradigm', type=str, choices=['hierarchical', 'swarm', 'neural', 'hybrid', 'auto'],
                        default='auto', help='Orchestration paradigm')
    parser.add_argument('--complexity', type=str, choices=['simple', 'moderate', 'complex', 'extreme'],
                        default='moderate', help='Project complexity')
    parser.add_argument('--resume', '-r', type=str, help='Resume from checkpoint')
    parser.add_argument('--build', action='store_true', help='Start build immediately')
    parser.add_argument('--validate', action='store_true', help='Validate environment')

    args = parser.parse_args()

    # Validate environment if requested
    if args.validate:
        validation = import_manager.validate_environment()
        safe_print("\n" + "="*60)
        safe_print("ENVIRONMENT VALIDATION")
        safe_print("="*60)
        safe_print(f"Mode: {validation['mode']}")
        safe_print(f"Components Available: {validation['components_available']}")
        if validation['warnings']:
            safe_print(f"Warnings: {validation['warnings']}")
        if validation['errors']:
            safe_print(f"Errors: {validation['errors']}")
        safe_print("="*60)
        return

    # Handle prompt mode
    if args.prompt:
        # Convert prompt to simple specification
        spec_text = f"""# {args.prompt}

## OBJECTIVES
- Build a working implementation based on the prompt

## FEATURES
- Core functionality as described
- Basic error handling
- Documentation

## OUTPUT
- Source code
- README
- Basic tests
"""
        # Create temp spec file
        spec_path = Path("temp_spec.md")
        spec_path.write_text(spec_text)
    else:
        spec_path = args.spec or "project_spec.md"

    # Check if spec exists or create example
    spec_path = Path(spec_path)
    if not spec_path.exists() and not args.prompt:
        safe_print(f"⚠️  Specification not found: {spec_path}")
        create_example = input("Would you like to create an example specification? (y/n): ")
        if create_example.lower() == 'y':
            example_spec = """# Example Todo App

A simple todo application for demonstration.

## Type: web_app
## Complexity: simple

## OBJECTIVES
- Create a functional todo application
- Allow users to add, edit, and delete tasks
- Persist data locally

## FEATURES
### Core Features
- Add new todos
- Mark todos as complete
- Delete todos
- Filter todos (all/active/completed)

### Optional Features
- Due dates
- Categories
- Search functionality

## TECHNICAL
- Language: Python or JavaScript
- Framework: Flask or React
- Database: SQLite or LocalStorage

## OUTPUT
- Source code
- README with instructions
- Basic tests
- Example data
"""
            spec_path.write_text(example_spec)
            safe_print(f"✅ Created example specification: {spec_path}")
        else:
            safe_print("Please provide a specification file or use --prompt")
            return

    # Initialize and run
    output_dir = args.output or f"outputs/{spec_path.stem}"

    safe_print("\n" + "="*60)
    safe_print("🏭 THE FACTORY - GENESIS PRIME")
    safe_print("="*60)
    safe_print(f"Specification: {spec_path}")
    safe_print(f"Output: {output_dir}")
    safe_print(f"Paradigm: {args.paradigm}")
    safe_print(f"Complexity: {args.complexity}")
    safe_print("="*60 + "\n")

    # Create genesis prime instance
    genesis = GenesisPrime(
        spec_path=str(spec_path),
        output_dir=output_dir,
        resume_checkpoint=args.resume
    )

    # Override complexity if specified
    if args.complexity and genesis.project_spec:
        genesis.project_spec.complexity = ComplexityLevel(args.complexity)

    # Run build
    if args.build or args.prompt or input("Start build? (y/n): ").lower() == 'y':
        try:
            result = asyncio.run(genesis.build())
            exit(0 if result.get('status') == 'success' else 1)
        except KeyboardInterrupt:
            safe_print("\n⚠️  Build interrupted by user")
            if genesis.checkpoint_manager:
                latest = genesis.checkpoint_manager.get_latest_checkpoint()
                if latest:
                    safe_print(f"💾 Latest checkpoint: {latest['checkpoint_id']}")
                    safe_print(f"   Resume with: --resume {latest['checkpoint_id']}")
            exit(1)
        except Exception as e:
            safe_print(f"\n❌ Build failed: {e}")
            exit(1)
    else:
        safe_print("Build cancelled")


if __name__ == "__main__":
    main()