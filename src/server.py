"""Main FastMCP server for AgilePlace integration."""

import logging
import os
from typing import Any, Optional

from fastmcp import FastMCP

from .auth import AgilePlaceAuth, AgilePlaceAuthError
from .client import AgilePlaceAPIError, AgilePlaceClient, RateLimitError
from .tools import boards, bulk, cards, connections, dependencies, query

# Set up logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP(
    "AgilePlace",
    instructions="""
    AgilePlace MCP Server provides access to the AgilePlace API for project management.
    
    Key capabilities:
    - Board management: List, view, and manage boards
    - Card operations: Create, read, update, delete, and move cards
    - Connections: Manage parent-child relationships between cards
    - Dependencies: Create and manage card dependencies
    - Bulk operations: Perform operations on multiple cards/boards
    - User and team queries: Search and retrieve user/team information
    
    Use these tools to integrate AgilePlace with AI assistants for project management tasks.
    """,
)

# Initialize auth and client as globals
try:
    auth = AgilePlaceAuth()
    logger.info(f"Authenticated to AgilePlace domain: {auth.domain}")
except AgilePlaceAuthError as e:
    logger.error(f"Authentication failed: {e}")
    raise

# Create a global client instance that will be used by all tools
_client: Optional[AgilePlaceClient] = None


def get_client() -> AgilePlaceClient:
    """Get or create the global API client."""
    global _client
    if _client is None:
        _client = AgilePlaceClient(auth)
    return _client


# Helper function to handle errors consistently
def handle_api_error(e: Exception) -> str:
    """Convert API errors to user-friendly messages."""
    if isinstance(e, RateLimitError):
        return f"Rate limit exceeded. Please try again later. {e.message}"
    elif isinstance(e, AgilePlaceAPIError):
        return f"API Error ({e.status_code}): {e.message}"
    elif isinstance(e, AgilePlaceAuthError):
        return f"Authentication Error: {e}"
    else:
        logger.exception("Unexpected error in tool")
        return f"Unexpected error: {str(e)}"


# ========================================
# Board Tools
# ========================================

@mcp.tool()
async def list_boards(
    search: Optional[str] = None,
    limit: int = 200,
    archived: bool = False,
) -> list[dict]:
    """
    List all boards accessible to the authenticated user.
    
    Args:
        search: Filter boards by title (optional)
        limit: Maximum number of boards to return (default: 200)
        archived: Include archived boards (default: False)
    """
    try:
        client = get_client()
        return await boards.list_boards(client, search, limit, archived=archived)
    except Exception as e:
        raise ValueError(handle_api_error(e))


@mcp.tool()
async def get_board(board_id: str) -> dict:
    """
    Get detailed information about a specific board including lanes, card types, and custom fields.
    
    Args:
        board_id: ID of the board to retrieve
    """
    try:
        client = get_client()
        return await boards.get_board(client, board_id)
    except Exception as e:
        raise ValueError(handle_api_error(e))


@mcp.tool()
async def get_board_cards(
    board_id: str,
    lanes: Optional[list[str]] = None,
    limit: int = 200,
) -> dict:
    """
    Get card faces (summary information) for cards on a board.
    
    Args:
        board_id: ID of the board
        lanes: List of lane IDs to filter by (optional)
        limit: Maximum number of cards to return (default: 200)
    """
    try:
        client = get_client()
        return await boards.get_board_cards(client, board_id, lanes, limit=limit)
    except Exception as e:
        raise ValueError(handle_api_error(e))


@mcp.tool()
async def get_leaf_lanes(board_id: str) -> list[dict]:
    """
    Get lanes that can hold cards (leaf lanes without children).
    
    Args:
        board_id: ID of the board
    """
    try:
        client = get_client()
        return await boards.get_leaf_lanes(client, board_id)
    except Exception as e:
        raise ValueError(handle_api_error(e))


@mcp.tool()
async def create_board(
    title: str,
    description: Optional[str] = None,
    template_id: Optional[str] = None,
) -> dict:
    """
    Create a new board.
    
    Args:
        title: Title of the new board
        description: Board description (optional)
        template_id: ID of template to base board on (optional)
    """
    try:
        client = get_client()
        return await boards.create_board(
            client, title, description=description, template_id=template_id
        )
    except Exception as e:
        raise ValueError(handle_api_error(e))


@mcp.tool()
async def get_board_members(
    board_id: str,
    search: Optional[str] = None,
) -> list[dict]:
    """
    Get assigned members (users and teams) on a board.
    
    Args:
        board_id: ID of the board
        search: Filter members by name (optional)
    """
    try:
        client = get_client()
        return await boards.get_board_members(client, board_id, search)
    except Exception as e:
        raise ValueError(handle_api_error(e))


# ========================================
# Card Tools
# ========================================

@mcp.tool()
async def list_cards(
    board_id: Optional[str] = None,
    since: Optional[str] = None,
    limit: int = 200,
) -> dict:
    """
    List cards with optional filtering.
    
    Args:
        board_id: Filter by board ID (optional)
        since: ISO 8601 date - only return cards modified after this date (optional)
        limit: Maximum number of cards to return (default: 200)
    """
    try:
        client = get_client()
        return await cards.list_cards(client, board_id, since, limit=limit)
    except Exception as e:
        raise ValueError(handle_api_error(e))


@mcp.tool()
async def get_card(card_id: str) -> dict:
    """
    Get full details of a specific card.
    
    Args:
        card_id: ID of the card to retrieve
    """
    try:
        client = get_client()
        return await cards.get_card(client, card_id)
    except Exception as e:
        raise ValueError(handle_api_error(e))


@mcp.tool()
async def get_card_activity(card_id: str, limit: int = 100) -> list[dict]:
    """
    Get activity history for a card.
    
    Args:
        card_id: ID of the card
        limit: Maximum number of events to return (default: 100)
    """
    try:
        client = get_client()
        return await cards.get_card_activity(client, card_id, limit)
    except Exception as e:
        raise ValueError(handle_api_error(e))


@mcp.tool()
async def create_card(
    board_id: str,
    lane_id: str,
    title: str,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    size: Optional[int] = None,
    tags: Optional[list[str]] = None,
) -> dict:
    """
    Create a new card on a board.
    
    Args:
        board_id: ID of the board
        lane_id: ID of the lane to create the card in
        title: Card title
        description: Card description (optional)
        priority: Priority level - 'low', 'normal', 'high', or 'critical' (optional)
        size: Card size (optional)
        tags: List of tags (optional)
    """
    try:
        client = get_client()
        return await cards.create_card(
            client,
            board_id,
            lane_id,
            title,
            description=description,
            priority=priority,
            size=size,
            tags=tags,
        )
    except Exception as e:
        raise ValueError(handle_api_error(e))


@mcp.tool()
async def update_card(card_id: str, **updates: Any) -> dict:
    """
    Update fields on an existing card.
    
    Args:
        card_id: ID of the card to update
        **updates: Field updates (title, description, priority, size, tags, etc.)
    """
    try:
        client = get_client()
        return await cards.update_card(client, card_id, **updates)
    except Exception as e:
        raise ValueError(handle_api_error(e))


@mcp.tool()
async def move_card(
    card_id: str,
    lane_id: str,
    position: Optional[int] = None,
) -> dict:
    """
    Move a card to a different lane.
    
    Args:
        card_id: ID of the card to move
        lane_id: ID of the destination lane
        position: Position in the destination lane (optional)
    """
    try:
        client = get_client()
        return await cards.move_card(client, card_id, lane_id, position)
    except Exception as e:
        raise ValueError(handle_api_error(e))


@mcp.tool()
async def delete_card(card_id: str) -> str:
    """
    Delete a card.
    
    Args:
        card_id: ID of the card to delete
    """
    try:
        client = get_client()
        await cards.delete_card(client, card_id)
        return f"Card {card_id} deleted successfully"
    except Exception as e:
        raise ValueError(handle_api_error(e))


@mcp.tool()
async def get_card_comments(card_id: str) -> list[dict]:
    """
    Get comments on a card.
    
    Args:
        card_id: ID of the card
    """
    try:
        client = get_client()
        return await cards.get_card_comments(client, card_id)
    except Exception as e:
        raise ValueError(handle_api_error(e))


@mcp.tool()
async def create_comment(card_id: str, text: str) -> dict:
    """
    Add a comment to a card.
    
    Args:
        card_id: ID of the card
        text: Comment text
    """
    try:
        client = get_client()
        return await cards.create_comment(client, card_id, text)
    except Exception as e:
        raise ValueError(handle_api_error(e))


@mcp.tool()
async def assign_users_to_card(
    card_id: str,
    user_ids: Optional[list[str]] = None,
    team_ids: Optional[list[str]] = None,
) -> dict:
    """
    Assign users and/or teams to a card.
    
    Args:
        card_id: ID of the card
        user_ids: List of user IDs to assign (optional)
        team_ids: List of team IDs to assign (optional)
    """
    try:
        client = get_client()
        return await cards.assign_users_to_card(client, card_id, user_ids, team_ids)
    except Exception as e:
        raise ValueError(handle_api_error(e))


# ========================================
# Connection Tools
# ========================================

@mcp.tool()
async def get_card_children(card_id: str, limit: int = 200) -> dict:
    """
    Get child cards connected to a parent card.
    
    Args:
        card_id: ID of the parent card
        limit: Maximum number of children to return (default: 200)
    """
    try:
        client = get_client()
        return await connections.get_card_children(client, card_id, limit)
    except Exception as e:
        raise ValueError(handle_api_error(e))


@mcp.tool()
async def get_card_parents(card_id: str, limit: int = 200) -> dict:
    """
    Get parent cards connected to a child card.
    
    Args:
        card_id: ID of the child card
        limit: Maximum number of parents to return (default: 200)
    """
    try:
        client = get_client()
        return await connections.get_card_parents(client, card_id, limit)
    except Exception as e:
        raise ValueError(handle_api_error(e))


@mcp.tool()
async def create_connection(parent_id: str, child_id: str) -> dict:
    """
    Create a parent-child connection between two cards.
    
    Args:
        parent_id: ID of the parent card
        child_id: ID of the child card
    """
    try:
        client = get_client()
        return await connections.create_connection(client, parent_id, child_id)
    except Exception as e:
        raise ValueError(handle_api_error(e))


@mcp.tool()
async def delete_connection(parent_id: str, child_id: str) -> str:
    """
    Remove a parent-child connection between two cards.
    
    Args:
        parent_id: ID of the parent card
        child_id: ID of the child card
    """
    try:
        client = get_client()
        await connections.delete_connection(client, parent_id, child_id)
        return f"Connection between {parent_id} and {child_id} deleted successfully"
    except Exception as e:
        raise ValueError(handle_api_error(e))


@mcp.tool()
async def get_connection_statistics(card_id: str) -> dict:
    """
    Get statistics about connected cards (children).
    
    Args:
        card_id: ID of the parent card
    """
    try:
        client = get_client()
        return await connections.get_connection_statistics(client, card_id)
    except Exception as e:
        raise ValueError(handle_api_error(e))


@mcp.tool()
async def connect_cards_bulk(connections_list: list[dict]) -> dict:
    """
    Create multiple parent-child connections in a single request.
    
    Args:
        connections_list: List of dicts with 'parentCardId' and 'childCardId'
    """
    try:
        client = get_client()
        return await connections.connect_cards_bulk(client, connections_list)
    except Exception as e:
        raise ValueError(handle_api_error(e))


# ========================================
# Dependency Tools
# ========================================

@mcp.tool()
async def get_card_dependencies(card_id: str) -> list[dict]:
    """
    Get all dependencies for a card.
    
    Args:
        card_id: ID of the card
    """
    try:
        client = get_client()
        return await dependencies.get_card_dependencies(client, card_id)
    except Exception as e:
        raise ValueError(handle_api_error(e))


@mcp.tool()
async def create_dependency(
    card_id: str,
    depends_on_card_id: str,
    dependency_type: str = "finish_to_start",
) -> dict:
    """
    Create a dependency between two cards.
    
    Args:
        card_id: ID of the dependent card
        depends_on_card_id: ID of the card that is depended upon
        dependency_type: Type - 'finish_to_start', 'start_to_start', 'finish_to_finish', 'start_to_finish'
    """
    try:
        client = get_client()
        return await dependencies.create_dependency(
            client, card_id, depends_on_card_id, dependency_type
        )
    except Exception as e:
        raise ValueError(handle_api_error(e))


@mcp.tool()
async def delete_dependency(dependency_id: str) -> str:
    """
    Delete a dependency.
    
    Args:
        dependency_id: ID of the dependency to delete
    """
    try:
        client = get_client()
        await dependencies.delete_dependency(client, dependency_id)
        return f"Dependency {dependency_id} deleted successfully"
    except Exception as e:
        raise ValueError(handle_api_error(e))


# ========================================
# User and Team Query Tools
# ========================================

@mcp.tool()
async def list_users(search: Optional[str] = None, limit: int = 25) -> dict:
    """
    List users in the organization.
    
    Args:
        search: Keyword search by user name and email (optional)
        limit: Maximum number of users to return (default: 25)
    """
    try:
        client = get_client()
        return await query.list_users(client, search, limit)
    except Exception as e:
        raise ValueError(handle_api_error(e))


@mcp.tool()
async def get_user(user_id: str) -> dict:
    """
    Get details about a specific user.
    
    Args:
        user_id: ID of the user to retrieve
    """
    try:
        client = get_client()
        return await query.get_user(client, user_id)
    except Exception as e:
        raise ValueError(handle_api_error(e))


@mcp.tool()
async def get_current_user() -> dict:
    """Get details about the currently authenticated user."""
    try:
        client = get_client()
        return await query.get_current_user(client)
    except Exception as e:
        raise ValueError(handle_api_error(e))


@mcp.tool()
async def list_teams(search: Optional[str] = None, limit: int = 100) -> dict:
    """
    List teams in the organization.
    
    Args:
        search: Filter teams by name (optional)
        limit: Maximum number of teams to return (default: 100)
    """
    try:
        client = get_client()
        return await query.list_teams(client, search, limit)
    except Exception as e:
        raise ValueError(handle_api_error(e))


@mcp.tool()
async def get_team(team_id: str) -> dict:
    """
    Get details about a specific team.
    
    Args:
        team_id: ID of the team to retrieve
    """
    try:
        client = get_client()
        return await query.get_team(client, team_id)
    except Exception as e:
        raise ValueError(handle_api_error(e))


# ========================================
# Bulk Operation Tools
# ========================================

@mcp.tool()
async def update_cards_bulk(card_ids: list[str], updates: dict[str, Any]) -> dict:
    """
    Update multiple cards with the same field values.
    
    Args:
        card_ids: List of card IDs to update (max 100)
        updates: Dictionary of fields to update on all cards
    """
    try:
        client = get_client()
        return await bulk.update_cards_bulk(client, card_ids, updates)
    except Exception as e:
        raise ValueError(handle_api_error(e))


@mcp.tool()
async def delete_cards_bulk(card_ids: list[str]) -> str:
    """
    Delete multiple cards in a single request.
    
    Args:
        card_ids: List of card IDs to delete (max 100)
    """
    try:
        client = get_client()
        await bulk.delete_cards_bulk(client, card_ids)
        return f"Successfully deleted {len(card_ids)} cards"
    except Exception as e:
        raise ValueError(handle_api_error(e))


@mcp.tool()
async def move_cards_bulk(moves: list[dict]) -> dict:
    """
    Move multiple cards to different lanes in a single request.
    
    Args:
        moves: List of move operations with 'cardId', 'laneId', and optional 'position'
    """
    try:
        client = get_client()
        return await bulk.move_cards_bulk(client, moves)
    except Exception as e:
        raise ValueError(handle_api_error(e))


@mcp.tool()
async def assign_members_bulk(
    board_ids: list[str],
    user_ids: Optional[list[str]] = None,
    team_ids: Optional[list[str]] = None,
    board_role: str = "boardUser",
) -> str:
    """
    Assign users or teams to multiple boards with a specific role.
    
    Args:
        board_ids: List of board IDs
        user_ids: List of user IDs to assign (optional)
        team_ids: List of team IDs to assign (optional)
        board_role: Role to assign - 'boardReader', 'boardUser', 'boardManager', 'boardAdministrator'
    """
    try:
        client = get_client()
        await bulk.assign_members_bulk(client, board_ids, user_ids, team_ids, board_role)
        return "Successfully assigned members to boards"
    except Exception as e:
        raise ValueError(handle_api_error(e))


def main():
    """Main entry point for the server."""
    mcp.run()


if __name__ == "__main__":
    main()

