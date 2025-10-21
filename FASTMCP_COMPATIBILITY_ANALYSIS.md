# FastMCP Compatibility Analysis

## 🔍 **Issues Identified**

After reviewing FastMCP documentation and our codebase, I've identified several potential issues that could cause build failures:

### 1. ✅ **FIXED: **kwargs Usage**
- **Issue**: `update_card(card_id: str, **updates: Any)` 
- **Status**: ✅ FIXED - Replaced with explicit parameters
- **Impact**: Would cause "Functions with **kwargs are not supported as tools" error

### 2. ⚠️ **POTENTIAL ISSUE: Complex Type Annotations**

#### Problematic Functions:
```python
# These might cause issues with FastMCP's type validation
async def connect_cards_bulk(connections_list: list[dict]) -> dict:
async def move_cards_bulk(moves: list[dict]) -> dict:
async def update_cards_bulk(card_ids: list[str], updates: dict[str, Any]) -> dict:
```

#### Why This Could Be Problematic:
- FastMCP expects simple type annotations
- Complex nested types like `list[dict]` and `dict[str, Any]` might not be properly serialized
- MCP clients send arguments as strings, requiring JSON parsing

### 3. ⚠️ **POTENTIAL ISSUE: Optional List Parameters**

#### Problematic Functions:
```python
async def get_board_cards(
    board_id: str,
    lanes: Optional[list[str]] = None,  # ← Could be problematic
    limit: int = 200,
) -> dict:

async def create_card(
    board_id: str,
    lane_id: str,
    title: str,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    size: Optional[int] = None,
    tags: Optional[list[str]] = None,  # ← Could be problematic
) -> dict:
```

#### Why This Could Be Problematic:
- FastMCP might not handle `Optional[list[str]]` properly
- MCP clients send list parameters as JSON strings
- Need explicit JSON parsing in function bodies

### 4. ⚠️ **POTENTIAL ISSUE: Return Type Complexity**

#### Problematic Return Types:
```python
async def get_board_cards(...) -> dict:  # ← Generic dict return
async def get_card_children(...) -> dict:  # ← Generic dict return
async def get_card_parents(...) -> dict:  # ← Generic dict return
```

#### Why This Could Be Problematic:
- Generic `dict` return types don't provide schema information
- FastMCP prefers specific return types for better tool descriptions
- Could cause serialization issues

## 🛠️ **Recommended Fixes**

### Fix 1: Simplify Complex Type Annotations

Replace complex types with string parameters and JSON parsing:

```python
# BEFORE (Problematic)
async def connect_cards_bulk(connections_list: list[dict]) -> dict:

# AFTER (FastMCP Compatible)
async def connect_cards_bulk(connections_json: str) -> dict:
    """
    Create multiple parent-child connections in a single request.
    
    Args:
        connections_json: JSON string with list of connections
                        [{"parentCardId": "123", "childCardId": "456"}]
    """
    try:
        connections_list = json.loads(connections_json)
        # ... rest of implementation
```

### Fix 2: Handle Optional List Parameters

```python
# BEFORE (Problematic)
async def get_board_cards(
    board_id: str,
    lanes: Optional[list[str]] = None,
    limit: int = 200,
) -> dict:

# AFTER (FastMCP Compatible)
async def get_board_cards(
    board_id: str,
    lanes_json: Optional[str] = None,
    limit: int = 200,
) -> dict:
    """
    Get card faces (summary information) for cards on a board.
    
    Args:
        board_id: ID of the board
        lanes_json: JSON string with list of lane IDs (optional)
        limit: Maximum number of cards to return (default: 200)
    """
    try:
        lanes = json.loads(lanes_json) if lanes_json else None
        # ... rest of implementation
```

### Fix 3: Add JSON Import

Ensure we have JSON parsing capability:

```python
import json
from typing import Any, Optional
```

## 🎯 **Priority Fixes Needed**

### High Priority (Will Cause Build Failures):
1. **Complex type annotations** - `list[dict]`, `dict[str, Any]`
2. **Optional list parameters** - `Optional[list[str]]`

### Medium Priority (May Cause Runtime Issues):
1. **Generic dict return types** - Could cause serialization issues
2. **Missing JSON parsing** - For complex parameter types

### Low Priority (Best Practices):
1. **Specific return types** - Better tool descriptions
2. **Input validation** - Better error handling

## 🧪 **Testing Strategy**

### 1. Test Each Problematic Function
```python
# Test complex parameter types
await connect_cards_bulk('[{"parentCardId": "123", "childCardId": "456"}]')
await move_cards_bulk('[{"cardId": "123", "laneId": "456", "position": 1}]')

# Test optional list parameters
await get_board_cards("board123", '["lane1", "lane2"]', 100)
await create_card("board123", "lane456", "Test Card", tags='["urgent", "bug"]')
```

### 2. Validate JSON Parsing
- Ensure all complex parameters are properly parsed
- Handle JSON parsing errors gracefully
- Provide clear error messages for invalid JSON

## 📊 **Impact Assessment**

### Functions That Need Fixing:
- `connect_cards_bulk` - Complex `list[dict]` parameter
- `move_cards_bulk` - Complex `list[dict]` parameter  
- `update_cards_bulk` - Complex `dict[str, Any]` parameter
- `get_board_cards` - Optional `list[str]` parameter
- `create_card` - Optional `list[str]` parameter
- `assign_users_to_card` - Optional `list[str]` parameters

### Functions That Are Safe:
- All simple parameter functions (strings, ints, booleans)
- Functions with only `Optional[str]` parameters
- Functions with simple return types

## 🚀 **Implementation Plan**

1. **Phase 1**: Fix high-priority complex type annotations
2. **Phase 2**: Fix optional list parameters
3. **Phase 3**: Add comprehensive JSON parsing
4. **Phase 4**: Test all functions with FastMCP
5. **Phase 5**: Update documentation

## ✅ **Expected Outcome**

After implementing these fixes:
- ✅ No more type annotation errors
- ✅ All complex parameters handled via JSON strings
- ✅ Proper JSON parsing and validation
- ✅ FastMCP Cloud deployment success
- ✅ All tools working correctly
