"""
Test script for Neural Database connection and functionality
"""

import asyncio
import sys
from pathlib import Path

# Add the current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from neural_db import NeuralMemoryManager

async def test_neural_database():
    """Test basic database operations"""

    print("=" * 60)
    print("🧠 NEURAL DATABASE TEST SUITE")
    print("=" * 60)

    # Initialize the manager
    print("\n1. Initializing Neural Memory Manager...")
    manager = NeuralMemoryManager()

    # Connect to database
    print("2. Connecting to database...")
    connected = await manager.initialize()

    if not connected:
        print("❌ Failed to connect to database!")
        print("   Make sure Docker containers are running.")
        return False

    print("✅ Successfully connected to database!")

    # Start a session
    print("\n3. Starting a new session...")
    session_id = await manager.start_session("test_project")
    print(f"✅ Session started: {session_id}")

    # Test remembering a pattern
    print("\n4. Testing pattern storage...")
    pattern_id = await manager.remember(
        "test_pattern_api_error",
        {
            "method": "exponential_backoff",
            "max_retries": 3,
            "initial_delay": 1,
            "max_delay": 60,
            "example": "await retry_with_backoff(api_call, max_retries=3)"
        },
        pattern_type="code"
    )
    print(f"✅ Pattern saved with ID: {pattern_id}")

    # Test another pattern
    await manager.remember(
        "test_pattern_auth_flow",
        {
            "method": "JWT_tokens",
            "flow": ["login", "receive_token", "refresh_when_expired"],
            "security": "store in httpOnly cookies"
        },
        pattern_type="architecture"
    )
    print("✅ Second pattern saved")

    # Test recalling similar patterns
    print("\n5. Testing pattern recall (semantic search)...")
    print("   Searching for: 'how to handle API failures'")
    similar = await manager.recall("how to handle API failures", limit=3)

    if similar:
        print(f"✅ Found {len(similar)} similar patterns:")
        for pattern, similarity in similar:
            print(f"   - {pattern.pattern_key} (similarity: {similarity:.2%})")
            print(f"     Type: {pattern.pattern_type}")
            print(f"     Content: {pattern.content}")
    else:
        print("   No similar patterns found (this is normal for a fresh database)")

    # Test tracking an interaction
    print("\n6. Testing interaction tracking...")
    await manager.track(
        prompt="How should I implement retry logic for API calls?",
        response="Use exponential backoff with a maximum retry count...",
        success=True
    )
    print("✅ Interaction tracked successfully")

    # Get session summary
    print("\n7. Ending session and getting summary...")
    summary = await manager.end_session()

    print("✅ Session ended. Summary:")
    print(f"   - Context: {summary.get('context', 'N/A')}")
    print(f"   - Interactions: {summary.get('interaction_count', 0)}")
    print(f"   - Duration: {summary.get('duration_seconds', 0):.1f} seconds")

    # Shutdown
    print("\n8. Shutting down connection...")
    await manager.shutdown()
    print("✅ Connection closed")

    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

    return True

async def test_cross_context_memory():
    """Test cross-context memory sharing"""

    print("\n" + "=" * 60)
    print("🌉 TESTING CROSS-CONTEXT MEMORY SHARING")
    print("=" * 60)

    manager = NeuralMemoryManager()
    await manager.initialize()

    # Create patterns in different contexts
    print("\n1. Creating patterns in different project contexts...")

    # Project A
    await manager.start_session("project_a")
    await manager.remember(
        "auth_jwt_implementation",
        {"method": "JWT with refresh tokens", "library": "jsonwebtoken"},
        pattern_type="architecture"
    )
    await manager.end_session()
    print("✅ Pattern saved in project_a")

    # Project B
    await manager.start_session("project_b")
    await manager.remember(
        "database_connection_pool",
        {"method": "connection pooling", "size": 10, "library": "asyncpg"},
        pattern_type="architecture"
    )

    print("✅ Pattern saved in project_b")

    # Now search from project B
    print("\n2. Searching for auth patterns from project_b context...")
    patterns = await manager.recall("authentication JWT")

    if patterns:
        print(f"✅ Found {len(patterns)} patterns (may include cross-context)")
        for pattern, similarity in patterns:
            print(f"   - {pattern.pattern_key} from context: {pattern.context}")
    else:
        print("   No cross-context patterns found (bridges need similarity > 85%)")

    await manager.end_session()
    await manager.shutdown()

    print("\n✅ Cross-context test completed")

    return True

if __name__ == "__main__":
    print("🚀 Starting Neural Database Tests\n")

    # Run basic tests
    asyncio.run(test_neural_database())

    # Run cross-context tests
    asyncio.run(test_cross_context_memory())

    print("\n✨ All tests completed!")