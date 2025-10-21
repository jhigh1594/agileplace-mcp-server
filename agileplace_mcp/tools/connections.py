"""Connection (parent/child relationship) tools for AgilePlace MCP Server."""

from typing import Optional

from agileplace_mcp.client import AgilePlaceClient


async def get_card_children(
    client: AgilePlaceClient,
    card_id: str,
    limit: int = 200,
    offset: int = 0,
) -> dict:
    """
    Get child cards connected to a parent card.

    Args:
        client: AgilePlace API client
        card_id: ID of the parent card
        limit: Maximum number of children to return (default: 200)
        offset: Number of children to skip (default: 0)

    Returns:
        Dictionary with 'cards' list and 'pageMeta'

    Example:
        result = await get_card_children(client, "123456")
        for child in result['cards']:
            print(f"Child: {child['title']}")
    """
    params = {
        "limit": limit,
        "offset": offset,
    }
    response = await client.get(f"/card/{card_id}/children", params=params)
    return response


async def get_card_children_ids(client: AgilePlaceClient, card_id: str) -> list[str]:
    """
    Get only the IDs of child cards (more efficient than full details).

    Args:
        client: AgilePlace API client
        card_id: ID of the parent card

    Returns:
        List of child card IDs

    Example:
        child_ids = await get_card_children_ids(client, "123456")
        print(f"Number of children: {len(child_ids)}")
    """
    response = await client.get(f"/card/{card_id}/children/ids")
    return response.get("childCardIds", [])


async def get_card_parents(
    client: AgilePlaceClient,
    card_id: str,
    limit: int = 200,
    offset: int = 0,
) -> dict:
    """
    Get parent cards connected to a child card.

    Args:
        client: AgilePlace API client
        card_id: ID of the child card
        limit: Maximum number of parents to return (default: 200)
        offset: Number of parents to skip (default: 0)

    Returns:
        Dictionary with 'cards' list and 'pageMeta'

    Example:
        result = await get_card_parents(client, "123456")
        for parent in result['cards']:
            print(f"Parent: {parent['title']}")
    """
    params = {
        "limit": limit,
        "offset": offset,
    }
    response = await client.get(f"/card/{card_id}/parents", params=params)
    return response


async def get_connection_statistics(client: AgilePlaceClient, card_id: str) -> dict:
    """
    Get statistics about connected cards (children).

    Includes counts of started, completed, blocked cards and their sizes.

    Args:
        client: AgilePlace API client
        card_id: ID of the parent card

    Returns:
        Dictionary with connection statistics

    Example:
        stats = await get_connection_statistics(client, "123456")
        print(f"Total: {stats['totalCount']}, Completed: {stats['completedCount']}")
    """
    response = await client.get(f"/card/{card_id}/connectedCardStatistics")
    return response


async def create_connection(
    client: AgilePlaceClient,
    parent_id: str,
    child_id: str,
) -> dict:
    """
    Create a parent-child connection between two cards.

    Args:
        client: AgilePlace API client
        parent_id: ID of the parent card
        child_id: ID of the child card

    Returns:
        Created connection object

    Example:
        connection = await create_connection(client, "parent123", "child456")
    """
    payload = {
        "parentCardId": parent_id,
        "childCardId": child_id,
    }
    response = await client.post("/card/connection", json=payload)
    return response


async def delete_connection(
    client: AgilePlaceClient,
    parent_id: str,
    child_id: str,
) -> None:
    """
    Remove a parent-child connection between two cards.

    Args:
        client: AgilePlace API client
        parent_id: ID of the parent card
        child_id: ID of the child card

    Example:
        await delete_connection(client, "parent123", "child456")
    """
    payload = {
        "parentCardId": parent_id,
        "childCardId": child_id,
    }
    await client.post("/card/deleteConnection", json=payload)


async def connect_cards_bulk(
    client: AgilePlaceClient,
    connections: list[dict],
) -> dict:
    """
    Create multiple parent-child connections in a single request.

    Args:
        client: AgilePlace API client
        connections: List of connection dictionaries with 'parentCardId' and 'childCardId'

    Returns:
        Dictionary with created connections

    Example:
        connections = [
            {"parentCardId": "parent1", "childCardId": "child1"},
            {"parentCardId": "parent1", "childCardId": "child2"},
            {"parentCardId": "parent2", "childCardId": "child3"},
        ]
        result = await connect_cards_bulk(client, connections)
    """
    response = await client.post("/card/connectMany", json={"connections": connections})
    return response


async def delete_connections_bulk(
    client: AgilePlaceClient,
    connections: list[dict],
) -> None:
    """
    Delete multiple parent-child connections in a single request.

    Args:
        client: AgilePlace API client
        connections: List of connection dictionaries with 'parentCardId' and 'childCardId'

    Example:
        connections = [
            {"parentCardId": "parent1", "childCardId": "child1"},
            {"parentCardId": "parent1", "childCardId": "child2"},
        ]
        await delete_connections_bulk(client, connections)
    """
    await client.post("/card/deleteConnections", json={"connections": connections})


async def connect_to_board(
    client: AgilePlaceClient,
    parent_id: str,
    child_board_id: str,
    child_lane_id: str,
    child_title: str,
    child_description: Optional[str] = None,
    child_type_id: Optional[str] = None,
) -> dict:
    """
    Create a new child card on a different board and connect it to a parent.

    Args:
        client: AgilePlace API client
        parent_id: ID of the parent card
        child_board_id: ID of the board to create child card on
        child_lane_id: ID of the lane to create child card in
        child_title: Title for the new child card
        child_description: Description for the child card (optional)
        child_type_id: Card type ID for the child card (optional)

    Returns:
        Dictionary with the new child card

    Example:
        child = await connect_to_board(
            client,
            parent_id="123",
            child_board_id="board456",
            child_lane_id="lane789",
            child_title="Sub-task for parent",
            child_description="Details here"
        )
    """
    payload = {
        "parentCardId": parent_id,
        "childBoardId": child_board_id,
        "childLaneId": child_lane_id,
        "childTitle": child_title,
    }

    if child_description:
        payload["childDescription"] = child_description

    if child_type_id:
        payload["childTypeId"] = child_type_id

    response = await client.post("/card/connectToBoard", json=payload)
    return response


async def connect_same_board(
    client: AgilePlaceClient,
    parent_id: str,
    child_lane_id: str,
    child_title: str,
    child_description: Optional[str] = None,
    child_type_id: Optional[str] = None,
) -> dict:
    """
    Create a new child card on the same board and connect it to a parent.

    Args:
        client: AgilePlace API client
        parent_id: ID of the parent card
        child_lane_id: ID of the lane to create child card in
        child_title: Title for the new child card
        child_description: Description for the child card (optional)
        child_type_id: Card type ID for the child card (optional)

    Returns:
        Dictionary with the new child card

    Example:
        child = await connect_same_board(
            client,
            parent_id="123",
            child_lane_id="lane456",
            child_title="Sub-task",
            child_description="Task details"
        )
    """
    payload = {
        "parentCardId": parent_id,
        "childLaneId": child_lane_id,
        "childTitle": child_title,
    }

    if child_description:
        payload["childDescription"] = child_description

    if child_type_id:
        payload["childTypeId"] = child_type_id

    response = await client.post("/card/connectSameBoard", json=payload)
    return response


async def delete_connections_by_board(
    client: AgilePlaceClient,
    parent_board_id: str,
    child_board_id: str,
) -> None:
    """
    Delete all connections between cards on two boards.

    Args:
        client: AgilePlace API client
        parent_board_id: ID of the parent board
        child_board_id: ID of the child board

    Example:
        await delete_connections_by_board(client, "board123", "board456")
    """
    payload = {
        "parentBoardId": parent_board_id,
        "childBoardId": child_board_id,
    }
    await client.post("/card/deleteConnectionsByBoard", json=payload)


async def get_child_boards(client: AgilePlaceClient, card_id: str) -> list[dict]:
    """
    Get boards that contain child cards of the specified card.

    Args:
        client: AgilePlace API client
        card_id: ID of the parent card

    Returns:
        List of board objects

    Example:
        boards = await get_child_boards(client, "123456")
        for board in boards:
            print(f"Board: {board['title']}")
    """
    response = await client.get(f"/card/{card_id}/childBoards")
    return response.get("boards", [])


async def get_parent_boards(client: AgilePlaceClient, card_id: str) -> list[dict]:
    """
    Get boards that contain parent cards of the specified card.

    Args:
        client: AgilePlace API client
        card_id: ID of the child card

    Returns:
        List of board objects

    Example:
        boards = await get_parent_boards(client, "123456")
        for board in boards:
            print(f"Board: {board['title']}")
    """
    response = await client.get(f"/card/{card_id}/parentBoards")
    return response.get("boards", [])

