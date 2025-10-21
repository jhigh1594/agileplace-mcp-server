# FastMCP **kwargs Fix

## 🚨 Issue Resolved

**Error:** `Functions with **kwargs are not supported as tools`

**Root Cause:** FastMCP doesn't support functions with `**kwargs` parameters in tool definitions.

## ✅ **What Was Fixed**

### Before (Broken):
```python
@mcp.tool()
async def update_card(card_id: str, **updates: Any) -> dict:
    # FastMCP doesn't support **kwargs
```

### After (Working):
```python
@mcp.tool()
async def update_card(
    card_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    size: Optional[int] = None,
    tags: Optional[list[str]] = None,
    lane_id: Optional[str] = None,
    position: Optional[int] = None,
) -> dict:
    # Build updates dict from provided parameters
    updates = {}
    if title is not None:
        updates["title"] = title
    # ... etc for all parameters
```

## 🎯 **How It Works Now**

### Explicit Parameters
The `update_card` function now accepts explicit optional parameters:
- `title` - New card title
- `description` - New card description  
- `priority` - Priority level (low, normal, high, critical)
- `size` - Card size
- `tags` - List of tags
- `lane_id` - Move to different lane
- `position` - Position in lane

### Internal Logic
The function builds an `updates` dictionary internally from the provided parameters, then passes it to the underlying `cards.update_card()` function.

## 🚀 **Usage Examples**

### Update Card Title
```python
await update_card(card_id="123", title="New Title")
```

### Update Multiple Fields
```python
await update_card(
    card_id="123",
    title="Updated Title",
    priority="high",
    tags=["urgent", "bug"]
)
```

### Move Card
```python
await update_card(
    card_id="123",
    lane_id="456",
    position=2
)
```

## ✅ **FastMCP Compatibility**

This approach:
- ✅ Uses explicit parameters (FastMCP compatible)
- ✅ Maintains all functionality
- ✅ Provides clear parameter documentation
- ✅ Allows flexible updates
- ✅ No **kwargs issues

## 🎉 **Result**

Your FastMCP Cloud deployment should now work without the **kwargs error!

The server will:
- ✅ Start successfully
- ✅ Register all tools
- ✅ Handle card updates properly
- ✅ Be ready for Claude Desktop connection
