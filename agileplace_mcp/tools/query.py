"""User and team query tools for AgilePlace MCP Server."""

from typing import Optional

from agileplace_mcp.client import AgilePlaceClient


# User Operations

async def list_users(
    client: AgilePlaceClient,
    search: Optional[str] = None,
    limit: int = 25,
    offset: int = 0,
    sort_by: str = "lastName",
) -> dict:
    """
    List users in the organization.

    Args:
        client: AgilePlace API client
        search: Keyword search by user name and email address (optional)
        limit: Maximum number of users to return (default: 25)
        offset: Number of users to skip (default: 0)
        sort_by: Sort order (default: 'lastName')
            - 'lastName': Sort by last name
            - 'firstNameAsc': Sort by first name ascending
            - 'firstNameDesc': Sort by first name descending
            - 'newUsers': Sort by newest users first
            - 'enabled': Show enabled users first
            - 'disabled': Show disabled users first
            - 'licenseTypeAsc': Sort by license type ascending
            - 'licenseTypeDesc': Sort by license type descending

    Returns:
        Dictionary with 'users' list and 'pageMeta'

    Example:
        result = await list_users(client, search="john", limit=10)
        for user in result['users']:
            print(f"{user['fullName']} - {user['emailAddress']}")
    """
    params = {
        "limit": limit,
        "offset": offset,
        "sortBy": sort_by,
    }

    if search:
        params["search"] = search

    response = await client.get("/user", params=params)
    return response


async def get_user(client: AgilePlaceClient, user_id: str) -> dict:
    """
    Get details about a specific user.

    Args:
        client: AgilePlace API client
        user_id: ID of the user to retrieve

    Returns:
        User object with full details

    Example:
        user = await get_user(client, "123456")
        print(f"{user['fullName']} - {user['role']}")
    """
    response = await client.get(f"/user/{user_id}")
    return response


async def get_current_user(client: AgilePlaceClient) -> dict:
    """
    Get details about the currently authenticated user.

    Args:
        client: AgilePlace API client

    Returns:
        Current user object

    Example:
        me = await get_current_user(client)
        print(f"Logged in as: {me['fullName']}")
    """
    response = await client.get("/user/me")
    return response


async def get_user_context(client: AgilePlaceClient) -> dict:
    """
    Get context information about the current user.

    Includes account settings, permissions, and preferences.

    Args:
        client: AgilePlace API client

    Returns:
        User context object

    Example:
        context = await get_user_context(client)
        print(f"Account: {context['accountId']}")
        print(f"Role: {context['role']}")
    """
    response = await client.get("/user/me/context")
    return response


# Team Operations

async def list_teams(
    client: AgilePlaceClient,
    search: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> dict:
    """
    List teams in the organization.

    Args:
        client: AgilePlace API client
        search: Filter teams by name (optional)
        limit: Maximum number of teams to return (default: 100)
        offset: Number of teams to skip (default: 0)

    Returns:
        Dictionary with 'teams' list and 'pageMeta'

    Example:
        result = await list_teams(client, search="engineering")
        for team in result['teams']:
            print(f"{team['name']}")
    """
    params = {
        "limit": limit,
        "offset": offset,
    }

    if search:
        params["search"] = search

    response = await client.get("/team", params=params)
    return response


async def get_team(client: AgilePlaceClient, team_id: str) -> dict:
    """
    Get details about a specific team.

    Args:
        client: AgilePlace API client
        team_id: ID of the team to retrieve

    Returns:
        Team object with full details

    Example:
        team = await get_team(client, "123456")
        print(f"{team['name']}: {team['description']}")
    """
    response = await client.get(f"/team/{team_id}")
    return response


async def list_team_users(
    client: AgilePlaceClient,
    team_id: str,
    limit: int = 100,
    offset: int = 0,
) -> dict:
    """
    List users that are members of a team.

    Args:
        client: AgilePlace API client
        team_id: ID of the team
        limit: Maximum number of users to return (default: 100)
        offset: Number of users to skip (default: 0)

    Returns:
        Dictionary with 'users' list and 'pageMeta'

    Example:
        result = await list_team_users(client, "team123")
        for user in result['users']:
            print(f"{user['fullName']}")
    """
    params = {
        "limit": limit,
        "offset": offset,
    }

    response = await client.get(f"/team/{team_id}/users", params=params)
    return response


async def list_team_boards(
    client: AgilePlaceClient,
    team_id: str,
    limit: int = 100,
    offset: int = 0,
) -> dict:
    """
    List boards that a team has access to.

    Args:
        client: AgilePlace API client
        team_id: ID of the team
        limit: Maximum number of boards to return (default: 100)
        offset: Number of boards to skip (default: 0)

    Returns:
        Dictionary with 'boards' list and 'pageMeta'

    Example:
        result = await list_team_boards(client, "team123")
        for board in result['boards']:
            print(f"{board['title']}")
    """
    params = {
        "limit": limit,
        "offset": offset,
    }

    response = await client.get(f"/team/{team_id}/boards", params=params)
    return response


async def list_team_subteams(
    client: AgilePlaceClient,
    team_id: str,
) -> list[dict]:
    """
    List sub-teams of a team.

    Args:
        client: AgilePlace API client
        team_id: ID of the parent team

    Returns:
        List of sub-team objects

    Example:
        subteams = await list_team_subteams(client, "team123")
        for subteam in subteams:
            print(f"Sub-team: {subteam['name']}")
    """
    response = await client.get(f"/team/{team_id}/subTeams")
    return response.get("teams", [])


# Organization Operations

async def get_organization(client: AgilePlaceClient) -> dict:
    """
    Get details about the current organization.

    Args:
        client: AgilePlace API client

    Returns:
        Organization object

    Example:
        org = await get_organization(client)
        print(f"Organization: {org['title']}")
    """
    response = await client.get("/organization")
    return response

