#!/usr/bin/env python3
"""
The Factory - Automatic Setup Script

This script automatically sets up The Factory with all dependencies.
Run this once on a new system, then use run_factory.py normally.
"""

import os
import sys
import subprocess
import venv
from pathlib import Path


def safe_print(text):
    """Print text, falling back to ASCII if Unicode fails"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Replace common Unicode characters with ASCII equivalents
        replacements = {
            '✅': '[OK]',
            '❌': '[X]',
            '⚠️': '[!]',
            '⚠': '[!]',
            '🔍': '[?]',
            '📦': '[*]',
            '🎉': '!!!',
            '🏭': '[#]',
            '╔': '=',
            '═': '=',
            '╗': '=',
            '║': '|',
            '╚': '=',
            '╝': '=',
        }
        for unicode_char, ascii_char in replacements.items():
            text = text.replace(unicode_char, ascii_char)
        print(text)


def print_banner():
    try:
        safe_print("""
╔═══════════════════════════════════════════════════════════════╗
║               THE FACTORY - AUTOMATIC SETUP                   ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    except UnicodeEncodeError:
        safe_print("""
===============================================================
              THE FACTORY - AUTOMATIC SETUP
===============================================================
    """)


def check_python_version():
    """Ensure Python 3.8+"""
    if sys.version_info < (3, 8):
        safe_print("❌ Python 3.8+ required")
        safe_print(f"   Current version: {sys.version}")
        sys.exit(1)
    safe_print(f"✅ Python version: {sys.version.split()[0]}")


def create_virtual_environment():
    """Create virtual environment if it doesn't exist"""
    venv_path = Path("venv")

    if venv_path.exists():
        safe_print("✅ Virtual environment already exists")
        return venv_path

    safe_print("📦 Creating virtual environment...")
    venv.create(venv_path, with_pip=True)
    safe_print("✅ Virtual environment created")
    return venv_path


def get_pip_path(venv_path):
    """Get path to pip in virtual environment"""
    if sys.platform == "win32":
        return venv_path / "Scripts" / "pip.exe"
    return venv_path / "bin" / "pip"


def get_python_path(venv_path):
    """Get path to python in virtual environment"""
    if sys.platform == "win32":
        return venv_path / "Scripts" / "python.exe"
    return venv_path / "bin" / "python"


def install_dependencies(venv_path):
    """Install dependencies in virtual environment"""
    pip_path = get_pip_path(venv_path)

    # Check which requirements file to use
    if Path("requirements-minimal.txt").exists():
        req_file = "requirements-minimal.txt"
        safe_print("📦 Installing minimal dependencies (faster)...")
    else:
        req_file = "requirements.txt"
        safe_print("📦 Installing all dependencies (may take a few minutes)...")

    # Upgrade pip first (non-critical, so ignore failures)
    safe_print("   Upgrading pip...")
    subprocess.run([str(pip_path), "install", "--upgrade", "pip"],
                   capture_output=True)

    # Install dependencies
    safe_print(f"   Installing from {req_file}...")
    result = subprocess.run(
        [str(pip_path), "install", "-r", req_file],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        safe_print(f"❌ Installation failed:")
        safe_print(result.stderr)
        sys.exit(1)

    safe_print("✅ Dependencies installed")


def create_activation_script():
    """Create easy activation script"""
    if sys.platform == "win32":
        script_name = "activate.bat"
        script_content = """@echo off
call venv\\Scripts\\activate.bat
echo.
echo ✅ The Factory environment activated!
echo.
echo Usage:
echo   python run_factory.py "Build something"
echo   python run_factory.py --help
echo.
"""
    else:
        script_name = "activate.sh"
        script_content = """#!/bin/bash
source venv/bin/activate
echo ""
echo "✅ The Factory environment activated!"
echo ""
echo "Usage:"
echo "  python run_factory.py 'Build something'"
echo "  python run_factory.py --help"
echo ""
"""

    Path(script_name).write_text(script_content, encoding='utf-8')
    if sys.platform != "win32":
        os.chmod(script_name, 0o755)

    safe_print(f"✅ Activation script created: {script_name}")


def create_run_script(venv_path):
    """Create direct run script that uses venv automatically"""
    python_path = get_python_path(venv_path)

    if sys.platform == "win32":
        script_name = "factory.bat"
        script_content = f"""@echo off
"{python_path}" run_factory.py %*
"""
    else:
        script_name = "factory.sh"
        script_content = f"""#!/bin/bash
"{python_path}" run_factory.py "$@"
"""

    Path(script_name).write_text(script_content)
    if sys.platform != "win32":
        os.chmod(script_name, 0o755)

    safe_print(f"✅ Direct run script created: {script_name}")


def verify_installation(venv_path):
    """Verify that The Factory can be imported"""
    python_path = get_python_path(venv_path)

    safe_print("🔍 Verifying installation...")

    test_script = """
import sys
try:
    from bootstrap.genesis_prime import GenesisPrime
    print("[OK] The Factory modules OK")
    sys.exit(0)
except ImportError as e:
    print(f"[X] Import failed: {e}")
    sys.exit(1)
"""

    result = subprocess.run(
        [str(python_path), "-c", test_script],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        safe_print(result.stdout.strip())
        safe_print("✅ Installation verified")
    else:
        safe_print(result.stdout.strip())
        safe_print("⚠️  Verification failed but installation may still work")


def print_next_steps():
    """Print what to do next"""
    try:
        banner = """
╔═══════════════════════════════════════════════════════════════╗
║                    SETUP COMPLETE! 🎉                         ║
╚═══════════════════════════════════════════════════════════════╝
"""
    except UnicodeEncodeError:
        banner = """
===============================================================
                   SETUP COMPLETE!
===============================================================
"""

    safe_print(banner + """
Ready to use The Factory! Choose one of:

Option 1: Direct usage (easiest)
  Windows: factory.bat "Build a todo app"
  Linux/Mac: ./factory.sh "Build a todo app"

Option 2: Activate environment first
  Windows: activate.bat
  Linux/Mac: source activate.sh
  Then: python run_factory.py "Build something"

Option 3: Interactive mode
  Windows: factory.bat
  Linux/Mac: ./factory.sh

Option 4: From examples
  Windows: factory.bat --spec examples/specs/gui_project_spec.md
  Linux/Mac: ./factory.sh --spec examples/specs/gui_project_spec.md

For help:
  Windows: factory.bat --help
  Linux/Mac: ./factory.sh --help

Happy building! 🏭
    """)


def main():
    print_banner()

    try:
        # Step 1: Check Python
        check_python_version()

        # Step 2: Create venv
        venv_path = create_virtual_environment()

        # Step 3: Install dependencies
        install_dependencies(venv_path)

        # Step 4: Create helper scripts
        create_activation_script()
        create_run_script(venv_path)

        # Step 5: Verify
        verify_installation(venv_path)

        # Step 6: Success!
        print_next_steps()

    except KeyboardInterrupt:
        safe_print("\n\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        safe_print(f"\n\n❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
