"""Board operations tools for AgilePlace MCP Server."""

from typing import Optional

from agileplace_mcp.client import AgilePlaceClient
from agileplace_mcp.models import Board, Card


async def list_boards(
    client: AgilePlaceClient,
    search: Optional[str] = None,
    limit: int = 200,
    offset: int = 0,
    archived: bool = False,
) -> list[dict]:
    """
    List all boards accessible to the authenticated user.

    Args:
        client: AgilePlace API client
        search: Filter boards by title (optional)
        limit: Maximum number of boards to return (default: 200)
        offset: Number of boards to skip (default: 0)
        archived: Include archived boards (default: False)

    Returns:
        List of board objects with id, title, description, and board role

    Example:
        boards = await list_boards(client, search="project")
    """
    params = {
        "limit": limit,
        "offset": offset,
    }

    if search:
        params["search"] = search

    if archived:
        params["archived"] = "true"

    response = await client.get("/board", params=params)
    return response.get("boards", [])


async def get_board(client: AgilePlaceClient, board_id: str) -> dict:
    """
    Get detailed information about a specific board.

    Includes lanes, card types, custom fields, tags, users, and planning series.

    Args:
        client: AgilePlace API client
        board_id: ID of the board to retrieve

    Returns:
        Complete board object with all configuration details

    Example:
        board = await get_board(client, "123456")
        print(f"Board: {board['title']}")
        print(f"Lanes: {len(board['lanes'])}")
    """
    response = await client.get(f"/board/{board_id}")
    return response


async def get_board_cards(
    client: AgilePlaceClient,
    board_id: str,
    lanes: Optional[list[str]] = None,
    cards: Optional[list[str]] = None,
    limit: int = 200,
    offset: int = 0,
    ignore_archive_date: bool = False,
) -> dict:
    """
    Get card faces (summary information) for cards on a board.

    This endpoint is used to populate the visual board interface.

    Args:
        client: AgilePlace API client
        board_id: ID of the board
        lanes: List of lane IDs to filter by (optional)
        cards: List of specific card IDs to retrieve (optional)
        limit: Maximum number of cards to return (default: 200)
        offset: Number of cards to skip (default: 0)
        ignore_archive_date: Include archived cards (default: False)

    Returns:
        Dictionary with 'cards' list and 'pageMeta' for pagination

    Example:
        result = await get_board_cards(client, "123456", lanes=["lane1", "lane2"])
        for card in result['cards']:
            print(f"{card['title']} - {card['laneId']}")
    """
    params = {
        "limit": limit,
        "offset": offset,
    }

    if lanes:
        params["lanes"] = ",".join(lanes)

    if cards:
        params["cards"] = ",".join(cards)

    if ignore_archive_date:
        params["ignoreArchiveDate"] = "true"

    response = await client.get(f"/board/{board_id}/card", params=params)
    return response


async def get_leaf_lanes(client: AgilePlaceClient, board_id: str) -> list[dict]:
    """
    Get lanes that can hold cards (leaf lanes without children).

    Args:
        client: AgilePlace API client
        board_id: ID of the board

    Returns:
        List of lane objects with id, title, and expandedTitle

    Example:
        lanes = await get_leaf_lanes(client, "123456")
        for lane in lanes:
            print(f"{lane['expandedTitle']}")
    """
    response = await client.get(f"/board/{board_id}/leafLanes")
    return response.get("lanes", [])


async def get_lane_counts(
    client: AgilePlaceClient,
    board_id: str,
    lanes: Optional[list[str]] = None,
) -> dict:
    """
    Get card counts and sizes for lanes on a board.

    Args:
        client: AgilePlace API client
        board_id: ID of the board
        lanes: List of specific lane IDs to get counts for (optional, defaults to all)

    Returns:
        Dictionary mapping lane IDs to their card counts and sizes

    Example:
        counts = await get_lane_counts(client, "123456", ["lane1", "lane2"])
        for lane_id, stats in counts['lanes'].items():
            print(f"Lane {lane_id}: {stats['cardCount']} cards")
    """
    params = {}
    if lanes:
        params["lanes"] = ",".join(lanes)

    response = await client.get(f"/board/{board_id}/laneCount", params=params)
    return response


async def create_board(
    client: AgilePlaceClient,
    title: str,
    description: Optional[str] = None,
    is_shared: bool = False,
    shared_board_role: str = "none",
    template_id: Optional[str] = None,
    from_board_id: Optional[str] = None,
    include_cards: bool = False,
    include_existing_users: bool = False,
    base_wip_on_card_size: bool = False,
    exclude_completed_and_archive_violations: bool = False,
) -> dict:
    """
    Create a new board.

    Args:
        client: AgilePlace API client
        title: Title of the new board
        description: Board description (optional)
        is_shared: Share board with other users by default
        shared_board_role: Default role for shared users (none, boardReader, boardUser, boardManager, boardAdministrator)
        template_id: ID of template to base board on (optional)
        from_board_id: ID of board to copy from (optional)
        include_cards: Copy cards from template or source board
        include_existing_users: Copy users from source board
        base_wip_on_card_size: Factor in card size for WIP calculations
        exclude_completed_and_archive_violations: Exclude done/archive lanes from WIP

    Returns:
        Dictionary with the new board's ID

    Example:
        board = await create_board(client, "My New Project", description="Q1 2024 project")
        print(f"Created board: {board['id']}")
    """
    payload = {
        "title": title,
        "isShared": is_shared,
        "sharedBoardRole": shared_board_role,
        "includeCards": include_cards,
        "includeExistingUsers": include_existing_users,
        "baseWipOnCardSize": base_wip_on_card_size,
        "excludeCompletedAndArchiveViolations": exclude_completed_and_archive_violations,
    }

    if description:
        payload["description"] = description

    if template_id:
        payload["templateId"] = template_id

    if from_board_id:
        payload["fromBoardId"] = from_board_id

    response = await client.post("/board", json=payload)
    return response


async def update_board(
    client: AgilePlaceClient,
    board_id: str,
    **updates,
) -> dict:
    """
    Update board settings.

    Args:
        client: AgilePlace API client
        board_id: ID of the board to update
        **updates: Key-value pairs of fields to update
            - title: str
            - description: str
            - isShared: bool
            - sharedBoardRole: str
            - baseWipOnCardSize: bool
            - excludeCompletedAndArchiveViolations: bool
            - customBoardUrl: str
            - enableCustomIcon: bool
            - customIconFieldLabel: str
            - allowUsersToDeleteCards: bool
            - defaultCardType: str (cardTypeId)
            - defaultTaskType: str (cardTypeId)
            - allowPlanviewIntegration: bool
            - level: int

    Returns:
        Dictionary with the board ID

    Example:
        await update_board(client, "123456", title="Updated Title", description="New description")
    """
    response = await client.patch(f"/board/{board_id}", json=updates)
    return response


async def archive_board(client: AgilePlaceClient, board_id: str) -> None:
    """
    Archive a board (administrators retain read-only access).

    Args:
        client: AgilePlace API client
        board_id: ID of the board to archive

    Example:
        await archive_board(client, "123456")
    """
    await client.post(f"/board/{board_id}/archive")


async def unarchive_board(client: AgilePlaceClient, board_id: str) -> None:
    """
    Restore a board from archive.

    Requires Account Administrator role.

    Args:
        client: AgilePlace API client
        board_id: ID of the board to unarchive

    Example:
        await unarchive_board(client, "123456")
    """
    await client.post(f"/board/{board_id}/unarchive")


async def delete_board(client: AgilePlaceClient, board_id: str) -> None:
    """
    Permanently delete a board.

    Requires Account Administrator role.

    Args:
        client: AgilePlace API client
        board_id: ID of the board to delete

    Example:
        await delete_board(client, "123456")
    """
    await client.delete(f"/board/{board_id}")


async def get_board_members(
    client: AgilePlaceClient,
    board_id: str,
    search: Optional[str] = None,
) -> list[dict]:
    """
    Get assigned members (users and teams) on a board.

    Returns top 50 members with cards assigned on the board.

    Args:
        client: AgilePlace API client
        board_id: ID of the board
        search: Filter members by name (optional)

    Returns:
        List of member objects with id, memberType (user/team), display name, and emailAddress

    Example:
        members = await get_board_members(client, "123456", search="john")
        for member in members:
            print(f"{member['display']} ({member['memberType']})")
    """
    params = {}
    if search:
        params["search"] = search

    response = await client.get(f"/board/{board_id}/members", params=params)
    return response.get("members", [])


async def get_board_activity(
    client: AgilePlaceClient,
    board_id: str,
    limit: int = 100,
    event_id: Optional[str] = None,
    direction: str = "older",
) -> list[dict]:
    """
    Get recent activity events on a board.

    Args:
        client: AgilePlace API client
        board_id: ID of the board
        limit: Maximum number of events to return (default: 100)
        event_id: Last event ID for pagination (optional)
        direction: Direction to page - 'older' or 'newer' (default: 'older')

    Returns:
        List of activity event objects

    Example:
        events = await get_board_activity(client, "123456", limit=50)
        for event in events:
            print(f"{event['type']}: {event['timestamp']}")
    """
    params = {
        "limit": limit,
        "direction": direction,
    }

    if event_id:
        params["eventId"] = event_id

    response = await client.get(f"/board/{board_id}/activity", params=params)
    return response.get("events", [])

