#!/usr/bin/env python3
"""Test script to verify import structure is correct."""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all imports work correctly."""
    try:
        # Test individual module imports
        from agileplace_mcp.auth import AgilePlaceAuth
        print("✅ auth module imports correctly")
        
        from agileplace_mcp.client import AgilePlaceClient
        print("✅ client module imports correctly")
        
        from agileplace_mcp.models import Board, Card
        print("✅ models module imports correctly")
        
        from agileplace_mcp.tools import boards, cards, connections
        print("✅ tools modules import correctly")
        
        print("\n🎉 All imports successful! The relative import issue is fixed.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_imports()
