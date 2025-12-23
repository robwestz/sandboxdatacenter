#!/usr/bin/env python3
"""
THE FACTORY - Main Entry Point

Universal Self-Building System that creates complete software projects
from specifications or prompts.

Usage:
    # Auto-generate from prompt (creates timestamped project)
    python run_factory.py "Build a todo app with React"

    # Build from project directory with spec
    python run_factory.py --project projects/my-project

    # Build from specification file
    python run_factory.py --spec examples/specs/gui_project_spec.md

    # Interactive mode
    python run_factory.py
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime
import argparse

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import genesis prime
from bootstrap.genesis_prime import main as genesis_main, GenesisPrime, ProjectSpecification
import asyncio


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
            '🎨': '[A]', '📝': '[E]',
            # Box drawing characters
            '╔': '=', '═': '=', '╗': '=', '║': '|', '╚': '=', '╝': '=',
            '╠': '|', '╣': '|', '╦': '=', '╩': '=', '╬': '+',
            # Block characters (for ASCII art)
            '█': '#', '▓': '#', '▒': ':', '░': '.',
            # Additional special chars
            '▀': '-', '▄': '_', '▌': '|', '▐': '|',
        }
        for unicode_char, ascii_char in replacements.items():
            text = text.replace(unicode_char, ascii_char)
        print(text)


def print_banner():
    """Print The Factory banner"""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     ████████╗██╗  ██╗███████╗                                ║
║     ╚══██╔══╝██║  ██║██╔════╝                                ║
║        ██║   ███████║█████╗                                  ║
║        ██║   ██╔══██║██╔══╝                                  ║
║        ██║   ██║  ██║███████╗                                ║
║        ╚═╝   ╚═╝  ╚═╝╚══════╝                                ║
║                                                               ║
║     ███████╗ █████╗  ██████╗████████╗ ██████╗ ██████╗ ██╗   ║
║     ██╔════╝██╔══██╗██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗╚██╗  ║
║     █████╗  ███████║██║        ██║   ██║   ██║██████╔╝ ╚██╗ ║
║     ██╔══╝  ██╔══██║██║        ██║   ██║   ██║██╔══██╗  ██║ ║
║     ██║     ██║  ██║╚██████╗   ██║   ╚██████╔╝██║  ██║  ██║ ║
║     ╚═╝     ╚═╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝  ╚═╝ ║
║                                                               ║
║            Universal Self-Building System v1.0                ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """
    safe_print(banner)


def generate_project_name_from_prompt(prompt: str) -> str:
    """Generate a clean project name from user prompt"""
    # Take first 30 chars, clean up
    name = prompt[:30].lower()
    # Replace spaces and special chars with hyphens
    name = ''.join(c if c.isalnum() else '-' for c in name)
    # Remove multiple hyphens
    name = '-'.join(filter(None, name.split('-')))
    return name


def determine_project_location(args):
    """
    Determines where to create/find the project.

    Returns: (project_dir, spec_path, is_auto_generated)
    """

    # Case 1: Explicit project directory given
    if args.project:
        project_dir = Path(args.project)
        spec_path = project_dir / "project_spec.md"

        if not spec_path.exists():
            safe_print(f"❌ No project_spec.md found in {project_dir}")
            safe_print(f"💡 Create one or use --spec to specify a different spec file")
            sys.exit(1)

        safe_print(f"📁 Using project directory: {project_dir}")
        safe_print(f"📋 Using spec: {spec_path}")
        return project_dir, spec_path, False

    # Case 2: Explicit spec file given
    elif args.spec:
        spec_path = Path(args.spec)

        if not spec_path.exists():
            safe_print(f"❌ Specification file not found: {spec_path}")
            sys.exit(1)

        # Determine project directory
        if args.output:
            project_dir = Path(args.output)
        else:
            # Create in projects/ with spec name
            project_name = spec_path.stem
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            project_dir = Path("projects") / f"{project_name}-{timestamp}"

        project_dir.mkdir(parents=True, exist_ok=True)

        safe_print(f"📋 Using spec: {spec_path}")
        safe_print(f"📁 Creating project in: {project_dir}")

        return project_dir, spec_path, False

    # Case 3: Natural language prompt (auto-generate)
    elif args.prompt:
        # Generate project name from prompt
        project_name = generate_project_name_from_prompt(args.prompt)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

        project_dir = Path("projects") / f"{project_name}-{timestamp}"
        project_dir.mkdir(parents=True, exist_ok=True)

        # Generate spec automatically
        spec_path = project_dir / "project_spec.md"
        safe_print(f"🤖 Auto-generating specification from prompt...")
        generated_spec = generate_spec_from_prompt(args.prompt)
        spec_path.write_text(generated_spec)

        safe_print(f"📋 Generated spec: {spec_path}")
        safe_print(f"📁 Project directory: {project_dir}")

        return project_dir, spec_path, True

    else:
        safe_print("❌ Must provide --project, --spec, or a prompt")
        safe_print("💡 Examples:")
        safe_print("   python run_factory.py 'Build a todo app'")
        safe_print("   python run_factory.py --project projects/my-app")
        safe_print("   python run_factory.py --spec examples/specs/gui_project_spec.md")
        sys.exit(1)


def generate_spec_from_prompt(prompt: str) -> str:
    """Generate a project specification from natural language prompt"""
    spec = f"""# Auto-Generated Project Specification

{prompt}

## Type: custom
## Complexity: moderate

## OBJECTIVES
- Implement the requested functionality based on user prompt
- Follow modern best practices and patterns
- Include proper error handling and validation
- Provide comprehensive documentation
- Include tests for core functionality

## FEATURES

### Core Features
- Main functionality as described: {prompt}
- Error handling and input validation
- Logging and monitoring
- Basic security measures
- API documentation (if applicable)

### Quality Requirements
- Clean, readable code with comments
- Unit tests for critical paths
- Integration tests for main workflows
- Security best practices (OWASP Top 10)
- Performance optimization where applicable

### Technical Requirements
- Use appropriate technology stack for the problem
- Modern architecture patterns
- Scalable design
- Production-ready code quality
- Docker containerization (if applicable)

## OUTPUT REQUIREMENTS
- Complete source code with proper structure
- README with setup instructions
- API documentation (if applicable)
- Tests with reasonable coverage (70%+)
- Deployment configuration
- Environment configuration examples

## NOTES
This specification was auto-generated from the user prompt: "{prompt}"

The Factory will analyze this and create an optimal implementation plan.
"""
    return spec


def save_metadata(project_dir: Path, metadata: dict):
    """Save build metadata to project directory"""
    metadata_path = project_dir / ".factory_metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2))
    safe_print(f"💾 Metadata saved: {metadata_path}")


async def build_project(project_dir: Path, spec_path: Path, is_auto_generated: bool):
    """Build a project from specification"""

    # Create output directory inside project
    output_dir = project_dir / "output"
    logs_dir = project_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    # Initialize metadata
    metadata = {
        "project_name": project_dir.name,
        "created_at": datetime.now().isoformat(),
        "spec_path": str(spec_path),
        "spec_auto_generated": is_auto_generated,
        "status": "running"
    }
    save_metadata(project_dir, metadata)

    # Run Genesis Prime
    safe_print(f"\n🚀 Starting Factory chain reaction...")
    safe_print(f"📍 Project: {project_dir}")
    safe_print(f"📍 Output: {output_dir}")

    start_time = datetime.now()

    try:
        genesis = GenesisPrime(
            spec_path=str(spec_path),
            output_dir=str(output_dir)
        )

        result = await genesis.build()

        # Update metadata on success
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        metadata.update({
            "completed_at": end_time.isoformat(),
            "duration_seconds": duration,
            "status": "success",
            # Add more metrics if available from result
        })
        save_metadata(project_dir, metadata)

        safe_print(f"\n✨ Build complete!")
        safe_print(f"⏱️  Duration: {duration:.0f} seconds")
        safe_print(f"📦 Output: {output_dir}")
        safe_print(f"📊 Metadata: {project_dir}/.factory_metadata.json")

        return result

    except Exception as e:
        # Update metadata on failure
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        metadata.update({
            "completed_at": end_time.isoformat(),
            "duration_seconds": duration,
            "status": "failed",
            "error": str(e)
        })
        save_metadata(project_dir, metadata)

        safe_print(f"\n❌ Build failed: {e}")
        raise


def print_menu():
    """Print interactive menu"""
    safe_print("\n" + "="*70)
    safe_print("THE FACTORY - Interactive Mode")
    safe_print("="*70)
    safe_print("\n1. Build from prompt (auto-generates spec)")
    safe_print("2. Build from existing project directory")
    safe_print("3. Build from specification file")
    safe_print("4. Build example: GUI Project (complex)")
    safe_print("5. Show documentation")
    safe_print("6. Exit")
    safe_print("\n" + "="*70)


def show_documentation():
    """Show usage documentation"""
    safe_print("\n" + "="*70)
    safe_print("THE FACTORY - Documentation")
    safe_print("="*70)
    safe_print("""
## Quick Start

### Option 1: Natural Language (Easiest)
```bash
python run_factory.py "Build a todo app with React and FastAPI"
```
The Factory will:
- Auto-generate specification
- Create timestamped project in projects/
- Build everything
- Output to projects/todo-app-TIMESTAMP/output/

### Option 2: Use Existing Project
```bash
mkdir projects/my-app
nano projects/my-app/project_spec.md
# Write your spec...

python run_factory.py --project projects/my-app
```

### Option 3: Build from Example Spec
```bash
python run_factory.py --spec examples/specs/gui_project_spec.md
```

## Project Structure

After building, your project looks like:
```
projects/your-project/
├── project_spec.md           # Your specification
├── .factory_metadata.json    # Build info (agents, time, etc)
├── logs/
│   └── build.log            # Detailed build logs
└── output/
    ├── frontend/            # Generated code
    ├── backend/
    ├── README.md
    └── ...
```

## Examples

Examples are in `examples/specs/`:
- gui_project_spec.md - Full SaaS platform (complex, 4-5 hours)

You can copy and modify these:
```bash
cp examples/specs/gui_project_spec.md projects/my-saas/project_spec.md
nano projects/my-saas/project_spec.md  # Customize
python run_factory.py --project projects/my-saas
```

## More Info

- System architecture: docs/system/SYSTEM_LLM.md
- How to write specs: docs/guides/SPEC_OPTIMIZATION_LLM.md
- Quick reference: docs/guides/QUICK_REFERENCE.md
- Visual explainer: visual_explainer/index.html
""")
    safe_print("="*70)


async def interactive_mode():
    """Run The Factory in interactive mode"""
    while True:
        print_menu()
        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == '1':
            # Build from prompt
            prompt = input("\n📝 Describe what you want to build:\n> ").strip()
            if prompt:
                args = argparse.Namespace(
                    prompt=prompt,
                    project=None,
                    spec=None,
                    output=None
                )
                try:
                    project_dir, spec_path, is_auto = determine_project_location(args)
                    await build_project(project_dir, spec_path, is_auto)
                except Exception as e:
                    safe_print(f"❌ Build failed: {e}")

        elif choice == '2':
            # Build from existing project
            project_path = input("\n📁 Enter project directory path:\n> ").strip()
            if project_path:
                args = argparse.Namespace(
                    project=project_path,
                    spec=None,
                    prompt=None,
                    output=None
                )
                try:
                    project_dir, spec_path, is_auto = determine_project_location(args)
                    await build_project(project_dir, spec_path, is_auto)
                except Exception as e:
                    safe_print(f"❌ Build failed: {e}")

        elif choice == '3':
            # Build from spec file
            spec_path = input("\n📋 Enter specification file path:\n> ").strip()
            if spec_path:
                args = argparse.Namespace(
                    spec=spec_path,
                    project=None,
                    prompt=None,
                    output=None
                )
                try:
                    project_dir, spec_path_resolved, is_auto = determine_project_location(args)
                    await build_project(project_dir, spec_path_resolved, is_auto)
                except Exception as e:
                    safe_print(f"❌ Build failed: {e}")

        elif choice == '4':
            # Build GUI example
            safe_print("\n🎨 Building GUI Project example...")
            safe_print("⚠️  This is a complex build (4-5 hours, 180+ agents)")
            confirm = input("Continue? (y/n): ").strip().lower()

            if confirm == 'y':
                args = argparse.Namespace(
                    spec="examples/specs/gui_project_spec.md",
                    project=None,
                    prompt=None,
                    output=None
                )
                try:
                    project_dir, spec_path, is_auto = determine_project_location(args)
                    await build_project(project_dir, spec_path, is_auto)
                except Exception as e:
                    safe_print(f"❌ Build failed: {e}")

        elif choice == '5':
            # Show documentation
            show_documentation()

        elif choice == '6':
            # Exit
            safe_print("\n👋 Thank you for using The Factory!")
            break

        else:
            safe_print("❌ Invalid choice. Please try again.")

        input("\nPress Enter to continue...")


def main():
    """Main entry point"""
    print_banner()

    # Parse arguments
    parser = argparse.ArgumentParser(
        description="The Factory - Universal Self-Building System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Build from natural language
  python run_factory.py "Build a todo app with React"

  # Build from project directory
  python run_factory.py --project projects/my-app

  # Build from spec file
  python run_factory.py --spec examples/specs/gui_project_spec.md

  # Interactive mode
  python run_factory.py
        """
    )

    parser.add_argument('prompt', nargs='*', help='Natural language project description')
    parser.add_argument('--project', '-p', help='Project directory with project_spec.md')
    parser.add_argument('--spec', '-s', help='Path to specification file')
    parser.add_argument('--output', '-o', help='Custom output directory (with --spec only)')

    # If no args, run interactive mode
    if len(sys.argv) == 1:
        try:
            asyncio.run(interactive_mode())
        except KeyboardInterrupt:
            safe_print("\n\n👋 Goodbye!")
        except Exception as e:
            safe_print(f"\n❌ Error: {e}")
            sys.exit(1)
        return

    args = parser.parse_args()

    # Convert prompt list to string
    if args.prompt:
        args.prompt = ' '.join(args.prompt)

    # Show help if requested
    if args.prompt and args.prompt.lower() in ['help', '-h', '--help']:
        parser.print_help()
        return

    # Determine project location
    try:
        project_dir, spec_path, is_auto_generated = determine_project_location(args)

        # Build the project
        asyncio.run(build_project(project_dir, spec_path, is_auto_generated))

    except Exception as e:
        safe_print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
