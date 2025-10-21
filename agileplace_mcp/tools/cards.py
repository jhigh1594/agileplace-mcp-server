"""Card operations tools for AgilePlace MCP Server."""

from typing import Any, Optional

from agileplace_mcp.client import AgilePlaceClient


# Read Operations

async def list_cards(
    client: AgilePlaceClient,
    board_id: Optional[str] = None,
    since: Optional[str] = None,
    only: Optional[list[str]] = None,
    limit: int = 200,
    offset: int = 0,
) -> dict:
    """
    List cards with optional filtering.

    Args:
        client: AgilePlace API client
        board_id: Filter by board ID (optional)
        since: ISO 8601 date - only return cards modified after this date (optional)
        only: List of fields to return (e.g., ['id', 'title', 'laneId']) (optional)
        limit: Maximum number of cards to return (default: 200)
        offset: Number of cards to skip (default: 0)

    Returns:
        Dictionary with 'cards' list and 'pageMeta'

    Example:
        # Get recent changes
        result = await list_cards(client, board_id="123", since="2024-01-01T00:00:00Z")
        
        # Get only specific fields
        result = await list_cards(client, only=["id", "title", "laneId"])
    """
    params = {
        "limit": limit,
        "offset": offset,
    }

    if board_id:
        params["board"] = board_id

    if since:
        params["since"] = since

    if only:
        params["only"] = ",".join(only)

    response = await client.get("/card", params=params)
    return response


async def get_card(client: AgilePlaceClient, card_id: str) -> dict:
    """
    Get full details of a specific card.

    Args:
        client: AgilePlace API client
        card_id: ID of the card to retrieve

    Returns:
        Complete card object with all fields

    Example:
        card = await get_card(client, "123456")
        print(f"{card['title']} - {card['priority']}")
    """
    response = await client.get(f"/card/{card_id}")
    return response


async def get_card_activity(
    client: AgilePlaceClient,
    card_id: str,
    limit: int = 100,
) -> list[dict]:
    """
    Get activity history for a card.

    Args:
        client: AgilePlace API client
        card_id: ID of the card
        limit: Maximum number of events to return (default: 100)

    Returns:
        List of activity event objects

    Example:
        events = await get_card_activity(client, "123456")
        for event in events:
            print(f"{event['type']}: {event['timestamp']}")
    """
    params = {"limit": limit}
    response = await client.get(f"/card/{card_id}/activity", params=params)
    return response.get("events", [])


# Write Operations

async def create_card(
    client: AgilePlaceClient,
    board_id: str,
    lane_id: str,
    title: str,
    description: Optional[str] = None,
    card_type_id: Optional[str] = None,
    priority: Optional[str] = None,
    size: Optional[int] = None,
    tags: Optional[list[str]] = None,
    assigned_user_ids: Optional[list[str]] = None,
    assigned_team_ids: Optional[list[str]] = None,
    external_card_id: Optional[str] = None,
    external_url: Optional[str] = None,
    planned_start: Optional[str] = None,
    planned_finish: Optional[str] = None,
    custom_icon_id: Optional[str] = None,
    custom_fields: Optional[dict[str, Any]] = None,
    index: Optional[int] = None,
) -> dict:
    """
    Create a new card on a board.

    Args:
        client: AgilePlace API client
        board_id: ID of the board
        lane_id: ID of the lane to create the card in
        title: Card title
        description: Card description (optional)
        card_type_id: Card type ID (optional)
        priority: Priority level - 'low', 'normal', 'high', or 'critical' (optional)
        size: Card size (optional)
        tags: List of tags (optional)
        assigned_user_ids: List of user IDs to assign (optional)
        assigned_team_ids: List of team IDs to assign (optional)
        external_card_id: External/custom card ID (optional)
        external_url: External URL link (optional)
        planned_start: Planned start date in ISO 8601 format (optional)
        planned_finish: Planned finish date in ISO 8601 format (optional)
        custom_icon_id: Custom icon/class of service ID (optional)
        custom_fields: Dictionary of custom field values {fieldId: value} (optional)
        index: Position in lane (optional)

    Returns:
        Dictionary with the new card object

    Example:
        card = await create_card(
            client,
            board_id="123",
            lane_id="456",
            title="Implement feature",
            description="New feature description",
            priority="high",
            size=5,
            tags=["backend", "api"]
        )
    """
    payload: dict[str, Any] = {
        "boardId": board_id,
        "laneId": lane_id,
        "title": title,
    }

    if description:
        payload["description"] = description

    if card_type_id:
        payload["typeId"] = card_type_id

    if priority:
        payload["priority"] = priority

    if size is not None:
        payload["size"] = size

    if tags:
        payload["tags"] = ",".join(tags)

    if assigned_user_ids:
        payload["assignedUserIds"] = assigned_user_ids

    if assigned_team_ids:
        payload["assignedTeamIds"] = assigned_team_ids

    if external_card_id:
        payload["externalCardID"] = external_card_id

    if external_url:
        payload["externalSystemUrl"] = external_url

    if planned_start:
        payload["plannedStart"] = planned_start

    if planned_finish:
        payload["plannedFinish"] = planned_finish

    if custom_icon_id:
        payload["classOfServiceId"] = custom_icon_id

    if custom_fields:
        payload["customFields"] = custom_fields

    if index is not None:
        payload["index"] = index

    response = await client.post("/card", json=payload)
    return response


async def update_card(
    client: AgilePlaceClient,
    card_id: str,
    **updates,
) -> dict:
    """
    Update fields on an existing card.

    Args:
        client: AgilePlace API client
        card_id: ID of the card to update
        **updates: Key-value pairs of fields to update
            - title: str
            - description: str
            - typeId: str (card type ID)
            - priority: str ('low', 'normal', 'high', 'critical')
            - size: int
            - tags: str (comma-separated)
            - assignedUserIds: list[str]
            - assignedTeamIds: list[str]
            - externalCardID: str
            - externalSystemUrl: str
            - plannedStart: str (ISO 8601)
            - plannedFinish: str (ISO 8601)
            - classOfServiceId: str
            - isBlocked: bool
            - blockReason: str
            - customFields: dict

    Returns:
        Updated card object

    Example:
        card = await update_card(
            client,
            "123456",
            title="Updated title",
            priority="critical",
            size=8
        )
    """
    response = await client.patch(f"/card/{card_id}", json=updates)
    return response


async def move_card(
    client: AgilePlaceClient,
    card_id: str,
    lane_id: str,
    position: Optional[int] = None,
) -> dict:
    """
    Move a card to a different lane.

    Args:
        client: AgilePlace API client
        card_id: ID of the card to move
        lane_id: ID of the destination lane
        position: Position in the destination lane (0-based, optional)

    Returns:
        Updated card object

    Example:
        card = await move_card(client, "123456", "lane789", position=0)
    """
    payload = {"laneId": lane_id}
    if position is not None:
        payload["position"] = position

    response = await client.post(f"/card/{card_id}/move", json=payload)
    return response


async def delete_card(client: AgilePlaceClient, card_id: str) -> None:
    """
    Delete a card.

    Args:
        client: AgilePlace API client
        card_id: ID of the card to delete

    Example:
        await delete_card(client, "123456")
    """
    await client.delete(f"/card/{card_id}")


# Metadata Operations

async def list_card_types(client: AgilePlaceClient, board_id: str) -> list[dict]:
    """
    Get card types for a board.

    Args:
        client: AgilePlace API client
        board_id: ID of the board

    Returns:
        List of card type objects

    Example:
        types = await list_card_types(client, "123456")
        for card_type in types:
            print(f"{card_type['name']}: {card_type['id']}")
    """
    board = await client.get(f"/board/{board_id}")
    return board.get("cardTypes", [])


async def list_tags(client: AgilePlaceClient, board_id: str) -> list[str]:
    """
    Get tags used on a board.

    Args:
        client: AgilePlace API client
        board_id: ID of the board

    Returns:
        List of tag strings

    Example:
        tags = await list_tags(client, "123456")
        print(f"Available tags: {', '.join(tags)}")
    """
    board = await client.get(f"/board/{board_id}")
    return board.get("tags", [])


# Comment Operations

async def get_card_comments(client: AgilePlaceClient, card_id: str) -> list[dict]:
    """
    Get comments on a card.

    Args:
        client: AgilePlace API client
        card_id: ID of the card

    Returns:
        List of comment objects

    Example:
        comments = await get_card_comments(client, "123456")
        for comment in comments:
            print(f"{comment['createdBy']['fullName']}: {comment['text']}")
    """
    response = await client.get(f"/card/{card_id}/comment")
    return response.get("comments", [])


async def create_comment(
    client: AgilePlaceClient,
    card_id: str,
    text: str,
) -> dict:
    """
    Add a comment to a card.

    Args:
        client: AgilePlace API client
        card_id: ID of the card
        text: Comment text

    Returns:
        Created comment object

    Example:
        comment = await create_comment(client, "123456", "This looks good!")
    """
    payload = {"text": text}
    response = await client.post(f"/card/{card_id}/comment", json=payload)
    return response


async def update_comment(
    client: AgilePlaceClient,
    card_id: str,
    comment_id: str,
    text: str,
) -> dict:
    """
    Update an existing comment.

    Args:
        client: AgilePlace API client
        card_id: ID of the card
        comment_id: ID of the comment
        text: Updated comment text

    Returns:
        Updated comment object

    Example:
        comment = await update_comment(client, "123", "456", "Updated text")
    """
    payload = {"text": text}
    response = await client.patch(f"/card/{card_id}/comment/{comment_id}", json=payload)
    return response


async def delete_comment(
    client: AgilePlaceClient,
    card_id: str,
    comment_id: str,
) -> None:
    """
    Delete a comment from a card.

    Args:
        client: AgilePlace API client
        card_id: ID of the card
        comment_id: ID of the comment to delete

    Example:
        await delete_comment(client, "123", "456")
    """
    await client.delete(f"/card/{card_id}/comment/{comment_id}")


# Attachment Operations

async def list_card_attachments(client: AgilePlaceClient, card_id: str) -> list[dict]:
    """
    Get attachments on a card.

    Args:
        client: AgilePlace API client
        card_id: ID of the card

    Returns:
        List of attachment objects

    Example:
        attachments = await list_card_attachments(client, "123456")
        for attachment in attachments:
            print(f"{attachment['name']} - {attachment['attachmentSize']} bytes")
    """
    response = await client.get(f"/card/{card_id}/attachment")
    return response.get("attachments", [])


async def delete_attachment(
    client: AgilePlaceClient,
    card_id: str,
    attachment_id: str,
) -> None:
    """
    Delete an attachment from a card.

    Args:
        client: AgilePlace API client
        card_id: ID of the card
        attachment_id: ID of the attachment to delete

    Example:
        await delete_attachment(client, "123", "456")
    """
    await client.delete(f"/card/{card_id}/attachment/{attachment_id}")


# Assignment Operations

async def assign_users_to_card(
    client: AgilePlaceClient,
    card_id: str,
    user_ids: Optional[list[str]] = None,
    team_ids: Optional[list[str]] = None,
) -> dict:
    """
    Assign users and/or teams to a card.

    Args:
        client: AgilePlace API client
        card_id: ID of the card
        user_ids: List of user IDs to assign (optional)
        team_ids: List of team IDs to assign (optional)

    Returns:
        Updated card object

    Example:
        card = await assign_users_to_card(
            client,
            "123456",
            user_ids=["user1", "user2"],
            team_ids=["team1"]
        )
    """
    payload = {}
    if user_ids:
        payload["assignedUserIds"] = user_ids
    if team_ids:
        payload["assignedTeamIds"] = team_ids

    response = await client.post(f"/card/{card_id}/assignMembers", json=payload)
    return response

