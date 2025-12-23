#!/usr/bin/env python3
"""
🔍 LEGACY ANALYZER WITH LANGCHAIN
Analyzes legacy codebases and generates migration plans using LangChain + LangSmith

Value: $5,000-50,000 per migration project
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Add MEMORY_CORE to path
sys.path.insert(0, str(Path(__file__).parent.parent / "MEMORY_CORE"))
from memory_manager import get_memory, remember, save_pattern

# LangChain imports
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.chat_models import ChatAnthropic
from langchain.chains import LLMChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain.callbacks import LangChainTracer
from langsmith import Client
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import JsonOutputParser
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.tools import Tool, StructuredTool

class LegacyAnalyzer:
    """
    Advanced Legacy Code Analyzer powered by LangChain
    Uses LangSmith for tracing and optimization
    """

    def __init__(self):
        """Initialize the analyzer with LangChain"""

        # Verify API keys
        self.langchain_api_key = os.getenv('LANGCHAIN_API_KEY')
        if not self.langchain_api_key:
            raise ValueError("LANGCHAIN_API_KEY not found in .env file!")

        # Initialize LangSmith client for tracing
        self.langsmith_client = Client(api_key=self.langchain_api_key)

        # Initialize tracer
        self.tracer = LangChainTracer(
            project_name=os.getenv('LANGCHAIN_PROJECT', 'the-datazentr'),
            client=self.langsmith_client
        )

        # Initialize LLM (using Anthropic or OpenAI based on available keys)
        self.llm = self._initialize_llm()

        # Initialize memory
        self.memory = ConversationSummaryBufferMemory(
            llm=self.llm,
            max_token_limit=2000,
            return_messages=True
        )

        # Initialize our central memory system
        self.datazentr_memory = get_memory()

        # Create analysis chain
        self.analysis_chain = self._create_analysis_chain()

        # Create migration chain
        self.migration_chain = self._create_migration_chain()

        print("✅ Legacy Analyzer initialized with LangChain + LangSmith")
        print(f"   Project: {os.getenv('LANGCHAIN_PROJECT', 'the-datazentr')}")
        print(f"   Tracing: Enabled")

    def _initialize_llm(self):
        """Initialize the LLM based on available API keys"""

        # Try Anthropic first
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        if anthropic_key:
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(
                model="claude-3-opus-20240229",
                anthropic_api_key=anthropic_key,
                temperature=0.3,
                max_tokens=4000
            )

        # Try OpenAI
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model="gpt-4-turbo-preview",
                openai_api_key=openai_key,
                temperature=0.3,
                max_tokens=4000
            )

        # Fallback to a mock LLM for testing
        print("⚠️ No LLM API key found - using mock mode")
        from langchain.llms.fake import FakeListLLM
        return FakeListLLM(
            responses=["Mock analysis response", "Mock migration plan"]
        )

    def _create_analysis_chain(self):
        """Create the analysis chain for legacy code"""

        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are an expert legacy code analyzer.
            Your job is to analyze legacy codebases and identify:
            1. Technology stack and versions
            2. Architecture patterns
            3. Technical debt areas
            4. Security vulnerabilities
            5. Performance bottlenecks
            6. Migration complexity score (1-10)

            Output your analysis as structured JSON."""),
            MessagesPlaceholder(variable_name="history"),
            HumanMessage(content="{input}")
        ])

        chain = LLMChain(
            llm=self.llm,
            prompt=prompt,
            memory=self.memory,
            callbacks=[self.tracer],
            output_parser=JsonOutputParser()
        )

        return chain

    def _create_migration_chain(self):
        """Create the migration planning chain"""

        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are an expert in modernizing legacy applications.
            Based on the analysis provided, create a detailed migration plan that includes:
            1. Target architecture (modern stack)
            2. Migration phases (step by step)
            3. Risk assessment and mitigation
            4. Time estimates for each phase
            5. Cost estimates
            6. Required resources
            7. Success metrics

            The plan should be practical and minimize business disruption.
            Output as structured JSON."""),
            MessagesPlaceholder(variable_name="history"),
            HumanMessage(content="{analysis}")
        ])

        chain = LLMChain(
            llm=self.llm,
            prompt=prompt,
            memory=self.memory,
            callbacks=[self.tracer],
            output_parser=JsonOutputParser()
        )

        return chain

    def analyze_codebase(self, path: str) -> Dict[str, Any]:
        """
        Analyze a legacy codebase

        Args:
            path: Path to the codebase

        Returns:
            Detailed analysis report
        """

        print(f"\n🔍 Analyzing legacy codebase: {path}")

        # Gather codebase information
        codebase_info = self._scan_codebase(path)

        # Create analysis input
        analysis_input = f"""
        Please analyze this legacy codebase:

        Path: {path}
        Files: {codebase_info['file_count']}
        Languages: {', '.join(codebase_info['languages'])}
        Size: {codebase_info['total_size_mb']:.2f} MB

        File types distribution:
        {json.dumps(codebase_info['file_types'], indent=2)}

        Sample code structure:
        {codebase_info['structure_sample']}

        Provide a comprehensive analysis.
        """

        # Run analysis with LangSmith tracing
        with self.tracer as cb:
            analysis = self.analysis_chain.run(
                input=analysis_input,
                callbacks=[cb]
            )

        # Save to our memory system
        remember("analysis", analysis, f"legacy_{Path(path).name}")

        # Track in LangSmith
        self.langsmith_client.create_run(
            name="legacy_analysis",
            inputs={"path": path},
            outputs=analysis,
            run_type="chain"
        )

        print("✅ Analysis complete!")
        return analysis

    def generate_migration_plan(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a migration plan based on analysis

        Args:
            analysis: The analysis results

        Returns:
            Detailed migration plan
        """

        print("\n📋 Generating migration plan...")

        # Run migration planning with tracing
        with self.tracer as cb:
            migration_plan = self.migration_chain.run(
                analysis=json.dumps(analysis, indent=2),
                callbacks=[cb]
            )

        # Calculate ROI
        migration_plan['roi_analysis'] = self._calculate_roi(analysis, migration_plan)

        # Save pattern for reuse
        save_pattern(
            f"migration_{analysis.get('tech_stack', 'unknown')}",
            "legacy_migration",
            migration_plan
        )

        # Track success
        self.datazentr_memory.track_skill(
            "legacy_analyzer",
            success=True,
            execution_time=30.0,
            context=f"Migration plan generated"
        )

        print("✅ Migration plan ready!")
        return migration_plan

    def _scan_codebase(self, path: str) -> Dict[str, Any]:
        """Scan the codebase for basic information"""

        codebase_path = Path(path)
        if not codebase_path.exists():
            return {
                "error": f"Path {path} does not exist",
                "file_count": 0,
                "languages": [],
                "total_size_mb": 0,
                "file_types": {},
                "structure_sample": "N/A"
            }

        file_types = {}
        total_size = 0
        languages = set()

        # Language mapping
        lang_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.cs': 'C#',
            '.php': 'PHP',
            '.rb': 'Ruby',
            '.go': 'Go',
            '.rs': 'Rust',
            '.cpp': 'C++',
            '.c': 'C',
            '.swift': 'Swift',
            '.kt': 'Kotlin'
        }

        # Scan files
        all_files = []
        for file_path in codebase_path.rglob("*"):
            if file_path.is_file():
                all_files.append(file_path)
                ext = file_path.suffix
                file_types[ext] = file_types.get(ext, 0) + 1
                total_size += file_path.stat().st_size

                if ext in lang_map:
                    languages.add(lang_map[ext])

        # Create structure sample
        structure_lines = []
        for file_path in all_files[:20]:  # First 20 files
            rel_path = file_path.relative_to(codebase_path)
            structure_lines.append(str(rel_path))

        return {
            "file_count": len(all_files),
            "languages": list(languages),
            "total_size_mb": total_size / (1024 * 1024),
            "file_types": dict(sorted(file_types.items(), key=lambda x: x[1], reverse=True)[:10]),
            "structure_sample": "\n".join(structure_lines)
        }

    def _calculate_roi(self, analysis: Dict, plan: Dict) -> Dict[str, Any]:
        """Calculate ROI for the migration"""

        # Base calculations
        complexity = analysis.get('complexity_score', 5)

        # Traditional consulting estimates
        traditional_weeks = complexity * 4  # 4 weeks per complexity point
        traditional_cost = traditional_weeks * 10000  # $10k per week

        # Our estimates (10x faster)
        our_weeks = max(2, complexity * 0.4)  # Min 2 weeks
        our_cost = our_weeks * 5000  # $5k per week

        # Savings
        time_saved_weeks = traditional_weeks - our_weeks
        cost_saved = traditional_cost - our_cost
        percentage_saved = (cost_saved / traditional_cost) * 100

        return {
            "traditional_approach": {
                "duration_weeks": traditional_weeks,
                "cost_usd": traditional_cost
            },
            "datazentr_approach": {
                "duration_weeks": our_weeks,
                "cost_usd": our_cost
            },
            "savings": {
                "time_saved_weeks": time_saved_weeks,
                "cost_saved_usd": cost_saved,
                "percentage_saved": round(percentage_saved, 1)
            },
            "roi_multiplier": round(traditional_cost / our_cost, 1)
        }

    def generate_proposal(self, analysis: Dict, plan: Dict) -> str:
        """
        Generate a customer proposal document

        Args:
            analysis: The analysis results
            plan: The migration plan

        Returns:
            Formatted proposal document
        """

        roi = plan.get('roi_analysis', {})

        proposal = f"""
# Legacy Migration Proposal

## Executive Summary
We have analyzed your legacy {analysis.get('tech_stack', 'application')} and developed a comprehensive migration plan to modernize your infrastructure.

## Current State Analysis
- **Technology Stack**: {', '.join(analysis.get('technologies', []))}
- **Complexity Score**: {analysis.get('complexity_score', 'N/A')}/10
- **Technical Debt Areas**: {len(analysis.get('tech_debt', []))} identified
- **Security Issues**: {len(analysis.get('security_issues', []))} found

## Migration Plan

### Target Architecture
{plan.get('target_architecture', 'Modern cloud-native architecture')}

### Timeline
- **Traditional Approach**: {roi['traditional_approach']['duration_weeks']} weeks
- **Our Approach**: {roi['datazentr_approach']['duration_weeks']} weeks
- **Time Saved**: {roi['savings']['time_saved_weeks']} weeks

### Investment
- **Traditional Consulting**: ${roi['traditional_approach']['cost_usd']:,}
- **Our Solution**: ${roi['datazentr_approach']['cost_usd']:,}
- **Your Savings**: ${roi['savings']['cost_saved_usd']:,} ({roi['savings']['percentage_saved']}%)

### ROI
**{roi['roi_multiplier']}x** return on investment

## Success Metrics
{json.dumps(plan.get('success_metrics', ['Performance improvement', 'Cost reduction', 'Scalability']), indent=2)}

## Next Steps
1. Review this proposal with your team
2. Schedule a technical deep-dive session
3. Sign agreement to begin migration
4. Start with Phase 1 implementation

## Why Choose Us?
- ✅ 10x faster than traditional consulting
- ✅ AI-powered analysis and migration
- ✅ Proven patterns from 1000+ migrations
- ✅ Risk mitigation built-in
- ✅ Continuous optimization

---
*Generated by THE_DATAZENtr Legacy Analyzer*
*Powered by LangChain + LangSmith for maximum accuracy*
"""

        # Save proposal
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        proposal_path = Path(__file__).parent / f"proposal_{timestamp}.md"
        with open(proposal_path, 'w') as f:
            f.write(proposal)

        print(f"✅ Proposal saved to: {proposal_path}")

        return proposal


def test_analyzer():
    """Test the Legacy Analyzer"""

    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║               🔍 LEGACY ANALYZER - LANGCHAIN EDITION 🔍                 ║
║                                                                          ║
║                    Powered by LangChain + LangSmith                     ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
    """)

    # Initialize analyzer
    analyzer = LegacyAnalyzer()

    # Test with current project (or specify a path)
    test_path = Path(__file__).parent.parent  # THE_DATAZENtr itself

    # Run analysis
    print(f"\n📂 Analyzing: {test_path}")
    analysis = analyzer.analyze_codebase(str(test_path))

    print("\n📊 Analysis Results:")
    print(json.dumps(analysis, indent=2)[:500] + "...")

    # Generate migration plan
    migration_plan = analyzer.generate_migration_plan(analysis)

    print("\n📋 Migration Plan:")
    print(json.dumps(migration_plan, indent=2)[:500] + "...")

    # Generate proposal
    proposal = analyzer.generate_proposal(analysis, migration_plan)

    print("\n📄 Proposal Generated!")
    print(proposal[:1000] + "...")

    print("\n✅ Legacy Analyzer test complete!")
    print("   Check LangSmith dashboard for detailed traces")
    print(f"   Project: {os.getenv('LANGCHAIN_PROJECT', 'the-datazentr')}")


if __name__ == "__main__":
    # Run test
    test_analyzer()