"""
Import Manager for The Factory
Handles smart dependency resolution with fallback cascade for standalone/integrated modes.

This module auto-detects the running mode and provides appropriate implementations
with graceful degradation when dependencies are unavailable.
"""

import sys
import importlib
import importlib.util
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, Callable, List
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RunMode(Enum):
    """System running modes"""
    STANDALONE = "standalone"    # Using lib/ directory
    INTEGRATED = "integrated"     # Using THE_ORCHESTRATOR
    MINIMAL = "minimal"          # Fallback only


class ImportManager:
    """
    Smart import manager that handles standalone and integrated modes.
    Provides fallback cascade for all critical dependencies.
    """

    def __init__(self):
        """Initialize import manager and detect running mode"""
        self.factory_root = Path(__file__).parent.parent
        self.orchestrator_path = None  # Will be set by detect_mode if found
        self.mode = self.detect_mode()
        self.loaded_modules = {}
        self.fallback_registry = {}

        # Configure paths based on mode
        self._configure_paths()

        logger.info(f"ImportManager initialized in {self.mode.value} mode")

    def detect_mode(self) -> RunMode:
        """
        Detect if running in standalone or integrated mode.

        Returns:
            RunMode: The detected running mode
        """
        # Check for THE_ORCHESTRATOR (integrated mode) - search multiple locations
        orchestrator_paths = [
            self.factory_root.parent / "THE_ORCHESTRATOR",  # ../THE_ORCHESTRATOR
            self.factory_root.parent.parent / "THE_ORCHESTRATOR",  # ../../THE_ORCHESTRATOR
        ]

        for orchestrator_path in orchestrator_paths:
            if orchestrator_path.exists() and orchestrator_path.is_dir():
                logger.info(f"Detected THE_ORCHESTRATOR at {orchestrator_path}")
                self.orchestrator_path = orchestrator_path  # Store for later use
                return RunMode.INTEGRATED

        # Check for lib/ directory (standalone mode)
        lib_path = self.factory_root / "lib"
        if lib_path.exists() and lib_path.is_dir():
            # Verify it has content
            if any(lib_path.iterdir()):
                logger.info(f"Detected lib/ directory at {lib_path}")
                return RunMode.STANDALONE

        # Neither exists - minimal mode with fallbacks only
        logger.warning("Neither lib/ nor THE_ORCHESTRATOR found - using minimal mode")
        return RunMode.MINIMAL

    def _configure_paths(self):
        """Configure Python paths based on detected mode"""
        if self.mode == RunMode.STANDALONE:
            # Add lib/ to path for standalone mode
            lib_path = str(self.factory_root / "lib")
            if lib_path not in sys.path:
                sys.path.insert(0, lib_path)
                logger.info(f"Added {lib_path} to sys.path")

        elif self.mode == RunMode.INTEGRATED:
            # Add THE_ORCHESTRATOR to path for integrated mode
            if self.orchestrator_path:
                orchestrator_path_str = str(self.orchestrator_path)
                if orchestrator_path_str not in sys.path:
                    sys.path.insert(0, orchestrator_path_str)
                    logger.info(f"Added {orchestrator_path_str} to sys.path")

    def get_sovereign_classes(self) -> Tuple[Optional[type], Optional[type]]:
        """
        Get SOVEREIGN classes with fallback.

        Returns:
            Tuple of (BaseAgent, ConsciousnessSubstrate) or (None, None) if unavailable
        """
        # Try cascade: integrated -> standalone -> None
        attempts = []

        if self.mode == RunMode.INTEGRATED:
            attempts.append(("SOVEREIGN_AGENTS.CORE.sovereign_core", "integrated"))
        elif self.mode == RunMode.STANDALONE:
            attempts.append(("SOVEREIGN_AGENTS.CORE.sovereign_core", "standalone"))

        for module_path, source in attempts:
            try:
                module = importlib.import_module(module_path)
                BaseAgent = getattr(module, "BaseAgent", None)
                ConsciousnessSubstrate = getattr(module, "ConsciousnessSubstrate", None)

                if BaseAgent and ConsciousnessSubstrate:
                    logger.info(f"Successfully loaded SOVEREIGN classes from {source}")
                    return BaseAgent, ConsciousnessSubstrate
            except (ImportError, AttributeError) as e:
                logger.debug(f"Could not load SOVEREIGN classes from {source}: {e}")
                continue

        logger.warning("SOVEREIGN classes not available - will use fallbacks")
        return None, None

    def get_neural_components(self) -> Tuple[Optional[type], Optional[Callable], Optional[Callable]]:
        """
        Get Neural Overlay components with fallback.

        Returns:
            Tuple of (NeuralCore, remember_pattern, get_recommendation) or fallbacks
        """
        # Try to load real neural components
        attempts = []

        if self.mode == RunMode.INTEGRATED:
            attempts.append(("NEVER_FORGET", "integrated"))
        elif self.mode == RunMode.STANDALONE:
            attempts.append(("NEVER_FORGET", "standalone"))

        for base_module, source in attempts:
            try:
                # Try to import NeuralCore
                neural_module = importlib.import_module(f"{base_module}.neural_core")
                NeuralCore = getattr(neural_module, "NeuralCore", None)

                # Try to import hook functions
                hook_module = importlib.import_module(f"{base_module}.minimal_hook")
                remember_pattern = getattr(hook_module, "remember_pattern", None)
                get_recommendation = getattr(hook_module, "get_recommendation", None)

                if NeuralCore and remember_pattern and get_recommendation:
                    logger.info(f"Successfully loaded Neural components from {source}")
                    return NeuralCore, remember_pattern, get_recommendation
            except (ImportError, AttributeError) as e:
                logger.debug(f"Could not load Neural components from {source}: {e}")
                continue

        # Return mock implementations if real ones unavailable
        logger.info("Using mock Neural components")
        from lib.fallback_implementations.mock_neural import (
            MockNeuralCore, mock_remember_pattern, mock_get_recommendation
        )
        return MockNeuralCore, mock_remember_pattern, mock_get_recommendation

    def get_orchestrator(self, paradigm: str = "SOVEREIGN", config: Optional[Dict[str, Any]] = None):
        """
        Get orchestrator with fallback cascade.

        Args:
            paradigm: Requested paradigm (will fallback if unavailable)
            config: Configuration for orchestrator

        Returns:
            Orchestrator instance (SOVEREIGN, Simple, or Minimal)
        """
        config = config or {}

        # Define fallback cascade
        orchestrator_cascade = []

        # Try SOVEREIGN first if available
        if self.mode in [RunMode.INTEGRATED, RunMode.STANDALONE]:
            orchestrator_cascade.append(("sovereign", self._try_sovereign_orchestrator))

        # Always include simple orchestrator as fallback
        orchestrator_cascade.append(("simple", self._try_simple_orchestrator))

        # Minimal as last resort
        orchestrator_cascade.append(("minimal", self._try_minimal_orchestrator))

        # Try each orchestrator in cascade
        for name, factory in orchestrator_cascade:
            try:
                orchestrator = factory(paradigm, config)
                if orchestrator:
                    logger.info(f"Using {name} orchestrator")
                    return orchestrator
            except Exception as e:
                logger.warning(f"{name} orchestrator unavailable: {e}")
                continue

        raise RuntimeError("No orchestrator available - system cannot function")

    def _try_sovereign_orchestrator(self, paradigm: str, config: Dict[str, Any]):
        """Try to load SOVEREIGN orchestrator"""
        try:
            if self.mode == RunMode.INTEGRATED:
                from sovereign_loader import SovereignLoader
            elif self.mode == RunMode.STANDALONE:
                from lib.SOVEREIGN_AGENTS.SOVEREIGN.the_sovereign import TheSovereign
                return TheSovereign(config)
            else:
                return None

            loader = SovereignLoader()
            return loader.create_orchestrator(paradigm, config)
        except ImportError as e:
            logger.debug(f"SOVEREIGN orchestrator not available: {e}")
            return None

    def _try_simple_orchestrator(self, paradigm: str, config: Dict[str, Any]):
        """Try to load Simple orchestrator"""
        try:
            from lib.fallback_implementations.simple_orchestrator import SimpleOrchestrator
            return SimpleOrchestrator(config)
        except ImportError as e:
            logger.debug(f"Simple orchestrator not available: {e}")
            return None

    def _try_minimal_orchestrator(self, paradigm: str, config: Dict[str, Any]):
        """Load minimal orchestrator (always available)"""
        # Inline minimal implementation - always works
        logger.warning("Using minimal orchestrator - very limited functionality")

        class MinimalOrchestrator:
            """Absolute minimal orchestrator for emergency fallback"""

            def __init__(self, config):
                self.config = config

            async def build_project(self, spec, output_dir):
                """Minimal build - just creates structure"""
                output_dir.mkdir(parents=True, exist_ok=True)
                (output_dir / "src").mkdir(exist_ok=True)
                (output_dir / "tests").mkdir(exist_ok=True)
                (output_dir / "docs").mkdir(exist_ok=True)

                # Create minimal README
                readme = output_dir / "README.md"
                readme.write_text(f"# {spec.name}\n\nProject created by The Factory (minimal mode)")

                return {
                    "status": "success",
                    "mode": "minimal",
                    "output_dir": str(output_dir)
                }

        return MinimalOrchestrator(config)

    def get_chain_reactor(self):
        """
        Get ChainReactor implementation with fallback.

        Returns:
            ChainReactor instance or fallback
        """
        # Try to import the real ChainReactor
        try:
            from chain_reactor import ChainReactor
            logger.info("Using standard ChainReactor")
            return ChainReactor
        except ImportError:
            # Use simple fallback
            logger.warning("Using fallback ChainReactor")
            from lib.fallback_implementations.simple_agent import SimpleChainReactor
            return SimpleChainReactor

    def register_fallback(self, component: str, fallback: Callable):
        """
        Register a fallback for a component.

        Args:
            component: Component name
            fallback: Fallback implementation
        """
        self.fallback_registry[component] = fallback
        logger.info(f"Registered fallback for {component}")

    def get_component(self, component: str, *args, **kwargs):
        """
        Get a component with automatic fallback.

        Args:
            component: Component name
            *args, **kwargs: Arguments for component initialization

        Returns:
            Component instance
        """
        # Try to get the real component
        component_map = {
            "orchestrator": self.get_orchestrator,
            "chain_reactor": self.get_chain_reactor,
            "sovereign": self.get_sovereign_classes,
            "neural": self.get_neural_components,
        }

        if component in component_map:
            return component_map[component](*args, **kwargs)

        # Check for registered fallback
        if component in self.fallback_registry:
            logger.info(f"Using registered fallback for {component}")
            return self.fallback_registry[component](*args, **kwargs)

        raise ValueError(f"Unknown component: {component}")

    def validate_environment(self) -> Dict[str, Any]:
        """
        Validate the environment and available components.

        Returns:
            Dictionary of validation results
        """
        validation = {
            "mode": self.mode.value,
            "components_available": {},
            "paths_configured": [],
            "warnings": [],
            "errors": []
        }

        # Check SOVEREIGN availability
        base_agent, consciousness = self.get_sovereign_classes()
        validation["components_available"]["sovereign"] = base_agent is not None

        # Check Neural availability
        neural_core, _, _ = self.get_neural_components()
        validation["components_available"]["neural"] = neural_core.__name__ != "MockNeuralCore"

        # Check orchestrator availability
        try:
            orch = self.get_orchestrator()
            validation["components_available"]["orchestrator"] = True
        except:
            validation["components_available"]["orchestrator"] = False
            validation["errors"].append("No orchestrator available")

        # Check paths
        validation["paths_configured"] = [p for p in sys.path if "the_factory" in p]

        # Add warnings based on mode
        if self.mode == RunMode.MINIMAL:
            validation["warnings"].append("Running in minimal mode - limited functionality")
        elif self.mode == RunMode.STANDALONE:
            validation["warnings"].append("Running in standalone mode - using local copies")

        return validation

    def __repr__(self):
        return f"ImportManager(mode={self.mode.value})"


# Singleton instance
_import_manager_instance = None


def get_import_manager() -> ImportManager:
    """
    Get the singleton ImportManager instance.

    Returns:
        ImportManager: The singleton instance
    """
    global _import_manager_instance
    if _import_manager_instance is None:
        _import_manager_instance = ImportManager()
    return _import_manager_instance


# Convenience functions
def detect_mode() -> str:
    """Detect and return the current running mode"""
    return get_import_manager().mode.value


def get_orchestrator(*args, **kwargs):
    """Get orchestrator with automatic fallback"""
    return get_import_manager().get_orchestrator(*args, **kwargs)


def get_sovereign_classes():
    """Get SOVEREIGN classes with fallback"""
    return get_import_manager().get_sovereign_classes()


def validate_environment():
    """Validate the current environment"""
    return get_import_manager().validate_environment()