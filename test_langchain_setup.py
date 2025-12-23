#!/usr/bin/env python3
"""
🧪 TEST LANGCHAIN SETUP
Verifierar att LangChain/LangSmith är korrekt konfigurerat
"""

import os
import sys
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def test_environment():
    """Test that environment variables are loaded"""
    print("\n🔍 Testing environment variables...")

    langchain_key = os.getenv('LANGCHAIN_API_KEY')
    if langchain_key:
        # Hide most of the key for security
        masked_key = f"{langchain_key[:10]}...{langchain_key[-10:]}"
        print(f"✅ LANGCHAIN_API_KEY found: {masked_key}")
    else:
        print("❌ LANGCHAIN_API_KEY not found!")
        return False

    # Check other settings
    project = os.getenv('LANGCHAIN_PROJECT', 'not-set')
    print(f"   Project: {project}")

    tracing = os.getenv('LANGCHAIN_TRACING_V2', 'false')
    print(f"   Tracing: {tracing}")

    return True

def test_langsmith_connection():
    """Test LangSmith connection"""
    print("\n🔗 Testing LangSmith connection...")

    try:
        from langsmith import Client

        api_key = os.getenv('LANGCHAIN_API_KEY')
        if not api_key:
            print("❌ No API key available")
            return False

        # Initialize client
        client = Client(api_key=api_key)

        # Test connection by listing projects (this should work with any valid key)
        try:
            # Create a test run
            test_run = client.create_run(
                name="connection_test",
                run_type="chain",
                inputs={"test": "Testing THE_DATAZENtr connection"},
                outputs={"status": "connected"}
            )
            print(f"✅ LangSmith connected successfully!")
            print(f"   Test run created: {test_run.id[:8]}...")
            return True
        except Exception as e:
            print(f"⚠️ LangSmith connection failed: {e}")
            return False

    except ImportError:
        print("❌ LangSmith not installed. Run: pip install langsmith")
        return False

def test_langchain_import():
    """Test that LangChain can be imported"""
    print("\n📦 Testing LangChain imports...")

    modules_to_test = [
        "langchain",
        "langchain_core",
        "langchain_community",
        "langsmith"
    ]

    all_ok = True
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"✅ {module} imported successfully")
        except ImportError:
            print(f"❌ {module} not installed. Run: pip install {module}")
            all_ok = False

    return all_ok

def test_memory_system():
    """Test that our memory system works"""
    print("\n🧠 Testing MEMORY_CORE integration...")

    try:
        # Add MEMORY_CORE to path
        sys.path.insert(0, str(Path(__file__).parent / "MEMORY_CORE"))
        from memory_manager import get_memory

        memory = get_memory()
        health = memory.health_check()

        if health['status'] == 'healthy' or health['status'] == 'empty':
            print(f"✅ Memory system operational: {health['status']}")
            return True
        else:
            print(f"❌ Memory system error: {health.get('error', 'unknown')}")
            return False
    except Exception as e:
        print(f"❌ Memory system not accessible: {e}")
        return False

def main():
    """Run all tests"""
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║                    🧪 LANGCHAIN SETUP VERIFICATION 🧪                    ║
║                                                                          ║
║                     Testing all configurations...                       ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
    """)

    results = {
        "Environment": test_environment(),
        "LangChain Import": test_langchain_import(),
        "LangSmith Connection": test_langsmith_connection(),
        "Memory System": test_memory_system()
    }

    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)

    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False

    print("\n" + "="*70)
    if all_passed:
        print("🎉 ALL TESTS PASSED! LangChain is ready to use!")
        print("\nNext steps:")
        print("1. Run: python Skills/legacy_analyzer_langchain.py")
        print("2. Check LangSmith dashboard: https://smith.langchain.com")
        print("3. Start building with LangChain!")
    else:
        print("⚠️ Some tests failed. Please fix the issues above.")
        print("\nTo install missing packages:")
        print("pip install -r requirements.txt")

    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)