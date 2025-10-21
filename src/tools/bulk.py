"""Bulk operations tools for AgilePlace MCP Server."""

from typing import Any, Optional

from ..client import AgilePlaceClient


async def update_cards_bulk(
    client: AgilePlaceClient,
    card_ids: list[str],
    updates: dict[str, Any],
) -> dict:
    """
    Update multiple cards with the same field values.

    Args:
        client: AgilePlace API client
        card_ids: List of card IDs to update (max 100)
        updates: Dictionary of fields to update on all cards
            - title: str
            - description: str
            - typeId: str
            - priority: str
            - size: int
            - tags: str (comma-separated)
            - assignedUserIds: list[str]
            - assignedTeamIds: list[str]
            - classOfServiceId: str
            - isBlocked: bool
            - blockReason: str

    Returns:
        Dictionary with update results

    Example:
        result = await update_cards_bulk(
            client,
            card_ids=["123", "456", "789"],
            updates={"priority": "high", "tags": "urgent,review"}
        )
    """
    payload = {
        "cardIds": card_ids,
        "updates": updates,
    }
    response = await client.post("/card/bulk", json=payload)
    return response


async def delete_cards_bulk(client: AgilePlaceClient, card_ids: list[str]) -> None:
    """
    Delete multiple cards in a single request.

    Args:
        client: AgilePlace API client
        card_ids: List of card IDs to delete (max 100)

    Example:
        await delete_cards_bulk(client, ["123", "456", "789"])
    """
    payload = {"cardIds": card_ids}
    await client.post("/card/deleteMany", json=payload)


async def move_cards_bulk(
    client: AgilePlaceClient,
    moves: list[dict],
) -> dict:
    """
    Move multiple cards to different lanes in a single request.

    Args:
        client: AgilePlace API client
        moves: List of move operations, each with 'cardId' and 'laneId'
            Optional 'position' field for placement in lane

    Returns:
        Dictionary with move results

    Example:
        moves = [
            {"cardId": "123", "laneId": "lane1", "position": 0},
            {"cardId": "456", "laneId": "lane2"},
            {"cardId": "789", "laneId": "lane1", "position": 1},
        ]
        result = await move_cards_bulk(client, moves)
    """
    payload = {"moves": moves}
    response = await client.post("/card/bulk/move", json=payload)
    return response


async def assign_members_bulk(
    client: AgilePlaceClient,
    board_ids: list[str],
    user_ids: Optional[list[str]] = None,
    team_ids: Optional[list[str]] = None,
    board_role: str = "boardUser",
) -> None:
    """
    Assign users or teams to multiple boards with a specific role.

    Maximum of 500 operations (board_ids × (user_ids + team_ids)).

    Args:
        client: AgilePlace API client
        board_ids: List of board IDs to grant access to
        user_ids: List of user IDs to assign (optional)
        team_ids: List of team IDs to assign (optional)
        board_role: Role to assign (default: 'boardUser')
            - 'boardReader': Read-only access
            - 'boardUser': Can edit cards
            - 'boardManager': Can manage board settings
            - 'boardAdministrator': Full board control

    Example:
        # Assign 2 users to 3 boards as board users (6 operations)
        await assign_members_bulk(
            client,
            board_ids=["board1", "board2", "board3"],
            user_ids=["user1", "user2"],
            board_role="boardUser"
        )
    """
    payload = {
        "boardIds": board_ids,
        "boardRole": board_role,
    }

    if user_ids:
        payload["userIds"] = user_ids

    if team_ids:
        payload["teamIds"] = team_ids

    await client.post("/board/access", json=payload)


async def remove_members_bulk(
    client: AgilePlaceClient,
    board_ids: list[str],
    user_ids: Optional[list[str]] = None,
    team_ids: Optional[list[str]] = None,
    emails: Optional[list[str]] = None,
) -> None:
    """
    Remove users or teams from multiple boards.

    WARNING: This is destructive - removed users will lose:
    - Card assignments on these boards
    - Subscriptions to cards, lanes, and boards

    Maximum of 500 operations (board_ids × (user_ids + team_ids + emails)).

    Args:
        client: AgilePlace API client
        board_ids: List of board IDs to remove access from
        user_ids: List of user IDs to remove (optional)
        team_ids: List of team IDs to remove (optional)
        emails: List of email addresses to remove (optional)

    Example:
        await remove_members_bulk(
            client,
            board_ids=["board1", "board2"],
            user_ids=["user1", "user2"]
        )
    """
    payload = {"boardIds": board_ids}

    if user_ids:
        payload["userIds"] = user_ids

    if team_ids:
        payload["teamIds"] = team_ids

    if emails:
        payload["emails"] = emails

    await client.delete("/board/access", json=payload)

