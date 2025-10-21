"""Bulk operations tools for AgilePlace MCP Server."""

from typing import Any, Optional

from agileplace_mcp.client import AgilePlaceClient


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
            - parentCardId: str (set parent relationship)
            - mirrorSourceCardId: str (mirror from another card)

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
            Optional 'moveChildren' boolean to move child cards with parent
            Optional 'moveParents' boolean to move parent cards with child

    Returns:
        Dictionary with move results

    Example:
        moves = [
            {"cardId": "123", "laneId": "lane1", "position": 0},
            {"cardId": "456", "laneId": "lane2", "moveChildren": True},
            {"cardId": "789", "laneId": "lane1", "position": 1, "moveParents": True},
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


# Card Creation and Relationship Operations

async def create_cards_bulk(
    client: AgilePlaceClient,
    cards: list[dict],
) -> dict:
    """
    Create multiple cards with optional parent/child relationships in a single request.

    Args:
        client: AgilePlace API client
        cards: List of card creation dictionaries, each containing:
            - destination: dict with boardId, laneId, or cardId
            - title: str (required)
            - description: str (optional)
            - typeId: str (optional)
            - priority: str (optional) - 'low', 'normal', 'high', 'critical'
            - size: int (optional)
            - tags: list[str] (optional)
            - assignedUserIds: list[str] (optional)
            - assignedTeamIds: list[str] (optional)
            - externalCardID: str (optional)
            - externalSystemUrl: str (optional)
            - plannedStart: str (optional) - ISO 8601 date
            - plannedFinish: str (optional) - ISO 8601 date
            - customIconId: str (optional)
            - customFields: dict (optional)
            - connections: dict (optional) - with 'parents' and 'children' lists
            - dependencies: list[dict] (optional) - dependency objects
            - mirrorSourceCardId: str (optional)
            - copiedFromCardId: str (optional)

    Returns:
        Dictionary with created card results

    Example:
        cards = [
            {
                "destination": {"boardId": "123"},
                "title": "Parent Card",
                "description": "Main feature card",
                "priority": "high",
                "size": 5
            },
            {
                "destination": {"laneId": "456"},
                "title": "Child Card 1",
                "description": "Sub-task 1",
                "connections": {
                    "parents": ["parent_card_id"]  # Will be updated after creation
                }
            }
        ]
        result = await create_cards_bulk(client, cards)
    """
    payload = {"cards": cards}
    response = await client.post("/card/bulk/create", json=payload)
    return response


async def update_cards_with_relationships_bulk(
    client: AgilePlaceClient,
    card_ids: list[str],
    updates: dict[str, Any],
) -> dict:
    """
    Update multiple cards with relationship modifications.

    Enhanced version of update_cards_bulk that supports parent/child relationships.

    Args:
        client: AgilePlace API client
        card_ids: List of card IDs to update (max 100)
        updates: Dictionary of fields to update on all cards, including:
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
            - parentCardId: str (set parent relationship)
            - mirrorSourceCardId: str (mirror from another card)
            - connections: dict (modify relationships)
                - addParents: list[str] (card IDs to add as parents)
                - removeParents: list[str] (card IDs to remove as parents)
                - addChildren: list[str] (card IDs to add as children)
                - removeChildren: list[str] (card IDs to remove as children)

    Returns:
        Dictionary with update results

    Example:
        result = await update_cards_with_relationships_bulk(
            client,
            card_ids=["123", "456"],
            updates={
                "priority": "high",
                "connections": {
                    "addParents": ["parent123"],
                    "addChildren": ["child789"]
                }
            }
        )
    """
    payload = {
        "cardIds": card_ids,
        "updates": updates,
    }
    response = await client.post("/card/bulk", json=payload)
    return response


async def manage_connections_bulk(
    client: AgilePlaceClient,
    operations: list[dict],
) -> dict:
    """
    Perform bulk connection management operations (create, update, delete).

    Args:
        client: AgilePlace API client
        operations: List of connection operations, each with:
            - operation: str - 'create', 'delete', or 'update'
            - parentCardId: str
            - childCardId: str
            - dependencyType: str (optional, for updates) - 'finish_to_start', 'start_to_start', etc.

    Returns:
        Dictionary with operation results

    Example:
        operations = [
            {
                "operation": "create",
                "parentCardId": "parent123",
                "childCardId": "child456"
            },
            {
                "operation": "delete", 
                "parentCardId": "parent789",
                "childCardId": "child999"
            }
        ]
        result = await manage_connections_bulk(client, operations)
    """
    payload = {"operations": operations}
    response = await client.post("/card/connections/bulk", json=payload)
    return response


async def manage_dependencies_bulk(
    client: AgilePlaceClient,
    dependencies: list[dict],
) -> dict:
    """
    Create, update, or delete multiple dependencies in a single request.

    Args:
        client: AgilePlace API client
        dependencies: List of dependency operations, each with:
            - operation: str - 'create', 'update', or 'delete'
            - cardId: str (dependent card)
            - dependsOnCardId: str (card being depended upon)
            - dependencyType: str (optional) - 'finish_to_start', 'start_to_start', 'finish_to_finish', 'start_to_finish'
            - dependencyId: str (required for update/delete operations)

    Returns:
        Dictionary with dependency operation results

    Example:
        dependencies = [
            {
                "operation": "create",
                "cardId": "456",
                "dependsOnCardId": "123",
                "dependencyType": "finish_to_start"
            },
            {
                "operation": "delete",
                "dependencyId": "dep789"
            }
        ]
        result = await manage_dependencies_bulk(client, dependencies)
    """
    payload = {"dependencies": dependencies}
    response = await client.post("/card/dependencies/bulk", json=payload)
    return response


async def create_cards_with_relationships_bulk(
    client: AgilePlaceClient,
    cards: list[dict],
    relationships: Optional[dict] = None,
) -> dict:
    """
    Create multiple cards and establish relationships between them in a single request.

    This is a convenience function that combines card creation with relationship management.

    Args:
        client: AgilePlace API client
        cards: List of card creation dictionaries (same format as create_cards_bulk)
        relationships: Optional dictionary defining relationships between created cards:
            - parentChild: list[dict] - each with 'parentIndex', 'childIndex', 'parentCardId', 'childCardId'
            - dependencies: list[dict] - dependency relationships

    Returns:
        Dictionary with created cards and established relationships

    Example:
        cards = [
            {"destination": {"boardId": "123"}, "title": "Parent Card"},
            {"destination": {"boardId": "123"}, "title": "Child Card 1"},
            {"destination": {"boardId": "123"}, "title": "Child Card 2"}
        ]
        relationships = {
            "parentChild": [
                {"parentIndex": 0, "childIndex": 1},
                {"parentIndex": 0, "childIndex": 2}
            ]
        }
        result = await create_cards_with_relationships_bulk(client, cards, relationships)
    """
    payload = {"cards": cards}
    if relationships:
        payload["relationships"] = relationships
    
    response = await client.post("/card/bulk/create-with-relationships", json=payload)
    return response


async def update_card_relationships_bulk(
    client: AgilePlaceClient,
    card_relationships: list[dict],
) -> dict:
    """
    Update relationships for multiple cards in a single request.

    Args:
        client: AgilePlace API client
        card_relationships: List of card relationship updates, each with:
            - cardId: str
            - operation: str - 'add_parents', 'remove_parents', 'add_children', 'remove_children', 'set_parent'
            - cardIds: list[str] - card IDs to add/remove as parents/children
            - parentCardId: str (for set_parent operation)

    Returns:
        Dictionary with relationship update results

    Example:
        card_relationships = [
            {
                "cardId": "123",
                "operation": "add_parents",
                "cardIds": ["parent1", "parent2"]
            },
            {
                "cardId": "456", 
                "operation": "set_parent",
                "parentCardId": "parent3"
            }
        ]
        result = await update_card_relationships_bulk(client, card_relationships)
    """
    payload = {"cardRelationships": card_relationships}
    response = await client.post("/card/relationships/bulk", json=payload)
    return response

